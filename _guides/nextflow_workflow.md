---
title: "Nextflow Workflow"
layout: single
---

# Nextflow Workflow

The actual nextflow workflow will be located in the `main.nf` file. This file will
contain the logic for running the pipeline. By our convention, this file will be
at the top level of the project directory. You may technically name this file
whatever you like, but we will refer to it as `main.nf` in this guide. 

## Nextflow Workflow Format

```bash
#!/usr/bin/env nextflow

include { ALIGN } from './modules/align.nf'
include { POST_ALIGN } from './modules/post_align.nf'
include { PARSE_LOG } from './modules/parse_log.nf'

workflow {

    Channel.fromPath(params.reads) 
    | splitCsv(header: true)
    | map { it -> tuple(it.sample, it.fastq) }    
    | set { sample_ch }

    ALIGN(sample_ch)
    POST_ALIGN(ALIGN.out.bam)
    PARSE_LOG(ALIGN.out.log)
}
```

## include

The `include` statement is used to import a module into the workflow. This will
allow us to pass the various files we want processed to these modules performing
separate tasks. You must refer to the process by the name you give it in the
include statement and this name must match what is used in the module file.

## Workflow logic

In the actual workflow section, you will define channels containing the information
you want processed. You will then pass these channels to the processes you want to
run. 

For example, in the above workflow, we define a channel containing the reads we want
processed and pass it to the align process. We then pass the output of the align
process to the post_align process and finally pass the output of the post_align
process to the parse_log process. 

Lines 24-27 define a channel that contains information stored in a CSV file. The
`Channel.fromPath` function is used to create a channel from a file path. The
`splitCsv` function is used to split the CSV file into rows. The `map` function is
used to transform the rows into a channel containing tuples. The `set` function is
used to store the channel in a variable.

Although that sounds complicated, you can think of a channel as a list containing
the information you want processed and passed to your workflow. In our situation,
this is a sample name and a file corresponding to that sample. We will often
create channels from CSV files, but we can also create channels in other ways. 
The advantage of creating from a CSV file is that it can be easily modified and
improves the readability of your workflow by making it clear what files are being
processed.

## Dependencies

Central to the idea of workflow management tools is the idea of dependencies. A 
dependency in a workflow is a process that must be run before another process can
be run. Oftentimes, this will be a file that must be created before another file
can be created. In bioinformatics, we are typically transforming the original 
data files into a different format through our analyses. For example, when we
align sequencing reads from a FASTQ file to a reference genome, we create a BAM
file containing the alignments. We cannot create a BAM file without first aligning
the reads and processing the FASTQ file. 

## Pleasingly parallel

Oftentimes, our problems in bioinformatics are known as "pleasingly parallel" or
more pessimistically, "embarrassingly parallel." This means that we can solve 
our problem by splitting our tasks into independent parts that can be run
at the same time. For example, when we align sequencing reads to a reference
genome, we can align the reads from each sample to the genome at the same time.
This is because the alignment of the reads from one sample does not depend on
the alignment of the reads from another sample. 

Nextflow and other workflow management tools when used in conjunction with a
high performance computing (HPC) cluster can take advantage of this parallelism
by running multiple processes at the same time, which can drastically increase
the runtime of our analyses (though not always in a perfectly linear fashion).

Nextflow will implicitly parallelize our workflow. When input channels with multiple
elements are provided to processes, it will automatically spawn separate process
instances for each element in the channel. 