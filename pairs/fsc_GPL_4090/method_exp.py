import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]

sys.path.insert(0, str(PROJECT_ROOT))

import testbed

MODELS_ROOT = HERE / "runs/models_exp"   # same as the training script
OUTPUT_ROOT = HERE / "runs" / "eval_exp"


# 1. CONFIGURATION (same experiments as generation / training)

STUDENTS = ["BGE", "MiniLM"]
VARIANTS = ["dense", "bm25"]

EXPERIMENTS = {
    "negatives_sweep": {
        "negatives_list": [10, 20, 30, 40, 50],
        "datasets": ["scifact", "nfcorpus"],
    },
    "ideal": {
        "negatives_list": [50],
        "datasets": ["scifact", "nfcorpus"],
    },
}


# 2. BUILD THE LIST OF CHECKPOINTS
#
#   runs/models_exp/<exp>/<dataset>/genq_<student>/
#   runs/models_exp/<exp>/<dataset>/nneg_<n>/gpl_<variant>_<student>/
#
# Each run is saved as:
#   runs/eval_exp/<exp>/<model_label>/<dataset>.json
#   with model_label = genq_<student>  or  gpl_<variant>_<student>_nneg<n>

CHECKPOINTS = []  # (exp, dataset, model_label, student, checkpoint_path)

for exp_name, exp in EXPERIMENTS.items():
    for dataset in exp["datasets"]:
        model_root = MODELS_ROOT / exp_name / dataset

        for student in STUDENTS:
            CHECKPOINTS.append((
                exp_name, dataset, f"genq_{student}", student,
                model_root / f"genq_{student}",
            ))

            for nneg in exp["negatives_list"]:
                for variant in VARIANTS:
                    CHECKPOINTS.append((
                        exp_name, dataset, f"gpl_{variant}_{student}_nneg{nneg}", student,
                        model_root / f"nneg_{nneg}" / f"gpl_{variant}_{student}",
                    ))


# 3. EVALUATE CHECKPOINTS

loaded_data = {}  # load each test set only once

for exp_name, dataset, model_label, student, checkpoint in CHECKPOINTS:

    print(f"\n{'=' * 50}")
    print(f"Experiment: {exp_name}")
    print(f"Dataset: {dataset}")
    print(f"Model: {model_label}")
    print(f"Checkpoint: {checkpoint}")
    print(f"{'=' * 50}")


    model = SentenceTransformer(str(checkpoint), device=testbed.device())

    # Same corpus and queries as the official testbed
    if dataset not in loaded_data:
        loaded_data[dataset] = testbed.load(dataset)
    corpus, queries, _ = loaded_data[dataset]

    # Query prefix for BGE models
    query_prefix = testbed.BGE_QUERY if student == "BGE" else ""

    # Same preprocessing and ranking as testbed dense baselines
    run = testbed.dense_search(
        model,
        corpus,
        queries,
        query_prefix=query_prefix,
        batch_size=16)

    # Save in the format expected by testbed.py score
    model_output_dir = OUTPUT_ROOT / exp_name / model_label
    model_output_dir.mkdir(parents=True, exist_ok=True)

    output_path = model_output_dir / f"{dataset}.json"
    testbed.save_run(run, output_path)

    print(f"Saved run: {output_path}")

print("\nAll model retrieval runs completed.")