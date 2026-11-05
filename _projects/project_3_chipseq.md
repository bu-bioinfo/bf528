---
title: "Project 3: ChIPseq"
layout: single
---

{% assign report = site.baseurl | append: "/projects/project_3_report/" %}

# Workflow Visualization

![workflow]({{ site.baseurl }}/assets/images/project-3-workflow-diagram.svg)

# Project 3 Instructions

Now that we have experience with Nextflow from two prior projects, the
directions for this project will be much less detailed. I will describe what you
should do and you will be expected to implement it yourself. If you are asked to 
perform a certain task, you should create working nextflow modules, construct
the proper channels in your `main.nf`, and run your workflow. 

Please follow all the conventions we've established so far in the course.

These conventions include:

  1. Using isolated containers specific for each tool 
  2. Writing extensible and generalizable nextflow modules for each task
  3. Declaring records for the inputs and outputs of each process and using
  static typing for your params, process inputs and outputs
  4. Encoding reference file paths in the `nextflow.config`
  5. Encoding sample info and sample file paths in a csv that drives your workflow
  6. Requesting appropriate computational resources per job
  7. Including a `stub` block in every process

## Fill out the specifications.md provided

Before you start any work on the pipeline, fill out the sections in the provided
`specifications.md`. This is meant to give you practice thinking at a high-level
about what your pipeline is doing, how it is behaving, and which points are critical
for you to review or validate. This will become especially important to keep in
mind once you start using agentic coding harnesses to develop workflows. 

## Important Note for developing your workflow

As in project 2, you should always include a `stub` block in every process that
uses `touch` to generate fake versions of the outputs your process expects. Until
you are 100% confident your workflow performs as expected, you should always run
it with:

```bash
nextflow run main.nf -stub
```

This is really important for this project since the real data is quite large
and you will only run it with the full data once you are sure that your pipeline
has the desired behavior. 

# Containers for Project 3

FastQC: `ghcr.io/bu-cds-bf528/fastqc:latest`

MultiQC: `ghcr.io/bu-cds-bf528/multiqc:latest`

Bowtie2: `ghcr.io/bu-cds-bf528/bowtie2:latest`

deepTools: `ghcr.io/bu-cds-bf528/deeptools:latest`

Trimmomatic: `ghcr.io/bu-cds-bf528/trimmomatic:latest`

Samtools: `ghcr.io/bu-cds-bf528/samtools:latest`

Bedtools: `ghcr.io/bu-cds-bf528/bedtools:latest`

HOMER/Samtools: `ghcr.io/bu-cds-bf528/homer_samtools:latest`

# Phase 1: Blind analysis

## Overview

This was a ChIPseq experiment from human cell lines that generated two replicates,
each with an IP and an INPUT sample. This works out to four samples in total
(IP_rep1, IP_rep2, INPUT_rep1 and INPUT_rep2). The replicates are paired and
denoted by the suffix _rep1 and _rep2. The IP and INPUT for each
replicate originated from the same sample and should be used together when 
performing peak calling. 

IP (Immunoprecipitate) refers to the reads for the factor of interest and INPUT
refers to the reads for the control. The IP samples were the sequences enriched
for binding for our factor of interest. INPUT is used to normalize the IP reads
and allow us to make more robust inferences about enrichment of binding in the
IP relative to what we expected in the background or INPUT. 

For many NGS experiments, the initial steps are largely universal. We perform
quality control on the sequencing reads, build an index for the reference
genome, and align the reads. However, the source of the data will inform what
quality metrics are relevant and the particular choice of tools to accomplish
these steps. For RNAseq, it is important to use a splice-aware aligner when
aligning against a reference **genome** since our sequences originated from
mRNA. For ChIPseq experiments, our reads originated from DNA sequences and we
can use a non-splice aware algorithm to map our reads to the reference genome.

