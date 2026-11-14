
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]

sys.path.insert(0, str(PROJECT_ROOT))

import testbed

ROOT = HERE
CHECKPOINT_DIR = ROOT / "runs" / "models" / "test"
OUTPUT_DIR = ROOT / "runs/eval_test"


# 1. CONFIGURATION

DATASETS = ["scifact", "nfcorpus"]

MODELS = [
    "gpl_BGE",
    "gpl_MiniLM",
    "genq_BGE",
    "genq_MiniLM",
    "gpl_bm25_BGE",
    "gpl_bm25_MiniLM",
]

CHECKPOINTS = {
    (dataset, model): CHECKPOINT_DIR / model / dataset
    for dataset in DATASETS
    for model in MODELS
}


# 2. EVALUATE CHECKPOINTS

for (dataset, model_name), checkpoint in CHECKPOINTS.items():

    print(f"\n{'=' * 50}")
    print(f"Dataset: {dataset}")
    print(f"Model: {model_name}")
    print(f"Checkpoint: {checkpoint}")
    print(f"{'=' * 50}")

    if not checkpoint.is_dir():
        print(f"Checkpoint not found: {checkpoint}")
        continue

    print(f"Loading model: {model_name}")

    model = SentenceTransformer(
        str(checkpoint),
        device=testbed.device()
    )

    # Same corpus and queries as the official testbed
    corpus, queries, _ = testbed.load(dataset)

    # Query prefix for BGE models
    query_prefix = (
        testbed.BGE_QUERY
        if model_name.endswith("_BGE")
        else ""
    )

    # Same preprocessing and ranking as testbed dense baselines
    run = testbed.dense_search(
        model,
        corpus,
        queries,
        query_prefix=query_prefix,
        batch_size=16
    )

    # Save in the format expected by testbed.py score
    model_output_dir = OUTPUT_DIR / model_name
    model_output_dir.mkdir(parents=True, exist_ok=True)

    output_path = model_output_dir / f"{dataset}.json"

    testbed.save_run(run, output_path)

    print(f"Saved run: {output_path}")

print("\nAll model retrieval runs completed.")
