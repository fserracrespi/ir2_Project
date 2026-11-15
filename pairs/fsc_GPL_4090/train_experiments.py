from pathlib import Path
import math

from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.train import TrainRetriever
from sentence_transformers import losses
from torch.utils.data import DataLoader

from gpl.toolkit import (
    load_sbert,
    MarginDistillationLoss,
    GenerativePseudoLabelingDataset,
    rescale_gpl_training_data,
)

# 1. CONFIGURATION (same settings as the validated training script)
WORK_DIR = Path(__file__).resolve().parent
GENERATED_ROOT = WORK_DIR / "runs" / "generated_GPL"
MODELS_ROOT = WORK_DIR / "runs" / "models_EXP"

STUDENTS = {"BGE": "BAAI/bge-small-en-v1.5", "MiniLM": "sentence-transformers/all-MiniLM-L6-v2"}
BASE_STEPS = {"scifact": 243, "nfcorpus": 227, "arguana": 271}  # must match gpl_steps in generate_gpl_data.py

QGEN_PREFIX = "query_gen"
BATCH_GPL = 32               # must match BATCH_GPL in generate_experiments.py
BATCH_GENQ = 75
MAX_SEQ_LENGTH = 350

# Both students normalize their embeddings -> margins in [-2, 2];
# the cross-encoder margins (~[-15, 15]) are rescaled to match.
GPL_SCORE_FUNCTION = "cos_sim"
RESCALE_RANGE = (-2.0, 2.0)      # None to disable rescaling

SCHEDULER = "constantlr"         # "constantlr" | "warmupconstant" | "warmuplinear"
LR = 2e-5
WARMUP_RATIO = 0.1               # only used by the "warmup*" schedulers

VARIANTS = ["dense", "bm25"]
SKIP_EXISTING = True             # skip a model whose output folder already has a saved model

# ----------------------------------------------------------------------
# 2. EXPERIMENTS
#
#   negatives_sweep: nneg = 10..50, base steps            (+ GenQ, once)
#   steps_sweep:     nneg = 50, steps = base x 1..5, one data folder per steps value
#
#   data:   runs/generated_GPL/negatives_sweep/<dataset>/base/
#           runs/generated_GPL/negatives_sweep/<dataset>/nneg_<n>/<variant>/
#           runs/generated_GPL/steps_sweep/<dataset>/steps_<s>/<variant>/
#   models: runs/models_exp/negatives_sweep/<dataset>/genq_<student>/
#           runs/models_exp/negatives_sweep/<dataset>/nneg_<n>/gpl_<variant>_<student>/
#           runs/models_exp/steps_sweep/<dataset>/steps_<s>/gpl_<variant>_<student>/
# ----------------------------------------------------------------------

NEGATIVES_LIST = [10, 20, 30, 40, 50]
STEPS_NNEG = 50
STEPS_MULTIPLIERS = [1, 2, 3, 4, 5]

RUN_NEGATIVES_SWEEP = True
RUN_STEPS_SWEEP = True


def warmup_for(steps):
    if SCHEDULER.lower() == "constantlr":
        return 0
    return max(1, int(steps * WARMUP_RATIO))


def already_trained(output_dir):
    return SKIP_EXISTING and (Path(output_dir) / "config.json").exists()


# 3. PREPARE GPL DATA (verification + rescaling, once per folder)
REQUIRED = [
    "corpus.jsonl",
    f"{QGEN_PREFIX}-queries.jsonl",
    f"{QGEN_PREFIX}-qrels/train.tsv",
    "hard-negatives.jsonl",
    "gpl-training-data.tsv",
]
_prepared = {}


def prepare_gpl_data(path):
    path = Path(path)
    if path in _prepared:
        return _prepared[path]

    missing = [f for f in REQUIRED if not (path / f).exists()]
    if missing:
        raise FileNotFoundError(f"Missing files in {path}: {missing}")

    fname = "gpl-training-data.tsv"
    if RESCALE_RANGE is not None:
        if GPL_SCORE_FUNCTION != "cos_sim":
            print(f"WARNING: rescaling while gpl_score_function = {GPL_SCORE_FUNCTION}")
        new_min, new_max = RESCALE_RANGE
        print(f"Rescaling margins in {path} to [{new_min}, {new_max}]")
        fname = rescale_gpl_training_data(str(path), new_min, new_max)
    elif GPL_SCORE_FUNCTION == "cos_sim":
        print("WARNING: no rescaling while gpl_score_function = cos_sim")

    _prepared[path] = path / fname
    return _prepared[path]


def available_steps(gpl_data_file):
    """How many distinct batches the pseudo-label file holds."""
    with open(gpl_data_file) as f:
        rows = sum(1 for line in f if line.strip())
    return rows // BATCH_GPL


