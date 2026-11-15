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
| genq_BGE (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.657 | 0.934 | RRF (BM25 + MiniLM) | **-0.060 [-0.089, -0.031]** | < 0.001 |
| genq_BGE (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.657 | 0.934 | bge-small-en-v1.5 | **-0.052 [-0.075, -0.031]** | < 0.001 |
| genq_MiniLM (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.639 | 0.934 | RRF (BM25 + MiniLM) | **-0.079 [-0.108, -0.051]** | < 0.001 |
| genq_MiniLM (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.639 | 0.934 | all-MiniLM-L6-v2 | -0.006 [-0.029, +0.016] | 0.587 |
| gpl_bm25_BGE_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.114 | 0.259 | RRF (BM25 + MiniLM) | **-0.603 [-0.651, -0.554]** | < 0.001 |
| gpl_bm25_BGE_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.114 | 0.259 | bge-small-en-v1.5 | **-0.595 [-0.644, -0.546]** | < 0.001 |
| gpl_bm25_MiniLM_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.260 | 0.465 | RRF (BM25 + MiniLM) | **-0.458 [-0.507, -0.410]** | < 0.001 |
| gpl_bm25_MiniLM_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.260 | 0.465 | all-MiniLM-L6-v2 | **-0.386 [-0.435, -0.337]** | < 0.001 |
| gpl_dense_BGE_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.231 | 0.424 | RRF (BM25 + MiniLM) | **-0.487 [-0.538, -0.434]** | < 0.001 |
| gpl_dense_BGE_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.231 | 0.424 | bge-small-en-v1.5 | **-0.479 [-0.531, -0.427]** | < 0.001 |
| gpl_dense_MiniLM_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.337 | 0.604 | RRF (BM25 + MiniLM) | **-0.381 [-0.433, -0.330]** | < 0.001 |
| gpl_dense_MiniLM_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.337 | 0.604 | all-MiniLM-L6-v2 | **-0.309 [-0.360, -0.258]** | < 0.001 |
| genq_BGE (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.662 | 0.935 | RRF (BM25 + MiniLM) | **-0.056 [-0.086, -0.026]** | < 0.001 |
| genq_BGE (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.662 | 0.935 | bge-small-en-v1.5 | **-0.048 [-0.071, -0.026]** | < 0.001 |
| genq_MiniLM (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.636 | 0.920 | RRF (BM25 + MiniLM) | **-0.081 [-0.112, -0.052]** | < 0.001 |
| genq_MiniLM (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.636 | 0.920 | all-MiniLM-L6-v2 | -0.009 [-0.033, +0.015] | 0.457 |
| gpl_bm25_BGE_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.430 | 0.731 | RRF (BM25 + MiniLM) | **-0.288 [-0.335, -0.241]** | < 0.001 |
| gpl_bm25_BGE_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.430 | 0.731 | bge-small-en-v1.5 | **-0.280 [-0.327, -0.234]** | < 0.001 |
| gpl_bm25_BGE_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.433 | 0.754 | RRF (BM25 + MiniLM) | **-0.285 [-0.330, -0.238]** | < 0.001 |
| gpl_bm25_BGE_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.433 | 0.754 | bge-small-en-v1.5 | **-0.277 [-0.323, -0.232]** | < 0.001 |
| gpl_bm25_BGE_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.458 | 0.775 | RRF (BM25 + MiniLM) | **-0.259 [-0.304, -0.213]** | < 0.001 |
| gpl_bm25_BGE_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.458 | 0.775 | bge-small-en-v1.5 | **-0.252 [-0.295, -0.208]** | < 0.001 |
| gpl_bm25_BGE_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.462 | 0.765 | RRF (BM25 + MiniLM) | **-0.255 [-0.301, -0.209]** | < 0.001 |
| gpl_bm25_BGE_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.462 | 0.765 | bge-small-en-v1.5 | **-0.247 [-0.292, -0.203]** | < 0.001 |
| gpl_bm25_BGE_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.475 | 0.800 | RRF (BM25 + MiniLM) | **-0.242 [-0.286, -0.198]** | < 0.001 |
| gpl_bm25_BGE_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.475 | 0.800 | bge-small-en-v1.5 | **-0.235 [-0.278, -0.193]** | < 0.001 |
| gpl_bm25_MiniLM_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.426 | 0.766 | RRF (BM25 + MiniLM) | **-0.292 [-0.339, -0.248]** | < 0.001 |
| gpl_bm25_MiniLM_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.426 | 0.766 | all-MiniLM-L6-v2 | **-0.220 [-0.264, -0.176]** | < 0.001 |
| gpl_bm25_MiniLM_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.438 | 0.773 | RRF (BM25 + MiniLM) | **-0.280 [-0.326, -0.234]** | < 0.001 |
| gpl_bm25_MiniLM_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.438 | 0.773 | all-MiniLM-L6-v2 | **-0.207 [-0.252, -0.163]** | < 0.001 |
| gpl_bm25_MiniLM_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.432 | 0.791 | RRF (BM25 + MiniLM) | **-0.286 [-0.332, -0.240]** | < 0.001 |
| gpl_bm25_MiniLM_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.432 | 0.791 | all-MiniLM-L6-v2 | **-0.213 [-0.258, -0.170]** | < 0.001 |
| gpl_bm25_MiniLM_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.441 | 0.808 | RRF (BM25 + MiniLM) | **-0.276 [-0.322, -0.231]** | < 0.001 |
| gpl_bm25_MiniLM_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.441 | 0.808 | all-MiniLM-L6-v2 | **-0.204 [-0.248, -0.161]** | < 0.001 |
| gpl_bm25_MiniLM_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.443 | 0.810 | RRF (BM25 + MiniLM) | **-0.275 [-0.321, -0.231]** | < 0.001 |
| gpl_bm25_MiniLM_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.443 | 0.810 | all-MiniLM-L6-v2 | **-0.203 [-0.246, -0.160]** | < 0.001 |
| gpl_dense_BGE_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.471 | 0.819 | RRF (BM25 + MiniLM) | **-0.247 [-0.292, -0.201]** | < 0.001 |
| gpl_dense_BGE_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.471 | 0.819 | bge-small-en-v1.5 | **-0.239 [-0.282, -0.197]** | < 0.001 |
| gpl_dense_BGE_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.480 | 0.832 | RRF (BM25 + MiniLM) | **-0.237 [-0.281, -0.194]** | < 0.001 |
| gpl_dense_BGE_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.480 | 0.832 | bge-small-en-v1.5 | **-0.230 [-0.271, -0.188]** | < 0.001 |
| gpl_dense_BGE_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.475 | 0.832 | RRF (BM25 + MiniLM) | **-0.243 [-0.286, -0.198]** | < 0.001 |
| gpl_dense_BGE_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.475 | 0.832 | bge-small-en-v1.5 | **-0.235 [-0.277, -0.194]** | < 0.001 |
| gpl_dense_BGE_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.487 | 0.829 | RRF (BM25 + MiniLM) | **-0.230 [-0.273, -0.186]** | < 0.001 |
| gpl_dense_BGE_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.487 | 0.829 | bge-small-en-v1.5 | **-0.223 [-0.264, -0.181]** | < 0.001 |
| gpl_dense_BGE_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.497 | 0.847 | RRF (BM25 + MiniLM) | **-0.221 [-0.264, -0.177]** | < 0.001 |
| gpl_dense_BGE_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.497 | 0.847 | bge-small-en-v1.5 | **-0.213 [-0.255, -0.172]** | < 0.001 |
| gpl_dense_MiniLM_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.421 | 0.800 | RRF (BM25 + MiniLM) | **-0.296 [-0.343, -0.250]** | < 0.001 |
| gpl_dense_MiniLM_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.421 | 0.800 | all-MiniLM-L6-v2 | **-0.224 [-0.268, -0.180]** | < 0.001 |
| gpl_dense_MiniLM_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.429 | 0.819 | RRF (BM25 + MiniLM) | **-0.289 [-0.334, -0.245]** | < 0.001 |
| gpl_dense_MiniLM_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.429 | 0.819 | all-MiniLM-L6-v2 | **-0.216 [-0.259, -0.173]** | < 0.001 |
| gpl_dense_MiniLM_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.434 | 0.819 | RRF (BM25 + MiniLM) | **-0.284 [-0.329, -0.240]** | < 0.001 |
| gpl_dense_MiniLM_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.434 | 0.819 | all-MiniLM-L6-v2 | **-0.212 [-0.255, -0.169]** | < 0.001 |
| gpl_dense_MiniLM_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.446 | 0.834 | RRF (BM25 + MiniLM) | **-0.272 [-0.319, -0.227]** | < 0.001 |
| gpl_dense_MiniLM_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.446 | 0.834 | all-MiniLM-L6-v2 | **-0.200 [-0.244, -0.156]** | < 0.001 |
| gpl_dense_MiniLM_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.459 | 0.838 | RRF (BM25 + MiniLM) | **-0.258 [-0.304, -0.214]** | < 0.001 |
| gpl_dense_MiniLM_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.459 | 0.838 | all-MiniLM-L6-v2 | **-0.186 [-0.229, -0.144]** | < 0.001 |

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
| genq_BGE (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.345 | 0.322 | BM25 top-100 + cross-encoder | -0.002 [-0.019, +0.014] | 0.782 |
| genq_BGE (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.345 | 0.322 | bge-small-en-v1.5 | +0.004 [-0.006, +0.015] | 0.392 |
| genq_MiniLM (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.325 | 0.302 | BM25 top-100 + cross-encoder | **-0.022 [-0.041, -0.005]** | 0.012 |
| genq_MiniLM (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.325 | 0.302 | all-MiniLM-L6-v2 | +0.008 [-0.003, +0.020] | 0.142 |
| gpl_bm25_BGE_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.090 | 0.096 | BM25 top-100 + cross-encoder | **-0.257 [-0.288, -0.226]** | < 0.001 |
| gpl_bm25_BGE_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.090 | 0.096 | bge-small-en-v1.5 | **-0.250 [-0.279, -0.220]** | < 0.001 |
| gpl_bm25_MiniLM_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.178 | 0.124 | BM25 top-100 + cross-encoder | **-0.169 [-0.195, -0.144]** | < 0.001 |
| gpl_bm25_MiniLM_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.178 | 0.124 | all-MiniLM-L6-v2 | **-0.138 [-0.162, -0.114]** | < 0.001 |
| gpl_dense_BGE_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.155 | 0.119 | BM25 top-100 + cross-encoder | **-0.192 [-0.222, -0.163]** | < 0.001 |
| gpl_dense_BGE_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.155 | 0.119 | bge-small-en-v1.5 | **-0.185 [-0.213, -0.157]** | < 0.001 |
| gpl_dense_MiniLM_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.204 | 0.148 | BM25 top-100 + cross-encoder | **-0.143 [-0.168, -0.120]** | < 0.001 |
| gpl_dense_MiniLM_nneg50 (ideal) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.204 | 0.148 | all-MiniLM-L6-v2 | **-0.113 [-0.135, -0.091]** | < 0.001 |
| genq_BGE (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.345 | 0.326 | BM25 top-100 + cross-encoder | -0.002 [-0.020, +0.015] | 0.798 |
| genq_BGE (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.345 | 0.326 | bge-small-en-v1.5 | +0.004 [-0.006, +0.016] | 0.421 |
| genq_MiniLM (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.317 | 0.304 | BM25 top-100 + cross-encoder | **-0.030 [-0.049, -0.013]** | 0.001 |
| genq_MiniLM (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.317 | 0.304 | all-MiniLM-L6-v2 | +0.001 [-0.010, +0.011] | 0.902 |
| gpl_bm25_BGE_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.294 | 0.253 | BM25 top-100 + cross-encoder | **-0.053 [-0.076, -0.030]** | < 0.001 |
| gpl_bm25_BGE_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.294 | 0.253 | bge-small-en-v1.5 | **-0.046 [-0.064, -0.028]** | < 0.001 |
| gpl_bm25_BGE_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.299 | 0.254 | BM25 top-100 + cross-encoder | **-0.048 [-0.072, -0.025]** | < 0.001 |
| gpl_bm25_BGE_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.299 | 0.254 | bge-small-en-v1.5 | **-0.041 [-0.059, -0.024]** | < 0.001 |
| gpl_bm25_BGE_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.298 | 0.259 | BM25 top-100 + cross-encoder | **-0.049 [-0.073, -0.025]** | < 0.001 |
| gpl_bm25_BGE_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.298 | 0.259 | bge-small-en-v1.5 | **-0.042 [-0.060, -0.024]** | < 0.001 |
| gpl_bm25_BGE_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.305 | 0.261 | BM25 top-100 + cross-encoder | **-0.042 [-0.066, -0.019]** | < 0.001 |
| gpl_bm25_BGE_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.305 | 0.261 | bge-small-en-v1.5 | **-0.035 [-0.053, -0.017]** | < 0.001 |
| gpl_bm25_BGE_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.305 | 0.264 | BM25 top-100 + cross-encoder | **-0.042 [-0.065, -0.019]** | < 0.001 |
| gpl_bm25_BGE_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.305 | 0.264 | bge-small-en-v1.5 | **-0.035 [-0.052, -0.018]** | < 0.001 |
| gpl_bm25_MiniLM_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.266 | 0.251 | BM25 top-100 + cross-encoder | **-0.081 [-0.104, -0.060]** | < 0.001 |
| gpl_bm25_MiniLM_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.266 | 0.251 | all-MiniLM-L6-v2 | **-0.051 [-0.067, -0.034]** | < 0.001 |
| gpl_bm25_MiniLM_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.268 | 0.259 | BM25 top-100 + cross-encoder | **-0.079 [-0.102, -0.058]** | < 0.001 |
| gpl_bm25_MiniLM_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.268 | 0.259 | all-MiniLM-L6-v2 | **-0.049 [-0.065, -0.032]** | < 0.001 |
| gpl_bm25_MiniLM_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.268 | 0.257 | BM25 top-100 + cross-encoder | **-0.080 [-0.103, -0.058]** | < 0.001 |
| gpl_bm25_MiniLM_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.268 | 0.257 | all-MiniLM-L6-v2 | **-0.049 [-0.066, -0.031]** | < 0.001 |
| gpl_bm25_MiniLM_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.269 | 0.260 | BM25 top-100 + cross-encoder | **-0.078 [-0.101, -0.057]** | < 0.001 |
| gpl_bm25_MiniLM_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.269 | 0.260 | all-MiniLM-L6-v2 | **-0.047 [-0.064, -0.031]** | < 0.001 |
| gpl_bm25_MiniLM_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.271 | 0.262 | BM25 top-100 + cross-encoder | **-0.076 [-0.098, -0.055]** | < 0.001 |
| gpl_bm25_MiniLM_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.271 | 0.262 | all-MiniLM-L6-v2 | **-0.045 [-0.061, -0.029]** | < 0.001 |
| gpl_dense_BGE_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.303 | 0.266 | BM25 top-100 + cross-encoder | **-0.044 [-0.067, -0.022]** | < 0.001 |
| gpl_dense_BGE_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.303 | 0.266 | bge-small-en-v1.5 | **-0.037 [-0.055, -0.020]** | < 0.001 |
| gpl_dense_BGE_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.306 | 0.264 | BM25 top-100 + cross-encoder | **-0.042 [-0.064, -0.019]** | < 0.001 |
| gpl_dense_BGE_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.306 | 0.264 | bge-small-en-v1.5 | **-0.035 [-0.052, -0.017]** | < 0.001 |
| gpl_dense_BGE_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.305 | 0.267 | BM25 top-100 + cross-encoder | **-0.043 [-0.065, -0.020]** | < 0.001 |
| gpl_dense_BGE_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.305 | 0.267 | bge-small-en-v1.5 | **-0.036 [-0.053, -0.018]** | < 0.001 |
| gpl_dense_BGE_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.305 | 0.274 | BM25 top-100 + cross-encoder | **-0.043 [-0.065, -0.020]** | < 0.001 |
| gpl_dense_BGE_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.305 | 0.274 | bge-small-en-v1.5 | **-0.036 [-0.054, -0.018]** | < 0.001 |
| gpl_dense_BGE_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.303 | 0.276 | BM25 top-100 + cross-encoder | **-0.044 [-0.067, -0.021]** | < 0.001 |
| gpl_dense_BGE_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.303 | 0.276 | bge-small-en-v1.5 | **-0.037 [-0.055, -0.019]** | < 0.001 |
| gpl_dense_MiniLM_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.267 | 0.247 | BM25 top-100 + cross-encoder | **-0.080 [-0.102, -0.059]** | < 0.001 |
| gpl_dense_MiniLM_nneg10 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.267 | 0.247 | all-MiniLM-L6-v2 | **-0.049 [-0.065, -0.033]** | < 0.001 |
| gpl_dense_MiniLM_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.269 | 0.251 | BM25 top-100 + cross-encoder | **-0.078 [-0.100, -0.057]** | < 0.001 |
| gpl_dense_MiniLM_nneg20 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.269 | 0.251 | all-MiniLM-L6-v2 | **-0.047 [-0.064, -0.031]** | < 0.001 |
| gpl_dense_MiniLM_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.272 | 0.253 | BM25 top-100 + cross-encoder | **-0.075 [-0.097, -0.055]** | < 0.001 |
| gpl_dense_MiniLM_nneg30 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.272 | 0.253 | all-MiniLM-L6-v2 | **-0.044 [-0.061, -0.028]** | < 0.001 |
| gpl_dense_MiniLM_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.272 | 0.256 | BM25 top-100 + cross-encoder | **-0.075 [-0.097, -0.054]** | < 0.001 |
| gpl_dense_MiniLM_nneg40 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.272 | 0.256 | all-MiniLM-L6-v2 | **-0.044 [-0.060, -0.028]** | < 0.001 |
| gpl_dense_MiniLM_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.270 | 0.254 | BM25 top-100 + cross-encoder | **-0.077 [-0.100, -0.056]** | < 0.001 |
| gpl_dense_MiniLM_nneg50 (negatives_sweep) ([fsc_GPL_4090](pairs/fsc_GPL_4090/)) | 0.270 | 0.254 | all-MiniLM-L6-v2 | **-0.046 [-0.062, -0.030]** | < 0.001 |

## ArguAna

| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |
|---|:-:|:-:|---|:-:|:-:|
| *BM25* | 0.516 | 0.969 | | | |
| *all-MiniLM-L6-v2* | 0.503 | 0.977 | | | |
| *bge-small-en-v1.5* | 0.606 | 0.986 | | | |
| *RRF (BM25 + MiniLM)* | 0.549 | 0.985 | | | |
| *BM25 top-100 + cross-encoder* | 0.422 | 0.969 | | | |
