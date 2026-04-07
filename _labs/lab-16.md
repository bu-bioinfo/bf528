---
title: "Lab 16 — Pseudobulk Differential Expression"
layout: single
---

**Key concepts and tools**
- Pseudobulk aggregation: summing counts per cell type per sample
- Why pseudobulk outperforms single-cell DE (handling replication)
- `aggregateAcrossCells` (scran) or equivalent
- DESeq2 on aggregated counts
- Design formula with cell type and condition
- Comparing pseudobulk results to naive single-cell DE
- Visualization: volcano plots, heatmaps per cell type

---

Standard differential expression tools like DESeq2 assume independent observations, but cells from the same sample are not independent — treating them as such inflates statistical power and produces false positives. Pseudobulk analysis solves this by aggregating each cell type's counts within each sample first, then running DESeq2 on those sample-level totals. This lab applies that approach to the preprocessed single-cell data from Lab 15, walking through the aggregation step, the DESeq2 model setup for multiple cell types, and a comparison of results to what you would get running DE naively on individual cells.
