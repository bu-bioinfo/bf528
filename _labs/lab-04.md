---
title: "Lab 4 - Nextflow Practice"
layout: single
---

Today we are going to get practice with channel manipulation and some useful 
nextflow operators. You will be given a series of tasks that represent common
patterns in bioinformatics workflows. 

# Objectives
- Gain proficiency with channel manipulation and nextflow operators
- Develop familiarity with common patterns in bioinformatics workflows

# Nextflow Resources

1. The guides provided in the `guides/` directory to help you with
the exercises. 
2. LLMs, stackoverflow, biostars, google, etc.
3. [Official Nextflow documentation](https://www.nextflow.io/docs/latest/)
4. Your classmates

# Common nextflow operators

There are a lot of operators and functions provided by Nextflow. In order to make
this assignment simpler, I will list out the most commonly used operators and
functions you will need to complete the exercises. 

- `Channel.fromPath`
- `Channel.fromFilePairs`
- `collect`
- `map`
- `join`
- `transpose`
- `combine`
- `branch`

# Changing how we specify computational environments

Up until this point, we have been using Conda to manage our computational environments.
but Nextflow supports a number of other alternatives. While Conda solves a number of
our problems when thinking about computational environment management, it does
have a number of limitations compared to other alternatives, namely containers.

We will discuss containers, Docker, and singularity in more detail in the future.
From now on, we will be using containers to manage our computational environments.

To do so, you will need to remember three things:

1. Change the `conda` line in the process to `container`
2. Instead of a path to a YML file, we will be using a URL to a container image
3. Instead of `-profile conda`, we will be using `-profile singularity`

# Singularity Images for this lab

- FASTQC:  ghcr.io/bf528/fastqc:latest
- MultiQC: ghcr.io/bf528/multiqc:latest
- Trimmomatic: ghcr.io/bf528/trimmomatic:latest

# How to work on these exercises

New command to run nextflow locally with singularity:
```bash
nextflow run <nf_file>.nf -profile singularity,local
```

or to submit the jobs to the cluster with singularity:

```bash
nextflow run <nf_file>.nf -profile singularity,cluster
```

In each directory, I have given you both a `test.nf` and a `main.nf` file. The
`test.nf` file is a simple example of how to use the nextflow operators and
functions. The `main.nf` file is the main pipeline that you will be working on.

Use the `test.nf` file to test your code and make sure you are creating the 
correct channels. Once you are confident that your code is working, you can copy
the code and logic from `test.nf` into `main.nf`.

Remember you can view the contents of any channel or process output by using
the `view` operator. Test out the different operators in the `test.nf` file. 

Remember that PROCESS outputs are also channels and you can manipulate them using
operators and save the new outputs to a new channel. 

# Creating a channel with files in two ways - Exercise 1

To create a channel from a CSV, we can use a combination of nextflow operators
and channel functions.

Navigate to the exercise_1/ directory and try to create a channel from the
CSV file provided to you in the nextflow.config. The CSV file contains the path
to a list of paired end FASTQ files for RNAseq data and the sample name.

You can use a combination of Channel.fromPath, `splitCsv`, `map`, and `tuple` to
create the channel. Recall that `map` is simply an operator that applies a function to 
each item in the channel. This function is meant to be flexible and can be any
function you want to apply to each item in the channel. 

Create a channel where each element is a tuple containing the sample name, and a
tuple of the paths to the R1 and R2 files. 

This will look something like:

```bash
[<sample_name>, [<path_to_R1>, <path_to_R2>]]
```

`test.nf`
- [ ] Make a channel that contains a tuple of the sample name, and a tuple of
the paths to the R1 and R2 files using `Channel.fromPath`, `splitCsv`, `map`, and `tuple`

`main.nf`
- [ ] Use the `Channel.fromFilePairs` function to create the same channel as above
from the path provided to you in the nextflow.config. Refer to the documentation [here](https://nextflow.io/docs/latest/reference/channel.html#fromfilepairs) for more information.
- [ ] Use the FASTQC module and run it on the channel created in the previous step.

# Manipulating channels - Exercise 2

If you look at the channel you created using `Channel.fromFilePairs`, you'll notice
that it creates a tuple within a tuple. If you look at the module for FASTQC that
I've provided you, you'll see that it runs FASTQC on the R1 and R2 files
at the same time. The command you can see is:

```bash
fastqc $reads[0] $reads[1]
```

This is because the input to the module is a tuple of the paths to the R1 and R2
files. You can individually access the elements of the tuple by their position
similar to how you would access elements of a list in python. 

While this would work, it will also have the effect of running FASTQC twice in 
the same process, which is not the most efficient way to do this. Instead, we want
to transform the channel created via `Channel.fromFilePairs` into a channel that
emits each read file separately. We also want to adjust our FASTQC module to only
process a single file. 

`test.nf`
- [ ] Find an appropriate nextflow operator that will transform the channel created
via `Channel.fromFilePairs` into a channel that emits each read file separately.
This operator should flatten any nested tuples and emit each nested item separately.

```bash
[P0rep1subsample, <path_to_R1>]
[P0rep1subsample, <path_to_R2>]
...
```
**INSTEAD OF**

```bash
[P0rep1subsample, [<path_to_R1>, <path_to_R2>]]
...
```

`test.nf`
- [ ] Find an appropriate operator to transform the channel created via 
`Channel.fromFilePairs` into a channel that emits each read file separately.

`main.nf`
- [ ] Use the code from the `test.nf` once successfully finished and run it on
the channel containing the R1 and R2 files. Use your new module to run FASTQC on
each read file separately.

`nextflow.config`
- [ ] Edit the `nextflow.config` and adjust how many jobs are submitted simultaneously.
- [ ] Run the `main.nf` file with the `-profile singularity,cluster` option and 
watch the output. 

# Using nextflow operators to group together the outputs of a channel - Exercise 3

You may have noticed that when you have printed out channels, it prints out 
each element on a new line. This would indicate that each element would be emitted
one at a time. This would be useful if we wanted to then send each new output
file to a different process. However, oftentimes we want to group together the 
outputs of a channel into a single element and process them all together, typically
for tasks that require all of the sample files to analyze. 

*Hypothetical Situation*: We are running a process that will generate a single
output file for each input file. We want to create a channel that contains a
list of all the output files that will be generated. Oftentimes, this is useful
when we need a process to operate on all output files generated by another
process. 

*Specific Situation*: We have a list of FASTQC Quality Control reports for a
number of samples. We want to create a channel that contains all of them so that
we can run MultiQC on them. MultiQC is a tool that will concatenate and summarize
the results of multiple quality control tools into a single report. In this case,
we want to gather all of the FASTQC files into the same channel so that MultiQC
has access to all of them.

I have given you a working nextflow pipeline that will run FASTQC on the list
of samples we created channels for previously. Run the `main.nf` and view the
output. 

`test.nf`
- [ ] Find an appropriate nextflow operator that will group all of the outputs
from a channel into a single element

`modules/`
- [ ] Make a module that runs MultiQC on the channel created in the previous step

`main.nf`
- [ ] Use the code from the `test.nf` once successfully finished and run your
module for MULTIQC. If successful, MULTIQC should run only once and generate a
single output file for all of the FASTQC files.
- [ ] When you've confirmed that it works successfully, switch the input to the
`Channel.fromFilePairs` function and run it on the full samples. You may find the
path to the full files in the nextflow.config.

**Hints**

- The MultiQC documentation can be found here: https://github.com/MultiQC/MultiQC
Please pay attention to the default running command as well as the files created.
The documentation will be helpful in understanding how to run the module.

- The input to your module can be: `path("*")`. What is this input indicating?

---
# Discussion of sequencing read QC using reports from a real dataset

Please look in the provided_results/ directory of exercise_3 and find the MultiQC
report called 'full_report.html'. We'll open it together and discuss what we see,
how we determine if something is concerning and how we might address any issues we
find. You can also look at the report you generated in exercise_3.

We will also work on a hypothetical question I will pose to you in class. 
---

# Make a channel that is the cross product of two other channels - Exercise 4

*Hypothetical Situation*: Oftentimes in bioinformatics, we are not sure what
value to use for a certain parameter. We may have a list of values we want to try
and we want to run the same process multiple times with each value. Workflow
management tools make it trivial to test any number of different combinations of
parameter values. 

*Specific Situation*: We are trying to decide on an optimal value of kmer when
attempting to perform *de novo* assembly of a genome. We want to try a range
of values and see which performs the best.

Given the channels created for you in the exercise_4.nf, use various nextflow
operators to create a new channel that contains all possible combinations of
the values in the two channels. 

`test.nf`
- [ ] Use an appropriate operator to create a new channel that contains all possible
combinations of the values in the two channels.

`nextflow.config`
- [ ] Edit the `nextflow.config` and adjust how many jobs are submitted simultaneously
to an appropriate amount.

`main.nf`
- [ ] Use the code from the `test.nf` once successfully finished and use the 
provided JELLYFISH module to run JELLYFISH on the channel you created. Make sure
you run this using the `-profile singularity,cluster` option.

# Combining multiple operators to create a channel - Exercise 5

*Background*: We will talk more in-detail about this when we get to RNAseq
analysis but the general output is typically a counts matrix representing the
number of reads that mapped to each gene or transcript in a sample. These counts
are then used to perform downstream analysis such as differential expression
analysis. These counts are generated by using the alignments, which encode the
position of where the reads map to the reference genome, and a GTF file
which stores the position of where the genes or transcripts are located in that
same reference. We can then "count" the number of reads that map to each gene or
transcript.

For this exercise, you will be using BAM files and a GTF file to generate a count
for every gene in that sample. We will be using VERSE to perform this task. Once
we count per sample, we will group all of the counts together so that we can run
a separate script that will combine them into a single file.

*Hypothetical Situation*: We are trying to group all of the output files from
a particular process whose output consists of a tuple and a file. We want to
only group the files and not the tuple.

*Specific Situation*: We have generated counts from BAM files for a number of 
samples and want to group them all together so that we can run a separate script
that will combine them into a single file.

`test.nf`
- [ ] Use a combination of operators to access the value of the tuple containing
the file, and group the files into a single channel

`bin/`
- [ ] Make the script executable using `chmod +x bin/concat_df.py`

`main.nf`
- [ ] Use the code from the `test.nf` once successfully finished and run the 
provided process, VERSE, on each of the BAM files and then run the 
provided script, CONCAT, to combine the counts into a single file.

# Extra 1 - Group two lists of files into a single channel

*Hypothetical Situation*: We want to aggregate all of the outputs from two 
separate processes into a single list of files.

*Specific Situation*: We want to collect the logs from both FASTQC and Trimmomatic
into one list so that we can run MultiQC on them.

`test.nf`
- [ ] Use an appropriate operator to aggregate the logs from both FASTQC and Trimmomatic
into one list.

`main.nf`
- [ ] Use the code from the `test.nf` once successfully finished and run the 
provided process, MULTIQC, on the list of logs.

# Extra 2 - Grouping channels based on the sample name

*Hypothetical Situation*: We have run two separate processes on each of our samples.
We need to join their output channels so that each sample has both of the output
files generated by the two processes. 

*Specific Situation*: We have created a FASTA index of a particular genome and
we wish to provide a region of interest to extract from the sequence. We will
need to group the channels based on the sample name so that we can extract the
region of interest from the sequence.

`test.nf`
- [ ] Use an appropriate operator to group the channels based on the sample name.
The resulting tuple should be a tuple with the sample name, .fa file, .fa.fai file,
and the region of interest file.

# Extra 3 - Filtering channels based on a value

*Hypothetical Situation*: We have run a process and wish to send the outputs
of the process to different processes based on the value of a tuple.

*Specific Situation*: We are analyzing an experiment with two conditions, WT and
KO. We want to send the outputs of the process to different processes based
on the condition.

This extra example will only have the test.nf. I have made a channel for you
that consists of 4 elements; each a tuple of a condition name and a file. 

`test.nf`
- [ ] Use an appropriate operator to make a new channel with just the files from 
the condition `WT`. The resulting channel should emit only the elements with `WT`
as their condition.
