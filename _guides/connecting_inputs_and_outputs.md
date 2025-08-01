---
title: "Connecting Inputs and Outputs"
layout: single
---

# Inputs and outputs

The key to connecting nextflow processes is to understand the cardinality and
order of the inputs and outputs of each process. 

Let's assume that we have the following processes (we will only focus on the
input and output declarations for now):

```bash
process SORT {
    ...
    output:
    tuple val(meta), path("*sorted.bam"), emit: sorted
    ...
}
```

```bash
process INDEX {
    ...
    input:
    tuple val(meta), path(sorted_bam)

    output:
    tuple val(meta), path("*sorted.bam"), path("*sorted.bam.bai"), emit:bai
    ... 
}
```

Remember that the name within the input declaration is simply a placeholder and
will be used to refer to the input within the process. We can refer to the values
associated with those variables using the `$` symbol in the nextflow process.

The val(meta) in the output declaration was not created but is the same value
passed through the input.

Keep in mind that nextflow checks whether a specific file is produced in the
output, so when we refer to path("*sorted.bam"), it is directly checking for
files to be created ending in `sorted.bam` and `sorted.bam.bai` when the process
completes.

## Connecting processes

Assume that the INDEX process depends on the SORT process and we wish to pass
the outputs of the SORT process to the INDEX process.

Notice how the **output** of SORT is a tuple containing the sample name and the sorted
bam file. The first position in the tuple is the sample name and the second position
is the sorted bam file. 

Notice how the **input** of INDEX is a tuple containing the sample name and the sorted
bam file. The first position in the tuple is the sample name and the second position
is the sorted bam file. 

In this case, we intentionally structured the input and output of the processes to
match each other. This means we can directly pass the output of SORT, which is a
tuple, to the input of INDEX.

```bash
include { SORT } from './modules/sort.nf'
include { INDEX } from './modules/index.nf'

workflow {
    SORT(fake_ch)
    INDEX(SORT.out.sorted)
}
```

We have also intentionally structured the output of INDEX to match the input of
the next process. We defined these outputs and inputs based on what files and
variables we knew each process would need to run and would produce. 

The output of INDEX is a tuple that looks like the following:

```bash
[meta, sorted.bam, sorted.bam.bai]
```

If we were to pass this to another process, we would need to ensure that the input
of the next process expects a tuple with this structure.

```bash
input:
tuple val(meta), path(sorted_bam), path(sorted_bai)
```

## Common Issues

The order specified in the input is how you refer to each element of the tuple. If
you pass a tuple as input with a different order, your variables will be mismatched.
For example, if the input of the process looks like:

```bash
input:
tuple val(meta), path(sorted_bam), path(sorted_bai)
```

And your input channel looks like:

```bash
[sorted.bam, sorted.bam.bai, meta]
```

When you refer to `$meta`, `$sorted_bam`, and `$sorted_bai`, nextflow will substitute
in `sorted.bam` for `$meta`, `sorted.bam.bai` for `$sorted_bam`, and `meta` for `$sorted_bai`.
This will likely cause an error in your downstream process. 