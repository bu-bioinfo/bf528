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

process ALIGN {
    label 'process_high'
    conda 'envs/star_env.yml'
    singularity 'ghcr.io/bf528/star:latest'
    publishDir params.outdir, pattern: "*.Log.final.out"

    input:
    tuple val(meta), path(reads)
    path(index)

    output:
    tuple val(meta), path("${meta}.Aligned.out.bam"), emit: bam
    tuple val(meta), path("${meta}.Log.final.out"), emit: log

    script:
    """
    STAR --runThreadN $task.cpus \
    --genomeDir $index \
    --readFilesIn $reads \
    --readFilesCommand zcat \
    --outFileNamePrefix $meta. \
    --outSAMtype BAM Unsorted
    """
}
```

For the moment, ignore what the actual commands are doing and simply focus on
the different sections of the module. 

## Shebang Line
At the top, we have a shebang line that tells the system to use the nextflow
interpreter to run the script. 

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

## publishDir

This line specifies a directory where the output of the process will be published.
We will discuss more of how Nextflow creates and manages output files. This line
will be used when we want to publish output files from various tasks. We will 
only use this when we need to easily view or gather important output files. Any
intermediate files that are not strictly necessary to view or gather will remain
in their work/ directory location.

## input

The input block specifies the inputs to the process. Usually for our workflows,
this will be a file corresponding to a sample that we are processing through a
series of steps. We will also typically include the name of the sample or status
of the sample as metadata along with the actual file. See the discussion on tuples
below for more information.

## output

The output block specifies the outputs of the process. Importantly, these outputs
must exist after the process successfully completes or nextflow will throw an error.

**N.B. If you are encountering an error where nextflow cannot find the output file, 
ensure that the commands in the script are producing the file named exactly as you
instruct nextflow to expect it in the output block.**

### val, tuple, path

These are qualifiers that specify different data types. Simply, `val` is a simple
value, `tuple` is a tuple of values, and `path` is a file path.

`val` can refer to a value of any data type. 

`path` will properly stage the file in the work directory and make it available
for use in the process. 

`tuple` is a tuple or list of values. Importantly, this is an ordered list of
values. This will allow you to group multiple values into a single definition.

For example, if we have the following process:

```bash
process ALIGN {
    input:
    tuple val(meta), path(reads)
    ...
}
```
You can see that the input is a tuple or list of two values. The first value
is a string corresponding to the metadata or sample identifier. The second value
is a path to the actual file itself. This is a common pattern we will use in 
bioinformatics workflows where we need to pass metadata that will be used to name
output files. 

On the backend, these tuples look like a list of values. For example, above, the
tuple may look something like:

```bash
["sample1", "/path/to/reads1.fastq"]
```

You may refer to individual elements in nextflow using the `$` symbol. For example:

```bash
$meta - "sample1"
$reads - "/path/to/reads1.fastq"
``` 

Keep in mind that the order matters when referring to the elements of the tuple.
Nexflow will substitute in the values passed in the input to the command upon 
execution.

So the above command at runtime would be:

```bash
STAR <other options> --readFilesIn /path/to/reads1.fastq --outFileNamePrefix sample1.
``` 

### emit

`emit` is used to name the particular outputs of a process. THis is useful for
when you need to pass the outputs of one process to different processes in the
workflow. 

For example, in the above example, we have two outputs:

```bash
output:
    tuple val(meta), path("${meta}.Aligned.out.bam"), emit: bam
    tuple val(meta), path("${meta}.Log.final.out"), emit: log
```

This means that we have two outputs, one for the BAM file and one for the log file.
We can refer to these outputs in the workflow using the `bam` and `log` names. 

If we were to look at the workflow main.nf, we would see something like this:

```bash
workflow {
    ALIGN()
    POST_ALIGN(ALIGN.out.bam)
    PARSE_LOG(ALIGN.out.log)
}
```

The `.out` is a Nextflow convention that is used to refer to the output channel
of a process. By using `emit`, we are able to pass the different outputs of the ALIGN
process to different downstream processes in the workflow. 

This also creates an implicit dependency between the processes. Nextflow will wait
for the ALIGN process to complete before running the POST_ALIGN process or the PARSE_LOG
process. 


## script

The script block specifies the commands to run for the process. This is a string
that will be executed by the process. The script string is by default executed
as a Bash script in the host environment. This may be a single or multiline string.

There are some edge cases where you will need to use either double or single quotes
depending on if you need to access system environment variables or Nextflow variables.
Please see [here](https://www.nextflow.io/docs/latest/process.html#script) for more discussion.