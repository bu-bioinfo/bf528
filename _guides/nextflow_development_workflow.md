---
title: "Nextflow Development Workflow"
layout: single
---

# Nextflow Development Workflow

Building a pipeline involves more than writing processes and connecting channels.
This guide describes the standard sequence of steps to use when developing,
testing, and running a Nextflow pipeline in this course. Following this order
will save you time and prevent the most common mistakes.

## The Recommended Order

```
write / edit → format → lint → stub run → local run → inspect logs → cluster run → review report
```

Each step is described below.

---

## 1. Format

Nextflow ships with a built-in formatter that standardizes indentation and
spacing in `.nf` files and `nextflow.config`. Run it before anything else so
your code is in a consistent state:

```bash
nextflow fmt main.nf
nextflow fmt nextflow.config
```

To format every `.nf` file in the project at once:

```bash
nextflow fmt .
```

The formatter will rewrite the file in place. This does not change the behavior
of your pipeline — it only cleans up whitespace and indentation. Running it
early means that any diff you create later reflects real changes, not formatting
noise.

If you are using VSCode, the [Nextflow extension](https://marketplace.visualstudio.com/items?itemName=nextflow.nextflow)
can format on save, which eliminates this step entirely.

---

## 2. Lint

Linting checks your pipeline for known mistakes and style violations before
you try to run it. There are two tools available:

### `nextflow lint`

The built-in linter catches syntax errors and structural issues in `.nf` files:

```bash
nextflow lint main.nf
```

Run this on individual module files as well:

```bash
nextflow lint modules/fastqc/main.nf
```

If there are no issues, the command exits silently. Any warnings or errors are
printed with the line number and a short description.

### `nf-core lint`

If `nf-core` tools are installed, the `lint` subcommand runs a broader set of
checks against community best practices — correct use of `publishDir`,
consistent label naming, proper container declarations, and more:

```bash
nf-core lint
```

Run this from the root of the project directory. Warnings do not stop the
pipeline from running, but they indicate patterns that are known to cause
problems in practice.

### `nextflow inspect`

`nextflow inspect` validates the process graph without running anything and
prints a JSON summary of every process, its declared inputs, outputs, and
directives:

```bash
nextflow inspect main.nf -profile conda,local
```

This is useful for confirming that your `include` statements resolved correctly
and that each process sees the inputs you expect.

---

## 3. Stub Run

A stub run executes your pipeline using placeholder `stub` blocks instead of
the real `script` blocks in each process. Each stub block creates empty output
files with `touch`, which is enough for Nextflow to verify that channels are
wired correctly.

```bash
nextflow run main.nf -profile conda,local -stub
```

This is the fastest and cheapest test of your pipeline's logic. It will catch:

- Missing or misnamed `emit` labels
- Channel type mismatches
- Incorrect `publishDir` paths
- Processes that never receive input because of a broken channel connection

It will **not** catch tool-level errors (wrong flags, missing input columns,
etc.) because the actual commands are never run.

Every process in your module should have a `stub` block that creates one `touch`
command for each declared output:

```groovy
process FASTP {

    input:
    tuple val(sample), path(read1), path(read2)

    output:
    tuple val(sample), path("${sample}_R1_trimmed.fastq.gz"), path("${sample}_R2_trimmed.fastq.gz"), emit: reads
    tuple val(sample), path("${sample}_fastp.json"), emit: log

    stub:
    """
    touch ${sample}_R1_trimmed.fastq.gz
    touch ${sample}_R2_trimmed.fastq.gz
    touch ${sample}_fastp.json
    """

    script:
    ...
}
```

If the stub block is missing a file that the `output` block declares, the run
will fail — which is the intended behavior. The stub is testing your output
declarations, not just your script.

---

## 4. Local Run

Once the stub run passes, run the pipeline on a small subset of real data
on your interactive node. This confirms the actual commands work before
committing cluster resources:

```bash
nextflow run main.nf -profile conda,local
```

Use a reduced samplesheet (one or two samples, subsampled reads) rather than
the full dataset. If a process fails, you will get the error immediately in your
terminal rather than waiting for a cluster job to be scheduled.

---

## 5. Inspect Logs

After any run — successful or failed — use `nextflow log` to examine what
happened.

### List all runs

```bash
nextflow log
```

Each row shows the run name, timestamp, status, and the command used to invoke
it.

### Inspect task-level detail

```bash
nextflow log <run-name> -f hash,name,status,exit,workdir
```

This prints one row per task. The columns you will use most often:

| Field | What it tells you |
|---|---|
| `hash` | The abbreviated path to the work directory |
| `name` | Process name and sample identifier |
| `status` | COMPLETED, CACHED, FAILED, or ABORTED |
| `exit` | Integer exit code (0 = success) |
| `workdir` | Full path to the task's work directory |

### Filter to failed tasks

```bash
nextflow log <run-name> -f name,workdir -filter 'status == "FAILED"'
```

### Read the task's exact command

Navigate to the work directory and open `.command.sh`:

```bash
cd <workdir>
cat .command.sh
```

This shows the exact shell script Nextflow ran — with all variables substituted
in. This is the most reliable way to reproduce a failure outside of Nextflow.
Other useful files in the same directory:

| File | Contents |
|---|---|
| `.command.err` | Stderr from the tool |
| `.command.out` | Stdout from the tool |
| `.command.log` | Combined stdout + stderr |
| `.exitcode` | Integer exit code |

---

## 6. Cluster Run

Once the local run is clean, submit to the cluster with the appropriate profile:

```bash
nextflow run main.nf -profile singularity,cluster
```

Include execution reports so you have a record of the run and resource usage:

```bash
nextflow run main.nf -profile singularity,cluster \
    -with-report report.html \
    -with-timeline timeline.html
```

The `-resume` flag (or `resume = true` in `nextflow.config`) will skip any
tasks that completed successfully in a previous run. This means that if a
pipeline fails partway through, you can fix the issue and resubmit without
re-running the early steps:

```bash
nextflow run main.nf -profile singularity,cluster -resume
```

---

## 7. Review the Report

Open `report.html` in a browser. The three sections to check after every run:

**Summary tab** — Did all tasks complete? Note the total wall time and any
processes that were retried.

**Tasks tab** — A table with one row per task. Check the `status` and `exit`
columns for anything unexpected. The `peak_rss` and `cpu_usage` columns show
actual memory and CPU consumption, which you can use to calibrate the resource
labels in `nextflow.config` for future runs.

**Resources tab** — Box plots of CPU and memory usage per process. If a process
consistently uses far less than you requested, lower its label. If it is
approaching the ceiling, raise it.

---

## `ext.args` — Tool Flags Belong in Config

A recurring pattern in this course is passing extra tool flags through
`nextflow.config` rather than hard-coding them in module files. This keeps
modules generic and reusable.

In `nextflow.config`:

```groovy
process {
    withName: 'FASTP' {
        ext.args = '--detect_adapter_for_pe --qualified_quality_phred 20'
    }
}
```

In the module:

```groovy
script:
def args = task.ext.args ?: ''
"""
fastp --in1 $read1 --in2 $read2 $args
"""
```

The `?: ''` is required. If `ext.args` is not set in the config, this
expression evaluates to an empty string and the tool runs without extra flags.
Without it, the process will throw a null reference error at runtime.

---

## Quick Reference

| Step | Command |
|---|---|
| Format all `.nf` files | `nextflow fmt .` |
| Lint a workflow | `nextflow lint main.nf` |
| Lint with nf-core rules | `nf-core lint` |
| Validate process graph | `nextflow inspect main.nf -profile conda,local` |
| Stub run | `nextflow run main.nf -profile conda,local -stub` |
| Local run | `nextflow run main.nf -profile conda,local` |
| Cluster run with reports | `nextflow run main.nf -profile singularity,cluster -with-report report.html -with-timeline timeline.html` |
| Resume a run | `nextflow run main.nf -profile singularity,cluster -resume` |
| List all runs | `nextflow log` |
| Inspect task detail | `nextflow log <run-name> -f hash,name,status,exit,workdir` |
| Filter to failed tasks | `nextflow log <run-name> -f name,workdir -filter 'status == "FAILED"'` |
