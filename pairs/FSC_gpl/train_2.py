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
)


# 1. CONFIGURATION


ROOT = Path("/app/pairs/FSC_gpl/runs")

CONFIGS = {"scifact": {"gpl_steps": 243}, "nfcorpus": {"gpl_steps": 227}}
STUDENTS = { "BGE": "BAAI/bge-small-en-v1.5", "MiniLM": "sentence-transformers/all-MiniLM-L6-v2"}

QGEN_PREFIX = "query_gen"

BATCH_GPL = 32
BATCH_GENQ = 16
MAX_SEQ_LENGTH = 350



# 2. GPL TRAINING FUNCTION


def train_gpl(
    data_path,
    student,
    output_dir,
    steps):

    corpus, gen_queries, _ = GenericDataLoader(
        str(data_path),
        prefix=QGEN_PREFIX).load(split="train")

    train_dataset = GenerativePseudoLabelingDataset(
        str(data_path / "gpl-training-data.tsv"),
        gen_queries,
        corpus)

    train_dataloader = DataLoader(
        train_dataset,
        shuffle=False,
        batch_size=BATCH_GPL,
        drop_last=True)

    model = load_sbert(
        student,
        max_seq_length=MAX_SEQ_LENGTH)

    train_loss = MarginDistillationLoss(
        model=model,
        similarity_fct="dot")

    warmup_steps = max(1, int(steps * 0.1))

    print(f"GPL steps: {steps}")
    print(f"Warmup steps: {warmup_steps}")

    model.fit(
        train_objectives=[
            (train_dataloader, train_loss)],
        epochs=1,
        steps_per_epoch=steps,
        warmup_steps=warmup_steps,
        output_path=str(output_dir),
        use_amp=False)


# 3. GENQ TRAINING FUNCTION (MNRL)

def train_genq(
    data_path,
    student,
    output_dir):

    corpus, gen_queries, gen_qrels = GenericDataLoader(
        str(data_path),
        prefix=QGEN_PREFIX).load(split="train")

    model = load_sbert(
        student,
        max_seq_length=MAX_SEQ_LENGTH)

    retriever = TrainRetriever(
        model=model,
        batch_size=BATCH_GENQ)

    train_samples = retriever.load_train(
        corpus,
        gen_queries,
        gen_qrels)

    train_dataloader = retriever.prepare_train(
        train_samples,
        shuffle=True)

    train_loss = losses.MultipleNegativesRankingLoss(
        model=retriever.model)

    steps = math.ceil(len(train_samples) / BATCH_GENQ)

    warmup_steps = max(1, int(steps * 0.1))

    print(f"GenQ steps: {steps}")
    print(f"Warmup steps: {warmup_steps}")

    retriever.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        warmup_steps=warmup_steps,
        output_path=str(output_dir),
        use_amp=False)

# 4. RUN EXPERIMENTS

for dataset_key, cfg in CONFIGS.items():

    GPL_STEPS = cfg["gpl_steps"]

    generated_path = ROOT / "generated_gpl/test" / dataset_key
    bm25_generated_path = ROOT / "generated_gpl/test_bm25" / dataset_key

    # Verify generation is complete
    for path in [generated_path, bm25_generated_path]:

        required_files = [path / "corpus.jsonl",
                            path / f"{QGEN_PREFIX}-queries.jsonl",
                            path / f"{QGEN_PREFIX}-qrels/train.tsv",
                            path / "hard-negatives.jsonl",
                            path / "gpl-training-data.tsv"]

    for model_name, student in STUDENTS.items():

        print(f"\n{'=' * 50}")
        print(f"Dataset: {dataset_key}")
        print(f"Student: {model_name}")
        print(f"{'=' * 50}")

        # Model outputs
        gpl_output = ROOT / f"models/test/gpl_{model_name}" / dataset_key
        genq_output = ROOT / f"models/test/genq_{model_name}" / dataset_key
        bm25_output = ROOT / f"models/test/gpl_bm25_{model_name}" / dataset_key

        # A. GPL: DENSE NEGATIVES + MARGINMSE

        print("\nTraining GPL Dense")

        train_gpl(
            data_path=generated_path,
            student=student,
            output_dir=gpl_output,
            steps=GPL_STEPS)

        # B. GENQ: MNRL
        
        print("\nTraining GenQ")

        train_genq(
            data_path=generated_path,
            student=student,
            output_dir=genq_output)

        # C. GPL: BM25 NEGATIVES + MARGINMSE
        
        print("\nTraining GPL BM25")

        train_gpl(
            data_path=bm25_generated_path,
            student=student,
            output_dir=bm25_output,
            steps=GPL_STEPS,
        )

        print(f"\nCompleted: {dataset_key} - {model_name}")

print("\nAll training experiments completed.")

#GPL — BGE / SciFact TERMINADO