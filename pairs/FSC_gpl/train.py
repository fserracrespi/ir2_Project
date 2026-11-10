from huggingface_hub import snapshot_download
import gpl 

models = [
    "doc2query/msmarco-t5-base-v1", #generator
    "cross-encoder/ms-marco-MiniLM-L6-v2", #crossencoder
    "BAAI/bge-small-en-v1.5", #student
    "sentence-transformers/msmarco-distilbert-base-v3", #bi_encoder_1
    "sentence-transformers/msmarco-MiniLM-L6-v3", #bi_encoder_2
]

for model_name in models:
    snapshot_download(repo_id=model_name, max_workers=8)
    print(f"Downloaded: {model_name}")



data_dict = {"scifact": "/app/data/scifact", "nfcorpus": "/app/data/nfcorpus"}

for dataset_key, dataset in data_dict.items():

    print(f"Starting GPL smoke test: {dataset_key}")

    gpl.train(
        path_to_generated_data=f"/app/pairs/FSC_gpl/runs/generated_gpl/smoke/{dataset_key}",

        # Student
        base_ckpt= "BAAI/bge-small-en-v1.5",  
        gpl_score_function="dot",

        # Smoke test
        gpl_steps=100,
        new_size=100,
        queries_per_passage=1,
        batch_size_generation=3,
        batch_size_gpl=4,
        negatives_per_query=5,

        # Output
        output_dir=f"/app/pairs/FSC_gpl/runs/models/smoke/{dataset_key}",
        evaluation_data=dataset,
        evaluation_output=f"/app/pairs/FSC_gpl/runs/evaluation/smoke/{dataset_key}",

        # Generator
        generator="doc2query/msmarco-t5-base-v1",

        # Hard negative mining
        retrievers=[
            "sentence-transformers/msmarco-distilbert-base-v3",
            "sentence-transformers/msmarco-MiniLM-L6-v3"
        ],
        retriever_score_functions=["cos_sim", "cos_sim"],

        # Pseudo labeling
        cross_encoder="cross-encoder/ms-marco-MiniLM-L-6-v2",

        qgen_prefix="query_gen",

        # Evaluation Stoped
        # do_evaluation=True,
        # eval_split="test",
        # use_train_qrels=False
    )

    print(f"Smoke test finished: {dataset_key}")

'''
gpl.train(
        path_to_generated_data=f"/app/pairs/FSC_gpl/runs/generated_gpl/real/{dataset_key}",

        # Student
        base_ckpt="BAAI/bge-small-en-v1.5",  
        gpl_score_function="dot",

        # Real test
        gpl_steps=1000,
        new_size=1000,  # None = full corpus
        queries_per_passage=3,
        batch_size_generation=2,
        batch_size_gpl=8,
        negatives_per_query=50,

        # Output
        output_dir=f"/app/pairs/FSC_gpl/runs/models/real/{dataset_key}",
        evaluation_data=dataset,
        evaluation_output=f"/app/pairs/FSC_gpl/runs/evaluation/real/{dataset_key}",

        # Generator
        generator="doc2query/msmarco-t5-base-v1",

        # Hard negative mining
        retrievers=[
            "sentence-transformers/msmarco-distilbert-base-v3",
            "sentence-transformers/msmarco-MiniLM-L6-v3"
        ],
        retriever_score_functions=["cos_sim", "cos_sim"],

        # Pseudo labeling
        cross_encoder="cross-encoder/ms-marco-MiniLM-L-6-v2",

        qgen_prefix="query_gen",
        do_evaluation=True,
        eval_split="test",
        use_train_qrels=False)
'''