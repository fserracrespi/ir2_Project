| | SciFact | NFCorpus | ArguAna |
|---|---|---|---|
| BEIR task | Fact-checking | Bio-medical IR | Argument retrieval |
| Documents | 5,183 | 3,633 | 8,674 |
| Test queries | 300 | 323 | 1,406 |
| Query style | Scientific claim ("0-dimensional biomaterials show inductive properties.") | Health title or question ("Food Dyes and ADHD") | A full argument paragraph |
| Document style | Paper title + abstract | Medical abstract | Counter-argument; `title` field holds topic tags |
| Relevance labels | Binary: 1 (339 judgments) | Graded: 1 (11,758), 2 (576) | Binary: 1 (1,406) |
| Relevant docs per query | 1.1 | 38.2 | 1.0 |
| ID format | numbers (`4983`) | `PLAIN-2` / `MED-10` | `test-sport-…-pro02a` → `…-pro02b` |

Sources: counts and labels from `testbed.load`; task categories, splits and relevant docs per query from the [BEIR dataset card on Hugging Face](https://huggingface.co/datasets/BeIR/beir).
