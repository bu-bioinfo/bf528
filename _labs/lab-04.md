---
title: "Lab 04 — Modules and Multi-Sample Pipelines"
layout: single
---

**Key concepts and tools**
- `include { PROCESS } from './modules/...'`
- `modules/` directory structure, one process per module file
- `tuple val(meta), path(file)` input/output pattern
- `samplesheet.csv`, `splitCsv(header: true)`, `map`
- `ncbi-datasets-cli` genome download
- Prokka genome annotation, GFF output format
- `samtools faidx` — FASTA indexing and coordinate extraction
- `join` channel operator — merging channels by key
- `-stub-run` — testing workflow logic without running real tools
- `-with-report` — HTML execution report
- `resume = true` in `nextflow.config`
- Process `label` directives and resource allocation
- Jupyter notebooks, conda environments as kernels, circos plots

---

This lab introduces the module system and multi-sample patterns that will be standard for the rest of the course. The pipeline downloads several bacterial genomes from NCBI, annotates them with Prokka, indexes each genome with `samtools faidx`, and extracts a specific gene's sequence by its GFF coordinates. The pipeline is scaffolded but incomplete — you fill in the inputs, outputs, and commands for each process, then connect them in `main.nf`.

## Process specifications

Each module is outlined below. Use `-stub-run` to confirm the workflow logic before running real tools.

**`ncbi_datasets_cli`** — Input: `tuple val(name), val(GCF)`. Output: `tuple val(name), path("*.fna")`.

**`prokka`** — Input: `tuple val(name), path(fna)`. Output: `tuple val(name), path("*.gff"), emit: gff`. Use `--outdir` and `--prefix` flags set to the sample name.

**`extract_region`** — Input: `tuple val(name), path(gff)`. Output: `tuple val(name), path("region_of_interest.txt")`. Uses the provided script in `bin/`.

**`samtools_faidx`** — Input: `tuple val(name), path(fna)`. Output: `tuple val(name), path(fna), path("*.fai")`.

**`samtools_faidx_subset`** — Input: `tuple val(name), path(fna), path(fai), path(region)`. Output: `tuple val(name), path("*_region.subset.fna")`. You will need a channel operator to merge the `samtools_faidx` and `extract_region` outputs by sample name before passing them here.

## Running

```bash
# Test workflow logic (no real tools run)
nextflow run main.nf -profile local,conda -stub-run

# Run locally once logic is confirmed
nextflow run main.nf -profile local,conda

# Submit to cluster with report
nextflow run main.nf -profile cluster,conda -with-report
```

## New features introduced

- **`-stub-run`** — executes the `stub` block of each process instead of `script`, creating empty placeholder files instantly. Use this to validate channel wiring before committing to a full run.
- **`-with-report`** — generates an HTML summary of resource usage per task after the run.
- **`resume = true`** — caches completed tasks so a failed run can restart from where it stopped.
- **Labels** — each process has a `label` that maps to CPU/memory settings in `nextflow.config`, replacing per-process `qsub` flags.

## Jupyter notebook

Create a conda environment from the provided `notebook_env.yml`, select it as the notebook kernel, and use BioPython to visualize the gene annotations for all downloaded genomes as a circos plot.
