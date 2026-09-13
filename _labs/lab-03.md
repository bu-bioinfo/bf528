---
title: "Lab 03 — Creating a Nextflow Workflow for Multiple Samples"
layout: single
---

**Key concepts and tools**
- Modularization: one process per `.nf` file under `modules/`, wired together with `include`
- `ncbi-datasets-cli` genome downloads
- Prokka genome annotation, GFF files
- `samtools faidx`, FASTA index (`.fai`), region coordinates (`chr:start-end`)
- Nextflow static typing: `record` types, dot notation, `nextflow.enable.types`
- `stub` block, `-stub` flag
- `ext.args`, `task.ext.args ?: ''`, `withName:` process selector
- `nextflow log`, `-f` fields, `-filter` expressions
- Work directory debugging: `.command.sh`, `.command.err`, `.exitcode`
- `-with-report`
- `resume` in `nextflow.config`
- Process `label`s and resource requests
- `nextflow lint`, `nextflow lint -format`
- `results` directory, `publish:` block

---

This lab moves you from a single-file pipeline to a modular, statically-typed
one: multiple processes, each in its own module, passing typed `record`s
between them instead of positional tuples.

You will read a specification document describing the pipeline's contract
end-to-end, then implement the missing pieces of each module and wire the
whole workflow together yourself.

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
> in `main.nf`
>
> **Criteria - How you'll know you're succeeding:** `nextflow run main.nf
> -stub` completes end-to-end for both samples with correctly-named
> placeholder outputs at every step. `nextflow run main.nf -profile
> conda,cluster` then completes without manual intervention.

## Diagnose and configure pipeline behavior using Nextflow's runtime and debugging tools

> **Purpose - Why This Matters:** Production pipelines need to be
> configurable and debuggable without editing module code. `ext.args` +
> `withName:` let you tune a tool's flags per run; `nextflow log` and the
> work directory let you see exactly what command ran (or would have run)
> and why it failed. Y
>
> **Task - What you will do:** Confirm that `nextflow.config`'s
> `withName: 'PROKKA'` sets `--kingdom Bacteria` via `ext.args`, by finding
> the `PROKKA` task's work directory with `nextflow log -filter` and
> inspecting `.command.sh`. Use `-stub` to validate your workflow wiring
> before running any real commands. You understand that you must request
> the right number of computational resources from the cluster and specify
> to use those resources in the actual command.
>
> **Criteria - How you'll know you're succeeding:** You can go from a run
> name to a specific task's work directory using `nextflow log -f workdir
> -filter '...'`, and can point to where `--kingdom Bacteria` appears in that
> task's `.command.sh`.

## Explain and verify Nextflow's task-level caching behavior

> **Purpose - Why This Matters:** With `resume = true`, Nextflow skips
> re-running any task whose hash hasn't changed, saving significant time on
> pipelines you re-run repeatedly while developing. Knowing what goes into
> that hash will lets you predict which tasks will rerun before you kick off a 
> run, and correctly interpret `cached` vs. re-executed tasks when something 
> looks off.
>
> **Task - What you will do:** After uncommenting the `withName: 'PROKKA'`
> block in `nextflow.config` and re-running your pipeline, observe which
> processes rerun and which stay `cached`. Explain why changing `PROKKA`'s
> `ext.args` forces `PROKKA`, `EXTRACT_REGION`, and `SAMTOOLS_FAIDX_SUBSET` to
> rerun, while `SAMTOOLS_FAIDX`stays cached. You should see similar behavior when
> you add a `label`.
>
> **Criteria - How you'll know you're succeeding:** You can correctly predict,
> before re-running, which processes will show as `cached` vs. re-executed,
> and can explain that prediction in terms of each task's hash (its inputs,
> script, and process directives) rather than just describing the observed
> output.

# AIAS Level Expectations (AIAS Level 2)

This lab builds directly on Lab 02's Nextflow foundations. Try to complete
the record-type and channel-wiring tasks on your own — this is where the
new conceptual content (static typing, joining channels) lives. You may
consult LLMs to have concepts explained, but write the wiring yourself.
