from pathlib import Path
import shutil

from huggingface_hub import snapshot_download
from beir.datasets.data_loader import GenericDataLoader
from gpl.toolkit import qgen, resize, NegativeMiner, PseudoLabeler


# Default values (can be overridden when calling the functions)
DEFAULT_GENERATOR = "doc2query/msmarco-t5-base-v1"
DEFAULT_TEACHER = "cross-encoder/ms-marco-MiniLM-L6-v2"
DEFAULT_RETRIEVERS = [
    "sentence-transformers/msmarco-distilbert-base-v3",
    "sentence-transformers/msmarco-MiniLM-L6-v3"]

PSEUDO_LABELS_FILE = "gpl-training-data.tsv"
HARD_NEGATIVES_FILE = "hard-negatives.jsonl"


def download_models(model_names, max_workers=2):
    """Download (or reuse from cache) the Hugging Face models."""
    for model_name in dict.fromkeys(model_names):
        if model_name == "bm25":
            continue
        snapshot_download(
            repo_id=model_name,
            max_workers=max_workers,
            ignore_patterns=["*.onnx", "*.msgpack", "*.h5", "*.ot"],
        )
        print(f"Downloaded: {model_name}")


# STEP 1: corpus + synthetic queries (done once per dataset)
def prepare_base_data(
    dataset_path,
    base_dir,
    *,
    new_size,
    queries_per_passage,
    generator=DEFAULT_GENERATOR,
    qgen_prefix="query_gen",
    batch_generation=32,
):
    """
    Resize the corpus and generate synthetic queries + qrels into `base_dir`.
    The result can be reused by several mining runs.
    """
    dataset_path, base_dir = Path(dataset_path), Path(base_dir)
    base_dir.mkdir(parents=True, exist_ok=True)

    if (base_dir / f"{qgen_prefix}-qrels" / "train.tsv").exists():
        print(f"Base data already there, skipped: {base_dir}")
        return base_dir

    print(f"\n{'=' * 50}")
    print(f"Preparing base data: {dataset_path.name} -> {base_dir}")
    print(f"{'=' * 50}")

    resize(
        data_path=str(dataset_path),
        output_path=str(base_dir),
        new_size=new_size,
    )
    print("Corpus generated.")

    qgen(
        data_path=str(base_dir),
        output_dir=str(base_dir),
        generator_name_or_path=generator,
        ques_per_passage=queries_per_passage,
        bsz=batch_generation,
        qgen_prefix=qgen_prefix,
    )
    print("Synthetic queries generated.")
    return base_dir


def _copy_base(base_dir, target_dir, qgen_prefix):
    """Copy only corpus, queries and qrels (no negatives / pseudo-labels)."""
    target_dir.mkdir(parents=True, exist_ok=True)
    for file_name in ["corpus.jsonl", f"{qgen_prefix}-queries.jsonl"]:
        shutil.copy2(base_dir / file_name, target_dir / file_name)
    shutil.copytree(
        base_dir / f"{qgen_prefix}-qrels",
        target_dir / f"{qgen_prefix}-qrels",
        dirs_exist_ok=True,
    )


# STEP 2: hard negatives + pseudo-labels (one run per configuration)
def mine_and_label(
    base_dir,
    output_dir,
    *,
    gpl_steps,
    negatives_per_query=10,
    variants=("dense", "bm25"),
    teacher=DEFAULT_TEACHER,
    retrievers=None,
    retriever_score_functions=None,
    qgen_prefix="query_gen",
    batch_gpl=32,
    max_seq_length=350,
    hard_negatives_from=None):

    """
    Copy the base data into <output_dir>/<variant>/ and run hard-negative
    mining + cross-encoder pseudo-labelling for each variant.

    hard_negatives_from: a folder with <variant>/hard-negatives.jsonl to copy
    instead of mining again (mining does not depend on gpl_steps).
    Steps already done (hard-negatives.jsonl, gpl-training-data.tsv) are skipped.

    Returns a dict {variant: Path}.
    """
    variants = list(variants)
    retrievers = list(retrievers or DEFAULT_RETRIEVERS)
    if retriever_score_functions is None:
        retriever_score_functions = ["cos_sim"] * len(retrievers)

    base_dir, output_dir = Path(base_dir), Path(output_dir)

    corpus, gen_queries, _ = GenericDataLoader(str(base_dir), prefix=qgen_prefix).load(split="train")

    variant_cfgs = {
        "dense": {"retrievers": retrievers, "score_functions": list(retriever_score_functions)},
        "bm25": {"retrievers": ["bm25"], "score_functions": ["none"]}}

    paths = {}
    for variant_name in variants:
        cfg = variant_cfgs[variant_name]
        path = output_dir / variant_name
        _copy_base(base_dir, path, qgen_prefix)

        print(f"\nGenerating {variant_name} (nneg={negatives_per_query}) -> {path}")

        if hard_negatives_from is not None:
            shutil.copy2(Path(hard_negatives_from) / variant_name / HARD_NEGATIVES_FILE,
                         path / HARD_NEGATIVES_FILE)
            print(f"Hard negatives reused from {hard_negatives_from}: {variant_name}")
        elif (path / HARD_NEGATIVES_FILE).exists():
            print(f"Hard negatives already there, skipped: {variant_name}")
        else:
            NegativeMiner(
                generated_path=str(path),
                prefix=qgen_prefix,
                retrievers=cfg["retrievers"],
                retriever_score_functions=cfg["score_functions"],
                nneg=negatives_per_query,
            ).run()
            print(f"Hard negatives generated: {variant_name}")

        if (path / PSEUDO_LABELS_FILE).exists():
            print(f"Pseudo labels already there, skipped: {variant_name}")
            paths[variant_name] = path
            continue

        PseudoLabeler(
            generated_path=str(path),
            gen_queries=gen_queries,
            corpus=corpus,
            total_steps=gpl_steps,
            batch_size=batch_gpl,
            cross_encoder=teacher,
            max_seq_length=max_seq_length,
        ).run()
        print(f"Pseudo labels generated: {variant_name}")

        paths[variant_name] = path
    return paths