# 4. GPL TRAINING (MarginMSE)
def train_gpl(data_path, gpl_data_file, student, output_dir, steps):
    if already_trained(output_dir):
        print(f"Skipping (already trained): {output_dir}")
        return

    corpus, gen_queries, _ = GenericDataLoader(
        str(data_path), prefix=QGEN_PREFIX).load(split="train")

    train_dataset = GenerativePseudoLabelingDataset(
        str(gpl_data_file), gen_queries, corpus)

    train_dataloader = DataLoader(
        train_dataset, shuffle=False, batch_size=BATCH_GPL, drop_last=True)

    passes = steps / max(1, len(train_dataloader))
    if passes > 1:
        print(f"NOTE: {steps} steps over {len(train_dataloader)} batches of data "
              f"-> the pseudo-labels are repeated {passes:.1f} times")

    model = load_sbert(student, max_seq_length=MAX_SEQ_LENGTH)
    train_loss = MarginDistillationLoss(model=model, similarity_fct=GPL_SCORE_FUNCTION)

    warmup_steps = warmup_for(steps)
    print(f"GPL steps: {steps} | scheduler: {SCHEDULER} | warmup: {warmup_steps} | lr: {LR}")
    print(f"Data: {gpl_data_file}")
    print(f"Output: {output_dir}")

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        steps_per_epoch=steps,
        scheduler=SCHEDULER,
        warmup_steps=warmup_steps,
        optimizer_params={"lr": LR},
        output_path=str(output_dir),
        use_amp=False)

# 5. GENQ TRAINING (MNRL)

def train_genq(data_path, student, output_dir):
    if already_trained(output_dir):
        print(f"Skipping (already trained): {output_dir}")
        return

    corpus, gen_queries, gen_qrels = GenericDataLoader(
        str(data_path), prefix=QGEN_PREFIX).load(split="train")

    model = load_sbert(student, max_seq_length=MAX_SEQ_LENGTH)

    retriever = TrainRetriever(model=model, batch_size=BATCH_GENQ)
    train_samples = retriever.load_train(corpus, gen_queries, gen_qrels)
    train_dataloader = retriever.prepare_train(train_samples, shuffle=True)
    train_loss = losses.MultipleNegativesRankingLoss(model=retriever.model)

    steps = math.ceil(len(train_samples) / BATCH_GENQ)
    warmup_steps = warmup_for(steps)
    print(f"GenQ steps: {steps} | scheduler: {SCHEDULER} | warmup: {warmup_steps} | lr: {LR}")

    retriever.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        scheduler=SCHEDULER,
        warmup_steps=warmup_steps,
        optimizer_params={"lr": LR},
        output_path=str(output_dir),
        use_amp=False)


# 6. RUN EXPERIMENTS
def header(text):
    print(f"\n{'=' * 60}\n{text}\n{'=' * 60}")


def negatives_sweep():
    for dataset_key, base_steps in BASE_STEPS.items():
        data_root = GENERATED_ROOT / "negatives_sweep" / dataset_key
        model_root = MODELS_ROOT / "negatives_sweep" / dataset_key

        # Verify and rescale every folder before training anything
        files = {(n, v): prepare_gpl_data(data_root / f"nneg_{n}" / v)
                 for n in NEGATIVES_LIST for v in VARIANTS}

        for model_name, student in STUDENTS.items():
            header(f"[negatives_sweep] {dataset_key} | {model_name}")

            # GenQ does not depend on negatives -> trained once on base/
            print("\nTraining GenQ")
            train_genq(data_root / "base", student, model_root / f"genq_{model_name}")

            for nneg in NEGATIVES_LIST:
                for variant in VARIANTS:
                    print(f"\nTraining GPL {variant} | nneg={nneg} | steps={base_steps}")
                    train_gpl(data_root / f"nneg_{nneg}" / variant, files[(nneg, variant)], student,
                              model_root / f"nneg_{nneg}" / f"gpl_{variant}_{model_name}", base_steps)


def steps_sweep():
    for dataset_key, base_steps in BASE_STEPS.items():
        # Same layout as the negatives sweep: one data folder per steps value,
        # each with its own pseudo-label file generated for exactly that many steps
        data_root = GENERATED_ROOT / "steps_sweep" / dataset_key
        model_root = MODELS_ROOT / "steps_sweep" / dataset_key
        steps_list = [base_steps * k for k in STEPS_MULTIPLIERS]

        # Verify and rescale every folder before training anything
        files = {(s, v): prepare_gpl_data(data_root / f"steps_{s}" / v)
                 for s in steps_list for v in VARIANTS}
        for (s, v), f in files.items():
            n = available_steps(f)
            print(f"{dataset_key}/steps_{s}/{v}: data for {n} distinct steps")
            if n < s:
                print(f"WARNING: {f} holds {n} batches but {s} steps are requested")

        for model_name, student in STUDENTS.items():
            header(f"[steps_sweep] {dataset_key} | {model_name} | nneg={STEPS_NNEG}")
            for k, steps in zip(STEPS_MULTIPLIERS, steps_list):
                for variant in VARIANTS:
                    print(f"\nTraining GPL {variant} | x{k} -> steps={steps}")
                    train_gpl(data_root / f"steps_{steps}" / variant, files[(steps, variant)], student,
                              model_root / f"steps_{steps}" / f"gpl_{variant}_{model_name}", steps)


if __name__ == "__main__":
    if RUN_NEGATIVES_SWEEP:
        negatives_sweep()
    if RUN_STEPS_SWEEP:
        steps_sweep()
    print("\nAll training experiments completed.")