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
| negatives_sweep/genq_BGE ([fsc_GPL_4090](pairs/results_EXP/)) | 0.664 | 0.947 | bge-small-en-v1.5 | **-0.045 [-0.068, -0.023]** | < 0.001 |
| negatives_sweep/genq_MiniLM ([fsc_GPL_4090](pairs/results_EXP/)) | 0.644 | 0.937 | all-MiniLM-L6-v2 | -0.002 [-0.023, +0.019] | 0.875 |
| negatives_sweep/gpl_bm25_BGE_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.476 | 0.785 | bge-small-en-v1.5 | **-0.234 [-0.278, -0.191]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.460 | 0.786 | bge-small-en-v1.5 | **-0.250 [-0.296, -0.205]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.450 | 0.761 | bge-small-en-v1.5 | **-0.260 [-0.304, -0.216]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.472 | 0.791 | bge-small-en-v1.5 | **-0.238 [-0.282, -0.196]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.453 | 0.792 | bge-small-en-v1.5 | **-0.257 [-0.300, -0.216]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.455 | 0.765 | bge-small-en-v1.5 | **-0.255 [-0.300, -0.212]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.446 | 0.737 | bge-small-en-v1.5 | **-0.264 [-0.310, -0.221]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.412 | 0.724 | bge-small-en-v1.5 | **-0.297 [-0.344, -0.253]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.376 | 0.686 | bge-small-en-v1.5 | **-0.334 [-0.382, -0.287]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.396 | 0.700 | bge-small-en-v1.5 | **-0.314 [-0.362, -0.269]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.480 | 0.801 | all-MiniLM-L6-v2 | **-0.165 [-0.206, -0.126]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.500 | 0.837 | all-MiniLM-L6-v2 | **-0.146 [-0.187, -0.106]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.468 | 0.813 | all-MiniLM-L6-v2 | **-0.177 [-0.220, -0.137]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.470 | 0.826 | all-MiniLM-L6-v2 | **-0.176 [-0.217, -0.136]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.470 | 0.799 | all-MiniLM-L6-v2 | **-0.176 [-0.217, -0.136]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.484 | 0.823 | all-MiniLM-L6-v2 | **-0.162 [-0.202, -0.122]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.442 | 0.781 | all-MiniLM-L6-v2 | **-0.203 [-0.245, -0.163]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.419 | 0.759 | all-MiniLM-L6-v2 | **-0.226 [-0.268, -0.185]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.425 | 0.744 | all-MiniLM-L6-v2 | **-0.221 [-0.264, -0.179]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.403 | 0.754 | all-MiniLM-L6-v2 | **-0.243 [-0.286, -0.200]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.467 | 0.822 | bge-small-en-v1.5 | **-0.243 [-0.286, -0.200]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.492 | 0.850 | bge-small-en-v1.5 | **-0.218 [-0.259, -0.178]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.504 | 0.858 | bge-small-en-v1.5 | **-0.206 [-0.246, -0.167]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.492 | 0.853 | bge-small-en-v1.5 | **-0.218 [-0.258, -0.180]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.501 | 0.853 | bge-small-en-v1.5 | **-0.209 [-0.249, -0.169]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.489 | 0.846 | bge-small-en-v1.5 | **-0.221 [-0.262, -0.182]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.469 | 0.843 | bge-small-en-v1.5 | **-0.240 [-0.283, -0.199]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.427 | 0.816 | bge-small-en-v1.5 | **-0.282 [-0.327, -0.239]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.419 | 0.777 | bge-small-en-v1.5 | **-0.291 [-0.336, -0.247]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.425 | 0.777 | bge-small-en-v1.5 | **-0.285 [-0.332, -0.239]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.470 | 0.827 | all-MiniLM-L6-v2 | **-0.176 [-0.219, -0.134]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.484 | 0.849 | all-MiniLM-L6-v2 | **-0.162 [-0.201, -0.123]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.485 | 0.863 | all-MiniLM-L6-v2 | **-0.160 [-0.201, -0.121]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.488 | 0.850 | all-MiniLM-L6-v2 | **-0.158 [-0.199, -0.118]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.478 | 0.846 | all-MiniLM-L6-v2 | **-0.168 [-0.210, -0.127]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.486 | 0.853 | all-MiniLM-L6-v2 | **-0.160 [-0.198, -0.123]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.463 | 0.821 | all-MiniLM-L6-v2 | **-0.182 [-0.224, -0.141]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.434 | 0.807 | all-MiniLM-L6-v2 | **-0.211 [-0.255, -0.170]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.419 | 0.804 | all-MiniLM-L6-v2 | **-0.227 [-0.272, -0.183]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.414 | 0.805 | all-MiniLM-L6-v2 | **-0.232 [-0.276, -0.188]** | < 0.001 |
| tsdae/tsdae_gpl_BGE ([fsc_GPL_4090](pairs/results_EXP/)) | 0.502 | 0.839 | bge-small-en-v1.5 | **-0.208 [-0.251, -0.167]** | < 0.001 |
| tsdae/tsdae_gpl_MiniLM ([fsc_GPL_4090](pairs/results_EXP/)) | 0.451 | 0.821 | all-MiniLM-L6-v2 | **-0.195 [-0.237, -0.152]** | < 0.001 |
| tsdae/tsdae_pretrain_BGE ([fsc_GPL_4090](pairs/results_EXP/)) | 0.349 | 0.713 | bge-small-en-v1.5 | **-0.361 [-0.407, -0.315]** | < 0.001 |
| tsdae/tsdae_pretrain_MiniLM ([fsc_GPL_4090](pairs/results_EXP/)) | 0.264 | 0.604 | all-MiniLM-L6-v2 | **-0.381 [-0.430, -0.333]** | < 0.001 |

