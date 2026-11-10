# IR2 Project: GPL (Generative Pseudo Labeling) for unsupervised domain adaptation in dense retrieval, Université Paris-Saclay.


GPL was implemented using the official library. Two separate Docker containers were required to avoid dependency conflicts: **`gpl`** for training and **`ir2`** for retrieval and evaluation.

### Workflow

1. **Training:** Open the `gpl` container and run `python /app/pairs/FSC_gpl/train.py`.
2. **Model configuration:** The GPL library allows selecting different generators, retrievers, cross-encoder teachers, and student models.
3. **Artifacts:** Training outputs and model checkpoints are saved in `pairs/FSC_gpl/runs/models/`.
4. **Retrieval:** Switch to the `ir2` container and run `python /app/pairs/FSC_gpl/method.py` to generate retrieval rankings using the GPL-trained model.
5. **Evaluation:** Use the IR2 testbed to evaluate retrieval performance against a selected baseline. For example:

   ```bash
   python /app/testbed.py score /app/pairs/FSC_gpl/runs \
     --method "GPL" \
     --pair FSC_gpl \
     --against bm25 \
     --out /app/pairs/FSC_gpl/results_bm25_vs_GPLs.json
   ```

6. **Results:** Evaluation metrics and comparisons are saved in `pairs/FSC_gpl/results_bm25_vs_GPLs.json`.
7. **Reporting:** Run `python /app/build_table.py` to update the results table.

**Note:** The GPL library also provides built-in retrieval evaluation. However, the IR2 testbed is used to maintain consistency with the repository's evaluation framework and ensure comparable results across methods.