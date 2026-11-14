# Shared results table

Built by `build_table.py` from `baselines/scores.json` and `pairs/*/results.json`: do not edit by hand.
A difference is in bold only when its p-value is below 0.05 and its confidence interval excludes zero.
Pair 00 is the instructor's worked example from the model presentation.

## SciFact

| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |
|---|:-:|:-:|---|:-:|:-:|
| *BM25* | 0.676 | 0.918 | | | |
| *all-MiniLM-L6-v2* | 0.646 | 0.925 | | | |
| *bge-small-en-v1.5* | 0.710 | 0.948 | | | |
| *RRF (BM25 + MiniLM)* | 0.718 | 0.948 | | | |
| *BM25 top-100 + cross-encoder* | 0.688 | 0.918 | | | |
| genq_BGE ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.642 | 0.924 | bge-small-en-v1.5 | **-0.068 [-0.092, -0.045]** | < 0.001 |
| genq_MiniLM ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.630 | 0.910 | all-MiniLM-L6-v2 | -0.016 [-0.038, +0.006] | 0.164 |
| gpl_BGE ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.459 | 0.815 | bge-small-en-v1.5 | **-0.251 [-0.295, -0.208]** | < 0.001 |
| gpl_MiniLM ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.412 | 0.782 | all-MiniLM-L6-v2 | **-0.234 [-0.278, -0.190]** | < 0.001 |
| gpl_bm25_BGE ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.438 | 0.735 | bge-small-en-v1.5 | **-0.272 [-0.318, -0.226]** | < 0.001 |
| gpl_bm25_MiniLM ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.419 | 0.756 | all-MiniLM-L6-v2 | **-0.227 [-0.271, -0.183]** | < 0.001 |

## NFCorpus

| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |
|---|:-:|:-:|---|:-:|:-:|
| *BM25* | 0.321 | 0.246 | | | |
| *all-MiniLM-L6-v2* | 0.316 | 0.311 | | | |
| *bge-small-en-v1.5* | 0.340 | 0.304 | | | |
| *RRF (BM25 + MiniLM)* | 0.342 | 0.310 | | | |
| *BM25 top-100 + cross-encoder* | 0.347 | 0.246 | | | |
| genq_BGE ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.339 | 0.320 | bge-small-en-v1.5 | -0.002 [-0.012, +0.009] | 0.786 |
| genq_MiniLM ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.313 | 0.295 | all-MiniLM-L6-v2 | -0.003 [-0.014, +0.008] | 0.579 |
| gpl_BGE ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.302 | 0.268 | bge-small-en-v1.5 | **-0.038 [-0.055, -0.021]** | < 0.001 |
| gpl_MiniLM ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.276 | 0.254 | all-MiniLM-L6-v2 | **-0.041 [-0.056, -0.025]** | < 0.001 |
| gpl_bm25_BGE ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.302 | 0.258 | bge-small-en-v1.5 | **-0.038 [-0.056, -0.021]** | < 0.001 |
| gpl_bm25_MiniLM ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.271 | 0.261 | all-MiniLM-L6-v2 | **-0.046 [-0.062, -0.030]** | < 0.001 |

## ArguAna

| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |
|---|:-:|:-:|---|:-:|:-:|
| *BM25* | 0.516 | 0.969 | | | |
| *all-MiniLM-L6-v2* | 0.503 | 0.977 | | | |
| *bge-small-en-v1.5* | 0.606 | 0.986 | | | |
| *RRF (BM25 + MiniLM)* | 0.549 | 0.985 | | | |
| *BM25 top-100 + cross-encoder* | 0.422 | 0.969 | | | |