## NFCorpus

| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |
|---|:-:|:-:|---|:-:|:-:|
| *BM25* | 0.321 | 0.246 | | | |
| *all-MiniLM-L6-v2* | 0.316 | 0.311 | | | |
| *bge-small-en-v1.5* | 0.340 | 0.304 | | | |
| *RRF (BM25 + MiniLM)* | 0.342 | 0.310 | | | |
| *BM25 top-100 + cross-encoder* | 0.347 | 0.246 | | | |
| negatives_sweep/genq_BGE ([fsc_GPL_4090](pairs/results_EXP/)) | 0.345 | 0.327 | bge-small-en-v1.5 | +0.005 [-0.004, +0.015] | 0.302 |
| negatives_sweep/genq_MiniLM ([fsc_GPL_4090](pairs/results_EXP/)) | 0.322 | 0.301 | all-MiniLM-L6-v2 | +0.006 [-0.004, +0.015] | 0.226 |
| negatives_sweep/gpl_bm25_BGE_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.291 | 0.249 | bge-small-en-v1.5 | **-0.049 [-0.066, -0.032]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.302 | 0.259 | bge-small-en-v1.5 | **-0.038 [-0.057, -0.020]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.308 | 0.259 | bge-small-en-v1.5 | **-0.032 [-0.050, -0.015]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.304 | 0.261 | bge-small-en-v1.5 | **-0.036 [-0.055, -0.018]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.300 | 0.255 | bge-small-en-v1.5 | **-0.041 [-0.058, -0.023]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.303 | 0.260 | bge-small-en-v1.5 | **-0.037 [-0.055, -0.018]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.290 | 0.247 | bge-small-en-v1.5 | **-0.050 [-0.069, -0.031]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.287 | 0.235 | bge-small-en-v1.5 | **-0.053 [-0.072, -0.034]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.284 | 0.236 | bge-small-en-v1.5 | **-0.056 [-0.076, -0.037]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.282 | 0.235 | bge-small-en-v1.5 | **-0.058 [-0.077, -0.039]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.276 | 0.253 | all-MiniLM-L6-v2 | **-0.041 [-0.056, -0.025]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.283 | 0.263 | all-MiniLM-L6-v2 | **-0.033 [-0.048, -0.018]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.286 | 0.267 | all-MiniLM-L6-v2 | **-0.030 [-0.045, -0.015]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.283 | 0.267 | all-MiniLM-L6-v2 | **-0.033 [-0.047, -0.018]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.283 | 0.262 | all-MiniLM-L6-v2 | **-0.033 [-0.048, -0.019]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.280 | 0.263 | all-MiniLM-L6-v2 | **-0.036 [-0.051, -0.021]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.266 | 0.255 | all-MiniLM-L6-v2 | **-0.050 [-0.067, -0.033]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.261 | 0.234 | all-MiniLM-L6-v2 | **-0.055 [-0.072, -0.038]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.263 | 0.246 | all-MiniLM-L6-v2 | **-0.053 [-0.069, -0.036]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.258 | 0.240 | all-MiniLM-L6-v2 | **-0.059 [-0.076, -0.041]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.307 | 0.276 | bge-small-en-v1.5 | **-0.033 [-0.050, -0.017]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.307 | 0.282 | bge-small-en-v1.5 | **-0.033 [-0.050, -0.016]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.301 | 0.276 | bge-small-en-v1.5 | **-0.039 [-0.057, -0.021]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.302 | 0.287 | bge-small-en-v1.5 | **-0.038 [-0.055, -0.021]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.298 | 0.277 | bge-small-en-v1.5 | **-0.043 [-0.060, -0.025]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.304 | 0.274 | bge-small-en-v1.5 | **-0.036 [-0.054, -0.019]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.290 | 0.271 | bge-small-en-v1.5 | **-0.050 [-0.070, -0.031]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.285 | 0.253 | bge-small-en-v1.5 | **-0.055 [-0.075, -0.036]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.270 | 0.240 | bge-small-en-v1.5 | **-0.071 [-0.091, -0.051]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.272 | 0.237 | bge-small-en-v1.5 | **-0.069 [-0.089, -0.049]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.291 | 0.263 | all-MiniLM-L6-v2 | **-0.025 [-0.039, -0.011]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.290 | 0.267 | all-MiniLM-L6-v2 | **-0.026 [-0.040, -0.012]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.276 | 0.258 | all-MiniLM-L6-v2 | **-0.040 [-0.055, -0.025]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.280 | 0.262 | all-MiniLM-L6-v2 | **-0.037 [-0.053, -0.021]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.277 | 0.262 | all-MiniLM-L6-v2 | **-0.039 [-0.054, -0.023]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.276 | 0.259 | all-MiniLM-L6-v2 | **-0.040 [-0.056, -0.024]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.272 | 0.255 | all-MiniLM-L6-v2 | **-0.044 [-0.060, -0.029]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.267 | 0.248 | all-MiniLM-L6-v2 | **-0.049 [-0.065, -0.033]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.250 | 0.239 | all-MiniLM-L6-v2 | **-0.067 [-0.086, -0.048]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.251 | 0.237 | all-MiniLM-L6-v2 | **-0.065 [-0.083, -0.047]** | < 0.001 |
| tsdae/tsdae_gpl_BGE ([fsc_GPL_4090](pairs/results_EXP/)) | 0.292 | 0.278 | bge-small-en-v1.5 | **-0.049 [-0.066, -0.032]** | < 0.001 |
| tsdae/tsdae_gpl_MiniLM ([fsc_GPL_4090](pairs/results_EXP/)) | 0.263 | 0.250 | all-MiniLM-L6-v2 | **-0.053 [-0.070, -0.036]** | < 0.001 |
| tsdae/tsdae_pretrain_BGE ([fsc_GPL_4090](pairs/results_EXP/)) | 0.097 | 0.155 | bge-small-en-v1.5 | **-0.244 [-0.272, -0.215]** | < 0.001 |
| tsdae/tsdae_pretrain_MiniLM ([fsc_GPL_4090](pairs/results_EXP/)) | 0.063 | 0.118 | all-MiniLM-L6-v2 | **-0.253 [-0.283, -0.222]** | < 0.001 |

