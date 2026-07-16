---
title: "Nextflow Subworkflows"
layout: single
---

# Subworkflows

A subworkflow is a named workflow that can be called from another workflow,
just like a process. Where a process wraps a single tool or command, a
subworkflow wraps a sequence of processes that you want to treat as a unit.

You have already seen workflows in `main.nf`. A subworkflow is the same
concept, but it is defined in its own file and imported with `include` rather
than living in `main.nf` directly.

## When to Extract a Subworkflow

The main motivation for a subworkflow is eliminating duplicated logic across
projects. In this course, several analysis steps appear in multiple projects
with nearly identical code:

- FastQC before and after trimming
- Samtools sort → index → flagstat on aligned BAMs
- Collecting QC files and running MultiQC

Writing this logic once as a subworkflow and importing it means that a
correction or improvement propagates to every project automatically rather than
requiring the same change to be made in multiple places.

The other motivation is readability. A `main.nf` that calls `READS_QC`,
`ALIGN`, and `BAM_QC` is easier to understand at a glance than one that
inlines thirty lines of channel wiring for each of those steps.

## Subworkflow File Structure

By convention, subworkflows for this course live in `projects/subworkflows/`.
Each subworkflow is its own `.nf` file:

```
projects/
├── subworkflows/
│   ├── reads_qc.nf
│   ├── bam_qc.nf
│   └── multiqc_report.nf
├── project-2-nextflow-solutions/
│   ├── main.nf
│   └── modules/
└── project-3-nextflow-solutions/
    ├── main.nf
    └── modules/
```

## Defining a Subworkflow

A subworkflow file looks like a normal module file, but contains a `workflow`
block instead of a `process` block. It also needs `nextflow.preview.types = true`
if the `take:` and `emit:` sections use type annotations.

Here is the `READS_QC` subworkflow as a full example:

```bash
nextflow.preview.types = true

include { FASTQC } from '../project-2-nextflow-solutions/modules/fastqc'
include { TRIM }   from '../project-2-nextflow-solutions/modules/trimmomatic'

record Sample {
    id: String
    reads: List<Path>
}

record TrimmedSample {
    id: String
    reads: List<Path>
    trim_log: Path
}

workflow READS_QC {
    take:
    samples_ch: Channel<Sample>
    adapters: Path

    main:
    pre_trim_qc  = FASTQC(samples_ch)
    trimmed_ch   = TRIM(samples_ch, adapters)
    post_trim_qc = FASTQC(trimmed_ch.map { s -> record(id: s.id, reads: s.reads) })

    emit:
    trimmed:      Channel<TrimmedSample> = trimmed_ch
    fastqc_pre:   Channel<Record>        = pre_trim_qc
    fastqc_post:  Channel<Record>        = post_trim_qc
}
```

The structure of a subworkflow mirrors that of a regular workflow:

- `take:` — the inputs the subworkflow expects, with type annotations
- `main:` — the processing logic
- `emit:` — the named outputs the subworkflow produces, with type annotations

## Typed `take:` and `emit:`

Type annotations in `take:` and `emit:` serve two purposes. First, they
document the contract: anyone reading the file can immediately see what type of
data the subworkflow expects and produces without tracing through the logic.
Second, the language server uses the annotations to validate that the channels
you pass in are compatible and that the channels you receive back are used
correctly.

The type annotation syntax is the same as in process inputs and workflow
parameters:

```bash
take:
samples_ch: Channel<Sample>   // a channel of Sample records
adapters: Path                // a single file path (dataflow value)
```

Emit annotations use an assignment form:

```bash
emit:
trimmed: Channel<TrimmedSample> = trimmed_ch
report:  Value<Path>            = report_file
```

If the declared type does not match the actual type of the assigned value,
the language server will report an error.

## Importing a Subworkflow

Subworkflows are imported with `include`, exactly like processes:

```bash
include { READS_QC } from '../../subworkflows/reads_qc'
include { BAM_QC }   from '../../subworkflows/bam_qc'
```

The path is relative to the file doing the importing. Because subworkflows
live one level above the project directories, you need to go up two levels from
a `main.nf` inside a project folder.

## Calling a Subworkflow

A subworkflow is called exactly like a process — by name, with its inputs as
arguments. The return value is the combined record of all emitted outputs:

```bash
workflow {
    read_pairs_ch = channel.fromList(params.reads)

    qc_out    = READS_QC(read_pairs_ch, params.adapters)
    align_out = ALIGN(qc_out.trimmed, params.genome)
    bam_out   = BAM_QC(align_out.bam)

    MULTIQC_REPORT(
        qc_out.fastqc_pre
            .mix(qc_out.fastqc_post)
            .mix(bam_out.flagstat)
            .flatMap { r -> r.files }
            .collect()
    )
}
```

Each emitted output is accessed as a field on the return value, using the name
given in the `emit:` section of the subworkflow. This is the same approach used
for process outputs with static typing — no `.out` property, just standard field
access on the return value.

## Record Types Across Files

When multiple files need to share the same record type — for example, both
`reads_qc.nf` and `main.nf` need to know what a `Sample` record looks like —
define the type in the subworkflow file and re-export it with `include`:

In `reads_qc.nf`:
```bash
record Sample {
    id: String
    reads: List<Path>
}
```

In `main.nf`:
```bash
include { READS_QC, Sample } from '../../subworkflows/reads_qc'
```

This ensures there is a single definition of `Sample` that both files agree on,
rather than two independent definitions that could silently diverge.

## Designing Subworkflow Inputs for Reuse

A subworkflow is more reusable when its `take:` types require only the fields
it actually needs. If `READS_QC` declares its input as `Channel<Sample>` where
`Sample` has only `id` and `reads`, then any richer sample record — one that
also carries `condition`, `replicate`, or any other project-specific fields —
will still be accepted due to duck-typing.

This means you can write a subworkflow once and call it from projects that have
different samplesheet columns, as long as all of them provide at least `id` and
`reads`.

Avoid declaring a `take:` type that requires fields the subworkflow does not
actually use. Doing so will make the subworkflow unnecessarily restrictive and
will break callers that have not included those fields.

## Subworkflows Available in This Course

The following shared subworkflows are provided under `projects/subworkflows/`:

| File | Workflow name | What it does | Used by |
|---|---|---|---|
| `reads_qc.nf` | `READS_QC` | Pre-trim FastQC → Trimmomatic → post-trim FastQC | Projects 2, 3 |
| `bam_qc.nf` | `BAM_QC` | Samtools sort → index → flagstat | Project 3 |
| `multiqc_report.nf` | `MULTIQC_REPORT` | Collect QC files and run MultiQC | Projects 2, 3 |
