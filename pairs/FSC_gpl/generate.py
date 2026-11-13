from pathlib import Path
import shutil

from huggingface_hub import snapshot_download
from beir.datasets.data_loader import GenericDataLoader
from gpl.toolkit import qgen, resize, NegativeMiner, PseudoLabeler



# 1. CONFIGURATION


ROOT = Path("/app/pairs/FSC_gpl/runs")

DATASETS = {"scifact": "/app/data/scifact", "nfcorpus": "/app/data/nfcorpus"}

CONFIGS = {
    "scifact": {
        "new_size": 2592,
        "queries_per_passage": 3,
        "gpl_steps": 243
    },
    "nfcorpus": {
        "new_size": 1816,
        "queries_per_passage": 4,
        "gpl_steps": 227}}

GENERATOR = "doc2query/msmarco-t5-base-v1"
TEACHER = "cross-encoder/ms-marco-MiniLM-L6-v2"

RETRIEVERS = ["sentence-transformers/msmarco-distilbert-base-v3", "sentence-transformers/msmarco-MiniLM-L6-v3"]

QGEN_PREFIX = "query_gen"

BATCH_GENERATION = 8
BATCH_GPL = 32
NEGATIVES_PER_QUERY = 10
MAX_SEQ_LENGTH = 350


# 2. DOWNLOAD GENERATION MODELS

for model_name in [GENERATOR, TEACHER, *RETRIEVERS]:

    snapshot_download(
        repo_id=model_name,
        max_workers=2,
    )

    print(f"Downloaded: {model_name}")



# 3. GENERATE DATA FOR EACH DATASET


for dataset_key, dataset_path in DATASETS.items():

    cfg = CONFIGS[dataset_key]

    generated_path = ROOT / "generated_gpl/test" / dataset_key
    bm25_generated_path = ROOT / "generated_gpl/test_bm25" / dataset_key

    bm25_generated_path.mkdir(parents=True, exist_ok=True)

    print(f"\n{'=' * 50}")
    print(f"Generating data: {dataset_key}")
    print(f"{'=' * 50}")
  
    # A. PREPARE CORPUS

    resize(
        data_path=dataset_path,
        output_path=str(generated_path),
        new_size=cfg["new_size"])

    print("Corpus generated.")

    # B. GENERATE SYNTHETIC QUERIES AND QRELS

    qgen(
        data_path=str(generated_path),
        output_dir=str(generated_path),
        generator_name_or_path=GENERATOR,
        ques_per_passage=cfg["queries_per_passage"],
        bsz=BATCH_GENERATION,
        qgen_prefix=QGEN_PREFIX,
    )

    print("Synthetic queries generated.")

    # C. LOAD GENERATED DATA

    corpus, gen_queries, gen_qrels = (
        GenericDataLoader(
            str(generated_path),
            prefix=QGEN_PREFIX,
        ).load(split="train"))

    # D. PREPARE BM25 DATA DIRECTORY

    for file_name in ["corpus.jsonl", f"{QGEN_PREFIX}-queries.jsonl"]:
        shutil.copy2(generated_path / file_name, bm25_generated_path / file_name)

    shutil.copytree(
        generated_path / f"{QGEN_PREFIX}-qrels",
        bm25_generated_path / f"{QGEN_PREFIX}-qrels",
        dirs_exist_ok=True)

    # E. GENERATE DENSE AND BM25 NEGATIVES

    variants = {
        "dense": {
            "path": generated_path,
            "retrievers": RETRIEVERS,
            "score_functions": ["cos_sim", "cos_sim"],
        },
        "bm25": {
            "path": bm25_generated_path,
            "retrievers": ["bm25"],
            "score_functions": ["none"],
        },
    }

    for variant_name, variant in variants.items():

        path = variant["path"]

        print(f"\nGenerating {variant_name}: {dataset_key}")

        # E1. HARD NEGATIVE MINING

        miner = NegativeMiner(
            generated_path=str(path),
            prefix=QGEN_PREFIX,
            retrievers=variant["retrievers"],
            retriever_score_functions=variant["score_functions"],
            nneg=NEGATIVES_PER_QUERY,
        )

        miner.run()

        print(f"Hard negatives generated: {variant_name}")

        # E2. CROSS-ENCODER PSEUDO LABELING

        pseudo_labeler = PseudoLabeler(
            generated_path=str(path),
            gen_queries=gen_queries,
            corpus=corpus,
            total_steps=cfg["gpl_steps"],
            batch_size=BATCH_GPL,
            cross_encoder=TEACHER,
            max_seq_length=MAX_SEQ_LENGTH,
        )

        pseudo_labeler.run()

        print(f"Pseudo labels generated: {variant_name}")

    print(f"\nGeneration completed: {dataset_key}")

print("\nAll generation experiments completed.")