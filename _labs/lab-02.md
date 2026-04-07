---
title: "Lab 02 — Workflow Basics"
layout: single
---

**Key concepts and tools**
- `wget`, FTP downloads from NCBI
- `qsub`, `qstat`, SGE cluster submission
- Nextflow `process` block: `input`, `output`, `script`
- `workflow` block, calling processes, passing outputs between processes
- `conda` directive, `envs/` YAML files
- `bin/` directory, `chmod +x`, shebang lines (`#!/usr/bin/env python`)
- `publishDir`, `emit`
- `nextflow run`, `-profile conda,local`, `-profile conda,cluster`
- `nextflow log <run-name> -f hash,name,exit,status`
- `argparse` in Python

---

Starting from a bare shell command and ending with a multi-process Nextflow pipeline, this lab walks through five iterations of the same task: download an *E. coli* genome and compute basic sequence statistics. Each iteration adds a layer and addresses a shortcoming of the previous approach.

## Iterations

**Iteration 1 — Command line**
Run `wget` and a Python script directly in the terminal. Simple but not reproducible: no record of what ran, nothing parallelizable, hardcoded to one file.

**Iteration 2 — Cluster submission with `qsub`**
Wrap each command in a bash script and submit with `qsub`. Adds a record and uses cluster resources, but steps must be manually chained and there is no easy way to check success.

**Iteration 3 — Basic Nextflow**
Wrap the same commands in Nextflow `process` blocks connected in a `workflow`. Nextflow stages each process in an isolated `work/` subdirectory identified by a hash. Use `nextflow log <run-name> -f hash,name,exit,status` to find those directories.

**Iteration 4 — Argparse**
Update the Python script to accept input/output file names via `argparse` flags instead of hardcoding them. Make the script executable (`chmod +x`) and call it by name from the process `script` block.

**Iteration 5 — Multiple outputs with `emit` and `publishDir`**
A single process produces two output files (GC content and sequence length). Use `emit:` to name each output so downstream processes can reference them individually. Add `publishDir` to copy final results out of `work/`.

## Setup

```bash
module load miniconda
conda activate nextflow_latest
```

Navigate into `iteration_X/` for each section. Run with:

```bash
nextflow run main.nf -profile conda,local    # local test
nextflow run main.nf -profile conda,cluster  # submit to SCC
```

## Optional

Rewrite the download step using `ncbi-datasets-cli` instead of `wget` and keep the rest of the pipeline unchanged (iteration 6).
