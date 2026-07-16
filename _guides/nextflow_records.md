---
title: "Nextflow Records"
layout: single
---

# Records

A record is a new data structure in Nextflow that groups related values together
under named fields. If you have used Python dataclasses or named tuples before,
records serve a similar purpose: they let you refer to individual pieces of data
by name rather than by their position in a list.

Records replace the `tuple val(meta), path(reads)` pattern that you may have
seen in older Nextflow pipelines. Understanding why they were introduced, and
how to use them, will make your pipelines easier to read, easier to debug, and
much harder to break accidentally.

## Why Records Replace Tuples

In a tuple-based workflow, every element is identified by its position. If your
process declares the following input:

```bash
input:
tuple val(sample_id), path(fastq_1), path(fastq_2)
```

Then the channel feeding this process must supply values in exactly that order.
The moment you reorder elements — perhaps by joining two channels that happen
to have a different tuple structure — Nextflow will silently assign the wrong
values to the wrong variables. You will not find out until the tool fails
with a confusing error, or worse, produces incorrect output.

Records eliminate this class of bug entirely. Fields are matched by name, not
by position. A record with the fields `id`, `fastq_1`, and `fastq_2` will
always supply the right value to the right variable, regardless of the order
the fields appear in.

## Creating a Record

The `record()` function creates a record from named fields:

```bash
my_sample = record(id: 'gut', fastq_1: file('gut_1.fq'), fastq_2: file('gut_2.fq'))
```

You can access any field using dot notation:

```bash
my_sample.id      // 'gut'
my_sample.fastq_1 // Path to gut_1.fq
```

This is analogous to accessing an attribute on a Python object:

```python
my_sample.id
my_sample.fastq_1
```

## Defining a Record Type

For records that you will use repeatedly — such as a sample throughout a
pipeline — you can define a named record type. This gives the record a name
that documents its structure and allows Nextflow to validate that any channel
claiming to carry that type actually contains the right fields.

```bash
record Sample {
    id: String
    fastq_1: Path
    fastq_2: Path
}
```

This definition goes at the top of your script, outside any `workflow` or
`process` block.

Once defined, you can reference the type by name anywhere a type annotation
is expected:

```bash
params {
    reads: List<Sample> = "${projectDir}/data/samplesheet.csv"
}
```

## Records in Process Inputs

When you define a typed process, you declare the input as a `record()` 
destructor. The destructor names each field and specifies its type:

```bash
process FASTQC {
    input:
    record(
        id: String,
        fastq_1: Path,
        fastq_2: Path
    )

    script:
    """
    fastqc -t $task.cpus ${fastq_1} ${fastq_2}
    """
}
```

Notice that inside the `script` block, you can refer directly to the field
names `id`, `fastq_1`, and `fastq_2` as variables. There is no indexing.

The destructor does not have to list every field present in the incoming record.
If the record also carries a `condition` field from an earlier step, the process
will still accept it — it simply ignores the fields it does not declare. This
behavior is called duck-typing and is covered in more detail below.

## Records in Process Outputs

Process outputs are defined using the `record()` constructor. Each field is
given a name and assigned a value:

```bash
process FASTQC {
    input:
    record(
        id: String,
        fastq_1: Path,
        fastq_2: Path
    )

    output:
    record(
        id: id,
        fastqc: file("fastqc_${id}_logs")
    )

    script:
    """
    fastqc -t $task.cpus ${fastq_1} ${fastq_2}
    """
}
```

Here `id: id` carries the sample identifier forward from the input into the
output record. The `file()` function captures the output directory from the
task's working directory. The resulting channel will emit records with two
fields: `id` and `fastqc`.

## Duck-Typing

Nextflow uses structural typing for records, which means that a record is
compatible with an input as long as it provides at least the fields the input
requires. It does not matter if the record has additional fields.

For example, if your pipeline has built up a record with the following fields:

```bash
record(id: 'gut', fastq_1: file('gut_1.fq'), fastq_2: file('gut_2.fq'), condition: 'treatment')
```

You can still pass this to a process that only declares:

```bash
input:
record(
    id: String,
    fastq_1: Path,
    fastq_2: Path
)
```

The `condition` field is simply not destructured. This means you can build up
richer records as your pipeline progresses — adding new fields from each process
output — without breaking any upstream process definitions.

## Merging Records

The `+` operator merges two records into a single record containing all fields
from both. This is useful when you want to annotate a sample with additional
information from a separate source:

```bash
base = record(id: 'gut', fastq_1: file('gut_1.fq'), fastq_2: file('gut_2.fq'))
extra = record(condition: 'treatment', replicate: 1)

merged = base + extra
// merged has fields: id, fastq_1, fastq_2, condition, replicate
```

If both records have a field with the same name, the right-hand record's value
takes precedence.

## Records in Workflows

Typed workflows use records in their channel annotations, which makes the
contract between a subworkflow and its caller explicit:

```bash
workflow READS_QC {
    take:
    samples_ch: Channel<Sample>

    main:
    pre_trim  = FASTQC(samples_ch)
    trimmed   = TRIM(samples_ch, params.adapters)
    post_trim = FASTQC(trimmed.map { s -> record(id: s.id, fastq_1: s.fastq_1, fastq_2: s.fastq_2) })

    emit:
    trimmed: Channel<TrimmedSample> = trimmed
}
```

The type annotation `Channel<Sample>` documents that this workflow expects a
channel of `Sample` records. If you pass in a channel of a different type, the
language server will report an error before you ever run the pipeline.

## Accessing Record Fields in Operators

When using records in operators like `map` or `flatMap`, you can access fields
by name in the closure:

```bash
samples_ch
    .map { s -> record(id: s.id, reads: [s.fastq_1, s.fastq_2]) }
    .view { s -> "Processing sample: ${s.id}" }
```

You can also destructure record fields directly in the closure parameter list:

```bash
samples_ch
    .flatMap { id, fastqc, quant -> [fastqc, quant] }
```

In this form the field names in the closure parameter list must match the field
names in the record.

## Summary

| Old pattern | Record equivalent |
|---|---|
| `tuple val(meta), path(reads)` | `record(id: String, reads: Path)` |
| `PROCESS.out[0]` / index access | `s.id`, `s.reads` / named field access |
| Must match tuple order exactly | Fields matched by name, order irrelevant |
| `emit: bam` + `.out.bam` | Output record field + standard assignment |
| Adding fields means a new tuple position | `record_a + record_b` merges fields |
