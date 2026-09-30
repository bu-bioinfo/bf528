---
title: "Project 2: RNAseq"
layout: single
---

I have broken up the project into week-by-week sections. However, these sections
are guidelines and not a strict timeline. Your report and project will be due
only at the day specified on the schedule. These sections are designed to 
fit a manageable number of tasks into each week and give you a rough timeline. 

# Docker images for your pipeline

FastQC: `ghcr.io/bf528/fastqc:latest`

MultiQC: `ghcr.io/bf528/multiqc:latest`

VERSE: `ghcr.io/bf528/verse:latest`

STAR: `ghcr.io/bf528/star:latest`

Pandas: `ghcr.io/bf528/pandas:latest`

Biopython: `ghcr.io/bf528/biopython:latest`

# Week 1: RNAseq

## Workflow Visualization

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

## Create a working directory for project 2

Accept the github classroom link and clone the assignment to your student
directory in /projectnb/bf528/students/*your_username*/. This link will be
posted on the blackboard site for our class.

## Necessary paths and files are in your nextflow.config

Please look in your nextflow.config for various variables that I have given you
that you will need to use in your pipeline. I have provided you the path to the
files as well as the reference genome and matching GTF. You can access these
values by `params.variable_name_in_config`.

## Fill out the specifications.md provided

Before you start working on the pipeline, fill out the sections in the provided
`specifications.md`. This is meant to give you practice thinking at a high-level
about what your pipeline is doing, how it is behaving, and which points are critical
for you to review or validate. This will become especially important to keep in
mind once you start using agentic coding harnesses to develop workflows. 

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
  container 'ghcr.io/bf528/fastqc:latest'
  ...

}
```

For this course, these containers were all pre-built and their specifications kept
in this public github repository: https://github.com/BF528/pipeline_containers.
Feel free to look into the repo for how the containers were built. We follow a
similar pattern where we specify the exact environment we would like created in
a YAML file and then generate the environment using micromamba installed in a
container. We will get some experience later in the semester with building your
own containers from scratch.

In general, the containers will be named following the same pattern:
`ghcr.io/bf528/<name-of-tool>:latest` (e.g. `ghcr.io/bf528/fastqc:latest`).

## Important Note for developing your workflow

As you develop your workflow, you should always include a `stub` block, described
more below. This also means that until you are 100% confident your workflow
performs as expected, you should always run it with:

```bash
nextflow run main.nf -stub
```

This is really important for this project since the real data is quite large
and you will only run it with the real data once you are sure that your pipeline
has the desired behavior. 

## Generating our input channels for nextflow

In your `main.nf` at the top-level of the directory, make two initial channels
that will serve as the starting point for your workflow and save them to 
appropriately named variables in the `workflow` block.

1. A channel of records that reads each element from the `samplesheet.csv`
and maintains the `name`, `R1`, and `R2` fields. The number of elements should
match the number of samples.

2. A channel of records that has "exploded" out the `R1` and `R2` fields. This
channel of records should contain N * 2 records, one per each fastq and sample.
This record should have fields `name` and `fastq`.

## Performing Quality Control

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

### Input Block

1. Specify the record you declared at the top as your `input` and provide it a
local variable name.

### Output Block

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
exact files Nextflow should expect. You can make use of the "*" to capture any
files ending in the patterns you want (e.g. "*.zip" or "*.html")

### Script Block

For all processes, you will need to look at the tools original documentation or
help information in order to figure out the command to run it. Since the documentation
for FastQC is well-hidden, I will give you the general shape of the command below:

```bash
fastqc <fastq-file>
```

### Stub Block

For every process, you will fill out a stub block that uses the `name` in the 
record field and the command `touch` to generate fake files that you can use
to troubleshoot your workflow as you develop it. 

Use the `name` value from your input record to name the fake files so they
match the filenames your output block expects. For example, if your output
expects `${name}.txt`, your stub block would be:

```bash
touch ${name}.txt
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

## Generate a file containing the gene IDs and their corresponding human gene symbols

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
previous scripts to allow the specification of command line arguments. 

2. The script should take a single file input (GTF) and output a single text
file.

3. Create a nextflow module, `modules/parse_gtf/main.nf` that calls this script
and provides the appropriate command line arguments necessary to run it.

4. You may use the biopython (`ghcr.io/bf528/biopython:latest`) or the pandas
(`ghcr.io/bf528/pandas:latest`) container to run this task as both of these
contain a python installation.

5. Incorporate this module to parse the GTF into your workflow `main.nf` and
pass it the appropriate GTF input encoded as a param. 

6. Include a `stub` block that uses `touch` to create an empty file with the
same name your output block expects.

## Generate a genome index using STAR

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

### Input Block

Use the record you constructed at the top of the module containing the FASTA
and GTF.

### Output Block

