---
title: "Lab 03 — Nextflow Basics"
layout: single
---

**Key concepts and tools**
- Modularization: one process per `.nf` file under `modules/`, wired together with `include`
- `ncbi-datasets-cli` genome downloads
- Prokka genome annotation, GFF files
- `samtools faidx`, FASTA index (`.fai`), region coordinates (`chr:start-end`)
- Nextflow static typing: `record` types, dot notation, `nextflow.enable.types`
- `stub` block, `-stub-run` flag
- `ext.args`, `task.ext.args ?: ''`, `withName:` process selector
- `nextflow log`, `-f` fields, `-filter` expressions
- Work directory debugging: `.command.sh`, `.command.err`, `.exitcode`
- `-with-report`, `-with-timeline`, `-with-dag`
- `resume` in `nextflow.config`
- Process `label`s and resource requests
- `nextflow lint`, `nextflow lint -format`, `nextflow inspect`
- Jupyter notebooks, conda environments for analysis, circos plots (`pyCirclize`)

---

This lab moves you from a single-file pipeline to a modular, statically-typed
one: multiple processes, each in its own module, and passing typed `record`s
between them.


You will read a specification document describing the pipeline end-to-end, then 
implement the missing pieces of each module and wire the whole workflow together
yourself.

# Learning Objectives

## Build a multi-sample Nextflow pipeline using statically-typed records to connect modular processes

> **Purpose - Why This Matters:** Real pipelines chain many tools together,
> and each step's output must exactly match the next step's expected input.
> Nextflow's typed `record` system lets you (and the language server) catch
> shape mismatches before a job ever runs, and modularization keeps each
> tool's logic isolated and independently readable.
>
> **Task - What you will do:** Declare the `AssemblyRequest`/`Genome` record
> types in `ncbi_datasets_cli`, construct the output `record(...)` in
> `prokka`, write the `script:` block in `extract_region`, declare
> `input:`/`output:` in `samtools_faidx`, and wire all five modules together
> in `main.nf` — including joining two channels on a shared key so
> `samtools_faidx_subset` gets both required records at once.
>
> **Criteria - How you'll know you're succeeding:** `nextflow run main.nf
> -profile local,conda -stub-run` completes end-to-end for both samples with
> correctly-named placeholder outputs at every step. `nextflow run main.nf
> -profile local,conda` then completes without manual intervention, producing
> a non-empty `<name>_region.subset.fna` for each genome.

## Diagnose and configure pipeline behavior using Nextflow's runtime and debugging tools

> **Purpose - Why This Matters:** Production pipelines need to be
> configurable and debuggable without editing module code. `ext.args` +
> `withName:` let you tune a tool's flags per run; `nextflow log` and the
> work directory let you see exactly what command ran (or would have run)
> and why it failed.
>
> **Task - What you will do:** Confirm that `nextflow.config`'s
> `withName: 'PROKKA'` sets `--kingdom Bacteria` via `ext.args`, by finding
> the `PROKKA` task's work directory with `nextflow log -filter` and
> inspecting `.command.sh`. Use `-stub-run` to validate your workflow wiring
> before running any real commands.
>
> **Criteria - How you'll know you're succeeding:** You can go from a run
> name to a specific task's work directory using `nextflow log -f workdir
> -filter '...'`, and can point to where `--kingdom Bacteria` appears in that
> task's `.command.sh`.

## Visualize pipeline outputs in a Jupyter notebook

> **Purpose - Why This Matters:** Bioinformatics analyses are frequently
> explored and communicated through notebooks that combine code, text, and
> figures — being able to load pipeline outputs into one and turn them into
> a figure is a core, recurring skill.
>
> **Task - What you will do:** Create a conda environment for notebook use,
> open it in VSCode or JupyterLab, and generate a circos plot of the genome
> annotations produced by your pipeline using `pyCirclize`.
>
> **Criteria - How you'll know you're succeeding:** You produce a circos
> plot rendered from your pipeline's own output files, not sample data.

# AIAS Level Expectations (AIAS Level 2)

This lab builds directly on Lab 02's Nextflow foundations. Try to complete
the record-type and channel-wiring tasks on your own — this is where the
new conceptual content (static typing, joining channels) lives. You may
consult LLMs to have concepts explained, but write the wiring yourself.
