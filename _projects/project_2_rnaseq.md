---
title: "Project 2: RNAseq"
layout: single
---

I have broken up the project into week-by-week sections. However, these sections
are guidelines and not a strict timeline. Your report and project will be due
only at the day specified on the schedule. These sections are designed to 
fit a manageable number of tasks into each week and give you a rough timeline.
I have given you a .Rmd file that you will periodically write sections of text in
as well as the place where you will perform the later steps of differential expression
and analysis.

# Before you begin

## Important note about the structure of this project

I have given you real data from a published paper but only limited information
about the experiment: the sample metadata and the comparison being tested
(control vs. experimental). For the first part of this project, you will build
your pipeline and analyze the data without knowing which study it comes from.
At the end of Week 2, I will post the original publication on Blackboard, and 
you will compare your results and interpretations with the authors'.

This is meant to let you explore the data and form your own conclusions before
seeing what the authors chose to highlight. Please read the Project 2 Report
Guidelines for a full description of what is expected in each phase.

## Changes to our environment management strategy and workflow

As we've discussed, conda environments are one solution to ensuring that your
analyses are run in a reproducible and portable manner. Containers are an
alternative technology that have a number of advantages over conda environments.
Going forward, we will be incorporating containers specifying our computational
environments into our pipeline.

One of the advantages of container technologies is that they usually offer a
robust ecosystem of shared containers (images) that are available in public
repositories for anyone to reuse. We have developed a set of containers for each
piece of software that we will be using in this course.

For all future process scripts that you develop in nextflow, instead of 
specifying the `conda` environment to execute the task with, you will instead
specify `container` and the image (a container built with a certain specification)
location. For example:

```
process FASTQC {
  container 'ghcr.io/bu-cds-bf528/fastqc:latest'
  ...

}
```

For this course, these containers were all pre-built and their specifications kept
in this public github repository: https://github.com/bu-cds-bf528/pipeline_containers.
Feel free to look into the repo for how the containers were built. We follow a
similar pattern where we specify the exact environment we would like created in
a YAML file and then generate the environment using micromamba installed in a
container. We will get some experience later in the semester with building your
own containers from scratch.

In general, the containers will be named following the same pattern:
`ghcr.io/bu-cds-bf528/<name-of-tool>:latest` (e.g. `ghcr.io/bu-cds-bf528/fastqc:latest`).

## Docker images for your pipeline

FastQC: `ghcr.io/bu-cds-bf528/fastqc:latest`

MultiQC: `ghcr.io/bu-cds-bf528/multiqc:latest`

VERSE: `ghcr.io/bu-cds-bf528/verse:latest`

STAR: `ghcr.io/bu-cds-bf528/star:latest`

Pandas: `ghcr.io/bu-cds-bf528/pandas:latest`

Biopython: `ghcr.io/bu-cds-bf528/biopython:latest`

# Week 1: RNAseq

## Workflow visualization

![workflow]({{ site.baseurl }}/assets/images/project-2-workflow-diagram.svg)

## Overview

A basic RNAseq analysis consists of sample quality control, alignment,
quantification and differential expression analysis. This week, we will be
performing quality control analysis on the sequencing reads, generating a genome
index for alignment, and making a mapping of human ensembl IDs to gene names.

## Objectives

- Perform basic quality control by running FASTQC on the sequencing reads

- Generate a delimited file containing the mapping of human ensembl ids to gene
  names

- Use STAR to create a genome index for the human reference genome

- Align your sequencing reads to the human reference genome using STAR

- Use MultiQC to generate a single report containing the quality metrics for
the sequencing reads and alignments

- Generate gene-level counts using VERSE for each of the samples

- Concatenate gene-level counts from each sample into a single counts matrix

## Creating a working directory for Project 2

Accept the github classroom link and clone the assignment to your student
directory in /projectnb/bf528/students/*your_username*/. This link will be
posted on the blackboard site for our class.

