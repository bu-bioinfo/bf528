---
title: Nextflow Best Practices
layout: default
nav_order: 99
---

# Nextflow best practices reference

A quick reference for the habits we follow in this course. Keep this open while working on labs and projects.

---

## Conventional commits

Every commit message follows this format:

```
<type>(<scope>): <short description>

[optional body]
```

**Types:**

| Type | When to use |
|---|---|
| `feat` | Adding new functionality to a process or workflow |
| `fix` | Correcting a bug or wrong output |
| `refactor` | Restructuring code without changing behavior (e.g. migrating to static types) |
| `docs` | Updating comments, README, or this book |
| `test` | Adding or updating test profiles or data |
| `chore` | Config, CI, dependency updates |
| `perf` | Performance improvements |

**Scope** should be the process, workflow, or config file being changed.

**Examples:**

```
feat(quant): add salmon index caching
fix(fastqc): correct output record field name
refactor(rnaseq): migrate workflow to static types
docs(params): document samplesheet format
chore(config): add test profile defaults
```

> **Rule of thumb:** commit after every logical unit of work — not at the end of the day, and not once per lab.

---

## Config vs script separation

Parameters live in **`main.nf`** (typed, documented, defaulted). Execution configuration lives in **`nextflow.config`**.

### `main.nf` — owns parameters

```groovy
params {
    // The input samplesheet of paired-end reads
    reads: List<Sample> = "${projectDir}/data/samples.csv"

    // The input transcriptome file
    transcriptome: Path = "${projectDir}/data/ref.fa"

    // Output directory
    outdir: Path = "results"

    // MultiQC config directory
    multiqc: Path = "${projectDir}/multiqc"
}
```

### `nextflow.config` — owns execution config

```groovy
profiles {
    test {
        params.reads = "${projectDir}/data/test_samples.csv"
    }
    hpc {
        process.executor = 'slurm'
        process.memory   = '16 GB'
    }
}
```

### Setting `NXF_SYNTAX_PARSER`

This is a runtime environment variable — it cannot go in `nextflow.config`. Use a `.env` file in your project root instead:

```
# .env
NXF_SYNTAX_PARSER=v2
```

Commit this file so all collaborators use the same parser.

### What goes where

| Concern | Location |
|---|---|
| Parameter types, defaults, descriptions | `params {}` block in `main.nf` |
| Test data defaults | `profiles { test {} }` in `nextflow.config` |
| Resource and executor config | `profiles { hpc {} }` in `nextflow.config` |
| Parser version | `.env` |

> **Never** use the legacy `params.foo = "..."` syntax at the top of `main.nf`. The typed `params {}` block replaces it entirely.

---

## Static typing

Enable static typing in every script that uses typed processes or workflows:

```groovy
nextflow.preview.types = true
```

### Records over tuples

Tuple elements are accessed by index — records are accessed by name. Always prefer records.

```groovy
// define a record type
record Sample {
    id:      String
    fastq_1: Path
    fastq_2: Path
}

// load samplesheet into a typed channel
read_pairs_ch = channel.fromList(params.reads)
```

### Typed process inputs and outputs

```groovy
process FASTQC {
    input:
    record(
        id:      String,
        fastq_1: Path,
        fastq_2: Path
    )

    output:
    record(
        id:     id,
        fastqc: file("fastqc_${id}_logs")
    )

    // ...
}
```

### Typed workflow take/emit

```groovy
workflow RNASEQ {
    take:
    read_pairs_ch: Channel<Sample>
    transcriptome: Path

    // ...

    emit:
    samples: Channel<AlignedSample> = samples_ch
}
```

### Patterns to avoid

| Anti-pattern | Replacement |
|---|---|
| `tuple val(id), path(fastq_1)` | `record(id: String, fastq_1: Path)` |
| `Channel.from(...)` | `channel.of(...)` |
| `.splitCsv()` as an operator | `.flatMap { csv -> csv.splitCsv() }` |
| `channel.fromFilePairs(glob)` | `channel.fromList(params.reads)` with a samplesheet |
| Implicit `it` closure parameter | Declare the parameter explicitly: `{ v -> v * 2 }` |

---

## Modularity and reusability

### One process per file

```
modules/
  fastqc.nf       // process FASTQC
  quant.nf        // process QUANT
  index.nf        // process INDEX
  rnaseq.nf       // workflow RNASEQ
main.nf           // entry workflow only
```

### Pass params as explicit arguments

Processes and subworkflows should be self-contained. Pass parameters in as arguments rather than accessing `params` globals inside a module.

```groovy
// good — explicit
RNASEQ(read_pairs_ch, params.transcriptome)

// avoid — implicit global access inside a module
process QUANT {
    script:
    "salmon quant -i ${params.index} ..."  // don't do this
}
```

### Patterns to avoid

| Anti-pattern | Replacement |
|---|---|
| `ch \| PROCESS \| map { ... }` | Standard assignments and method calls |
| `MY_WORKFLOW.out.foo` | Assign workflow outputs: `out = MY_WORKFLOW(...)` |
| `channel.of(1,2).set { ch }` | `ch = channel.of(1, 2)` |
| `channel.of(1,2).tap { ch }` | `ch = channel.of(1, 2)` |
| `each` input qualifier in processes | Use `combine` to produce a single tuple channel |

---

## Samplesheet over glob

Globs (`ggal_gut_{1,2}.fq`) have no static type, fail silently on unexpected filenames, and can't be validated before a run starts. Use a samplesheet instead.

### Samplesheet format

```csv
id,fastq_1,fastq_2
gut,data/ggal/gut_1.fq,data/ggal/gut_2.fq
liver,data/ggal/liver_1.fq,data/ggal/liver_2.fq
lung,data/ggal/lung_1.fq,data/ggal/lung_2.fq
```

- Must have a header row
- Must use `,` as the separator
- Column names must match the `record` field names

### Loading a samplesheet

```groovy
record Sample {
    id:      String
    fastq_1: Path
    fastq_2: Path
}

params {
    reads: List<Sample> = "${projectDir}/data/samples.csv"
}

workflow {
    read_pairs_ch = channel.fromList(params.reads)
    // ...
}
```

Nextflow automatically parses the CSV and validates each row against the `Sample` record type. Invalid rows fail at startup, not mid-run.

| Approach | Type-safe | Validated at startup | Version-controllable |
|---|---|---|---|
| Glob pattern | No | No | No |
| Samplesheet + `List<Sample>` | Yes | Yes | Yes |