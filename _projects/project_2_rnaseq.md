---
title: "Project 2: RNAseq"
layout: single
---

The projects are broken up into week-by-week sections. However, these sections
are guidelines and not a strict timeline. Your report and project will be due
only at the day specified on the schedule. These sections are designed to 
fit a manageable number of tasks into each week and give you a rough timeline. 

# Week 1: RNAseq

## Week 1 Overview

A basic RNAseq analysis consists of sample quality control, alignment,
quantification and differential expression analysis. This week, we will be
performing quality control analysis on the sequencing reads, generating a genome
index for alignment, and making a mapping of human ensembl IDs to gene names.

## Objectives

- Perform basic quality control by running FASTQC on the sequencing reads

- Generate a delimited file containing the mapping of human ensembl ids to gene
  names

- Use STAR to create a genome index for the human reference genome

## Create a working directory for project 1

Accept the github classroom link and clone the assignment to your student
directory in /projectnb/bf528/students/*your_username*/. This link will be
posted on the blackboard site for our class.

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
`ghcr.io/bf528/<name-of-tool>:latest` or `ghcr.io/bf528/fastqc:latest`.

**New command for running your workflow**

You will need to incorporate one more change to make your pipeline use these
containers. If you look in the `nextflow.config`, you'll see a profile labeled
singularity, which encodes some singularity options for nextflow to use. 

When running your pipeline, you will now use the `-profile singularity,local`
option, which will have Nextflow execute tasks with the specified container image
listed in the module. The config contains some common options that nextflow will
automatically add to the singularity command when run with the specified profile. 

```
nextflow run main.nf -profile singularity,local
```

As always, remember to activate your conda environment containing nextflow before
running your pipeline.

## Docker images for your pipeline

FastQC: `ghcr.io/bf528/fastqc:latest`

multiQC: `ghcr.io/bf528/multiqc:latest`

VERSE: `ghcr.io/bf528/verse:latest`

STAR: `ghcr.io/bf528/star:latest`

Pandas: `ghcr.io/bf528/pandas:latest`

## Generating our input channels for nextflow

This RNAseq pipeline will be driven by two channels that contain the starting
FASTQ files for each of the samples in the experiment. Nextflow has a built-in
function to simplify the generation of channels for samples from paired-end
sequencing experiments. The `Channel.fromFilePairs` channel function allows you
to detect paired end fastq files for each sample using similar pattern matching
in bash through the use of wildcard expansion (*).

