---
title: "Lab 13 — Single-Cell RNA-seq Setup"
layout: single
---

**Key concepts and tools**
- GEO accession numbers, EMBL-ENA download portal
- FTP links, `wget` for large file transfer
- `bamtofastq` (10X Genomics) — BAM to FASTQ conversion
- Cell Ranger `count` — alignment and UMI counting
- 10X Genomics library structure: CB (cell barcode), UMI tags
- Counts matrix: `filtered_feature_bc_matrix/`
- Samplesheet design for a download-and-process pipeline
- Building a Nextflow pipeline from scratch (no scaffold)

---

The starting point for the single-cell unit. Published 10X single-cell RNA-seq studies often deposit raw data as aligned BAM files rather than FASTQs, which means you need to reverse the alignment before re-running the standard pipeline. You will locate the appropriate files on EMBL-ENA, build a samplesheet with FTP links, and write a Nextflow pipeline (from an empty repo) that downloads the BAMs, converts them to FASTQs with `bamtofastq`, and runs `cellranger count` to produce the counts matrix used in the next two labs.

---

We are going to recreate findings from [this paper](https://www.nature.com/articles/s41467-020-20343-5), which characterizes isoform expression across cell types in the mouse hippocampus at postnatal day 7 using single-cell RNA-seq.

## Background

With 10X Chromium single-cell RNA-seq, many studies deposit data as aligned BAM files that carry cell barcode (CB) and UMI (UR) tags. To regenerate a counts matrix — for example, aligned to a newer reference — you must first reverse the alignment back to FASTQ and then re-run the full Cell Ranger pipeline.

## Starting from an empty repo

The GitHub Classroom repo is empty. You need to create the minimal Nextflow structure yourself:

```
your-repo/
├── main.nf
├── nextflow.config
└── modules/
    ├── download/main.nf
    ├── bamtofastq/main.nf
    └── cellranger_count/main.nf
```

## Finding and downloading the data

1. Find the GEO accession in the paper and search for it on [EMBL-ENA](https://www.ebi.ac.uk/ena/browser/)
2. Locate the FTP links for the BAM files
3. Encode the sample name and FTP link in a `samplesheet.csv`

**Start with the provided subset samplesheet** which points to small subsetted files. Switch to the full samplesheet once the pipeline is working.

## Modules to write

**Download** — Input: `tuple val(name), val(ftp_link)`. Use `wget` to download the BAM.

**bamtofastq** — Input: `tuple val(name), path(bam)`. Use the 10X `bamtofastq` utility. More threads will significantly reduce runtime.

Container: `ghcr.io/bf528/cellranger:latest`

**cellranger count** — Input: FASTQs + reference genome path. Point to the FASTQ directory, sample name, and reference. Output: the `filtered_feature_bc_matrix/` directory.

## Output

A successful run produces a `filtered_feature_bc_matrix/` directory per sample containing:
- `matrix.mtx.gz` — sparse count matrix
- `features.tsv.gz` — gene names
- `barcodes.tsv.gz` — cell barcodes

These are the input for QC and analysis in the next lab.

## Transferring your repo after the semester

```bash
git clone git@github.com:bf528/your-repo.git
cd your-repo/
git remote set-url origin git@github.com:<your_username>/new_repo.git
git push -u origin main
```

This preserves your full commit history.
