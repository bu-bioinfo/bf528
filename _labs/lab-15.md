---
title: "Lab 15 — Single-Cell Preprocessing in R"
layout: single
---

**Key concepts and tools**
- `SingleCellExperiment` (SCE) object: `colData`, `rowData`, `reducedDims`
- `scran`, `scater` — R single-cell analysis packages
- Quality control: `perCellQCMetrics`, `quickPerCellQC`
- Normalization: `computeSumFactors` (scran pooling)
- Feature selection: modeling gene variance, selecting highly variable genes
- PCA, UMAP via `scater`
- Graph-based clustering: `buildSNNGraph`, `igraph` community detection
- Marker gene detection: `findMarkers`
- R Markdown (`.Rmd`)

---

The R-side counterpart to Lab 13. Working in an R Markdown document, you will import the same single-cell counts data into a `SingleCellExperiment` object and repeat the core preprocessing steps using the Bioconductor ecosystem: QC filtering, sum-factor normalization with scran, highly variable gene selection, dimensionality reduction, and graph-based clustering. The lab also prepares the data structure needed for the pseudobulk analysis in Lab 16, introducing the concept of collapsing single-cell observations back to sample-level counts.
