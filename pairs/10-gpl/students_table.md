| Student | Modules | Pooling | Dim | Similarity | Normalized | Mean ‖q‖ | Score range | Max margin | Pos score | Neg score | Student margin |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Paper (GPL) | Transformer -> Pooling | mean | 768 | cosine | no | 11.02 | unbounded | unbounded | large | large | large |
| BGE-small | Transformer -> Pooling -> Normalize | cls | 384 | cosine | yes | 1.00 | [-1, 1] | 2 | 0.74 | 0.56 | 0.19 |
| MiniLM | Transformer -> Pooling -> Normalize | mean | 384 | cosine | yes | 1.00 | [-1, 1] | 2 | 0.49 | 0.07 | 0.42 |

Teacher `cross-encoder/ms-marco-MiniLM-L6-v2` on the same 8 scifact triples (raw logits):
pos -1.75, neg -10.83, margin mean 9.08 (min -0.16, max 17.09)

A cosine student can output margins of at most 2, so MarginMSE against raw teacher
margins cannot go below roughly (teacher margin - 2)^2; labels are rescaled to (-2, 2).
The paper's student uses an unnormalized dot product, so it can match raw margins.
