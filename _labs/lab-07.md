---
title: "Lab 07 — CRISPR Guide Design"
layout: single
---

**Key concepts and tools**
- `bgzip`, block-compressed FASTA
- `samtools faidx` — FASTA indexing and coordinate extraction
- GFF file format, extracting gene coordinates
- UCSC Table Browser — downloading genomic coordinate annotations
- BioPython: `SeqIO`, sequence scanning, string search
- CRISPR-Cas9 mechanism: 20 nt spacer + NGG PAM
- GC content calculation per guide
- `-stub-run` / `-stub` for workflow development
- `-with-report`
- DESeq2 LRT, interaction terms, time series (extended topics)

---

This lab bridges Nextflow pipeline development and biological reasoning. All modules are fully implemented — your task is to wire them together in `main.nf` and then implement the guide-finding logic in a Jupyter notebook.

## Nextflow activity

The workflow must:
1. `bgzip` the reference FASTA (required for indexed access)
2. Use the provided script to extract the start/stop coordinates of NM_000299 (PKP1) from the BED file into a `region_of_interest.txt`
3. Index the bgzipped genome with `samtools faidx`
4. Extract the PKP1 sequence using the FASTA, `.fai` index, and region file

Reference files are in `refs/` (or copy from `/projectnb/bf528/materials/lab04_template/`). All paths are configured in `nextflow.config`.

```bash
# Test workflow logic first
nextflow run main.nf -profile cluster,conda -stub-run

# Full run with report
nextflow run main.nf -profile cluster,conda -with-report
```

## BioPython activity

Create the conda environment from `envs/notebook_env.yml` and open the provided notebook.

1. Load the extracted PKP1 sequence with `SeqIO`
2. Scan every position on both strands for a 20 nt sequence followed by NGG
3. For each guide, report: sequence, genomic start coordinate, GC content (%)
4. Compare your results against `results/results.tsv` and the ChopChop screenshot in the repo

*Extra*: find guides on the minus strand as well.

---

# Extended topic — Time Series and Interaction Analyses in DESeq2

Most differential expression analyses compare two conditions. Real experiments are often more complex: multiple time points, factorial designs, or experiments where the effect of one variable depends on another. This section extends the standard DESeq2 workflow to handle those cases.

## LRT vs. Wald test

The standard Wald test compares two groups using a pre-specified contrast. The **likelihood ratio test** asks whether including time in the model explains significantly more variance than a reduced model without it — identifying any gene that changes across a time course regardless of the pattern.

```r
# Full model
dds <- DESeqDataSetFromMatrix(counts, coldata,
                              design = ~ genotype + time + genotype:time)
dds <- DESeq(dds, test = "LRT", reduced = ~ genotype)
res <- results(dds)
```

## Interaction terms

An interaction term (`genotype:time`) tests whether the trajectory of expression over time differs between genotypes.

```r
resultsNames(dds)                              # see all available coefficients
results(dds, name = "genotypeKO.timep4")       # interaction at a specific time
```

## Clustering temporal patterns

```r
vsd      <- vst(dds)
sig      <- rownames(res)[which(res$padj < 0.05)]
mat      <- assay(vsd)[sig, ]
mat_sc   <- t(scale(t(mat)))
pheatmap(mat_sc, cluster_cols = FALSE)
```

## Pairwise contrasts from a multi-level factor

```r
results(dds, contrast = c("time", "p7", "p0"))
```

## Tasks

1. Load the provided count matrix and sample metadata
2. Fit a model with `genotype`, `time`, and their interaction using the LRT
3. Identify genes significant at FDR < 0.05
4. Plot a heatmap of scaled expression ordered by time point
5. Extract pairwise contrasts between adjacent time points within each genotype
6. Interpret: which genes show a genotype-specific temporal response?
