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


# ----------------------------------------------------------------------
# STEP 1: corpus + synthetic queries (done once per dataset)
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# STEP 2: hard negatives + pseudo-labels (one run per configuration)
# ----------------------------------------------------------------------
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
    max_seq_length=350):

    """
    Copy the base data into <output_dir>/<variant>/ and run hard-negative
    mining + cross-encoder pseudo-labelling for each variant.

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

        NegativeMiner(
            generated_path=str(path),
            prefix=qgen_prefix,
            retrievers=cfg["retrievers"],
            retriever_score_functions=cfg["score_functions"],
            nneg=negatives_per_query,
        ).run()
        print(f"Hard negatives generated: {variant_name}")

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
# ONE-SHOT: single configuration
# ----------------------------------------------------------------------
def generate_gpl_data(
    dataset_path,
    output_dir,
    *,
    new_size,
    queries_per_passage,
    gpl_steps,
    negatives_per_query=10,
    variants=("dense", "bm25"),
    generator=DEFAULT_GENERATOR,
    teacher=DEFAULT_TEACHER,
    retrievers=None,
    retriever_score_functions=None,
    qgen_prefix="query_gen",
    batch_generation=32,
    batch_gpl=32,
    max_seq_length=350,
    download=True,
):
    """
    Full pipeline for ONE dataset and ONE configuration.

    Output layout:
        <output_dir>/base/    -> resized corpus + synthetic queries
        <output_dir>/dense/   -> negatives mined with dense retrievers
        <output_dir>/bm25/    -> negatives mined with BM25
    """
    variants = list(variants)
    retrievers = list(retrievers or DEFAULT_RETRIEVERS)
    output_dir = Path(output_dir)

    if download:
        download_models([generator, teacher] + (retrievers if "dense" in variants else []))

    base_dir = prepare_base_data(
        dataset_path,
        output_dir / "base",
        new_size=new_size,
        queries_per_passage=queries_per_passage,
        generator=generator,
        qgen_prefix=qgen_prefix,
        batch_generation=batch_generation,
    )
    return mine_and_label(
        base_dir,
        output_dir,
        gpl_steps=gpl_steps,
        negatives_per_query=negatives_per_query,
        variants=variants,
        teacher=teacher,
        retrievers=retrievers,
        retriever_score_functions=retriever_score_functions,
        qgen_prefix=qgen_prefix,
        batch_gpl=batch_gpl,
        max_seq_length=max_seq_length,
    )


# ----------------------------------------------------------------------
# PROJECT: negatives_per_query = 10, 20, 30, 40, 50 on SciFact and NFCorpus
# ----------------------------------------------------------------------
if __name__ == "__main__":
    WORK_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = WORK_DIR.parents[1]
    OUTPUT_ROOT = WORK_DIR / "runs" / "generated_GPL"

    EXPERIMENTS = {
        # Reduced setup: sweep over negatives_per_query
        "negatives_sweep": {
            "negatives_list": [10, 20, 30, 40, 50],
            "datasets": {
                "scifact": {
                    "path": PROJECT_ROOT / "data" / "scifact",
                    "new_size": 2592,
                    "queries_per_passage": 3,
                    "gpl_steps": 243,
                    "batch_gpl": 32,
                    "max_seq_length": 350
                },
                "nfcorpus": {
                    "path": PROJECT_ROOT / "data" / "nfcorpus",
                    "new_size": 1816,
                    "queries_per_passage": 4,
                    "gpl_steps": 227,
                    "batch_gpl": 32,
                    "max_seq_length": 350
                }
            }
        }
        # Ideal setup given the limitations: full corpus, 10 queries per passage, 10,000 GPL steps
        "ideal": {
            "negatives_list": [50],
            "datasets": {
                "scifact": {
                    "path": PROJECT_ROOT / "data" / "scifact",
                    "new_size": 5183,           # full corpus -> 51,830 synthetic queries
                    "queries_per_passage": 10,
                    "gpl_steps": 10_000,
                    "batch_gpl": 32,
                    "max_seq_length": 350
                },
                "nfcorpus": {
                    "path": PROJECT_ROOT / "data" / "nfcorpus",
                    "new_size": 3633,           # full corpus -> 36,330 synthetic queries
                    "queries_per_passage": 10,
                    "gpl_steps": 10_000,
                    "batch_gpl": 32,
                    "max_seq_length": 350
                }
            }
        }
    }

    download_models([DEFAULT_GENERATOR, DEFAULT_TEACHER, *DEFAULT_RETRIEVERS])

    for exp_name, exp in EXPERIMENTS.items():
        for name, cfg in exp["datasets"].items():
            dataset_root = OUTPUT_ROOT / exp_name / name

            # 1. Corpus + synthetic queries: generated ONCE per dataset
            base_dir = prepare_base_data(
                cfg["path"],
                dataset_root / "base",
                new_size=cfg["new_size"],
                queries_per_passage=cfg["queries_per_passage"]
            )

            # 2. Hard negatives + pseudo-labels for each negatives_per_query
            for nneg in exp["negatives_list"]:
                print(f"\n{'#' * 50}\n[{exp_name}] {name}: negatives_per_query = {nneg}\n{'#' * 50}")
                mine_and_label(
                    base_dir,
                    dataset_root / f"nneg_{nneg}",
                    gpl_steps=cfg["gpl_steps"],
                    negatives_per_query=nneg,
                    variants=["dense", "bm25"],
                    batch_gpl=cfg["batch_gpl"],
                    max_seq_length=cfg["max_seq_length"]
                )

    print("\nAll generation experiments completed.")