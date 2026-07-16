---
title: "Lab 02 — Workflow Basics"
layout: single
---

**Key concepts and tools**
- `wget`, FTP downloads from NCBI
- `qsub`, `qstat`, SGE cluster submission
- Nextflow `process` block: `input`, `output`, `script`
- `workflow` block, typed process inputs/outputs as record fields
- `conda` directive, `envs/` YAML files
- `bin/` directory, `chmod +x`, shebang lines (`#!/usr/bin/env python`)
- `argparse` in Python
- `publishDir`
- `nextflow run`, `-profile conda,local`, `-profile conda,cluster`
- `nextflow log <run-name> -f hash,name,exit,status`

---

Starting from a bare shell command and ending with a multi-process Nextflow pipeline, this lab walks through six iterations of the same task: download an *E. coli* genome and compute basic sequence statistics. Each iteration adds a layer and addresses a shortcoming of the previous approach.

## Setup

```bash
module load miniconda
conda activate nextflow_latest
export NXF_SYNTAX_PARSER=v2
```

Navigate into `iteration_X/` for each section. Run with:

```bash
nextflow run main.nf -profile conda,local    # local test
nextflow run main.nf -profile conda,cluster  # submit to SCC
```

---

## Iterations

**Iteration 1 — Command line**
Run `wget` and a Python script directly in the terminal. Simple but not reproducible: no record of what ran, nothing parallelizable, the input path is hardcoded in the script.

**Iteration 2 — Cluster submission with `qsub`**
Wrap each command in a bash script and submit with `qsub`. Adds a record of what ran and uses cluster resources, but steps must be manually chained in the right order. There is no automatic dependency tracking and no easy way to re-run only the steps that failed.

**Iteration 3 — Basic Nextflow**
Wrap the same commands in Nextflow `process` blocks connected in a `workflow`. This is the core Nextflow model — each process runs in an isolated `work/` subdirectory identified by a hash of its inputs. Two things happen automatically that qsub cannot do: if you re-run the pipeline and the inputs haven't changed, Nextflow skips the process and uses the cached result; if a process fails, only that process needs to re-run.

After your first run, inspect the execution record:

```bash
nextflow log <run-name> -f hash,name,exit,status
```

Navigate to the work directory for any task and open `.command.sh` to see exactly what Nextflow ran, and `.command.err` to see stderr if the task failed.

**Iteration 4 — `bin/` and script best practices**
The Python script from iteration 1 has its input and output file paths hardcoded. Before the pipeline gets any more complex, fix that: update the script to accept file names via `argparse` flags, place it in the `bin/` directory, and make it executable:

```bash
chmod +x bin/genome_stats.py
```

Nextflow automatically adds `bin/` to `PATH` inside every process, so the script can be called by name from the `script` block without specifying a path. Shebang lines (`#!/usr/bin/env python`) are required for this to work.

This iteration keeps the Nextflow pipeline structure identical to iteration 3 — the only change is that the Python script is now a proper command-line tool.

**Iteration 5 — Multi-process pipeline with typed outputs**
Split the pipeline into two processes: one that downloads the genome, and one that computes the statistics. The download process must finish before the stats process can start — Nextflow tracks this dependency automatically because the output of the first process is declared as the input of the second.

Process outputs in this course use the typed record form. A process declares what it emits as a record with named fields:

```bash
output:
record(
    name: name,
    fa: file("${name}.fna")
)
```

The calling workflow assigns the result to a variable and accesses fields directly:

```bash
workflow {
    genome_out = DOWNLOAD(params.accession)
    STATS(genome_out)
}
```

This is cleaner than the legacy `emit:` + `PROCESS.out.field` pattern — the channel type is explicit and the language server can validate it before you run anything.

**Iteration 6 — `publishDir`**
The output files from each process live inside `work/` subdirectories with hashed names. That is intentional — it keeps every run reproducible and isolated — but it makes it inconvenient to find your final results. `publishDir` copies (or symlinks) specific output files to a named directory:

```bash
process STATS {
    publishDir params.outdir, mode: 'copy'
    ...
}
```

Add `publishDir` only to processes that produce final outputs you want to inspect or share. Intermediate files that are only consumed by the next process in the pipeline do not need it.

---

## Optional

Rewrite the download step using `ncbi-datasets-cli` instead of `wget` and keep the rest of the pipeline unchanged (iteration 7).
