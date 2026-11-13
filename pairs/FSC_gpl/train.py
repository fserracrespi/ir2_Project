from pathlib import Path
from huggingface_hub import snapshot_download
import shutil

import gpl
from gpl.toolkit import mnrl

# 1. CONFIGURATION

ROOT = Path("/app/pairs/FSC_gpl/runs")
DATASETS = {"scifact": "/app/data/scifact", "nfcorpus": "/app/data/nfcorpus"}

GENERATOR = "doc2query/msmarco-t5-base-v1"
TEACHER = "cross-encoder/ms-marco-MiniLM-L6-v2"
STUDENTS = ["BAAI/bge-small-en-v1.5", "sentence-transformers/all-MiniLM-L6-v2"]

RETRIEVERS = ["sentence-transformers/msmarco-distilbert-base-v3", "sentence-transformers/msmarco-MiniLM-L6-v3"]

QGEN_PREFIX = "query_gen"


# 2. DOWNLOAD MODELS

models = [GENERATOR, TEACHER, *STUDENTS, *RETRIEVERS]

for model_name in models:
    snapshot_download(
        repo_id=model_name,
        max_workers=8,
    )
    print(f"Downloaded: {model_name}")


# 3. TRAIN GPL, GENQ AND GPL BM25

for dataset_key, dataset_path in DATASETS.items():

    if dataset_key == "scifact":
        NEW_SIZE = 2592
        QUERIES_PER_PASSAGE = 3
        GPL_STEPS = 972

    if dataset_key == "nfcorpus":
        NEW_SIZE = 1816
        QUERIES_PER_PASSAGE = 4
        GPL_STEPS = 908

    for STUDENT in STUDENTS:
        if STUDENT == "BAAI/bge-small-en-v1.5":
            MODEL_STUDENT='BGE'
        if STUDENT ==  "sentence-transformers/all-MiniLM-L6-v2":
            MODEL_STUDENT='MiniLM'

        print(f"\nStarting experiments: {dataset_key} with Student {MODEL_STUDENT}")

        generated_path = (ROOT/f"generated_gpl/test"/dataset_key)
        bm25_generated_path = (ROOT/f"generated_gpl/test_bm25"/dataset_key)

        gpl_output = (ROOT/f"models/test/gpl_{MODEL_STUDENT}"/dataset_key)
        genq_output = (ROOT/f"models/test/genq_{MODEL_STUDENT}"/dataset_key)
        bm25_output = (ROOT/f"models/test/gpl_bm25_{MODEL_STUDENT}"/dataset_key)
        evaluation_path = (ROOT/f"evaluation/test_{MODEL_STUDENT}"/dataset_key)

        bm25_evaluation_path = (ROOT/f"evaluation/test_bm25"/dataset_key)

        generated_path.mkdir(parents=True, exist_ok=True)
        bm25_generated_path.mkdir(parents=True, exist_ok=True)

        # A. GPL: QGen + Dense Negatives + Teacher + MarginMSE

        print(f"Training GPL: {dataset_key}")

        gpl.train(
            path_to_generated_data=str(generated_path),

            # Student
            base_ckpt=STUDENT,
            gpl_score_function="dot",

            # Training
            gpl_steps=GPL_STEPS,
            new_size=NEW_SIZE,
            queries_per_passage=QUERIES_PER_PASSAGE,
            batch_size_generation=8,
            batch_size_gpl=8,
            negatives_per_query=10,

            # Output
            output_dir=str(gpl_output),
            evaluation_data=dataset_path,
            evaluation_output=str(evaluation_path),

            # Query generation
            generator=GENERATOR,
            qgen_prefix=QGEN_PREFIX,

            # Hard-negative mining
            retrievers=RETRIEVERS,
            retriever_score_functions=["cos_sim", "cos_sim"],

            # Teacher
            cross_encoder=TEACHER,
        )

        print(f"GPL finished: {dataset_key}")


        # B. GENQ: Same Synthetic Queries + MNRL

        print(f"Training GenQ: {dataset_key}")

        # Reuse the queries and qrels created by GPL.

        mnrl(
            data_path=str(generated_path),
            base_ckpt=STUDENT,
            output_dir=str(genq_output),
            max_seq_length=350,
            use_amp=False,
            qgen_prefix=QGEN_PREFIX,
        )

        print(f"GenQ finished: {dataset_key}")

        # C. GPL ABLATION: BM25 Negatives + Teacher + MarginMSE

        print(f"Training GPL BM25: {dataset_key}")

        # Reuse exactly the same synthetic queries and corpus.
        # BM25 will generate its own hard negatives.

        shutil.copy2(generated_path/"corpus.jsonl", bm25_generated_path/"corpus.jsonl")
        shutil.copy2(generated_path/f"{QGEN_PREFIX}-queries.jsonl", bm25_generated_path/f"{QGEN_PREFIX}-queries.jsonl")
        shutil.copytree(generated_path/f"{QGEN_PREFIX}-qrels", bm25_generated_path/f"{QGEN_PREFIX}-qrels", dirs_exist_ok=True)

        gpl.train(
            path_to_generated_data=str(bm25_generated_path),

            # Student
            base_ckpt=STUDENT,
            gpl_score_function="dot",

            # Training
            gpl_steps=GPL_STEPS,
            new_size=NEW_SIZE,
            queries_per_passage=QUERIES_PER_PASSAGE,
            batch_size_generation=8,
            batch_size_gpl=8,
            negatives_per_query=10,

            # Output
            output_dir=str(bm25_output),
            evaluation_data=dataset_path,
            evaluation_output=str(bm25_evaluation_path),

            # Query generation
            generator=GENERATOR,
            qgen_prefix=QGEN_PREFIX,

            # Hard-negative mining: BM25
            retrievers=["bm25"],
            retriever_score_functions=["none"],

            # Teacher
            cross_encoder=TEACHER,
        )

        print(f"GPL BM25 finished: {dataset_key}")


    print("\nAll GPL / GenQ / GPL Ablation BM25 experiments completed.")