You will use this description of the samples to write the
[Experimental Design]({{ report }}#experimental-design-1-paragraph) section of
your report.

## Objectives

- Assess QC on sequencing reads using FastQC

- Trim adapters and low-quality reads using Trimmomatic

- Build a bowtie2 index for the human reference genome

- Align trimmed reads to the human reference genome

- Run samtools flagstat to assess alignment statistics

- Use MultiQC to aggregate all of the QC metrics

- Use samtools to sort and index your BAM (alignment) files

- Generate bigWig files from your BAM files using deepTools bamCoverage

## Quality Control, Genome indexing and alignment

Between the past projects and the early labs we did, you should have working modules
that perform quality control using FastQC, build a genome index
using bowtie2, and align reads to a genome. We are going to take advantage of
the modularity of nextflow and you can simply copy these working modules to this
repo.

The samples termed IP are the samples of interest (IP for a factor of interest)
and the samples labeled INPUT are the control samples. Remember ChIP-seq experiments
are paired (e.g. INPUT_rep1 is the control for IP_rep1)

1. Use the provided CSV files that point to both the subsampled and full files.
When you are developing the beginning of your workflow, use the subsampled files
(they will not work once you get to the peak calling step). I have made the initial
channel for you. You will switch to the full data before peak calling, as
described in [Switching to the full data](#switching-to-the-full-data).

**Please note that the subsampled_files are named differently than the full files!**

2. The paths to the human reference genome, GTF and a few other critical files
are already encoded in your `nextflow.config`. 

3. Update your workflow `main.nf` to perform quality control using FastQC and
trimmomatic, build a bowtie2 index for the human reference genome and align the
reads to the reference genome. Remember that we have worked on code for bowtie2 
build, bowtie2 align, multiqc, samtools sort, samtools index, and deeptools 
bamCoverage in labs.

**N.B. Some of the code from the labs will need to be modified to work for this specific experiment (paired end vs. single end, etc.)**

Remember to construct input and output records based on what you expect each
process to need and produce. 

## Sorting and indexing the alignments

Many subsequent analyses on our BAM files will require them to be both sorted
and indexed. Just like for large sequences in FASTA files, sorting and indexing
the alignments will allow us to perform much more efficient computational
operations on them.

1. Create modules that will sort and index your BAM files using Samtools. 

## Calculate alignment statistics using samtools flagstat

The samtools flagstat utility will report various statistics regarding the
alignment flags found in the BAM.

1. Create a module that will run samtools flagstat on all of your BAM files

## Aggregating QC results with MultiQC

Just like in project 2, we are going to use multiqc to collect the various
quality control metrics from our pipeline. Ensure that multiqc collects the
outputs from FastQC, Trimmomatic and flagstat. 

1. Make a channel in your workflow `main.nf` that collects all of the relevant
QC outputs needed for multiqc (fastqc zip files, trimmomatic log, and samtools
flagstat output)

2. Copy your previous multiqc module and incorporate it into your workflow to 
generate a MultiQC report for the listed outputs

You will use this MultiQC report for the
[Read Quality Control]({{ report }}#read-quality-control-1-2-paragraphs)
section of your report.

## Generating bigWig files from our BAM files

Now that we have sorted and indexed our alignments, we are going to generate
bigWig files or coverage tracks containing the number of reads per genomic
interval or bin for each sample. We will use these coverage tracks for calculating
correlation between our samples and visualizing the read coverage in specific
regions of interest. 

1. Use the `bamCoverage` deeptools utility to generate a bigWig file for each
of the sample BAM files. 

2. You may use all default parameters. If you wish, you may change the `-bs` and
`-p` flags as needed. 

## Create and use a single Jupyter notebook for any images, reports or written discussion

Please create a single jupyter notebook (.ipynb) that contains all of the 
requested figures, images or discussion described in the
[Project 3 report]({{ report }}). Please
create a dedicated .yml file that specifies any needed packages (including
an up-to-date installation of `ipykernel`). You may refer to the website for
instructions on how to do this.

This will enable your notebook to utilize the conda environment described in that
yml file and ensure that your analysis is done in a reproducible and potentially
portable manner.

## Plotting correlation between bigWigs

Recall that the bigWigs we generate represent the count of reads falling into
various genomic bins of a fixed size quantified from the alignments of each sample.
Assuming the experiment was successful, we naively expect that the IP samples 
should be highly similar to each other as they should be capturing the same
binding sites for the factor of interest. Following this logic, the input controls
which represent a random background of DNA from the genome should be *different*
from the IP samples and somewhat more similar to each other. 

We are going to perform a quick correlation analysis between the distances in
our bigWig representations of our BAM files to determine the similarity between
our samples with the above assumptions in mind.

1. Create a module and use the `multiBigwigSummary` utility in deeptools to create
a matrix containing the information from the bigWig files of all of your
samples.

2. Create a module and use the `plotCorrelation` utility in deeptools to generate
a plot of the distances between correlation coefficients for all of your samples.
You will need to choose whether to use a pearson or spearman correlation. In
a notebook you create, provide a short justification for what you chose. 

You will display and discuss this plot in the
[Sample Quality Control]({{ report }}#sample-quality-control-2-paragraphs)
section of your report.

## Create a Fingerprint Plot  

We discussed in class how fingerprint plots show how well the signal in a ChIPseq
sample can be distinguished from the background distribution of reads in the 
control. The basic intuition is that an ideal input would have a perfectly uniform
distribution of reads across the genome. A very specific and strong ChIPseq sample
should have a large proportion of its reads concentrated in a subset of regions 
(i.e. the regions the factor prefers to bind) as compared to the entire genome.

Conceptually, this plot bins the genome into intervals and counts how many alignments
fall into each bin. It then ranks the bins and plots the cumulative sum.

1. Create a module and use the `plotFingerprint` utility in Deeptools to generate
a fingerprint plot for all of your samples.

You will display and discuss this plot in the
[Sample Quality Control]({{ report }}#sample-quality-control-2-paragraphs)
section of your report.

## Switching to the full data

The subsampled files will not produce meaningful results for peak calling, so
you will need to switch to the full data before moving on. Once your stub runs
confirm that your workflow behaves as expected end-to-end, and your pipeline
runs successfully on the subsampled files up to this point, we are going to
apply our workflow to the original samples. Ensure that you requested a VSCode
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
nextflow run main.nf -profile singularity,cluster
```

You may examine the progress and status of your jobs by using the `qstat` utility
as discussed in lecture and lab. 

## Peak calling using HOMER

In plain terms, peak calling algorithms attempt to find areas of enriched reads
in a genome relative to background noise. HOMER is a commonly used tool that 
incorporates a Poisson model and other methodologies to make robust peak-finding
predictions. Generate a nextflow module and workflow that runs [HOMER](http://homer.ucsd.edu/homer/ngs/peaks.html)

1. Generate a module that runs `makeTagDirectory` on each of your BAM files

2. Generate a module that runs `findPeaks` on each of your tag directories
- Ensure that you specify the `-style factor` flag correctly for the samples

3. **You will need to figure out how to pass both the IP and the INPUT sample
for each replicate to the same command**. i.e. `findPeaks` should run twice
(IP_rep1 and INPUT_rep1) and (IP_rep2 and INPUT_rep2) as ChIP-seq
experiments have paired IP and INPUT samples. The rep1 samples were derived from the
same biological material and are a biological replicate for the rep2 samples. 
You will end up with two sets of peak calls, one for each replicate pair. 

4. HOMER generates a TXT file containing the peak outputs. Typically, we want
to work with peaks in the BED format. Generate a nextflow module that uses the
HOMER `pos2bed.pl` utility to convert the peak outputs to BED format.

## Generating a set of reproducible peaks with bedtools intersect

We discussed various strategies for determining a set of "reproducible" peaks. 
For the sake of expedience, we will be performing a simple intersection to come 
up with a single set of peaks from this experiment. **Please come up with a valid
intersection strategy for determining a reproducible peak. Remember that this choice
is subjective, so make a choice and justify it**

Generate a nextflow module and workflow that runs bedtools intersect to generate
a set of reproducible peaks.

1. Use the bedtools `intersect` tool to produce a single set of reproducible
peaks from both of your replicate experiments.

2. In your created notebook, please provide a quick statement on how you chose
to come up with a consensus set of peaks. 

You will report your peak counts and justify your intersection strategy in the
[Peak Calling and Filtering]({{ report }}#peak-calling-and-filtering-1-2-paragraphs)
section of your report.

## Filtering peaks found in ENCODE blacklist regions

In next generation sequencing experiments, there are certain regions of the
genome that have been empirically determined to be present at a high level
independent of cell line or experiment. These unstructured and anomalous regions
are problematic for certain analyses (ChIPseq) and are considered to be
signal-artifact regions and commonly stored in the form of a [blacklist](https://www.nature.com/articles/s41598-019-45839-z)

The Boyle Lab as part of the ENCODE project have very kindly produced a list of
these regions in some of the major model organisms using a standard methodology.
This list is encoded as a BED file and is hosted by the [Boyle
Lab](https://github.com/Boyle-Lab/Blacklist). Please encode the path to the
blacklist in your params, you may find the file in the refs/ directory under
materials/ for project 3. 

1. Create a module that uses bedtools to remove any peaks that overlap with the
blacklist BED for the most recent human reference genome. Generally speaking,
you can remove a peak if it overlaps a blacklisted region by even 1bp as that is
sufficiently close to consider it a signal-artifact region.

The number of peaks remaining after filtering is also reported in the
[Peak Calling and Filtering]({{ report }}#peak-calling-and-filtering-1-2-paragraphs)
section of your report.

## Annotating peaks to their nearest genomic feature using HOMER

Now that we have a single set of reproducible peaks with signal-artifact blacklisted
regions removed, we are going to annotate our peaks by assigning them an identity
based on their closest genomic feature. While we have discussed many caveats to 
annotating peaks in this fashion, it is a quick and exploratory analysis that 
enables quick determination of the genomic structures your peaks are located in and
their potential regulatory functions. You may find the manual page for HOMER and
this utility [here](http://homer.ucsd.edu/homer/ngs/annotation.html)

1. Create a module that uses HOMER and the `annotatePeaks.pl` script to annotate
your BED file of reproducible peaks (filtered to remove blacklisted regions).

2. **You should directly provide both a reference genome FASTA and the
matching GTF to use custom annotations.** Look further down the directions page
for the argument order. This will make use of your params for the reference
fasta and the GTF.

You will use these annotated peaks in the
[Annotation and Enrichment Analysis]({{ report }}#annotation-and-enrichment-analysis-2-3-paragraphs)
section of your report, and again when
[integrating with the RNAseq results]({{ report }}#integrating-your-peaks-with-their-rnaseq-results-3-4-paragraphs)
in Phase 2.

## Download an hg38 gene BED from UCSC table browser

We will be creating a plot which will provide a quick visualization of
the average signal across the gene body of all genes. We will scale every gene
to a uniform size and display the counts of alignments falling in the annotated
regions of the gene. This will allow us to quickly visualize at a very
high-level where we see the majority of binding for our factor of interest.

To do this, we have already generated our bigWig files, but we will require the
genomic coordinates of all of the genes in the reference genome. We will be
using the UCSC table browser to extract out this information.

Navigate to the [UCSC Table Browser](https://genome.ucsc.edu/cgi-bin/hgTables),
use the following settings to extract a BED file listing the TSS/TTS locations
for every gene in the reference genome:

![ucsc_tablebrowser]({{ site.baseurl }}/assets/images/ucsc_tablebrowser.png)

On the following page, do not change any options and you will be prompted to
download a BED file containing the requested information. Ensure that you select
the radio button for "Genome" and not "Position" so that your BED files has the
chromosome, start, and end positions of every gene in the reference genome and
not a selected region. 

1. Put this BED file into your `refs/` working directory on SCC. 

I have also provided this bed file in the materials/ directory for project 3.

This is a simple use case, but the UCSC table browser and UCSC genome browser
are incredibly powerful tools and repositories for genome-wide sequencing data.

## Generating a signal intensity plot for all human genes using computeMatrix and plotProfile for IP samples

Now that we have our bigWig files (count of reads falling into bins across the
genome) and the BED file of the start and end position of all of the genes in 
the hg38 reference, we will calculate and visualize the signal falling into 
these annotated regions focusing on the TSS/TES.

1. Use the `computeMatrix` utility in deeptools, your bigWig files, and the BED
file you downloaded to generate a matrix file containing the counts of reads
falling into the regions in the bed files. 

2. Ensure that you use the scale-regions mode, and you specify the options to add
2000bp of padding to both the start and end site. 

3. We are not interested in visualizing the input samples (which should represent
random background noise), use an appropriate nextflow operator to ensure this is 
only done for the IP samples. 

4. Use the outputs of `computeMatrix` for the `plotProfile` function and generate
a simple visualization of the read counts from the IP samples across the body of
genes from the hg38 reference. 

You will display and discuss this plot in the
[Signal Coverage Plot]({{ report }}#signal-coverage-plot-1-2-paragraphs)
section of your report.

## Finding enriched motifs in ChIP-seq peaks

We will be using the single set of reproducible and filtered peaks from Phase 1
to search for enriched motifs in our peaks. Many DNA binding proteins have been
found to have higher affinity for specific DNA binding sites with recurring sequence
and pattern. These motifs may reveal key information about gene regulation by
allowing for determination of what factors are binding in peaks. Remember that 
many DNA binding proteins bind as part of much larger multi-protein complexes that
work in tandem to regulate gene expression. We will be using the HOMER tool
to perform motif enrichment, you may find the manual [here](http://homer.ucsd.edu/homer/ngs/peakMotifs.html)

1. Use the `findMotifsGenome.pl` utility in HOMER to perform motif enrichment
analysis on your set of reproducible and filtered peaks. 

You will use the knownResults output in the
[Motif Finding]({{ report }}#motif-finding-1-2-paragraphs)
section of your report.

## Setting up the publish and output blocks

Use a `publish:` section inside of your `workflow` block and an `output` block
below it to send your key results to the `results/` directory for easy access.
Refer to the past examples in labs, project 2 or the nextflow documentation.
At minimum, publish the following:

- The MultiQC report
- The correlation plot from `plotCorrelation`
- The fingerprint plot from `plotFingerprint`
- The bigWig files for each sample (you will need these in Phase 2)
- The reproducible and filtered peaks BED file
- The annotated peaks from `annotatePeaks.pl`
- The signal intensity plot from `plotProfile`
- The motif enrichment results from `findMotifsGenome.pl`

## Analyze the annotated peaks

Use your annotated peaks list and perform an enrichment method of your choice.
This is purposefully open-ended, so you may consider filtering your peaks by
different categories before performing some kind of enrichment analysis. There
are a few peak / region based enrichment methods (GREAT) in addition to standard
methods used such as DAVID / Enrichr.

What to report is described in the
[Annotation and Enrichment Analysis]({{ report }}#annotation-and-enrichment-analysis-2-3-paragraphs)
section of your report.

## Write a methods section

Write a methods section for the complete analysis workflow implemented by your
pipeline, following the guidelines in the
[Methods]({{ report }}#methods-as-long-as-needed) section of your report.

# Phase 2: Informed analysis

**Reminder**

When you are asked to re-create the same figures found in the original publication
with your own results, remember that this is not meant to assert that one approach
or one set of results are the only right answer.

In science, we are constantly making assumptions and subjective choices, ideally
based on sound logic and past knowledge, that will greatly impact the
interpretation of the results we obtain. The purpose of this exercise is to
explore the factors that contribute to reproducibility in bioinformatics and
develop an understanding of what it means for an experiment or publication to be
"reproducible".

## Read the original paper

At the end of the 2nd week, the original publication will be posted to blackboard.
Please read through the paper with a particular focus on the ChIP-Seq experiment
presented in figure 2. This begins
[Phase 2]({{ report }}#phase-2-informed-analysis) of your report.

## Overlap your ChIPseq results with the original RNAseq data

In their publication find the link to their GEO submission and download their
differential expression RNAseq results. You will integrate **your** reproducible
and filtered peaks with **their** RNAseq results, using the publication's listed
significance thresholds. You may do this in python using pandas or R using
tidyverse / ggplot, starting by reading the RNAseq results and your annotated
peaks as dataframes.

You will likely not be able to exactly reproduce what the authors did for
figure 2F. Use the promoter-TSS start site from your annotated peaks in place of
the gene body.

For figures 2D and 2E, you will need your bigWig files, your filtered and
reproducible peaks, and a genome browser of your choice.

The figures to produce and questions to answer are in the
[Integrating Your Peaks with Their RNAseq Results]({{ report }}#integrating-your-peaks-with-their-rnaseq-results-3-4-paragraphs)
section of your report.

## Comparing key findings to the original paper

Find the supplementary information for the publication, focusing on
supplementary figures S2A, S2B, and S2C. You will need your MultiQC report,
your correlation plot, and your per-replicate and reproducible peak sets.

The figures to produce and questions to answer are in the
[Comparing Sequencing and Peak Results]({{ report }}#comparing-sequencing-and-peak-results-3-4-paragraphs)
section of your report.

