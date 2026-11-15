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


QGEN_PREFIX = "query_gen"


# ----------------------------------------------------------------------
# GPL TRAINING (MarginMSE on pseudo-labels)
# ----------------------------------------------------------------------
def train_gpl(data_path, student, output_dir, steps, batch_size=32, max_seq_length=350):

    data_path = Path(data_path)

    corpus, gen_queries, _ = GenericDataLoader(
        str(data_path), prefix=QGEN_PREFIX
    ).load(split="train")

    train_dataset = GenerativePseudoLabelingDataset(
        str(data_path / "gpl-training-data.tsv"),
        gen_queries,
        corpus,
    )

    train_dataloader = DataLoader(
        train_dataset,
        shuffle=False,
        batch_size=batch_size,
        drop_last=True,
    )

    model = load_sbert(student, max_seq_length=max_seq_length)

    train_loss = MarginDistillationLoss(model=model, similarity_fct="dot")

    warmup_steps = max(1, int(steps * 0.1))
    print(f"GPL steps: {steps}")
    print(f"Warmup steps: {warmup_steps}")

    model.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        steps_per_epoch=steps,
        warmup_steps=warmup_steps,
        output_path=str(output_dir),
        use_amp=False,
    )


# ----------------------------------------------------------------------
# GENQ TRAINING (MultipleNegativesRankingLoss, in-batch negatives)
# ----------------------------------------------------------------------
def train_genq(data_path, student, output_dir, batch_size=16, max_seq_length=350):

    corpus, gen_queries, gen_qrels = GenericDataLoader(
        str(data_path), prefix=QGEN_PREFIX
    ).load(split="train")

    model = load_sbert(student, max_seq_length=max_seq_length)

    retriever = TrainRetriever(model=model, batch_size=batch_size)

    train_samples = retriever.load_train(corpus, gen_queries, gen_qrels)
    train_dataloader = retriever.prepare_train(train_samples, shuffle=True)

    train_loss = losses.MultipleNegativesRankingLoss(model=retriever.model)

    steps = math.ceil(len(train_samples) / batch_size)
    warmup_steps = max(1, int(steps * 0.1))
    print(f"GenQ steps: {steps}")
    print(f"Warmup steps: {warmup_steps}")

    retriever.fit(
        train_objectives=[(train_dataloader, train_loss)],
        epochs=1,
        warmup_steps=warmup_steps,
        output_path=str(output_dir),
        use_amp=False,
    )


# ----------------------------------------------------------------------
# RUN EXPERIMENTS (same layout as the generation script)
#
#   runs/generated_GPL/<experiment>/<dataset>/base/               -> GenQ
#   runs/generated_GPL/<experiment>/<dataset>/nneg_<n>/dense/     -> GPL dense
#   runs/generated_GPL/<experiment>/<dataset>/nneg_<n>/bm25/      -> GPL bm25
#
#   runs/models/<experiment>/<dataset>/genq_<student>/
#   runs/models/<experiment>/<dataset>/nneg_<n>/gpl_dense_<student>/
#   runs/models/<experiment>/<dataset>/nneg_<n>/gpl_bm25_<student>/
# ----------------------------------------------------------------------
if __name__ == "__main__":
    WORK_DIR = Path(__file__).resolve().parent
    GENERATED_ROOT = WORK_DIR / "runs" / "generated_GPL"  
    MODELS_ROOT = WORK_DIR / "runs" / "models_exp"

    STUDENTS = {
        "BGE": "BAAI/bge-small-en-v1.5",
        "MiniLM": "sentence-transformers/all-MiniLM-L6-v2",
    }

    BATCH_GENQ = 16

    EXPERIMENTS = {
        "negatives_sweep": {
            "negatives_list": [10, 20, 30, 40, 50],
            "datasets": {
                "scifact": {"gpl_steps": 243, "batch_gpl": 32, "max_seq_length": 350},
                "nfcorpus": {"gpl_steps": 227, "batch_gpl": 32, "max_seq_length": 350},
            },
        },
        "ideal": {
            "negatives_list": [50],
            "datasets": {
                "scifact": {"gpl_steps": 10_000, "batch_gpl": 32, "max_seq_length": 350},
                "nfcorpus": {"gpl_steps": 10_000, "batch_gpl": 32, "max_seq_length": 350},
            },
        },
    }

    VARIANTS = ["dense", "bm25"]

    for exp_name, exp in EXPERIMENTS.items():
        for dataset_key, cfg in exp["datasets"].items():

            data_root = GENERATED_ROOT / exp_name / dataset_key
            model_root = MODELS_ROOT / exp_name / dataset_key

            for model_name, student in STUDENTS.items():

                print(f"\n{'=' * 50}")
                print(f"[{exp_name}] Dataset: {dataset_key} | Student: {model_name}")
                print(f"{'=' * 50}")

                # A. GENQ: does not depend on negatives -> trained once on base/
                genq_output = model_root / f"genq_{model_name}"
                print("\nTraining GenQ")
                train_genq(
                    data_path=data_root / "base",
                    student=student,
                    output_dir=genq_output,
                    batch_size=BATCH_GENQ,
                    max_seq_length=cfg["max_seq_length"],
                )

                # B. GPL: one model per negatives_per_query and variant
                for nneg in exp["negatives_list"]:
                    for variant in VARIANTS:

                        data_path = data_root / f"nneg_{nneg}" / variant
                        output_dir = model_root / f"nneg_{nneg}" / f"gpl_{variant}_{model_name}"

                        print(f"\nTraining GPL {variant} | nneg={nneg}")
                        train_gpl(
                            data_path=data_path,
                            student=student,
                            output_dir=output_dir,
                            steps=cfg["gpl_steps"],
                            batch_size=cfg["batch_gpl"],
                            max_seq_length=cfg["max_seq_length"],
                        )

                print(f"\nCompleted: [{exp_name}] {dataset_key} - {model_name}")

    print("\nAll training experiments completed.")