1. In the `nextflow.config`, specify a parameter called `reads` that encodes the
path to your fastq files and uses * to flexibly detect the sample name associated
with both paired files. Refer to the nextflow documentation [here](https://www.nextflow.io/docs/latest/reference/channel.html#fromfilepairs)
Our files are located at /projectnb/bf528/materials/project_2_rnaseq/subsampled_files/ for the subsampled files and /projectnb/bf528/materials/project_2_rnaseq/full_files/ for the full files.

2. In your workflow `main.nf`, use the `Channel.fromFilePairs` function and the
param you created in step 1 to create a channel called `align_ch`. You'll notice
that this function creates a channel with a structure we've seen before: a tuple
containing the base name of the file and a list containing the R1 and R2 file
associated with that sample.

```
align_ch

[sample1, [sample1_R1.fastq.gz, sample1_R2.fastq.gz]]
```

3. In your workflow `main.nf` create another channel using the exact logic from
above but add an additional operation to create a channel that has as many
elements in the channel as there are actual files (16). You may find information
on common nextflow operators that will enable this [here](https://www.nextflow.io/docs/latest/reference/operator.html)

Name this channel `fastqc_channel` and it should be a list tuples where the
first value is the name of the sample and the second is the path to the
associated file. This will look something like below:

```
fastqc_channel

[sample1, sample1_R1.fastq.gz]
[sample1, sample1_R2.fastq.gz]
```

## Performing Quality Control

At this point, you should have: 

- Setup a directory for this project by accepting the github classroom link

- Familiarized yourself with the changes to environment management and how to run
nextflow using containers

- Generate two channels in your `main.nf` with the size and elements specified
  above

We will begin by performing quality control on the FASTQ files generated from
the experiment. fastQC is a bioinformatics software tool that calculates and
generates descriptive graphics of the various quality metrics encoded in a FASTQ
file. We will use this tool to quickly check the basic quality of the sequencing
in this experiment.

3. Make a new process for fastqc in the `modules/` directory. Be sure to specify
the following in your module:

```
label 'process_low'
container 'ghcr.io/bf528/fastqc:latest'
publishDir <a param containing the path to results/>
```

4. Specify the inputs of the process to match the structure of the
`fastqc_channel` we just generated.For this module, please list two named
outputs, which will later allow us to use the individual outputs separately:

```
output:
tuple val(name), path('*.zip'), emit: zip
tuple val(name), path('*.html'), emit: html
```

This output definition will instruct nextflow that both of these files should
exist after FASTQC has run successfully. It will capture the html report and zip
file separately and allow you to pass these different values through channels
separately (i.e. FASTQC.out.zip would refer specifically to the zip file created
by the FASTQC task)

Remember you can use wildcard expansions in the path output to flexibly detect
files with certain extensions without specifying their full filename.

5. The shell command should be the successful fastqc command you ran earlier. 
Ensure that the following argument is included in your actual fastQC command:

```
-t $task.cpus
```

6. Incorporate the FASTQC process into your workflow `main.nf` and provide it the
proper channel. 

## Generate a file containing the gene IDs and their corresponding human gene symbols

As we've discussed, it's often more intuitive for us to use gene names rather than
their IDs. While there are external services that can perform this for us (biomaRt), 
it is often better to extract this information from the GTF file associated
with the exact version of the reference genome we are using. This will ensure
that we are as consistent as possible with our labeling. 

Whenever we need to perform operations using custom code, we are going to use
the conventions established in project 0. We will place this script in the `bin/`
directory and make it executable. We will then create a nextflow module that will
provide the appropriate command line arguments to the script.

1. Generate a python script that parses the GTF file you were provided and creates
a delimited file containing the ensembl human ID and its corresponding gene name. 
Please copy and modify the `argparse` code used in the project 0 script to allow
the specification of command line arguments. The script should take the GTF as
input and output a single text file containing the requested information. 

2. Create a nextflow module that calls this script and provides the appropriate
command line arguments necessary to run it.

3. You may use the biopython (ghcr.io/bf528/biopython:latest) or the pandas
(ghcr.io/bf528/pandas:latest) container to run this task as both of these
contain a python installation.

4. Incorporate this module to parse the GTF into your workflow `main.nf` and
pass it the appropriate GTF input encoded as a param. 

## Creating your own process labels

As we discussed in class, you can request various ranges of computational resources
for your jobs / processes to use through the `qsub` command and its accompanying
options. 

Please refer to the following page for [common combinations](https://www.bu.edu/tech/support/research/system-usage/running-jobs/batch-script-examples/#MEMORY)
of options to request specific amounts of resources from nodes on the SCC. 

1. By now you have noticed that some modules have a `label` and you can see in
the `nextflow.config` in the profiles section the exact qsub command and options
each label requests. 

2. Create two new labels named `process_medium` and `process_high`. For `process_medium`,
use the correct options to request 8 cores and <= 32GB ram For `process_high`,
set the options to request 16 cores and <= 128GB ram.

You will need to add a clusterOptions line to the `process_high` to specify the
additional flags. 

## Generate a genome index

Most alignment algorithms require an index to be generated to make the alignment
process more efficient and expedient. These index files are both specific to the
tool and the reference genome used to build them. We will be using the STAR
aligner, one of the most commonly used alignment tools for RNAseq.

1. Read the beginning of the [documentation](https://github.com/alexdobin/STAR)
for how to generate a STAR index.

2. Generate a module and process that creates a STAR index for our reference
genome. This process will require two inputs, the reference genome and the
associated GTF file. Ensure that the following are specified in your module:

```
label 'process_high'
container 'ghcr.io/bf528/star:latest'
```

3. The outputs of this process will be a directory of multiple files that all
comprise the index. You will have to create this directory prior to running the
STAR command. Use all of the basic options specified in the manual and leave
them at their default values. Be sure to also include the following argument
in your STAR command:

```
--runThreadN $task.cpus
```

4. Incorporate this process into your workflow and pass it the appropriate
inputs from your params encoding the path to the reference genome fasta and GTF
file.

5. **Make sure you submit this particular job to the cluster with the following
command**: 

```
nextflow run main.nf -profile singularity,cluster
```

## Week 1 Tasks Summary

1. Clone the github classroom link for this project

2. Copy the necessary files to your working directory. These files will include
the following:

  - Gencode hg38 reference genome for the primary assembly
  - Gencode GTF for the primary assembly
  - The subsampled FASTQ files
  
3. Generate a nextflow channel called `align_ch` that has 6 total elements where
each element is a tuple containing two elements: the name of the sample, and a
list of both of the associated paired end files.

4. Generate a nextflow channel called `fastqc_channel` that has 12 total
elements where each element is a tuple containing two elements: the name of the
sample, and one of the FASTQ files. 

5. Generate a module that successfully runs FASTQC using the `fastqc_channel`

6. Develop an external script that parses the GTF and writes a delimited file
where one column represents the ensembl human IDs and the value in the other 
column is the associated human gene symbol. 

7. Generate a module that successfully creates a STAR index using the params
containing the path to your reference genome assembly and GTF

## Week 2: RNAseq

## Section Links

[Week 2 Overview](#week-2-overview)

[Objectives](#objectives)

[Aligning reads to the genome](#aligning-reads-to-the-genome)

[Performing post-alignment QC](#performing-post-alignment-qc)

[Quantifying alignments to the genome](#quantifying-alignments-to-the-genome)

[Concatenating count outputs into a single matrix](#concatenating-count-outputs-into-a-single-matrix)

[Week 2 Detailed Task Summary](#week-2-detailed-task-summary)

## Week 2 Overview

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

## Docker images for your pipeline

FastQC: `ghcr.io/bf528/fastqc:latest`

multiQC: `ghcr.io/bf528/multiqc:latest`

VERSE: `ghcr.io/bf528/verse:latest`

STAR: `ghcr.io/bf528/star:latest`

Pandas: `ghcr.io/bf528/pandas:latest`

## Aligning reads to the genome

Last week you generated a STAR index to enable alignment of reads to the human
reference genome. This week, you will use this index to align the sequencing
reads to the genome. 

Remember that paired end reads are almost always used in conjunction with each
other (R1 and R2) and that they collectively represent the reads from a single
sample. When we align both of these paired end reads to the genome, we will
generate a single set of all valid alignments for the sample.

By default, many alignment programs will output these alignments in SAM format.
As discussed in lecture, the BAM format is a compressed version of SAM files that
contains the same information. Oftentimes, we will simply choose to generate BAM
files in place of SAM files in order to preserve disk space. 

1. Look at the documentation for
[STAR](https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf) and
focus on section 3 (pg. 7) for how to use STAR to run a basic mapping job.
Construct a working nextflow module that performs basic alignment using STAR.

Your STAR command should include only the following options and all others may be left
at their default value:

`--runThreadN`, `--genomeDir`, `--readFilesIn`, `--readFilesCommand`, 
`--outFileNamePrefix`, `--outSAMtype`

2. Remember that by default, nextflow stores all of the outputs for a specific
task in the staged directory in which it ran. Often, we will want to inspect
the output files or log files from various processes. 

Ensure that your STAR module has two separate named outputs using `emit`. The two
outputs will be the BAM file and another for the log file generated during
alignment named with the extension `.Log.final.out`. 

3. Ensure that you use the `process_high` for the `label` and the appropriate
container `ghcr.io/bf528/star:latest`.

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

## Performing post-alignment QC

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

1. Make a new module that will run
[MultiQC](https://github.com/MultiQC/MultiQC). You can specify the label as
`process_low` and set `publishDir` to your `results/` directory. We will take
advantage of the staging directory strategy that nextflow uses to run MultiQC.

By default, MultiQC will simply scan a directory and automatically detect any
of the common output files and logs created by the bioinformatics tools it
supports. For your `input`, you can simply specify `path('*')` and it creates
an HTML file as an `output`.

2. The tricky part with running MultiQC and Nextflow is that you will need to 
gather all of the output files from FASTQC and STAR and ensure that multiqc only
runs after all of the samples have been processed by both of these tools.

Use a combination of `map()`, `collect()`, `mix()`, `flatten()` to create a
single channel that contains a list with all of the output files from FASTQC and
STAR logs for every sample and call it `multiqc_ch`. Remember that you may access
the outputs of a previous process by using the `.out()` notation (i.e. ALIGN.out
or FASTQC.out.zip).

See below for an example of what the channel should look like:

**In class, we may have used the `.html` file as the output for FastQC, multiQC
will need the `.zip` file. You can either change the output or add another specifically
for the `.zip` file created by FastQC.

```
multiqc_channel

[sample1_R1_fastqc.zip, sample1_R2_fastqc.zip, sample1.Log.final.out,
sample2_R1_fastqc.zip, sample2_R2_fastqc.zip, sample2.Log.final.out, ...]

```

3. Add the MultiQC module to your workflow `main.nf` and run MultiQC. MultiQC
should run a single time and only after every alignment and fastqc process has
finished. 

4. Ensure that your `multiqc_report.html` is successfully created and contains
the QC information from both FASTQC and STAR for all of your samples. You may
open the HTML file through SCC ondemand. 

5. Make sure to include the `-f` flag in your multiqc command. 

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

1. Generate a module that runs
[VERSE](https://kim.bio.upenn.edu/software/verse_manual.html) on each of your
BAM files. You may leave all options at their default parameters. Be sure to
include the `-S` flag in your final command.

2. Run the VERSE module in your workflow `main.nf` and quantify the alignments
in each of the BAM files

## Concatenating count outputs into a single matrix

After VERSE has run successfully, you will have generated a single set of counts
for each of your samples. To perform differential expression analysis, we will
need to combine count outputs from each sample into a single file where the rows
are the genes and the columns are the sample counts.

1. Write a python script that will concatenate all of the verse output files and
write a single counts matrix containing all of your samples. As with any
external script, make it executable with a proper shebang line and use argparse
to allow the incorporation of command line arguments. I suggest you use `pandas`
for this task and you can use the pandas container `ghcr.io/bf528/pandas:latest`.

2. Generate a module that runs this script and create a channel in your workflow
`main.nf` that consists of all of the VERSE outputs. Incorporate this script
into your workflow and Ensure that this module / script only executes after
*all* of the VERSE tasks have finished.

## Week 2 Detailed Task Summary

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

## Week 3: RNAseq

## Section Links

[Week 3 Overview](#week-3-overview)

[Objectives](#objectives)

[Switching to the full data](#switching-to-the-full-data)

[Evaluate the QC metrics for the full data](#evaluate-the-qc-metrics-for-the-full-data)

[Filtering the counts matrix](#filtering-the-counts-matrix)

[Performing differential expression analysis using the filtered counts](#performing-differential-expression-analysis-using-the-filtered-counts)

[RNAseq Quality Control Plots](#rnaseq-quality-control-plots)

[FGSEA Analysis](#fgsea-analysis)

## Week 3 Overview

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

## Docker images for your pipeline

FastQC: `ghcr.io/bf528/fastqc:latest`

multiQC: `ghcr.io/bf528/multiqc:latest`

VERSE: `ghcr.io/bf528/verse:latest`

STAR: `ghcr.io/bf528/star:latest`

Pandas: `ghcr.io/bf528/pandas:latest`

## Switching to the full data

Once you've confirmed that your pipeline works end-to-end on the subsampled files,
we are going to properly apply our workflow to the original samples. This will
require only a few alterations in order to do. 

1. Create a new directory in `samples/` called `full_files/`. Copy the original
files from `/projectnb/bf528/materials/project_1_rnaseq/full_files/` to your 
newly created directory. 

2. Edit your `nextflow.config` and change the path found in your `params.reads`
to reflect the location of your full files.

Most of our bioinformatics experiments will involve relatively large files and
expensive operations. Even relatively small RNAseq experiments will still
involve aligning tens of millions of reads to genomes that are many megabases
long. Now that we are working with these larger files, we should not and in some
cases, will not, be able to run these tasks locally on the same node that our
VSCode session is running.

We will switch now to running our jobs on the cluster utilizing the `qsub` utility
for queuing jobs to run on compute nodes. This will enable us to both request
nodes that have faster processors / more RAM and to easily parallelize our tasks
that can run simultaneously. 

As a reminder, to run your workflow on the cluster, switch to using the
`cluster` profile option in place of the `local` flag as in project 0. Your new
nextflow command should now be:

```
nextflow run main.nf -profile singularity,cluster
```

You may also need to unset the `resume = true` option in your config, or manually
set `resume = false` when you attempt to rerun your workflow on the full data. 

You may examine the progress and status of your jobs by using the `qstat` utility
as discussed in lecture and lab. 

## Evaluate the QC metrics for the full data

After your pipeline has finished, inspect the MultiQC report generated from 
the full samples.

1. In your provided notebook, comment on the general quality of the sequencing
reads. Write a paragraph in the style of a publication reporting what you find and
any metrics that might be concerning. 

## Analysis Tasks

You will typically be performing analyses in either a jupyter notebook or Rmarkdown.
With the SCC, we will not be able to easily encapsulate R in an isolated environment.

Instead, simply load the R module (on the launch page for VSCode in on-demand) 
as you boot your VSCode extension and work in aRmarkdown. You may install packages
as needed and ensure that you record the versions used with the `sessionInfo()` 
function.

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
  ranked by padj. Your results should have the corresponding gene names for
  each gene symbol. (You extracted these earlier...)
  
  2. Choose an appropriate padj threshold and report the number of significant
  genes at this threshold. 
  
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
for specific directions on how to do this, 

2. Perform PCA on this normalized counts matrix and overlay the sample
information in a biplot of PC1 vs. PC2

3. Create a heatmap or graphic of the sample-to-sample distances for the experiment

4. In a notebook, comment in no less than two paragraphs about your
interpretations of these plots and what they indicate about the samples, and the 
experiment.

## FGSEA Analysis

Perform a GSEA analysis on your RNAseq results. You are free to use any method
available though we recommend [fgsea](https://bioconductor.org/packages/release/bioc/html/fgsea.html).

1. Choose an appropriate ranking metric and use the [C2 canonical
pathways MSIGDB dataset](https://www.gsea-msigdb.org/gsea/msigdb/human/collections.jsp#C2)
to perform a basic GSEA analysis.

2. Using a statistical threshold of your choice, generate a figure or plot that
displays the top most significant results from the FGSEA results.

3. In a notebook, briefly remark on your results and what seems interesting to
you about the biology.

## Week 4: RNAseq

## Section Links

[Week 4 Overview](#week-4-overview)

[Objectives](#objectives)

[Read the original paper](#read-the-original-paper)

[Replicate figure 3C and 3F](#replicate-figure-3c-and-3f)

[Write a methods section for your pipeline](#write-a-methods-section-for-your-pipeline)

[Week 4 Detailed Tasks Summary](#week-4-detailed-tasks-summary)

## Week 4 Overview

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

Focus on figure 3C and specifically their discussion of their RNAseq results. 

1. Create a volcano plot similar to the one seen in figure 3c. Use your DAVID
or GSEA results and create a plot with the same information as 3F using your
findings.     

2. Read their discussion of their results and specifically address the following
in your provided notebook:

  - Compare how many significant genes are up- and down-regulated in their
  findings and yours (using their significance threshold). Ensure you list how 
  many you find vs. how many they report. 

  - Compare their enrichment results with your DAVID and GSEA analysis. Comment
  on any differences you observe and why there are discrepancies.

## Write a methods section for your pipeline

We will have briefly discussed how to write a methods section. Please write a 
methods section for the workflow you've implemented with your pipeline in the 
style we've discussed. 

1. In your notebook, write a brief methods section for your workflow

2. Read the methods for the paper and in your provided notebook, please ensure
you briefly discuss any differences in the methods you used and how that may
change what results you find. 

## Copy the provided discussion questions into your notebook and answer them

I have made a separate repo with a Rmd containing a few conceptual questions
related to the project. Please copy these questions into your notebook (the one
where you've been doing your analysis) and do your best to answer them. 
A few of the questions have a "correct" answer, but several of them are more
conceptual in nature and I am looking mostly at your thought process. 

## Week 4 Detailed Tasks Summary

1. Read the original publication and focus specifically on the RNAseq experiment

2. Recreate figures 3C and 3F with your own results and ensure you address the
listed questions in your notebook

3. Write a methods section in the style we've discussed for your workflow

4. Address the additional questions provided to you in your notebook
