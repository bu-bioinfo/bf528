---
title: "Lab 10 — Genome Browsers and Alignment"
layout: single
---

**Key concepts and tools**
- Bowtie2 — splice-unaware short-read aligner, index building
- STAR — splice-aware RNA-seq aligner, index building
- `samtools sort`, `samtools index`
- BAM and BAI file format
- `bamCoverage` (deepTools) — BAM to bigWig conversion
- bigWig format, coverage tracks
- IGV — loading BAMs, bigWigs; paired-end read visualization
- Splice-aware vs. splice-unaware alignment: visual differences at exon junctions
- `branch` operator — routing samples to different processes

---

You will build a Nextflow pipeline that aligns RNA-seq reads with two different aligners — Bowtie2 (splice-unaware) and STAR (splice-aware) — then sorts and indexes both BAM files and converts them to bigWig coverage tracks. Several modules are provided; you complete the `samtools sort`, `samtools index`, and `bamCoverage` modules and write the workflow that connects them.

## Workflow tasks

1. Build a Bowtie2 index and a STAR index for human chr16 (hg38)
2. Align the `bowtie2` sample with Bowtie2 and the `star` sample with STAR — use a channel operator to route each sample to the correct aligner
3. Sort and index both resulting BAM files with samtools
4. Generate a bigWig coverage track from each BAM with `bamCoverage`

Samples are subsetted for speed — run locally:

```bash
nextflow run main.nf -profile singularity,local
```

## IGV

Open an SCC Desktop interactive session (OnDemand) to run the IGV desktop app. Load both BAM files and both bigWig tracks. Navigate to a gene with multiple exons and observe how reads from the STAR-aligned BAM span splice junctions while reads from the Bowtie2 BAM do not.

Pre-generated results are available at `/projectnb/bf528/materials/lab07_template/visualization/` if your pipeline is still running.
