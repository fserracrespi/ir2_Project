import gc
import sys
from pathlib import Path

import torch
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent
PROJECT_ROOT = HERE.parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

import testbed

MODELS_ROOT = HERE / "runs" / "models_EXP"   
OUTPUT_ROOT = HERE / "runs" / "eval_EXP"


# ----------------------------------------------------------------------
# 1. CONFIGURATION (same experiments as generation / training)
# ----------------------------------------------------------------------
DATASETS = ["scifact", "nfcorpus","arguana"]
STUDENTS = ["BGE", "MiniLM"]
VARIANTS = ["dense", "bm25"]

NEGATIVES_LIST = [10, 20, 30, 40, 50]
STEPS_MULTIPLIERS = [1, 2, 3, 4, 5]
# Base steps per dataset: must match BASE_STEPS in train_gpl_experiments.py
# (the steps sweep folders are named steps_<base x k>)
BASE_STEPS = {"scifact": 243, "nfcorpus": 227, "arguana": 271}

RUN_NEGATIVES_SWEEP = True
RUN_STEPS_SWEEP = True
SKIP_EXISTING = True      # do not recompute a run that is already saved
BATCH_SIZE = 16


# ----------------------------------------------------------------------
# 2. BUILD THE LIST OF CHECKPOINTS
#
#   models (train_experiments.py):
#     runs/models_exp/negatives_sweep/<dataset>/genq_<student>/
#     runs/models_exp/negatives_sweep/<dataset>/nneg_<n>/gpl_<variant>_<student>/
#     runs/models_exp/steps_sweep/<dataset>/steps_<s>/gpl_<variant>_<student>/   (s = base x k)
#
#   runs (one folder per model, ready for `testbed.py score <folder>`):
#     runs/eval_exp/negatives_sweep/genq_<student>/<dataset>.json
#     runs/eval_exp/negatives_sweep/gpl_<variant>_<student>_nneg<n>/<dataset>.json
#     runs/eval_exp/steps_sweep/gpl_<variant>_<student>_x<k>/<dataset>.json
#   (the steps sweep is labelled by multiplier, so each folder groups the
#    same x<k> across datasets even though the absolute steps differ)
# ----------------------------------------------------------------------
CHECKPOINTS = []  # (exp, dataset, model_label, student, checkpoint_path)

for dataset in DATASETS:
    for student in STUDENTS:

        if RUN_NEGATIVES_SWEEP:
            root = MODELS_ROOT / "negatives_sweep" / dataset
            CHECKPOINTS.append(("negatives_sweep", dataset, f"genq_{student}", student,
                                root / f"genq_{student}"))
            for nneg in NEGATIVES_LIST:
                for variant in VARIANTS:
                    CHECKPOINTS.append(("negatives_sweep", dataset,
                                        f"gpl_{variant}_{student}_nneg{nneg}", student,
                                        root / f"nneg_{nneg}" / f"gpl_{variant}_{student}"))

        if RUN_STEPS_SWEEP:
            root = MODELS_ROOT / "steps_sweep" / dataset
            for k in STEPS_MULTIPLIERS:
                steps = BASE_STEPS[dataset] * k
                for variant in VARIANTS:
                    CHECKPOINTS.append(("steps_sweep", dataset,
                                        f"gpl_{variant}_{student}_x{k}", student,
                                        root / f"steps_{steps}" / f"gpl_{variant}_{student}"))


# ----------------------------------------------------------------------
# 3. EVALUATE CHECKPOINTS
# ----------------------------------------------------------------------
loaded_data = {}  # load each test set only once
missing, done, skipped = [], 0, 0

for exp_name, dataset, model_label, student, checkpoint in CHECKPOINTS:
    output_path = OUTPUT_ROOT / exp_name / model_label / f"{dataset}.json"

    if SKIP_EXISTING and output_path.exists():
        skipped += 1
        continue
    if not (checkpoint / "config.json").exists():
        print(f"MISSING checkpoint, skipped: {checkpoint}")
        missing.append(checkpoint)
        continue

    print(f"\n{'=' * 50}")
    print(f"Experiment: {exp_name} | Dataset: {dataset} | Model: {model_label}")
    print(f"Checkpoint: {checkpoint}")
    print(f"{'=' * 50}")

    model = SentenceTransformer(str(checkpoint), device=testbed.device())

    # Same corpus and queries as the official testbed
    if dataset not in loaded_data:
        loaded_data[dataset] = testbed.load(dataset)
    corpus, queries, _ = loaded_data[dataset]

    # BGE needs its query instruction, as in the testbed baseline
    query_prefix = testbed.BGE_QUERY if student == "BGE" else ""

    # Same document text, cosine ranking and top-k as the testbed dense baselines
    run = testbed.dense_search(model, corpus, queries,
                               query_prefix=query_prefix, batch_size=BATCH_SIZE)

    testbed.save_run(run, output_path)
    print(f"Saved run: {output_path}")
    done += 1

    del model
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

print(f"\nDone: {done} new runs, {skipped} already there, {len(missing)} checkpoints missing.")
for m in missing:
    print(f"  missing: {m}")