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


# 1. CONFIGURATION
WORK_DIR = Path(__file__).resolve().parent
ROOT = WORK_DIR / "runs"

CONFIGS = {"scifact": {"gpl_steps": 243}, "nfcorpus": {"gpl_steps": 227}, "arguana": {"gpl_steps":271}}
STUDENTS = {"BGE": "BAAI/bge-small-en-v1.5", "MiniLM": "sentence-transformers/all-MiniLM-L6-v2"}

QGEN_PREFIX = "query_gen"

BATCH_GPL = 32
BATCH_GENQ = 75
MAX_SEQ_LENGTH = 350

# Student similarity function and margin rescaling.
# Both students normalize their embeddings, so their margin lies in [-2, 2],
# while the cross-encoder produces margins in logits (roughly [-15, 15]).
# Without rescaling, MarginMSE chases unreachable targets.
GPL_SCORE_FUNCTION = "cos_sim"   # "dot" or "cos_sim"
RESCALE_RANGE = (-2.0, 2.0)      # None to disable rescaling

# Learning-rate scheduler (sentence-transformers):
#   "constantlr"     -> fixed LR, no warmup, no decay
#   "warmupconstant" -> warmup, then fixed LR
#   "warmuplinear"   -> default: warmup + linear decay to 0
SCHEDULER = "constantlr"
LR = 2e-5
WARMUP_RATIO = 0.1               # only used by the "warmup*" schedulers


def warmup_for(steps):
    if SCHEDULER.lower() == "constantlr":
        return 0
    return max(1, int(steps * WARMUP_RATIO))


# 2. PREPARE GPL DATA (verification + rescaling, once per folder)

REQUIRED = [
    "corpus.jsonl",
    f"{QGEN_PREFIX}-queries.jsonl",
    f"{QGEN_PREFIX}-qrels/train.tsv",
    "hard-negatives.jsonl",
    "gpl-training-data.tsv",
]


def prepare_gpl_data(path):
    missing = [f for f in REQUIRED if not (path / f).exists()]
    if missing:
        raise FileNotFoundError(f"Missing files in {path}: {missing}")

    fname = "gpl-training-data.tsv"
    if RESCALE_RANGE is not None:
        if GPL_SCORE_FUNCTION != "cos_sim":
            print(f"WARNING: rescaling while gpl_score_function = {GPL_SCORE_FUNCTION}")
        new_min, new_max = RESCALE_RANGE
        print(f"Rescaling margins in {path} to [{new_min}, {new_max}]")
        # Writes a new file and returns its name; the original is left untouched
        fname = rescale_gpl_training_data(str(path), new_min, new_max)
    elif GPL_SCORE_FUNCTION == "cos_sim":
        print("WARNING: no rescaling while gpl_score_function = cos_sim")

    return path / fname


# 3. GPL TRAINING (MarginMSE)

def train_gpl(data_path, gpl_data_file, student, output_dir, steps):
    corpus, gen_queries, _ = GenericDataLoader(
        str(data_path), prefix=QGEN_PREFIX).load(split="train")

    train_dataset = GenerativePseudoLabelingDataset(
        str(gpl_data_file), gen_queries, corpus)

    train_dataloader = DataLoader(
        train_dataset, shuffle=False, batch_size=BATCH_GPL, drop_last=True)

    model = load_sbert(student, max_seq_length=MAX_SEQ_LENGTH)

    train_loss = MarginDistillationLoss(
        model=model, similarity_fct=GPL_SCORE_FUNCTION)

    warmup_steps = warmup_for(steps)
    print(f"GPL steps: {steps} | scheduler: {SCHEDULER} | warmup: {warmup_steps} | lr: {LR}")
    print(f"Data: {gpl_data_file}")

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        steps_per_epoch=steps,
        scheduler=SCHEDULER,
        warmup_steps=warmup_steps,
        optimizer_params={"lr": LR},
        output_path=str(output_dir),
        use_amp=False)


# 4. GENQ TRAINING (MNRL)

def train_genq(data_path, student, output_dir):
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


# 5. RUN EXPERIMENTS

for dataset_key, cfg in CONFIGS.items():
    GPL_STEPS = cfg["gpl_steps"]

    generated_path = ROOT / "generated_gpl_smoke/test_smoke" / dataset_key
    bm25_generated_path = ROOT / "generated_gpl_smoke/test_bm25_smoke" / dataset_key

    # Verify and rescale ONCE per folder (not once per student)
    dense_gpl_file = prepare_gpl_data(generated_path)
    bm25_gpl_file = prepare_gpl_data(bm25_generated_path)

    for model_name, student in STUDENTS.items():
        print(f"\n{'=' * 50}")
        print(f"Dataset: {dataset_key}")
        print(f"Student: {model_name}")
        print(f"{'=' * 50}")

        gpl_output = ROOT / f"models_smoke/gpl_{model_name}" / dataset_key
        genq_output = ROOT / f"models_smoke/genq_{model_name}" / dataset_key
        bm25_output = ROOT / f"models_smoke/gpl_bm25_{model_name}" / dataset_key

        print("\nTraining GPL Dense")
        train_gpl(generated_path, dense_gpl_file, student, gpl_output, GPL_STEPS)

        print("\nTraining GenQ")
        train_genq(generated_path, student, genq_output)

        print("\nTraining GPL BM25")
        train_gpl(bm25_generated_path, bm25_gpl_file, student, bm25_output, GPL_STEPS)

        print(f"\nCompleted: {dataset_key} - {model_name}")

print("\nAll training experiments completed.")