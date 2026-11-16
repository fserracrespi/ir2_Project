# Demo: GPL vs GenQ vs zero-shot (SciFact, BGE-small)

Run `demo.ipynb` in Colab (GPU), then open the public link it prints. Each query shows the top 5 documents of zero-shot BGE, GenQ and GPL side by side; for test queries, relevant documents are marked ✓.

| | Query | What it shows |
|---|---|---|
| Hero | [query] | [e.g. GPL and GenQ find the relevant paper that zero-shot misses] |
| Failure | [query] | [e.g. zero-shot ranks the relevant paper first; GPL loses it from the top 5] |
| Wildcard | typed live, e.g. "[query]" | how each model handles a free-form question |

Fallback recording: [link]
Static fallback page: `demo_scifact_bge.html`