## nextflow.config - Locating the necessary paths and files

Please look in your nextflow.config for various variables that I have given you
that you will need to use in your pipeline. I have provided you the path to the
files as well as the reference genome and matching GTF. You can access these
values by `params.variable_name_in_config`.

## specifications.md - Filling out the specifications document

Before you start working on the pipeline, fill out the sections in the provided
`specifications.md`. This is meant to give you practice thinking at a high-level
about what your pipeline is doing, how it is behaving, and which points are critical
for you to review or validate. This will become especially important to keep in
mind once you start using agentic coding harnesses to develop workflows. 

I have filled out the validation table partially with the steps and I ask that you
simply provide how you will validate each step and be confident in what was produced.
It is fine to go back and edit this if anything changes as you develop your workflow. 

## rnaseq-report.Rmd - Writing the initial experimental design and methods

1. Fill in the section for Experimental Design in the provided .Rmd. You may find
the guidelines for doing so here: [Experimental Design]({{ site.baseurl }}/projects/project_2_report#experimental-design-1-paragraph)

2. Please write a methods section for your workflow in this same .Rmd. You will
need to come back to this section after you make certain choices in your method
of filtering your counts and differential expression analysis, but write the methods
now for just the pipeline. You may find the guidelines for the methods section here:
[Methods Section]({{ site.baseurl }}/projects/project_2_report/#methods-as-long-as-needed)

## General guidance for developing your workflow

### Running with `-stub` during development

As you develop your workflow, you should always include a `stub` block, described
more below. This also means that until you are 100% confident your workflow
performs as expected, you should always run it with:

```bash
nextflow run main.nf -stub
```

This is really important for this project since the real data is quite large
and you will only run it with the real data once you are sure that your pipeline
has the desired behavior. 

### Assigning process labels to your modules

Please refer to the following page for [common combinations](https://www.bu.edu/tech/support/research/system-usage/running-jobs/batch-script-examples/#MEMORY)
of options to request specific amounts of resources from nodes on the SCC. 

I have provided you with a variety of pre-set labels, choose the ones you think
are appropriate for each task based on their complexity. You can use the provided
nextflow report as a baseline for what might be appropriate. 

## main.nf (top-level) - Generating our input channels

In your `main.nf` at the top-level of the directory, make two initial channels
that will serve as the starting point for your workflow and save them to 
appropriately named variables in the `workflow` block.

1. A channel of records that reads each element from the `samplesheet.csv`
and maintains the `name`, `R1`, and `R2` fields. The number of elements should
match the number of samples.

2. A channel of records that has "exploded" out the `R1` and `R2` fields. This
channel of records should contain N * 2 records, one per each fastq and sample.
This record should have fields `name` and `fastq`.

## modules/fastqc/main.nf - Performing quality control

Look for the partially filled in module, `modules/fastqc/main.nf`. This is the
only one I will provide. 

### Construct the input and output records

1. Declare a record at the top that matches the channel you constructed previously
containing fields `name` and `fastq`.

2. Declare a record at the top that matches the output of FastQC:
  - FastQC automatically creates two files

### Additional labels and directives

1. Add a label that indicates how many computational resources to use for this
process.

2. Add a `container` directive that specifies to nextflow what environment to run
this process in.

### Input block

1. Specify the record you declared at the top as your `input` and provide it a
local variable name.

### Output block

In general, you will always have to know what files are created by the tool you
are using. Some tools automatically create files with certain pre-set naming 
patterns, other tools will stream the results to stdout and expect you to create
a file. 

For FastQC, it is not well-documented what is produced so I will tell you upfront.
FastQC creates two output files based on a FASTQ passed to it with the following
patterns: "<fastq_filename_without_file_extension>_fastqc.html" and 
"<fastq_filename_without_file_extension>_fastqc.zip". 

1. Specify the output using the record you declared at the top holding two files,
the .zip and the .html. Remember that you need to declare in the output the
exact files Nextflow should expect. You can make use of the "`*`" to capture any
files ending in the patterns you want (e.g. "`*.zip`" or "`*.html`")

### Script block

For all processes, you will need to look at the tools original documentation or
help information in order to figure out the command to run it. Since the documentation
for FastQC is well-hidden, I will give you the general shape of the command below:

```bash
fastqc <fastq-file>
```

### Stub block

For every process, you will fill out a stub block that uses the `name` in the 
record field and the command `touch` to generate fake files that you can use
to troubleshoot your workflow as you develop it. 

Use the `name` value from your input record to name the fake files so they
match the filenames your output block expects. For example, if your output
expects `${name}.txt`, your stub block would be:

```bash
touch ${name}.txt
```

For our records if you had a process that looked like this:

```bash
record FastqRec {
    name: String
    fastq: Path

}

process FASTQC {
    label 'process_low'
    container 'ghcr.io/bf528/fastqc:latest'

    input:
    reads: FastqRec

    output:
    record(zip: file("*.zip"), html: file("*.html"))

    script:
    """
    fastqc -t $task.cpus $reads.fastq
    """

    stub:
    """
    touch ${reads.fastq.simpleName}.html
    touch ${reads.fastq.simpleName}.zip
    """
}

# You can see that we have referred to a local variable, `reads`, in the input which
# holds the FastqRec record. From that, ${reads.fastq} will print out the string 
# corresponding to the filename.

# .simpleName is a function that returns the filename without the extension so
# ${reads.fastq.simpleName} will take the string `control_rep1_R1.fastq.gz`
# and produce the string `control_rep1_R1`

# You will need to use this in other stub runs to use the actual name in the fake file
# created by the stub block. 

```

**N.B.** For FastQC specifically, the R1 and R2 records for a sample share the
same `name`. If you name your fake files using only `name`, the R1 and R2 outputs
will have identical filenames and one will overwrite the other when they are
published to the same directory. Instead, name the fake files after the FASTQ
file itself, just like FastQC does. `simpleName` strips everything after the
first `.` in a filename (e.g. `sample1_R1.fastq.gz` becomes `sample1_R1`):

```bash
touch ${<your_record>.fastq.simpleName}_fastqc.html
touch ${<your_record>.fastq.simpleName}_fastqc.zip
```

### In your main.nf

1. Call this module in your workflow on the channel of `name` and `fastq` records
you constructed previously.

## bin/parse_gtf.py - Creating a map between gene identifiers and gene symbols

As we've discussed, it's often more intuitive for us to use gene names rather than
their IDs. You are likely familiar with seeing genes referenced by their names
in the literature, such as BRCA1 or TP53. However, there are many different identifier
systems used to label genes, including ensembl gene ids, which are a common and
principled way of labeling and identifying genes. These gene IDS tend to be more
stable and consistent across references to the organism and are more standardized. 
Our genes will originally be in the ensembl gene id format, and we will need to 
convert them to gene names for downstream analysis. 

It is often better to extract this information from the GTF file associated
with the exact version of the reference genome we are using. This will ensure
that our labels are as internally consistent as possible. 

Whenever we need to perform operations using custom code, we are going to use
the conventions established in project 1. We will place this script in the `bin/`
directory and make it executable. We will then create a nextflow module that will
provide the appropriate command line arguments to the script.

1. Generate a python script `bin/parse_gtf.py` that parses the GTF file you were
provided and creates a delimited file containing the ensembl human ID and its 
corresponding gene name. Please copy and modify the `argparse` code used in 
previous scripts to allow the specification of command line arguments. The
script should take a single file input (GTF) and output a single text file.

## modules/parse_gtf/main.nf - Running the parse_gtf script

### Construct the input and output records

The input will be a single path to the GTF file.

The output will be a single path to the delimited text file your script creates.

### Additional labels and directives

Ensure it will run in an appropriate environment and specify what label to use
for computational resources. You may use the biopython
(`ghcr.io/bu-cds-bf528/biopython:latest`) or the pandas (`ghcr.io/bu-cds-bf528/pandas:latest`)
container to run this task as both of these contain a python installation.

### Input block

Specify the GTF as a single path input.

### Output block

Specify the delimited file your script writes. Make sure the filename matches
the name you pass to your script's output argument.

### Script block

Call `parse_gtf.py` and provide the appropriate command line arguments necessary
to run it.

### Stub block

Remember to include a `stub` block that uses `touch` to create an empty file
with the same name your output block expects.

### In your main.nf

1. Call this module in your workflow and pass it the appropriate GTF input
encoded as a param. 

## modules/star_index/main.nf - Generating a genome index using STAR

### Tool documentation

[STAR Documentation](https://github.com/alexdobin/STAR)

- Section 2 describes how to create a genome index and you may use the default
commands without changing any options
- Remember that you can run multiple commands in the script block of nextflow by
writing them on new lines. You can use the `mkdir` command to create the output
directory for the index files and then reference that same directory in the command.

### Construct the input and output records

1. The input record should contain two files, the genome FASTA file and the 
associated GTF

2. The output will be a single path to the directory that STAR creates. The STAR
index is composed of a set of files contained within the same directory. 

### Additional labels and directives

Ensure that it has an appropriate `label` and `container` specification.

### Input block

Use the record you constructed at the top of the module containing the FASTA
and GTF.

### Output block

STAR will output a set of files that comprise the index together. In your command
below, create a directory and have STAR output its index into that directory.

The output of this process will be a single directory path containing all of the
files comprising the index. 

### Script block

Check the documentation for the appropriate command and flags. You may use default
settings for the STAR index command. Ensure that you include the following flag
in that command so that STAR actually makes use of the threads you specify in
your `label`.

```bash
mkdir star_index
<star-genome-index-command> --runThreadN $task.cpus <other-options>
```

### Stub block

Remember to include a `stub` block. Since the output is a directory, use `mkdir`
to create an empty directory with the same name your output block expects.

### In your main.nf

1. Call this module in your workflow and pass it the genome FASTA and GTF
encoded as params (e.g. file(params.gtf)).

## modules/star_align/main.nf - Aligning reads to the genome

Remember that paired end reads are almost always used in conjunction with each
other (R1 and R2) and that they collectively represent the reads from a single
fragment generated from the same sample. When we align both of these paired end
reads to the genome, we will generate a single set of all valid alignments for 
the sample.

By default, many alignment programs will output these alignments in SAM format.
As discussed in lecture, the BAM format is a compressed version of SAM files that
contains the same information. Oftentimes, we will simply choose to generate BAM
files in place of SAM files in order to preserve disk space. 

### Tool documentation

[STAR Alignment](https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf) 
- Focus on section 3 (pg. 7) for how to use STAR to run a basic mapping job.

Remember back to the required aspects for your nextflow modules for last week 
and construct a working nextflow module that performs basic alignment using STAR.

### Construct the input and output records

Your input should be a record that has the sample name, and the two associated R1
and R2 files (you've already constructed a channel holding this information)

The output for this process should be the BAM file created and the log file.

### Additional labels and directives

Ensure it will run in an appropriate environment and specify what label to use
for computational resources. 

### Input block

Assign the record to a local variable so you can access its fields in your
command.

### Output block

Construct a record containing the generated BAM file and the log file. 

### Script block

Your STAR command should include only the following options and all others may be left
at their default value:

`--runThreadN`, `--genomeDir`, `--readFilesIn`, `--readFilesCommand`, 
`--outFileNamePrefix`, `--outSAMtype`

- At the end of your STAR command, please add the following code:

```bash
2> ${sample.name}.Log.final.out
```

For example, if you named your input record `sample`:

```bash
STAR --runThreadN $task.cpus --genomeDir <directory> --readFilesIn <reads> --readFilesCommand zcat --outFileNamePrefix ${sample.name}. --outSAMtype <option> 2> ${sample.name}.Log.final.out
```

The `2>` redirects the standard error to the log file and this is what will enable
us to collect the alignment statistics from the log file. Replace `sample` with
whatever local variable name you gave your input record, but you should name the
log file with the same name as the sample identifier. 

The log file from STAR will allow us to collect certain statistics about the
alignment rates that are useful for quality control purposes. As a general rule
of thumb, if there were no obvious issues with the sequencing preparation or
errors in the alignment, we expect a substantial proportion of our reads to
align to the reference genome. For well-annotated and studied genomes like human
or mouse, we usually see alignment rates >70-80% for successful NGS experiments.
Lower alignment rates are often expected for genomes that have not been
sequenced to the same quality and depth as the more commonly used references.
Make sure to evaluate these alignment rates in an experiment-specific context as
there is no set threshold or cutoff that is appropriate for all cases.

**N.B.** Ensure that you use the `--runThreadN $task.cpus` so that this
process actually uses the cores you request from the label. Alignment is a 
highly parallelizable process that will be greatly sped up by using multiple
cores.

### Stub block

Remember to include a `stub` block. Use the `name` value from your input record
to `touch` a fake BAM file and log file with the same names your output
block expects (e.g. `${name}.Log.final.out`).

### In your main.nf

1. Call this module in your workflow on the channel of `name`, `R1`, and `R2`
records, along with the index produced by your STAR index process.

## modules/multiqc/main.nf - Aggregating QC results after alignment

Typically after performing alignment, it is good to obtain a few post-alignment
quality control metrics to quickly check if there appear to be any major
problems with the data. At this step, we will typically evaluate the quality of
the reads themselves (PHRED scores, contamination, etc.) along with the
alignment rate to the reference genome.

As we've discussed, in larger experiments, it will quickly become cumbersome or
unfeasible to manually inspect the results for all of our samples individually.
Additionally, if we only look at one sample at a time, we may miss larger trends
or biases across all of our samples. To solve this issue, we will be making use
of MultiQC, which is a tool that simply aggregates the relevant logs and outputs
from various bioinformatics utilities into a nicely formatted HTML report.

Since you are working with files that have been intentionally filtered to make
them smaller, the actual outputs from fastQC and STAR will be misleading. Do
*not* draw any conclusions from these reports generated on the subsetted data;
the results will only be meaningful when you've switched to running this
pipeline on the full dataset.

### Tool documentation

[MultiQC Documentation](https://github.com/MultiQC/MultiQC). 

### Construct the input and output records

The input will be a list of Paths (List<path>)

The output will be a single HTML file called "multiqc_report.html" by default.

### Additional labels and directives

Ensure it will run in an appropriate environment and specify what label to use
for computational resources. 

### Input block

MultiQC will scan the current directory and automatically detect known output files.
The input will simply take advantage of Nextflow staging to gather together all
of the files into the same location.

### Output block

MultiQC creates a single file output called "multiqc_report.html" by default.

### Script block

Look at the documentation for the appropriate command.

### Stub block

Remember to include a `stub` block that uses `touch` to create an empty
`multiqc_report.html`.

### In your main.nf

1. Use appropriate operators to gather together all of the STAR output logs, and
the FastQC .ZIP file results into a single channel. 

Hint: You will need to use the map, mix and collect operators to access the 
elements in the records and transform it into a channel containing a list of
all the logs and fastqc ZIP files. You can use the following to access a specific
element from all the records in the channel:

align_output_channel.map { it.log }

## modules/verse/main.nf - Quantifying alignments to the genome

In RNAseq, we are interested in quantifying gene expression and comparing that
expression across conditions. We have so far generated alignments from the reads
from all of our samples to their appropriate reference genome. We will use the
information contained within the GTF (what each region of the genome represents)
to assign these alignments to features and count them. 

For differential expression analysis, our feature of interest will be exons as
those are the regions of genes that largely comprise the sequences found in mRNA
(which is what we are measuring and what was originally sequenced). We will
generate a single count for every gene representing the sum of the union of all
alignments falling into every exon annotated to that gene. This gene-level count
will be used as a proxy for that gene's expression in a particular sample.

We will be using VERSE, which is a read counting tool that will quantify
alignments into counts based on a feature of interest. VERSE also has built-in
strategies for assigning counts hierarchically in the case of overlapping features.

### Tool documentation

[VERSE Documentation](https://kim.bio.upenn.edu/software/verse_manual.html)
- You may leave all options at their default parameters. 
- Be sure to include the `-S` flag in your final command.

### Construct the input and output records

VERSE requires the BAM file and the GTF file. The input record should contain
the sample `name` and the BAM file; you can get these from the record your STAR
process outputs. The GTF is shared by every sample, so provide it separately on
its own line.

The output record should contain the sample `name` and the file of interest
created by VERSE, which is named with the pattern "`*.exon.txt`".

### Additional labels and directives

Ensure it will run in an appropriate environment and specify what label to use
for computational resources. 

### Input block

List the record containing the `name` and BAM and the GTF on new lines in the
input and then pass them left-to-right in the process call in your `main.nf`.

### Output block

VERSE creates a single file of interest with a known pattern.

### Script block

Read the documentation and fill out the script block appropriately. 

### Stub block

Remember to include a `stub` block. Use the `name` value from your input record
to `touch` a fake `${name}.exon.txt` file so it matches the output pattern.

### In your main.nf

1. Call this module in your workflow on the records output by your STAR alignment
process, along with the GTF encoded as a param.  The GTF is from your `nextflow.config`
so you can specify it like: `file(params.gtf)`.

## bin/concat_cts.py - Concatenating count outputs into a single matrix

After VERSE has run successfully, you will have generated a single set of counts
for each of your samples. To perform differential expression analysis, we will
need to combine count outputs from each sample into a single file where the rows
are the genes and the columns are the sample counts.

1. Write a python script, `bin/concat_cts.py`, that will concatenate all of the 
VERSE output files and write a single counts matrix containing all of your samples.
As with any external script, make it executable with a proper shebang line and 
use argparse to allow the incorporation of command line arguments. I suggest you
use `pandas` for this task.

Look at the structure of the .exon.txt files. The final counts matrix / CSV
should have the same number of rows as the number of genes in the reference
genome and the same number of columns as the number of samples.

## modules/concat_cts/main.nf - Running the concat_cts script

### Construct the input and output records

The input will be a list of Paths (List<path>) to all of the VERSE output files.

The output will be a single path to the counts matrix your script creates.

### Additional labels and directives

Ensure it will run in an appropriate environment and specify what label to use
for computational resources. You can use the pandas container
`ghcr.io/bu-cds-bf528/pandas:latest`.

### Input block

Specify the list of VERSE output files as your input. Nextflow will stage all of
them into the same working directory.

### Output block

Specify the counts matrix your script writes. Make sure the filename matches the
name you pass to your script's output argument.

### Script block

Call `concat_cts.py` and provide the appropriate command line arguments necessary
to run it, including all of the VERSE output files.

### Stub block

Remember to include a `stub` block that uses `touch` to create an empty file
with the same name your output block expects.

### In your main.nf

1. Use appropriate nextflow operators to gather all of the VERSE outputs together
into a single channel and pass it to this module. Since your VERSE process outputs
records, you will need to extract just the `.exon.txt` file from each record first
and group them into a single list containing all of the files from every sample.

## Week 1 tasks summary

In general, remember that once you have fully developed a module to `include`
it in your top-level `main.nf` and start to call it on the appropriate channels
and outputs to link together your workflow in the appropriate order. 

1. Clone the github classroom link for this project

2. Use the files contained within your `nextflow.config`
  
3. Generate a nextflow channel that has 6 total elements where
each element is a record containing three fields, `name`, `R1` and `R2`

4. Generate a nextflow channel that has 12 total
elements where each element is a record containing two fields, `name` and `fastq`

5. Generate a module that successfully runs FASTQC

6. Develop an external script that parses the GTF and writes a delimited file
where one column represents the ensembl human IDs and the value in the other 
column is the associated human gene symbol. Develop the accompanying nextflow
module, `modules/parse_gtf/main.nf` that runs this script. 

7. Generate a module that successfully creates a STAR index using FASTA and GTF.

8. Generate a module that runs STAR to align reads to a reference genome
  - Ensure that you output the alignments in BAM format
  - Use all default parameters
  - Specify the log file with extension (.Log.final.out) as a nextflow output
  
9. Make a module that runs MultiQC using a channel that contains all of the FASTQC
outputs and all of the STAR output log files

10 Create a module that runs VERSE on all of your output BAM files to generate
gene-level counts for all of your samples
 
11. Write a python script that uses `pandas` to concatenate all of the VERSE
outputs into a single counts matrix. Generate an accompanying nextflow module
that runs this python script

# Week 2: RNAseq

## Overview

By now, your pipeline should execute all of the necessary steps to perform
sample quality control, alignment, and quantification. This week, we will focus
on re-running the pipeline with the full data files and beginning a basic
differential expression analysis.

## Objectives

- Re-run your working pipeline on the full data files

- Evaluate the QC metrics for the original samples

- Choose a filtering strategy for your raw counts matrix

- Perform basic differential expression on your data using DESeq2 

- Generate a sample-to-sample distance plot and PCA plot for your experiment

## main.nf (top-level) - Setting up the publish and output blocks

In the top-level `main.nf` you were provided, you were given the `publish:` block
inside of the `workflow` block and the `output` block below the `workflow` block.

Use the past examples in labs or the nextflow documentation and ensure that you
send the results of `multiqc`, `parse_gtf` and `concat_cts` at minimum to the
`results/` directory for easy access.

## Switching to the full data

Once you've confirmed that your pipeline works end-to-end on the subsampled files,
we are going to properly apply our workflow to the original samples. This will
require only a few alterations in order to do. Ensure that you requested a VScode
session that lasts for at least 12 hours.

1. Look in your nextflow config for the param pointing to the samplesheet for
the full data. 

- **It is very important you ensure your pipeline runs to completion before
running it on the full data. When you do run it on the full data, please only
run it once!**


2. In your initial channels in your `main.nf`, change the samplesheet you read
from the subsampled samplesheet to the full data samplesheet. 

3. Now run your pipeline for real using the following command:

```bash
nextflow run main.nf -profile singularity,cluster -with-report
```

You may examine the progress and status of your jobs by using the `qstat` utility
as discussed in lecture and lab. 

## rnaseq-report.Rmd - Evaluating the QC metrics for the full data

After your pipeline has finished, inspect the MultiQC report generated from 
the full samples.

1. In your provided notebook, comment on the general quality of the sequencing
reads. Use the guidelines here: [sequencing quality control]({{ site.baseurl }}/projects/project_2_report/#read-quality-control-1-2-paragraphs)

## rnaseq-report.Rmd - Filtering the counts matrix

We will typically filter our counts matrices to remove genes that we believe
will be uninformative for the DE analysis. It is important to remember that
filtering is subjective and meant to reduce computational time, or remove 
uninformative rows. 

In your provided `rnaseq-report.Rmd`, load in the matrix of counts and generate
a new matrix of filtered counts according to your choice of strategy.

1. Choose a filtering strategy and apply it to your counts matrix. 

2. In the same .Rmd, record the following in text about your choice of filtering
strategy and other details: [Filtering Counts]({{ site.baseurl }}/projects/project_2_report/#filtering-the-counts-matrix-1-2-paragraphs)

## rnaseq-report.Rmd - Performing differential expression analysis

Refer to the DESeq2 vignette on how to perform a basic differential expression
analysis. For this dataset, you will simply be testing for differences between
the condition (control vs. experimental). Choose an appropriate padj threshold
to generate a list of statistically significant differentially expressed genes
from your analysis. 

You may refer to the official [DESeq2](https://bioconductor.org/packages/3.21/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)
vignette or the [BF530](https://bu-bioinfo.github.io/biological-data-science-in-r/biology-bioinformatics.html#differential-expression-rnaseq) instructions for how to run a basic differential expression analysis.  

Perform a basic differential expression analysis and ensure you do the following
based on the guidelines here: [Differential Expression Analysis]({{ site.baseurl }}/projects/project_2_report/#differential-expression-analysis-3-4-paragraphs)

## rnaseq-report.Rmd - Generating RNAseq quality control plots

It is common to produce both a PCA plot as well as a sample-to-sample distance
matrix from our counts to assist us in our confidence in whether the differences
we see in the differential expression analysis can likely be contributed to our
biological condition of interest. All of these plots have convenient wrapper
functions already implemented in DESeq2 (see the vignette).

1. Choose an appropriate normalization strategy (rlog or vst) and generate a
normalized counts matrix for the experiment. Refer to the DESeq2 vignette [here](https://bioconductor.org/packages/3.21/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#count-data-transformations)
for specific directions on how to do this.

2. Please follow the guidelines here for how to report these findings: [RNAseq Quality
Control Plots]({{ site.baseurl }}/projects/project_2_report/#differential-expression-analysis-3-4-paragraphs)

## rnaseq-report.Rmd - Performing gene set enrichment analysis

Perform a GSEA analysis on your RNAseq results. You are free to use any method
available though we recommend [fgsea](https://bioconductor.org/packages/release/bioc/html/fgsea.html). Please refer to the following resources:

[Gene Set Enrichment Analysis](https://bu-bioinfo.github.io/biological-data-science-in-r/biology-bioinformatics.html#gene-set-enrichment-analysis)

[fgsea](https://bu-bioinfo.github.io/biological-data-science-in-r/biology-bioinformatics.html#fgsea)

To do this, you will need to do a few steps:

1. Choose an appropriate ranking metric (I suggest log2FoldChange) and create a
ranked list of your genes and log2FoldChange in descending order. **N.B.** For
GSEA specifically, you should **not** filter by significance and your list should
be every gene discovered in the experiment.

2. Go to the [C2 canonical pathways MSIGDB dataset](https://www.gsea-msigdb.org/gsea/msigdb/human/collections.jsp#C2) and download it to your local computer and upload it to
your working directory on the cluster

3. Use either GSEABase or the fgsea function to read in the gene set file (.gmt)

4. Run fgsea using default parameters

5. Using a statistical threshold of your choice, generate a figure or plot that
displays the top most significant results from the FGSEA results.


# Weeks 3 and 4: RNAseq

## Overview

For these final weeks, use this time to finish up any tasks you weren't able to 
complete. There are no nextflow tasks this week, but you will be asked to create
some figures from the original paper using your own findings. Do all of these
tasks in the same notebook, `rnaseq-report.Rmd`.

## Objectives

- Read the original publication, focusing on its RNAseq analysis

- Replicate Figures 3C and 3F using your own results

- Compare your results and interpretations with the authors'

- Complete the Phase 2 portion of the report

## Reading the original paper

The original publication was given to you in a post on blackboard. Please read
the paper and focus specifically on their analysis and discussion of their RNAseq
experiment. 

## rnaseq-report.Rmd - Writing the Phase 2 report

Please follow the guidelines here to finish the Phase 2 portion of the report.

[Phase 2 Report]({{ site.baseurl }}/projects/project_2_report/#phase-2-informed-analysis)