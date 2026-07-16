---
title: "Lab 04 — Multi-Sample Pipelines and Modules"
layout: single
---

**Key concepts and tools**
- Samplesheets — CSV files as structured pipeline input
- `List<RecordType>` params and automatic CSV parsing
- `channel.fromList(params.samplesheet)` — channel from a typed list
- Named record types: `record Sample { name: String; url: String }`
- Record field propagation — carrying `name` through every process
- `include { PROCESS } from './modules/...'` — the modules system
- `stub:` block and `-stub-run` — testing pipeline logic without real tools
- `.map {}`, `.collect()` — channel operators for multi-sample aggregation
- `publishDir` on a collection process

---

This lab extends the single-genome pipeline from lab 2 to process multiple bacterial genomes in parallel. The bioinformatics tools are unchanged — `wget` and `genome_stats.py` — so the focus is entirely on Nextflow patterns: samplesheets, typed records, modules, and aggregating per-sample results into a single summary.

## Setup

```bash
module load miniconda
conda activate nextflow_latest
export NXF_SYNTAX_PARSER=v2
```

```bash
nextflow run main.nf -profile conda,local    # local test
nextflow run main.nf -profile conda,cluster  # submit to SCC
```

## Structure

```
main.nf               # complete — defines record types, includes, workflow
samplesheet.csv       # three bacterial genomes
modules/
  download/main.nf    # typed I/O provided — fill in script block
  genome_stats/main.nf
  summarize/main.nf   # fully complete — see how List<Path> input works
bin/
  genome_stats.py
envs/
  biopython_env.yml
```

## Task 1 — Read `main.nf` and `samplesheet.csv`

`main.nf` is fully complete. Read it before writing any code. Notice:

- Three named record types at the top: `Sample`, `GenomeFile`, `StatsFile`. The `Sample` fields `name` and `url` match the CSV column names — Nextflow parses the CSV automatically.
- `channel.fromList(params.samplesheet)` emits one record per row.
- Three `include` statements import processes from `modules/`.
- The workflow uses `.map` and `.collect()` to gather all per-sample stats files before passing them to `SUMMARIZE`.

## Task 2 — Write the DOWNLOAD module

`modules/download/main.nf` has the typed I/O already filled in. Fill in the `script` block:

```bash
wget ${url} -O ${name}.fna.gz
```

Input record fields (`name`, `url`) are available as variables in the `script` block directly. Test wiring before downloading anything:

```bash
nextflow run main.nf -profile conda,local -stub-run
```

The `stub:` block runs instead of `script:`, creating empty placeholder files instantly. A clean stub run confirms that all includes resolve and channels wire correctly.

## Task 3 — Write the GENOME_STATS module

`modules/genome_stats/main.nf` has the typed I/O already filled in. Fill in the `script` block:

```bash
genome_stats.py -i ${fa} -n ${name} -o ${name}_stats.tsv
```

Make the script executable first:

```bash
chmod +x bin/genome_stats.py
```

## Task 4 — Run and inspect

```bash
nextflow run main.nf -profile conda,cluster
```

After the run, check `results/summary.tsv` — it should have a header row and one data line per genome. Then inspect the execution log:

```bash
nextflow log <run-name> -f hash,name,exit,status
```

Navigate into a `work/` subdirectory and open `.command.sh` to see exactly what command ran for that task.

## Optional

Add a fourth genome to `samplesheet.csv` and re-run. Only the new genome's processes execute — the other three are served from cache.
