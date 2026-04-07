---
title: "Lab 11 — Covariates in DESeq2"
layout: single
---

**Key concepts and tools**
- DESeq2: `DESeqDataSetFromMatrix`, `DESeq`, `results`
- Design formula: `~ covariate + condition`
- Size factor normalization, variance-stabilizing transformation (VST)
- Confounding variables and batch effects
- PCA, sample distance heatmaps
- Volcano plots, MA plots
- R Markdown (`.Rmd`): inline code, knitting to HTML
- Mouse adipocyte RNA-seq data (WT vs. GPS2-KO)
- nf-core pipelines, `nf-core/rnaseq`, nf-core modules

---

A guided R Markdown walkthrough of a differential expression analysis that includes a biological covariate. The dataset is RNA-seq from wild-type and GPS2-knockout mouse adipocytes. You will build DESeq2 models with and without the covariate in the design formula, compare how its inclusion changes the results, and visualize the differences through PCA, heatmaps, and volcano plots. The emphasis is on understanding what a covariate does statistically and when it matters, not on writing code from scratch — the Rmd is mostly provided and you follow along, answering interpretive questions.

---

# Extended topic — Using nf-core Pipelines

nf-core is a community effort to maintain high-quality, production-ready Nextflow pipelines for common bioinformatics tasks. Rather than writing an alignment or RNA-seq pipeline from scratch, you can use a tested, well-documented nf-core pipeline directly — and then adapt its outputs to your specific analysis.

## The nf-core ecosystem

```bash
pip install nf-core               # install the nf-core CLI tools
nf-core list                       # browse available pipelines
nf-core launch nf-core/rnaseq     # interactive parameter wizard
```

Every nf-core pipeline has a standardized samplesheet format, a `nextflow_schema.json` defining all parameters, institutional profiles in `conf/`, and a MultiQC summary report as output.

## Running nf-core/rnaseq

```csv
sample,fastq_1,fastq_2,strandedness
SRR001,/path/SRR001_R1.fastq.gz,/path/SRR001_R2.fastq.gz,auto
```

```bash
nextflow run nf-core/rnaseq \
    -profile singularity,cluster \
    --input samplesheet.csv \
    --outdir results/ \
    --genome GRCh38 \
    -r 3.14.0
```

Always pin a release with `-r` for reproducibility.

## Key outputs

| Path | Contents |
|---|---|
| `results/star_salmon/salmon.merged.gene_counts.tsv` | Count matrix (genes × samples) |
| `results/multiqc/multiqc_report.html` | Aggregated QC |
| `results/trimgalore/` | Trimmed reads and adapter reports |

## Using nf-core modules in your own pipelines

```bash
nf-core modules install fastqc
nf-core modules install star/align
```

Each module installs into `modules/nf-core/<tool>/main.nf` with a standardized interface compatible with the patterns already learned in this course.

## Linting

```bash
nf-core lint
```

Checks `publishDir` usage, label consistency, container declarations, and more — a useful quality bar even outside nf-core.

## Tasks

1. Run `nf-core/rnaseq` with `-profile singularity,cluster` on the provided subset data
2. Open the MultiQC report and identify any QC flags
3. Load the merged count matrix into R and confirm its dimensions
4. Install the `fastqc` and `multiqc` nf-core modules into a blank Nextflow project and wire them together
