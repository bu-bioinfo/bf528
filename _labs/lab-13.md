---
title: "Lab 13 — Single-Cell QC with Scanpy"
layout: single
---

**Key concepts and tools**
- Scanpy: `sc.read_10x_mtx`, `sc.pp`, `sc.tl`, `sc.pl`
- AnnData object: `.X`, `.obs`, `.var`, `.uns`, `.obsm`
- QC metrics: `n_genes_by_counts`, `total_counts`, `pct_counts_mt`
- Doublet detection
- Normalization: `sc.pp.normalize_total`, `sc.pp.log1p`
- Highly variable gene selection: `sc.pp.highly_variable_genes`
- PCA: `sc.tl.pca`
- Neighborhood graph: `sc.pp.neighbors`
- UMAP: `sc.tl.umap`
- Leiden clustering: `sc.tl.leiden`
- Cell type annotation using marker genes
- Jupyter notebook workflow

---

This lab introduces Scanpy and the AnnData data structure used throughout the Python single-cell ecosystem. Starting from the counts matrix produced in Lab 12, you will load two mouse hippocampus samples, compute and filter on QC metrics (mitochondrial read fraction, gene counts), normalize and log-transform, select highly variable genes, run PCA, build a neighborhood graph, and embed with UMAP. Leiden clustering produces candidate cell populations that you then annotate by examining known marker gene expression. The full analysis lives in a Jupyter notebook and follows the canonical Scanpy workflow.