## ArguAna

| Method | nDCG@10 | Recall@100 | Compared with | Δ nDCG@10 [95 % CI] | p |
|---|:-:|:-:|---|:-:|:-:|
| *BM25* | 0.516 | 0.969 | | | |
| *all-MiniLM-L6-v2* | 0.503 | 0.977 | | | |
| *bge-small-en-v1.5* | 0.606 | 0.986 | | | |
| *RRF (BM25 + MiniLM)* | 0.549 | 0.985 | | | |
| *BM25 top-100 + cross-encoder* | 0.422 | 0.969 | | | |
| negatives_sweep/genq_BGE ([fsc_GPL_4090](pairs/results_EXP/)) | 0.532 | 0.983 | bge-small-en-v1.5 | **-0.074 [-0.088, -0.060]** | < 0.001 |
| negatives_sweep/genq_MiniLM ([fsc_GPL_4090](pairs/results_EXP/)) | 0.516 | 0.978 | all-MiniLM-L6-v2 | **+0.014 [+0.002, +0.025]** | 0.021 |
| negatives_sweep/gpl_bm25_BGE_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.407 | 0.927 | bge-small-en-v1.5 | **-0.199 [-0.218, -0.179]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.378 | 0.914 | bge-small-en-v1.5 | **-0.228 [-0.248, -0.208]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.363 | 0.898 | bge-small-en-v1.5 | **-0.243 [-0.263, -0.222]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.374 | 0.914 | bge-small-en-v1.5 | **-0.232 [-0.252, -0.211]** | < 0.001 |
| negatives_sweep/gpl_bm25_BGE_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.373 | 0.909 | bge-small-en-v1.5 | **-0.233 [-0.253, -0.212]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.369 | 0.898 | bge-small-en-v1.5 | **-0.237 [-0.258, -0.217]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.363 | 0.890 | bge-small-en-v1.5 | **-0.242 [-0.263, -0.222]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.336 | 0.871 | bge-small-en-v1.5 | **-0.270 [-0.290, -0.248]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.350 | 0.856 | bge-small-en-v1.5 | **-0.256 [-0.276, -0.234]** | < 0.001 |
| steps_sweep/gpl_bm25_BGE_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.320 | 0.842 | bge-small-en-v1.5 | **-0.286 [-0.306, -0.265]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.410 | 0.959 | all-MiniLM-L6-v2 | **-0.092 [-0.110, -0.075]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.378 | 0.944 | all-MiniLM-L6-v2 | **-0.125 [-0.143, -0.107]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.388 | 0.945 | all-MiniLM-L6-v2 | **-0.114 [-0.132, -0.096]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.368 | 0.942 | all-MiniLM-L6-v2 | **-0.134 [-0.153, -0.115]** | < 0.001 |
| negatives_sweep/gpl_bm25_MiniLM_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.379 | 0.933 | all-MiniLM-L6-v2 | **-0.124 [-0.143, -0.106]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.376 | 0.939 | all-MiniLM-L6-v2 | **-0.127 [-0.145, -0.108]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.371 | 0.930 | all-MiniLM-L6-v2 | **-0.131 [-0.151, -0.112]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.347 | 0.907 | all-MiniLM-L6-v2 | **-0.156 [-0.175, -0.136]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.353 | 0.895 | all-MiniLM-L6-v2 | **-0.150 [-0.170, -0.130]** | < 0.001 |
| steps_sweep/gpl_bm25_MiniLM_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.346 | 0.896 | all-MiniLM-L6-v2 | **-0.156 [-0.176, -0.137]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.379 | 0.909 | bge-small-en-v1.5 | **-0.227 [-0.247, -0.207]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.375 | 0.903 | bge-small-en-v1.5 | **-0.231 [-0.251, -0.211]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.370 | 0.918 | bge-small-en-v1.5 | **-0.236 [-0.256, -0.215]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.361 | 0.910 | bge-small-en-v1.5 | **-0.245 [-0.265, -0.224]** | < 0.001 |
| negatives_sweep/gpl_dense_BGE_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.360 | 0.900 | bge-small-en-v1.5 | **-0.246 [-0.267, -0.226]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.365 | 0.909 | bge-small-en-v1.5 | **-0.241 [-0.261, -0.221]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.345 | 0.890 | bge-small-en-v1.5 | **-0.261 [-0.282, -0.240]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.340 | 0.855 | bge-small-en-v1.5 | **-0.266 [-0.287, -0.244]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.323 | 0.841 | bge-small-en-v1.5 | **-0.283 [-0.303, -0.261]** | < 0.001 |
| steps_sweep/gpl_dense_BGE_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.320 | 0.844 | bge-small-en-v1.5 | **-0.286 [-0.307, -0.264]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg10 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.373 | 0.922 | all-MiniLM-L6-v2 | **-0.130 [-0.148, -0.112]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg20 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.369 | 0.923 | all-MiniLM-L6-v2 | **-0.134 [-0.152, -0.116]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg30 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.380 | 0.933 | all-MiniLM-L6-v2 | **-0.123 [-0.141, -0.104]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg40 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.383 | 0.936 | all-MiniLM-L6-v2 | **-0.120 [-0.138, -0.102]** | < 0.001 |
| negatives_sweep/gpl_dense_MiniLM_nneg50 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.361 | 0.931 | all-MiniLM-L6-v2 | **-0.142 [-0.161, -0.124]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x1 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.376 | 0.938 | all-MiniLM-L6-v2 | **-0.127 [-0.145, -0.108]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x2 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.362 | 0.931 | all-MiniLM-L6-v2 | **-0.141 [-0.160, -0.122]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x3 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.345 | 0.905 | all-MiniLM-L6-v2 | **-0.157 [-0.177, -0.138]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x4 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.350 | 0.890 | all-MiniLM-L6-v2 | **-0.153 [-0.172, -0.133]** | < 0.001 |
| steps_sweep/gpl_dense_MiniLM_x5 ([fsc_GPL_4090](pairs/results_EXP/)) | 0.334 | 0.896 | all-MiniLM-L6-v2 | **-0.169 [-0.188, -0.149]** | < 0.001 |
| tsdae/tsdae_gpl_BGE ([fsc_GPL_4090](pairs/results_EXP/)) | 0.329 | 0.883 | bge-small-en-v1.5 | **-0.277 [-0.297, -0.257]** | < 0.001 |
| tsdae/tsdae_gpl_MiniLM ([fsc_GPL_4090](pairs/results_EXP/)) | 0.360 | 0.910 | all-MiniLM-L6-v2 | **-0.143 [-0.163, -0.124]** | < 0.001 |
| tsdae/tsdae_pretrain_BGE ([fsc_GPL_4090](pairs/results_EXP/)) | 0.302 | 0.835 | bge-small-en-v1.5 | **-0.304 [-0.324, -0.283]** | < 0.001 |
| tsdae/tsdae_pretrain_MiniLM ([fsc_GPL_4090](pairs/results_EXP/)) | 0.271 | 0.775 | all-MiniLM-L6-v2 | **-0.232 [-0.253, -0.211]** | < 0.001 |
