"""Why GPL needs rescaled labels for BGE / MiniLM but not for the paper's student.

Prints, for each student model:
  1. its module stack (Transformer -> Pooling -> [Normalize])
  2. its similarity function and whether embeddings are L2-normalized
  3. the score range it can produce, i.e. the largest margin it can ever output
and compares that with the raw margins of the cross-encoder teacher on a few
SciFact (query, relevant doc, random doc) triples.

Put it in pairs/10-gpl/ and run it from anywhere:  python inspect_students.py
Writes the same summary to pairs/10-gpl/students_table.md for the slides.
"""
import os, sys, random
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))   # pairs/10-gpl -> repo root
sys.path.insert(0, ROOT)
os.chdir(ROOT)                                           # testbed expects to run from the root
import numpy as np
import torch
from sentence_transformers import SentenceTransformer, CrossEncoder
from sentence_transformers.models import Normalize, Pooling
import testbed

STUDENTS = {
    "Paper (GPL)": "GPL/msmarco-distilbert-margin-mse",
    "BGE-small":   "BAAI/bge-small-en-v1.5",
    "MiniLM":      "sentence-transformers/all-MiniLM-L6-v2",   # change if you used another MiniLM
}
TEACHER = "cross-encoder/ms-marco-MiniLM-L6-v2"
DATASET = "scifact"
N_TRIPLES = 8
random.seed(0)

# ---- a few (query, positive, random negative) triples ----------------------
corpus, queries, qrels = testbed.load(DATASET)
texts = dict(zip(corpus, testbed.doc_texts(corpus)))
doc_ids = list(corpus)
triples = []
for qid, rel in qrels.items():
    pos = [d for d, r in rel.items() if r > 0 and d in texts]
    if qid in queries and pos:
        neg = random.choice(doc_ids)
        if neg not in rel:
            triples.append((queries[qid], texts[pos[0]], texts[neg]))
    if len(triples) == N_TRIPLES:
        break
Q = [t[0] for t in triples]; P = [t[1] for t in triples]; N = [t[2] for t in triples]

# ---- teacher margins (raw logits, as used for the GPL labels) --------------
teacher = CrossEncoder(TEACHER)
t_pos = np.array(teacher.predict(list(zip(Q, P))))
t_neg = np.array(teacher.predict(list(zip(Q, N))))
t_margin = t_pos - t_neg

# ---- students ---------------------------------------------------------------
def pooling_name(mod):
    """Pooling mode, robust across sentence-transformers versions."""
    for attr in ("get_pooling_mode_str", "pooling_mode"):
        v = getattr(mod, attr, None)
        if v is not None:
            try:
                return str(v() if callable(v) else v)
            except Exception:
                pass
    try:
        cfg = mod.get_config_dict()
        if "pooling_mode" in cfg:
            return str(cfg["pooling_mode"])
        on = [k.replace("pooling_mode_", "").replace("_tokens", "") for k, val in cfg.items()
              if k.startswith("pooling_mode_") and val is True]
        if on:
            return "+".join(on)
    except Exception:
        pass
    return "?"


rows = []
for label, name in STUDENTS.items():
    m = SentenceTransformer(name, device="cpu")
    stack = " -> ".join(type(mod).__name__ for mod in m)
    normalized = any(isinstance(mod, Normalize) for mod in m)
    pooling = next((pooling_name(mod) for mod in m if isinstance(mod, Pooling)), "?")
    sim = getattr(m, "similarity_fn_name", None) or "cosine"

    prefix = testbed.BGE_QUERY if label == "BGE-small" else ""
    q = m.encode([prefix + x for x in Q], convert_to_tensor=True)
    p = m.encode(P, convert_to_tensor=True)
    n = m.encode(N, convert_to_tensor=True)
    if "cos" in str(sim).lower():
        f = lambda a, b: torch.nn.functional.cosine_similarity(a, b, dim=1)
    else:
        f = lambda a, b: (a * b).sum(dim=1)
    s_pos = f(q, p).cpu().numpy()
    s_neg = f(q, n).cpu().numpy()
    s_margin = s_pos - s_neg
    q_norm = float(q.norm(dim=1).mean())

    bounded = normalized or sim == "cosine"
    rows.append({
        "Student": label, "Model": name, "Modules": stack, "Pooling": pooling,
        "Dim": q.shape[1], "Similarity": sim,
        "Normalized": "yes" if normalized else "no",
        "Mean ‖q‖": f"{q_norm:.2f}",
        "Score range": "[-1, 1]" if bounded else "unbounded",
        "Max margin": "2" if bounded else "unbounded",
        "Pos score": f"{s_pos.mean():.2f}", "Neg score": f"{s_neg.mean():.2f}",
        "Student margin": f"{s_margin.mean():.2f}",
    })
    print(f"\n=== {label}: {name}")
    print(m)

# ---- print + save ------------------------------------------------------------
cols = ["Student", "Modules", "Pooling", "Dim", "Similarity", "Normalized", "Mean ‖q‖",
        "Score range", "Max margin", "Pos score", "Neg score", "Student margin"]
lines = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
lines += ["| " + " | ".join(str(r[c]) for c in cols) + " |" for r in rows]
lines += ["",
          f"Teacher `{TEACHER}` on the same {len(triples)} {DATASET} triples (raw logits):",
          f"pos {t_pos.mean():.2f}, neg {t_neg.mean():.2f}, "
          f"margin mean {t_margin.mean():.2f} (min {t_margin.min():.2f}, max {t_margin.max():.2f})",
          "",
          "A cosine student can output margins of at most 2, so MarginMSE against raw teacher",
          "margins cannot go below roughly (teacher margin - 2)^2; labels are rescaled to (-2, 2).",
          "The paper's student uses an unnormalized dot product, so it can match raw margins."]
table = "\n".join(lines)
print("\n" + table)
out = os.path.join(HERE, "students_table.md")
with open(out, "w", encoding="utf-8") as f:
    f.write(table + "\n")
print(f"\nSaved {out}")


# === Paper (GPL): GPL/msmarco-distilbert-margin-mse                                                               |  0.00B /  265MB            
# SentenceTransformer(
#   (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'DistilBertModel'})
#   (1): Pooling({'embedding_dimension': 768, 'pooling_mode': 'mean', 'include_prompt': True})
# )
     
# === BGE-small: BAAI/bge-small-en-v1.5                                                                                 | 0/199 [00:00<?, ?it/s]
# SentenceTransformer(
#   (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'BertModel'})
#   (1): Pooling({'embedding_dimension': 384, 'pooling_mode': 'cls', 'include_prompt': True})
#   (2): Normalize({'module_input_name': 'sentence_embedding', 'module_output_name': 'sentence_embedding'})
# )
# Loading weights: 100%|████████████████████████████████████████████████████████████████████████████████████| 103/103 [00:00<00:00, 3514.07it/s]
# model.safetensors: downloading bytes: ████████▊                                                                           | 28.0MB, 1.50MB/s  
# === MiniLM: sentence-transformers/all-MiniLM-L6-v2                                                                    | 0/103 [00:00<?, ?it/s]
# SentenceTransformer(
#   (0): Transformer({'transformer_task': 'feature-extraction', 'modality_config': {'text': {'method': 'forward', 'method_output_name': 'last_hidden_state'}}, 'module_output_name': 'token_embeddings', 'architecture': 'BertModel'})
#   (1): Pooling({'embedding_dimension': 384, 'pooling_mode': 'mean', 'include_prompt': True})
#   (2): Normalize({'module_input_name': 'sentence_embedding', 'module_output_name': 'sentence_embedding'})
# )   