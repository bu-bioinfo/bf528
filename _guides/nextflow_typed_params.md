---
title: "Nextflow Typed Parameters"
layout: single
---

# Typed Parameters

Nextflow pipelines need a way to accept inputs from the person running them —
things like the path to a samplesheet, a reference genome, or an output
directory. These are pipeline parameters.

Typed parameters let you declare exactly what type each parameter should be,
provide sensible defaults, and have Nextflow automatically load and validate
structured input files like CSV samplesheets. This replaces the older approach
of writing `params.reads = "..."` at the top of `main.nf` and then
constructing channels by hand using `splitCsv` and `map`.

## The `params {}` Block

Instead of assigning parameters one at a time with `params.foo = value`, you
declare them together in a `params {}` block:

```bash
params {
    // The input samplesheet
    reads: List<Sample> = "${projectDir}/data/samplesheet.csv"

    // The reference genome
    genome: Path = "${projectDir}/data/genome.fa"

    // Where to write results
    outdir: Path = 'results'
}
```

Each line has the form `name: Type = default_value`. The type annotation tells
Nextflow what kind of value to expect. The default value is used when the
parameter is not provided on the command line.

The `params {}` block goes at the top of your `main.nf`, outside any `workflow`
block. Unlike the older `params.foo = ...` syntax, you do not need
`nextflow.preview.types = true` to use it — the typed `params {}` block has
been available since Nextflow 25.10.

## Basic Types

The types you will use most often for individual parameters are:

| Type | What it represents |
|---|---|
| `String` | A text value |
| `Path` | A file or directory path |
| `Integer` | A whole number |
| `Boolean` | `true` or `false` |

For example:

```bash
params {
    genome: Path = "${projectDir}/data/genome.fa"
    min_mapq: Integer = 20
    save_intermediates: Boolean = false
    outdir: Path = 'results'
}
```

## Required Parameters

A parameter that has no default value is required. If a user runs the pipeline
without providing it, Nextflow will fail immediately with a clear error
message instead of running partway through and failing when the missing value
is first used.

```bash
params {
    // No default — must be provided at runtime
    reads: List<Sample>

    // Has a default — optional
    outdir: Path = 'results'
}
```

**N.B.** `Boolean` parameters with no default value will default to `false`
rather than being treated as required. This matches common command-line
convention where a flag is either present (true) or absent (false).

## Collection Parameters and Samplesheets

The most powerful feature of typed parameters is automatic samplesheet loading.
When a parameter has a collection type — `List<T>`, `Set<T>`, or `Bag<T>` —
and you supply a file path rather than a literal list, Nextflow will
automatically read and parse the file into a collection of the specified type.

This means the pattern of reading a CSV file with `splitCsv` and building
tuples with `map` can be replaced by a single parameter declaration.

### Defining a Record Type for Your Samples

First, define a record type that matches the columns in your samplesheet:

```bash
record Sample {
    id: String
    fastq_1: Path
    fastq_2: Path
}
```

The field names must match the column headers in the CSV file exactly. The
field types tell Nextflow how to convert the raw string values from the CSV
into the appropriate Nextflow types (`Path` values will be resolved relative
to the location of the samplesheet).

### Declaring the Parameter

```bash
params {
    reads: List<Sample> = "${projectDir}/data/samplesheet.csv"
}
```

### The Samplesheet

The CSV file must have a header row with column names that match the record
field names:

```bash
id,fastq_1,fastq_2
gut,/path/to/gut_1.fq,/path/to/gut_2.fq
liver,/path/to/liver_1.fq,/path/to/liver_2.fq
lung,/path/to/lung_1.fq,/path/to/lung_2.fq
```

**N.B.** The column separator must be a comma. Nextflow does not support
tab-separated files for this feature.

### Loading the Collection into a Channel

Once the parameter is declared, creating a channel from it is straightforward:

```bash
workflow {
    read_pairs_ch = channel.fromList(params.reads)

    RNASEQ(read_pairs_ch, params.genome)
}
```

`channel.fromList` emits each record in the list as a separate channel value.
The resulting channel has type `Channel<Sample>`, which means the type checker
can verify that it is compatible with any process or workflow that expects
`Sample` records.

Compare this to the older approach, which required several chained operations
and produced a channel with no type information:

```bash
// Old approach — no type information, hard to validate
Channel.fromPath(params.reads)
    | splitCsv(header: true)
    | map { row -> tuple(row.id, file(row.fastq_1), file(row.fastq_2)) }
    | set { read_pairs_ch }
```

## JSON and YAML Samplesheets

CSV is not the only supported format. Collection-type parameters can also be
loaded from JSON or YAML files. Nextflow will infer the format from the file
extension.

A JSON samplesheet equivalent to the CSV above would look like this:

```json
[
  { "id": "gut",   "fastq_1": "/path/to/gut_1.fq",   "fastq_2": "/path/to/gut_2.fq"   },
  { "id": "liver", "fastq_1": "/path/to/liver_1.fq", "fastq_2": "/path/to/liver_2.fq" }
]
```

The same `List<Sample>` parameter type handles all three formats. The format
is determined at runtime by the file extension of the value passed to the
parameter.

## Overriding Parameters at Runtime

Typed parameters behave the same as legacy parameters for the purposes of
overriding. You can supply a new value on the command line:

```bash
nextflow run main.nf --reads /path/to/my_samplesheet.csv --outdir /scratch/results
```

You can also supply parameter values in a params file using the `-params-file`
flag:

```bash
nextflow run main.nf -params-file my_params.json
```

Where `my_params.json` might look like:

```json
{
  "reads": "/path/to/my_samplesheet.csv",
  "outdir": "/scratch/results"
}
```

Values provided on the command line take precedence over the defaults in the
`params {}` block. This resolution order is the same as it has always been in
Nextflow.

## Parameters in Config vs. Script

Typed parameters should be declared in the script (in `main.nf`) when they
represent inputs that vary between runs — sample files, output paths, algorithm
settings. Parameters that are fixed infrastructure concerns, like the path to a
shared reference database on the SCC, belong in `nextflow.config` rather than
the script.

As a rule of thumb: if a student running the pipeline would reasonably want to
change the value, put it in the `params {}` block. If it is a detail about how
the pipeline runs on this particular cluster, put it in the config.
