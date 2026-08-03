---
title: "Nextflow Modules"
layout: single
---

# Nextflow Modules

Nextflow modules are a way to specify the commands that will be run for each
task in your pipeline. In this class, when we refer to a nextflow module, we are
referring to a separate process for each of our tasks. These modules will
encompass a single analysis or processing step.

## Nextflow Module Format

```bash
#!/usr/bin/env nextflow

nextflow.preview.types = true

process ALIGN {
    label 'process_high'
    conda 'envs/star_env.yml'
    singularity 'ghcr.io/bf528/star:latest'

    input:
    record(
        id: String,
        reads: Path
    )
    index: Path

    output:
    record(
        id: id,
        bam: file("${id}.Aligned.out.bam"),
        log: file("${id}.Log.final.out")
    )

    script:
    """
    STAR --runThreadN $task.cpus \
    --genomeDir $index \
    --readFilesIn $reads \
    --readFilesCommand zcat \
    --outFileNamePrefix ${id}. \
    --outSAMtype BAM Unsorted
    """
}
```

For the moment, ignore what the actual commands are doing and simply focus on
the different sections of the module.

## Shebang Line
At the top, we have a shebang line that tells the system to use the nextflow
interpreter to run the script.

## Static Typing

The `nextflow.preview.types = true` line enables static typing for this file.
It must be present in every module that declares typed process inputs or
outputs, as we do here with `record()`. See
[Nextflow Static Typing]({{ site.baseurl }}{% link _guides/nextflow_static_typing.md %})
for the full explanation of what this flag turns on and why it exists.

## Process Name

The name of the process is specified in the process block. This is the name that
will be used to refer to the process in the workflow. Importantly, this is case
sensitive and must match the name of the process in the workflow.

If we were to call this in the main.nf, it would be ALIGN().

## label

The label is a way to assign a label to the process. For our purposes, these 
labels will let us define a particular set of computational resources to request
when submitting to the SCC. This will allow us to request different amounts of
resources for different processes without having to manually specify every time.

## conda / singularity

These lines specify either the conda environment or singularity container to use
for the process. We will be creating our own conda YML files for each tool we use
and storing them in the envs directory. In future projects, you will use pre-built
containers made for this class.

## input

The input block specifies the inputs to the process. Usually for our workflows,
this will be a file corresponding to a sample that we are processing through a
series of steps, along with metadata such as the sample identifier. With static
typing, related values like these are grouped into a `record()`, and any
additional standalone inputs are declared below it with a `name: Type`
annotation. See the discussion of records below for more detail.

## output

The output block specifies the outputs of the process. Importantly, these outputs
must exist after the process successfully completes or nextflow will throw an error.

**N.B. If you are encountering an error where nextflow cannot find the output file, 
ensure that the commands in the script are producing the file named exactly as you
instruct nextflow to expect it in the output block.**

### record

A `record` groups related values together under named fields. It replaces the
older `tuple val(meta), path(reads)` pattern you may see in legacy pipelines.
Fields are matched by name rather than by position, so there is no risk of
values being assigned to the wrong variable if a channel's element order ever
changes.

In the process above, the input is a `record` with two fields: `id`, a
`String` identifying the sample, and `reads`, a `Path` to the FASTQ file. A
third input, `index`, is declared separately since it isn't part of that
per-sample record — it's a single path shared across every invocation of the
process.

```bash
input:
record(
    id: String,
    reads: Path
)
index: Path
```

Inside the process, you refer to a record's fields directly by name — there is
no positional indexing:

```bash
$id    // the sample identifier
$reads // the path to the FASTQ file
```

So the STAR command at runtime for a sample named `sample1` would look like:

```bash
STAR <other options> --readFilesIn /path/to/reads1.fastq --outFileNamePrefix sample1.
```

For the full discussion of defining named record types, duck-typing, and
merging records, see
[Nextflow Records]({{ site.baseurl }}{% link _guides/nextflow_records.md %}).

### Named Outputs

Outputs are also constructed as a `record`, with each field given a name and a
value:

```bash
output:
record(
    id: id,
    bam: file("${id}.Aligned.out.bam"),
    log: file("${id}.Log.final.out")
)
```

Here `id: id` carries the sample identifier forward from the input into the
output record, and `bam` and `log` are the two files this process produces.

If we were to look at the workflow main.nf, we would see something like this:

```bash
workflow {
    align_out = ALIGN(sample_ch, index)
    POST_ALIGN(align_out.bam)
    PARSE_LOG(align_out.log)
}
```

Each output is accessed as a named field on the value returned by the process
call — there is no `.out` property or `emit:` needed at the process level.
This also creates an implicit dependency between the processes: Nextflow will
wait for the ALIGN process to complete before running POST_ALIGN or PARSE_LOG,
since both depend on values produced by ALIGN.

## script

The script block specifies the commands to run for the process. This is a string
that will be executed by the process. The script string is by default executed
as a Bash script in the host environment. This may be a single or multiline string.

There are some edge cases where you will need to use either double or single quotes
depending on if you need to access system environment variables or Nextflow variables.
Please see [here](https://www.nextflow.io/docs/latest/process.html#script) for more discussion.
