---
title: "Lab 12 — Differential Peak Analysis (ATACseq)"
layout: single
---

**Key concepts and tools**
- ATACseq library preparation concepts: transposon insertion, open chromatin
- Bowtie2 ATACseq flags: `-X 2000`, `--no-discordant`, `--no-mixed`
- MACS3 peak calling — ATACseq mode
- BED file format
- DiffBind: `dba`, `dba.count`, `dba.contrast`, `dba.analyze`, `dba.report`
- Consensus peak set, read counting in peaks
- Differential accessibility analysis
- bigWig tracks and IGV visualization
- `Channel.fromFilePairs`, samplesheet with condition metadata

---

This lab processes six ATACseq samples from a cancer cell line before and after IL-31 stimulation. You build a Nextflow pipeline to align reads with Bowtie2 (using ATACseq-specific parameters), call peaks with MACS3, sort and index BAMs, and generate bigWig tracks. In the second hour you use the DiffBind R package to define a consensus peak set, count reads across samples, and call differentially accessible regions between conditions. The pipeline structure is largely yours to design — most modules are provided, but you connect them and determine the MACS3 command. Results are loaded into IGV and compared against the published figures.

---

## Background

We will be analyzing data from [this paper](https://pmc.ncbi.nlm.nih.gov/articles/PMC7889151/), which performed ATACseq in a cancer cell line to examine how the chromatin environment changes following IL-31 stimulation.

## ATACseq-specific parameters

**Bowtie2 flags:**
- `-X 2000` — allow fragment sizes up to 2000 bp to capture di- and tri-nucleosome events
- `--no-discordant` — discard reads where both pairs do not align concordantly
- `--no-mixed` — discard reads where only one end of a pair aligns

**MACS3:** peak calling must be run in ATACseq mode. Consult the documentation to determine the appropriate flags.

## Setup

Your initial channel must include both the SRR identifier and the condition label for each sample. Use the samplesheet, `Channel.fromFilePairs`, and an appropriate operator to produce a tuple structured as `(SRR_id, reads, condition_name)`.

## First hour — Nextflow pipeline

Build a workflow that:
1. Indexes the human reference genome with Bowtie2
2. Aligns all 6 samples using the ATACseq-specific Bowtie2 flags
3. Sorts and indexes the BAM files
4. Calls peaks with MACS3
5. Generates bigWig coverage tracks

Most modules are provided. You are responsible for the MACS3 module and wiring the workflow together. Use `-stub-run` to validate channel logic before submitting to the cluster.

```bash
nextflow run main.nf -profile conda,local -stub-run
nextflow run main.nf -profile conda,cluster
```

## Second hour — DiffBind

Once alignment and peak calling have finished, use DiffBind in R to:

1. Read in the sample metadata CSV (BAM paths + peak files + condition labels)
2. Build a consensus peak set across all samples with `dba`
3. Count reads in consensus peaks with `dba.count`
4. Define the contrast (stimulated vs. unstimulated) with `dba.contrast`
5. Run differential analysis with `dba.analyze` (uses DESeq2 on the backend)
6. Export significant results as a BED file with `dba.report`

Start with default DiffBind parameters — most well-documented tools work reasonably with defaults.

## Visualization

Load the BAMs, bigWigs, and the differentially accessible BED file into IGV. Compare enriched regions against the figures in the paper. Consider: what higher-throughput approaches could you use to characterize these regions beyond visual inspection?