STAR will output a set of files that comprise the index together. In your command
below, create a directory and have STAR output its index into that directory.

The output of this process will be a single directory path containing all of the
files comprising the index. 

### Script Block

Check the documentation for the appropriate command and flags. You may use default
settings for the STAR index command. Ensure that you include the following flag
in that command so that STAR actually makes use of the threads you specify in
your `label`.

```bash
--runThreadN $task.cpus
```

### Stub Block

Remember to include a `stub` block. Since the output is a directory, use `mkdir`
to create an empty directory with the same name your output block expects.

## Assigning process labels to your modules

Please refer to the following page for [common combinations](https://www.bu.edu/tech/support/research/system-usage/running-jobs/batch-script-examples/#MEMORY)
of options to request specific amounts of resources from nodes on the SCC. 

I have provided you with a variety of pre-set labels, choose the ones you think
are appropriate for each task based on their complexity. Make this a habit for
every process even though I explicitly instructed you for just these two. 

## Week 1 Tasks Summary

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

# Week 2: RNAseq

## Overview

Now that we have performed basic quality control on the FASTQ files, we are
going to map them to the human reference genome to generate alignments for
each of our sequencing reads. After alignment, we will aggregate the outputs from
FASTQC and STAR into a single report summarizing some of the important quality
control metrics describing our sequencing reads and the alignments. We will then
quantify the alignments in our BAM file to the gene-level using VERSE. 

## Objectives

- Align your sequencing reads to the human reference genome using STAR

- Use MultiQC to generate a single report containing the quality metrics for
the sequencing reads and alignments

- Generate gene-level counts using VERSE for each of the samples

- Concatenate gene-level counts from each sample into a single counts matrix

## Aligning reads to the genome

Last week you generated a STAR index to enable alignment of reads to the human
reference genome. This week, you will use this index to align the sequencing
reads to the genome. 

Remember that paired end reads are almost always used in conjunction with each
other (R1 and R2) and that they collectively represent the reads from a single
fragment and sample. When we align both of these paired end reads to the genome,
we will generate a single set of all valid alignments for the sample.

By default, many alignment programs will output these alignments in SAM format.
As discussed in lecture, the BAM format is a compressed version of SAM files that
contains the same information. Oftentimes, we will simply choose to generate BAM
files in place of SAM files in order to preserve disk space. 

### STAR Alignment Documentation

[STAR Alignment](https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf) 
- Focus on section 3 (pg. 7) for how to use STAR to run a basic mapping job.

Remember back to the required aspects for your nextflow modules for last week 
and construct a working nextflow module that performs basic alignment using STAR.

### Additional labels and directives

Ensure it will run in an appropriate environment and specify what label to use
for computational resources. 

### Construct the input and output records

Your input should be a record that has the sample name, and the two associated R1
and R2 files (you've already constructed a channel holding this information)

The output for this process should be the BAM file created and the log file.

### Input Block

Assign the record to a local variable so you can access its fields in your
command.

### Output Block

Construct a record containing the generated BAM file and the log file. 

### Script Block

Your STAR command should include only the following options and all others may be left
at their default value:

`--runThreadN`, `--genomeDir`, `--readFilesIn`, `--readFilesCommand`, 
`--outFileNamePrefix`, `--outSAMtype`

- At the end of your STAR command, please add the following code:

```bash
2> ${<name_from_your_record>}.Log.final.out
``` 

or 

```bash
STAR --runThreadN $task.cpus --genomeDir <directory> --readFilesIn <reads> --readFilesCommand zcat --outFileNamePrefix <name>. --outSAMtype <option> 2> ${name}.Log.final.out
``` 

The `2>` redirects the standard error to the log file and this is what will enable
us to collect the alignment statistics from the log file. The ${name} may differ
based on how you have named your input record, but you should name the log file
with the same name as the sample identifier. 

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

**N.B.** Ensure that you use the `--runThreadN $task.cpus` to ensure that this
process actually uses the cores you request from the label. Alignment is a 
highly parallelizable process that will be greatly sped up by using multiple
cores.

### Stub Block

Remember to include a `stub` block. Use the `name` value from your input record
to `touch` a fake BAM file and log file with the same names your output
block expects (e.g. `${name}.Log.final.out`).

## Performing post-alignment QC and aggregating all QC results together

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

### Tool Documentation
[MultiQC Documentation](https://github.com/MultiQC/MultiQC). 

### Construct the input and output records

The input will be a list of Paths (List<path>)

The output will be a single HTML file called "multiqc_report.html" by default.

### Additional labels and directives

Ensure it will run in an appropriate environment and specify what label to use
for computational resources. 

### Input Block

MultiQC will scan the current directory and automatically detect known output files.
The input will simply take advantage of Nextflow staging to gather together all
of the files into the same location.

### Output Block

MultiQC creates a single file output called "multiqc_report.html" by default.

### Script Block

Look at the documentation for the appropriate command.

### Stub Block

Remember to include a `stub` block that uses `touch` to create an empty
`multiqc_report.html`.

### In your main.nf

1. Use appropriate operators to gather together all of the STAR output logs, and
the FastQC results into a single channel. 

## Quantifying alignments to the genome

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

### Tool Documentation
[VERSE Documentation](https://kim.bio.upenn.edu/software/verse_manual.html)
- You may leave all options at their default parameters. 
- Be sure to include the `-S` flag in your final command.

### Construct the input and output records

VERSE requires the BAM file and the GTF file. You can provide these separately
to the process by listing them on new lines. 

The file of interest created by verse is named with the pattern "*.exon.txt".

### Additional labels and directives

Ensure it will run in an appropriate environment and specify what label to use
for computational resources. 

### Input Block

List the BAM files and the GTF on new lines in the input and then pass them
left-to-right in the process call in your `main.nf`.

### Output Block

VERSE creates a single file of interest with a known pattern.

### Script Block

Read the documentation and fill out the script block appropriately. 

### Stub Block

Remember to include a `stub` block. Use the sample `name` to `touch` a fake
`${name}.exon.txt` file so it matches the output pattern.

## Concatenating count outputs into a single matrix

After VERSE has run successfully, you will have generated a single set of counts
for each of your samples. To perform differential expression analysis, we will
need to combine count outputs from each sample into a single file where the rows
are the genes and the columns are the sample counts.

1. Write a python script, `bin/concat_cts.py`, that will concatenate all of the 
VERSE output files and write a single counts matrix containing all of your samples.
As with any external script, make it executable with a proper shebang line and 
use argparse to allow the incorporation of command line arguments. I suggest you
use `pandas` for this task and you can use the pandas container 
`ghcr.io/bf528/pandas:latest`.
  - Look at the structure of the .exon.txt files. The final counts matrix / CSV
  should have the same number of rows as the number of genes in the reference
  genome and the same number of columns as the number of samples.

2. Generate a module, `modules/concat_cts/main.nf`,  that runs this script
according to all of the conventions for modules. Don't forget to include a `stub`
block that uses `touch` to create an empty counts matrix with the same name your
output block expects.

3. In your top-level `main.nf` workflow script, use appropriate nextflow operators
to gather all of the VERSE outputs together. 

## Week 2 Tasks Summary

1. Generate a module that runs STAR to align reads to a reference genome
  - Ensure that you output the alignments in BAM format
  - Use all default parameters
  - Specify the log file with extension (.Log.final.out) as a nextflow output
  
2. Make a module that runs MultiQC using a channel that contains all of the FASTQC
outputs and all of the STAR output log files

3. Create a module that runs VERSE on all of your output BAM files to generate
gene-level counts for all of your samples
 
4. Write a python script that uses `pandas` to concatenate all of the VERSE
outputs into a single counts matrix. Generate an accompanying nextflow module
that runs this python script

# Week 3: RNAseq

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

## Switching to the full data

Once you've confirmed that your pipeline works end-to-end on the subsampled files,
we are going to properly apply our workflow to the original samples. This will
require only a few alterations in order to do. Ensure that you requested a VScode
session that lasts for at least 12 hours.


1. Look in your nextflow config for the `full_reads` param. 

- **It is very important you ensure your pipeline runs to completion before
running it on the full data. When you do run it on the full data, please only
run it once!**


2. In your initial channels in your `main.nf`, change the `params.subset_reads`
to `params.full_reads`. 

3. Now run your pipeline for real using the following command:

```bash
nextflow run main.nf -profile singularity,cluster
```

You may examine the progress and status of your jobs by using the `qstat` utility
as discussed in lecture and lab. 

## Evaluate the QC metrics for the full data

After your pipeline has finished, inspect the MultiQC report generated from 
the full samples.

1. In your provided notebook, comment on the general quality of the sequencing
reads. Write a paragraph in the style of a publication reporting what you find and
any metrics that might be concerning. 

## Analysis Tasks - Rmarkdown Notebook

You will typically be performing analyses in either a jupyter notebook or Rmarkdown.
With the SCC, we will not be able to easily encapsulate R in an isolated environment.

Instead, simply load the R module (on the launch page for VSCode in on-demand) 
as you boot your VSCode extension and work in a Rmarkdown notebook. You may install packages
as needed and ensure that you record the versions used with the `sessionInfo()` 
function.

I highly recommend you use Rmarkdown for this project. It will make it much easier
for you to generate your report as nearly all of the analysis tasks will be done
in R. 


## Filtering the counts matrix

We will typically filter our counts matrices to remove genes that we believe
will be uninformative for the DE analysis. It is important to remember that
filtering is subjective and meant to reduce computational time, or remove 
uninformative rows. 

1. Choose a filtering strategy and apply it to your counts matrix. In the provided
notebook, report the strategy you used and create a plot or a table that demonstrates
the effects of your filtering on the counts for all of your samples. Ensure you
mention how many genes are present before and after your filtering threshold. 

## Performing differential expression analysis using the filtered counts

Refer to the DESeq2 vignette on how to perform a basic differential expression
analysis. For this dataset, you will simply be testing for differences between
the condition (control vs. experimental). Choose an appropriate padj threshold
to generate a list of statistically significant differentially expressed genes
from your analysis. 

You may refer to the official [DESeq2](https://bioconductor.org/packages/3.21/bioc/vignettes/DESeq2/inst/doc/DESeq2.html)
vignette or the [BF591](https://bu-bioinfo.github.io/r-for-biological-sciences/biology-bioinformatics.html#differential-expression-rnaseq) instructions for how to run a basic differential expression analysis.  

Perform a basic differential expression analysis and produce the following as well
formatted figures:

  1. A table containing the DESeq2 results for the top ten significant genes 
  ranked by padj. Your results should have the corresponding gene name for
  each ensembl gene ID. You should not need to use bioMart or any other utility,
  you have already created a file from when you parsed the GTF that contains
  the gene names for each ensembl gene ID. 
  - Note that this is not your list of differentially expressed genes. This is just
  a quick figure that displays some of the most differentially expressed genes
  
  
  2. Choose an appropriate padj threshold and report the number of significant
  genes remaining that satisfy this threshold. Make sure you filter your list to 
  only contain these genes. **This will be the list of genes you should use as 
  input for the DAVID or ENRICHR analysis**
  
  3. The results from a DAVID or ENRICHR analysis on the significant genes at
  your chosen padj threshold. Comment in a notebook what results you find most
  interesting from this analysis. 

## RNAseq Quality Control Plots

It is common to produce both a PCA plot as well as a sample-to-sample distance
matrix from our counts to assist us in our confidence in whether the differences
we see in the differential expression analysis can likely be contributed to our
biological condition of interest. All of these plots have convenient wrapper
functions already implemented in DESeq2 (see the vignette).

1. Choose an appropriate normalization strategy (rlog or vst) and generate a
normalized counts matrix for the experiment. Refer to the DESeq2 vignette [here](https://bioconductor.org/packages/3.21/bioc/vignettes/DESeq2/inst/doc/DESeq2.html#count-data-transformations)
for specific directions on how to do this.

2. Perform PCA on this normalized counts matrix and overlay the sample
information in a biplot of PC1 vs. PC2

3. Create a heatmap or graphic of the sample-to-sample distances for the experiment

4. In a notebook, comment in no less than two paragraphs about your
interpretations of these plots and what they indicate about the samples, and the 
experiment.

## FGSEA Analysis

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

6. In your notebook, briefly remark on your results and what seems interesting to
you about the biology.

# Week 4: RNAseq

## Overview

For the final week, use this time to finish up any tasks you weren't able to 
complete. There are no nextflow tasks this week, but you will be asked to create
some figures from the original paper using your own findings. Do all of these
tasks in the notebook you created from week 3. 

## Objectives

- Read the original publication with a specific focus on their RNAseq experiment

- Reproduce figures 3C and 3F with your own findings and compare them in your
discussion

- Write a short methods section for your pipeline and compare with the methods
published in the original paper

## Read the original paper

The original publication was given to you in a post on blackboard. Please read
the paper and focus specifically on their analysis and discussion of their RNAseq
experiment. 

## Replicate figure 3C and 3F

Focus on figures 3C and 3F and specifically their discussion of their RNAseq results. 

1. Create a volcano plot similar to the one seen in figure 3C. Use your DAVID
or GSEA results and create a plot with the same information as 3F using your
findings.

2. Read their discussion of their results and specifically address the following
in your provided notebook:

  - Compare how many significant genes are up- and down-regulated in their
  findings and yours (using their significance threshold). Ensure you list how 
  many you find vs. how many they report. 

  - Compare their enrichment results with your DAVID and GSEA analysis. Comment
  on any differences you observe and why there are discrepancies.

## Week 4 Tasks Summary

1. Read the original publication and focus specifically on the RNAseq experiment

2. Recreate figures 3C and 3F with your own results and ensure you address the
listed questions in your notebook

3. Write a methods section in the style we've discussed for your workflow

4. Ensure you read the Project 2 Report Guidelines for a full description of
what is expected of you. 

# REMINDER TO CLEAN UP YOUR WORKING DIRECTORY

When you have successfully run your project 2 pipeline, please ensure that you 
fully delete your work/ directory and any large files that you may have published
to your results/ directory. 

You may use the following command:

```bash
rm -rf work/
```

These samples are very large and we have limited disk space. I will be checking
your working directories to ensure you do this. 