
import sys
from pathlib import Path
from sentence_transformers import SentenceTransformer

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1]))

import testbed

# Checkpoints produced by GPL training
CHECKPOINTS = {
    "scifact": "//app/pairs/FSC_gpl/runs/models/smoke/scifact",
    "nfcorpus": "/app/pairs/FSC_gpl/runs/models/smoke/nfcorpus",}

for name, checkpoint in CHECKPOINTS.items():

    print(f"Retrieving GPL on {name}")

    model = SentenceTransformer(
        checkpoint,
        device=testbed.device()
    )

    # Same corpus and queries as the official testbed
    corpus, queries, _ = testbed.load(name)

    # Same preprocessing and ranking as testbed dense baselines
    run = testbed.dense_search(
        model,
        corpus,
        queries,
        batch_size=16
    )

    testbed.save_run(run, HERE / "runs" / f"{name}.json")

    print(f"Saved run: {name}")