# ----------------------------------------------------------------------
# PROJECT
#
#   negatives_sweep: nneg = 10, 20, 30, 40, 50 with the base steps
#   steps_sweep:     nneg = 50, steps = base_steps x 1, 2, 3, 4, 5
#
# Both sweeps work the same way: one folder per value, each with its own
# pseudo-label file generated by the PseudoLabeler for that number of steps.
# The steps sweep reuses base/ and the nneg_50 hard negatives of the negatives
# sweep (mining does not depend on the steps).
#
#   runs/generated_GPL/negatives_sweep/<dataset>/base/
#   runs/generated_GPL/negatives_sweep/<dataset>/nneg_<n>/{dense,bm25}/
#   runs/generated_GPL/steps_sweep/<dataset>/steps_<s>/{dense,bm25}/
# ----------------------------------------------------------------------
if __name__ == "__main__":
    WORK_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = WORK_DIR.parents[1]
    OUTPUT_ROOT = WORK_DIR / "runs" / "generated_GPL"

    # The file holds gpl_steps x batch_gpl rows
    BATCH_GPL = 32
    MAX_SEQ_LENGTH = 350

    DATASETS = {
        "scifact": {"path": PROJECT_ROOT / "data" / "scifact", "new_size": 2592,
                    "queries_per_passage": 3, "gpl_steps": 243},
        "nfcorpus": {"path": PROJECT_ROOT / "data" / "nfcorpus", "new_size": 1816,
                     "queries_per_passage": 4, "gpl_steps": 227},
        "arguana": {"path": PROJECT_ROOT / "data" / "arguana", "new_size": 2892,
                     "queries_per_passage": 3, "gpl_steps": 271},
    }
    NEGATIVES_LIST = [10, 20, 30, 40, 50]
    STEPS_NNEG = 50
    STEPS_MULTIPLIERS = [1, 2, 3, 4, 5]

    RUN_NEGATIVES_SWEEP = True
    RUN_STEPS_SWEEP = True

    download_models([DEFAULT_GENERATOR, DEFAULT_TEACHER, *DEFAULT_RETRIEVERS])

    for name, cfg in DATASETS.items():
        neg_root = OUTPUT_ROOT / "negatives_sweep" / name

        # 1. Corpus + synthetic queries: generated ONCE per dataset, shared by both sweeps
        base_dir = prepare_base_data(
            cfg["path"], neg_root / "base",
            new_size=cfg["new_size"], queries_per_passage=cfg["queries_per_passage"])

        # 2. Negatives sweep (nneg_50 is always needed: the steps sweep reuses its negatives)
        nnegs = NEGATIVES_LIST if RUN_NEGATIVES_SWEEP else [STEPS_NNEG]
        for nneg in nnegs:
            print(f"\n{'#' * 50}\n[negatives_sweep] {name}: nneg = {nneg}\n{'#' * 50}")
            mine_and_label(
                base_dir, neg_root / f"nneg_{nneg}",
                gpl_steps=cfg["gpl_steps"], negatives_per_query=nneg,
                batch_gpl=BATCH_GPL, max_seq_length=MAX_SEQ_LENGTH)

        # 3. Steps sweep (nneg = 50): one folder per number of steps
        if RUN_STEPS_SWEEP:
            for mult in STEPS_MULTIPLIERS:
                steps = cfg["gpl_steps"] * mult
                print(f"\n{'#' * 50}\n[steps_sweep] {name}: steps = {steps} (x{mult}), "
                      f"nneg = {STEPS_NNEG}, {steps * BATCH_GPL} pseudo-labels\n{'#' * 50}")
                mine_and_label(
                    base_dir, OUTPUT_ROOT / "steps_sweep" / name / f"steps_{steps}",
                    gpl_steps=steps, negatives_per_query=STEPS_NNEG,
                    batch_gpl=BATCH_GPL, max_seq_length=MAX_SEQ_LENGTH,
                    hard_negatives_from=neg_root / f"nneg_{STEPS_NNEG}")

    print("\nAll generation experiments completed.")