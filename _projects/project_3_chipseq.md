---
title: "Project 3: ChIPseq"
layout: single
---


# Week 1: ChIPseq

## Section Links

[Project 2 Directions](#project-2-directions)

[Week 1 Overview](#week-1-overview)

[Objectives](#objectives)

[Containers for Project 2](#containers-for-project-2)

[Quality Control, Genome indexing and alignment](#quality-control-genome-indexing-and-alignment)

[Sorting and indexing the alignments](#sorting-and-indexing-the-alignments)

[Calculate alignment statistics using samtools flagstat](#calculate-alignment-statistics-using-samtools-flagstat)

[Aggregating QC results with MultiQC](#aggregating-qc-results-with-multiqc)

[Generating bigWig files from our BAM files](#generating-bigwig-files-from-our-bam-files)

[Week 1 Tasks Summary](#week-1-tasks-summary)

## Project 2 Directions

Now that we have experience with Nextflow from two prior projects, the
directions for this project will be much less detailed. I will describe what you
should do and you will be expected to implement it yourself. If you are asked to 
perform a certain task, you should create working nextflow modules, construct
the proper channels in your `main.nf`, and run your workflow. 

Please follow all the conventions we've established so far in the course.

These conventions include:

  1. Using isolated containers specific for each tool
  2. Write extensible and generalizble nextflow modules for each task
  3. Encoding reference file paths in the `nextflow.config`
  4. Encoding sample info and sample file paths in a csv that drives your workflow
  5. Requesting appropriate computational resources per job

## Week 1 Overview

For many NGS experiments, the initial steps are largely universal. We perform
quality control on the sequencing reads, build an index for the reference
genome, and align the reads. However, the source of the data will inform what
quality metrics are relevant and the particular choice of tools to accomplish
these steps. For RNAseq, it is important to use a splice-aware aligner when
aligning against a reference **genome** since our sequences originated from
mRNA. For ChIPseq experiments, our reads originated from DNA sequences and we
can use a non-splice aware algorithm to map our reads to the reference genome.

## Objectives

- Assess QC on sequencing reads using FastQC

- Trim adapters and low-quality reads using Trimmomatic

- Align trimmed reads to the human reference genome

- Run samtools flagstat to assess alignment statistics

- Use MultiQC to aggregate all of the QC metrics

- Use samtools to sort and index your BAM (alignment) files

## Containers for Project 2

FastQC: `ghcr.io/bf528/fastqc:latest`

multiQC: `ghcr.io/bf528/multiqc:latest`

bowtie2: `ghcr.io/bf528/bowtie2:latest`

deeptools: `ghcr.io/bf528/deeptools:latest`

trimmomatic: `ghcr.io/bf528/trimmomatic:latest`

samtools: `ghcr.io/bf528/samtools:latest`

macs3: `ghcr.io/bf528/macs3:latest`

bedtools: `ghcr.io/bf528/bedtools:latest`

homer: `ghcr.io/bf528/homer:latest`

homer/samtools: `ghcr.io/bf528/homer_samtools:latest`

## Quality Control, Genome indexing and alignment

Between project 1 and the early labs we did, you should have working modules
that perform quality control using FastQC and trimmomatic, build a genome index
using bowtie2, and align reads to a genome. We are going to take advantage of
the modularity of nextflow by simply copying these previous modules and
incorporating them into this workflow.

The samples termed IP are the samples of interest (IP for a factor of interest)
and the samples labeled INPUT are the control samples. Remember ChIP-seq experiments
are paired (e.g. INPUT_rep1 is the control for IP_rep1)

1. Use the provided CSV files that point to both the subsampled and full files.
When you are developing the beginning of your workflow, use the subsampled files
(they will not work once you get to the peak calling step). 

**Please note that the subsampled_files are named differently than the full files!**

2. The paths to the human reference genome, GTF and a few other critical files
are already encoded in your `nextflow.config`. 

3. Update your workflow `main.nf` to perform quality control using FastQC and
trimmomatic, build a bowtie2 index for the human reference genome and align the
reads to the reference genome. Remember that we have worked on code for
trimmomatic and bowtie2 in the labs.

**N.B. Some of the code from the labs will need to be modified to work for this specific experiment (paired end vs. single end, etc.)**

## Sorting and indexing the alignments

Many subsequent analyses on our BAM files will require them to be both sorted
and indexed. Just like for large sequences in FASTA files, sorting and indexing
the alignments will allow us to perform much more efficient computational
operations on them.

1. Create a module(s) that will both sort and index your BAM files using Samtools. 

## Calculate alignment statistics using samtools flagstat

The samtools flagstat utility will report various statistics regarding the
alignment flags found in the BAM.

1. Create a module that will run samtools flagstat on all of your BAM files

## Aggregating QC results with MultiQC

Just like in project 1, we are going to use multiqc to collect the various
quality control metrics from our pipeline. Ensure that multiqc collects the
outputs from FastQC, Trimmomatic and flagstat. 

1. Make a channel in your workflow `main.nf` that collects all of the relevant
QC outputs needed for multiqc (fastqc zip files, trimmomatic log, and samtools
flagstat output)

2. Copy your previous multiqc module and incorporate it into your workflow to 
generate a MultiQC report for the listed outputs

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

## Week 1 Tasks Summary

- Create nextflow modules that run the following tools:
  
  1. FastQC
  2. Trimmomatic
  3. Bowtie2-index

- Sort and index your bams using a single nextflow module and samtools

- Calculate alignment statistics using samtools flagstat

- Aggregate all of the QC output results from the previous tools using MultiQC

- Generate a nextflow module that uses deeptools to create bigWig representations
of your BAM files

## Week 2: ChIPseq

## Section Links

[Week 2 Overview](#week-2-overview)

[Objectives](#objectives)

[Containers for Project 2](#containers-for-project-2)

[Plotting correlation between bigWigs](#plotting-correlation-between-bigwigs)

[Peak calling using MACS3](#peak-calling-using-macs3)

[Generating a set of reproducible peaks with bedtools intersect](#generating-a-set-of-reproducible-peaks-with-bedtools-intersect)

[Filtering peaks found in ENCODE blacklist regions](#filtering-peaks-found-in-encode-blacklist-regions)

[Annotating peaks to their nearest genomic feature using HOMER](#annotating-peaks-to-their-nearest-genomic-feature-using-homer)

[Week 2 Tasks Summary](#week-2-tasks-summary)

## Week 2 Overview

For week 2, you will be performing a quick quality control check by plotting
the correlation between the bigWigs you generated last week. Then, you will be
performing standard peak calling analysis using MACS3, generating a single set
of reproducible and filtered peaks, and annotating those peaks to their nearest
genomic feature. 

## Objectives

- Plot the correlation between the bigWig representations of your samples

- Perform peak calling using MACS3 on each of the two replicate experiments

- Use bedtools to generate a single set of reproducible peaks with ENCODE
blacklist regions filtered out

- Annotate your filtered, reproducible peaks using HOMER

## Containers for Project 2

FastQC: `ghcr.io/bf528/fastqc:latest`

multiQC: `ghcr.io/bf528/multiqc:latest`

bowtie2: `ghcr.io/bf528/bowtie2:latest`

deeptools: `ghcr.io/bf528/deeptools:latest`

trimmomatic: `ghcr.io/bf528/trimmomatic:latest`

samtools: `ghcr.io/bf528/samtools:latest`

macs3: `ghcr.io/bf528/macs3:latest`

bedtools: `ghcr.io/bf528/bedtools:latest`

homer: `ghcr.io/bf528/homer:latest`

homer/samtools: `ghcr.io/bf528/homer_samtools:latest`

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

1. Create a module and use the multiBigwigsummary utility in deeptools to create
a matrix containing the information from the bigWig files of all of your
samples.

2. Create a module and use the plotCorrelation utility in deeptools to generate
a plot of the distances between correlation coefficients for all of your samples.
You will need to choose whether to use a pearson or spearman correlation. In
a notebook you create, provide a short justification for what you chose. 

## Peak calling using MACS3

In plain terms, peak calling algorithms attempt to find areas of enriched reads
in a genome relative to background noise. MACS3 (Model-Based Analysis of Chip-Seq)
is a commonly used tool that incorporates a Poisson model and other methodologies to 
make robust peak-finding predictions. Generate a nextflow module and workflow
that runs MACS3. 

1. Use the [MACS3 manual](https://macs3-project.github.io/MACS/docs/callpeak.html)
for the callpeak utility and create module that successfully runs `callpeak`

2. Ensure that you specify the `-g` flag correctly for the human reference genome

3. **You will need to figure out how to pass both the IP and the Control sample
for each replicate to the same command**. i.e. callpeak should run twice
(IP_rep1 and control_rep1) and (IP_rep2 and control_rep2) as ChIP-seq
experiments have paired IP and controls. The rep1 samples were derived from the
same biological material and is a biological replicate for the rep 2 samples. 
You will end up with two sets of peak calls, one for each replicate pair. 

## Generating a set of reproducible peaks with bedtools intersect

We discussed various strategies for determining a set of "reproducible" peaks. 
For the sake of expedience, we will be performing a simple intersection to come 
up with a single set of peaks from this experiment. **Please come up with a valid
intersection strategy for determine a reproducible peak. Remember that this choice
is subjective, so make a choice and justify it**

Generate a nextflow module and workflow that runs bedtools intersect to generate
a set of reproducible peaks.

1. Use the bedtools `intersect` tool to produce a single set of reproducible
peaks from both of your replicate experiments.

2. In your created notebook, please provide a quick statement on how you chose
to come up with a consensus set of peaks. 

## Filtering peaks found in ENCODE blacklist regions

In next generation sequencing experiments, there are certain regions of the
genome that have been empirically determined to be present at a high level
independent of cell line or experiment. These unstructured and anomalous regions
are problematic for certain analyses (ChIPseq) and are considered to be
signal-artifact regions and commonly stored in the form of a [blacklist](https://www.nature.com/articles/s41598-019-45839-z)

The Boyle LAB as part of the ENCODE project have very kindly produced a list of
these regions in some of the major model organisms using a standard methodology.
This list is encoded as a BED file and is hosted by the [Boyle
Lab](https://github.com/Boyle-Lab/Blacklist)/ Please encode the path to the
blacklist in your params, you may find the file in the refs/ directory under
materials/ for project 2. 

1. Create a module that uses bedtools to remove any peaks that overlap with the
blacklist BED for the most recent human reference genome. 

2. In your provided notebook, please write a short section on the strategy you
employed to remove blacklisted regions. Typically, any peaks that overlap a
blacklisted region by even 1bp will be removed. You may choose a different
strategy if you prefer as long as you justify your choice in the notebook you
create.

## Annotating peaks to their nearest genomic feature using HOMER

Now that we have a single set of reproducible peaks with signal-artifact blacklisted
regions removed, we are going to annotate our peaks by assigning them an identity
based on their closest genomic feature. While we have discussed many caveats to 
annotating peaks in this fashion, it is a quick and exploratory analysis that 
enables quick determination of the genomic structures your peaks are located in and
their potential regulatory functions. You may find the manual page for HOMER and
this utility [here](http://homer.ucsd.edu/homer/ngs/annotation.html)

1. Create a module that uses `homer` and the `annotatePeaks.pl` script to annotate
your BED file of reproducible peaks (filtered to remove blacklisted regions).

2. You can and should directly provide both a reference genome FASTA and the
matching GTF to use custom annotations. Look further down the directions page
for the argument order.

## Week 2 Tasks Summary

- Create nextflow modules and a script that performs the following tasks:
  
  1. Create a correlation plot between the sample bigWigs using deeptools 
  multiBigWigSummary and plotCorrelation
  2. Use MACS3 callpeak to perform peak calling on both replicate experiments
  3. Generate a single set of reproducible peaks using bedtools
  4. Filter peaks contained within the ENCODE blacklist using bedtools
  5. Annotate peaks to their nearest genomic feature using HOMER

## Week 3: ChIPseq

## Section Links

[Week 3 Overview](#week-3-overview)

[Objectives](#objectives)

[Containers for Project 2](#containers-for-project-2)

[Create and use a single Jupyter notebook for any images, reports or written discussion](#create-and-use-a-single-jupyter-notebook-for-any-images-reports-or-written-discussion)

[Download a HG38 gene BED from UCSC table browser](#download-a-hg38-gene-bed-from-ucsc-table-browser)

[Generating a signal intensity plot for all human genes using computeMatrix and plotProfile for IP samples](#generating-a-signal-intensity-plot-for-all-human-genes-using-computematrix-and-plotprofile-for-ip-samples)

[Finding enriched motifs in ChIP-seq peaks](#finding-enriched-motifs-in-chip-seq-peaks)

[Week 3 Tasks Summary](#week-3-tasks-summary)

## Week 3 Overview

In week 3, you will be using the UCSC table browser to obtain a BED file
containing the start and end positions of every gene in the HG38 human reference
genome. This will enable you to plot the signal coverage from your samples in
relation to genic structure (Transcription Start Site and Transcription
Termination Site). You will also be performing motif enrichment to determine
what motifs appear to be enriched in the binding sites detected in your peaks.

## Objectives

- Extract the TSS and TTS for every gene in the hg38 reference in BED format
using the UCSC table browser

- Use the deeptools utilities computeMatrix and plotProfile, the UCSC BED, and
your IP sample bigwigs to create a signal intensity plot

- Perform motif enrichment on your reproducible and filtered peaks using HOMER

## Containers for Project 2

FastQC: `ghcr.io/bf528/fastqc:latest`

multiQC: `ghcr.io/bf528/multiqc:latest`

bowtie2: `ghcr.io/bf528/bowtie2:latest`

deeptools: `ghcr.io/bf528/deeptools:latest`

trimmomatic: `ghcr.io/bf528/trimmomatic:latest`

samtools: `ghcr.io/bf528/samtools:latest`

macs3: `ghcr.io/bf528/macs3:latest`

bedtools: `ghcr.io/bf528/bedtools:latest`

homer: `ghcr.io/bf528/homer:latest`

homer/samtools: `ghcr.io/bf528/homer_samtools:latest`

## Create and use a single Jupyter notebook for any images, reports or written discussion

Please create a single jupyter notebook (.ipynb) that contains all of the 
requested figures, images or discussion requested. As in Project 0, please
create a dedicated .yml file that specifies any needed packages (including
an up-to-date installation of `ipykernel`). You may refer back to project 0
for how this setup works: https://bu-bioinfo.github.io/bf528/week-4-genome-analytics.html#make-a-conda-environment-with-pycirclize-and-ipykernel

This will enable your notebook to utilize the conda environment described in that
yml file and ensure that your analysis is done in a reproducible and potentially
portable manner.

## Download a HG38 gene BED from UCSC table browser

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

```{r, echo=FALSE}
knitr::include_graphics("projects/project_2_chipseq/ucsc_tablebrowser.png")
```

On the following page, do not change any options and you will be prompted to
download a BED file containing the requested information. 

    1. Put this BED file into your `refs/` working directory on SCC. 
    
I have also provided this bed file in the materials/ directory for project 2.

This is a simple use case, but the UCSC table browser and UCSC genome browser
are incredibly powerful tools and repositories for genome-wide sequencing data.

## Generating a signal intensity plot for all human genes using computeMatrix and plotProfile for IP samples

Now that we have our bigWig files (count of reads falling into bins across the
genome) and the BED file of the start and end position of all of the genes in 
the hg38 reference, we will calculate and visualize the signal falling into 
these annotated regions. 

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

5. In your created notebook, please write a short paragraph describing the figure
including details regarding how it was generated and what it appears to indicate
about your data. 

## Finding enriched motifs in ChIP-seq peaks

We will be using the single set of reproducible and filtered peaks from last week
to search for enriched motifs in our peaks. Many DNA binding proteins have been
found to have higher affinity for specific DNA binding sites with recurring sequence
and pattern. These motifs may reveal key information about gene regulation by
allowing for determination of what factors are binding in peaks. Remember that 
many DNA binding proteins bind as part of much larger multi-protein complexes that
work in tandem to regulate gene expression. We will be using the HOMER tool
to perform motif enrichment, you may find the manual [here](http://homer.ucsd.edu/homer/ngs/peakMotifs.html)

1. Use the `findMotifsGenome.pl` utility in homer to perform motif enrichment
analysis on your set of reproducible and filtered peaks. 

2. In the notebook you create, please make a table or take a screenshot of the top
ten enriched motifs that are found from the motif analysis.

3. Write a short paragraph discussing the top results you found and what you
believe the results indicate. 

## Week 3 Tasks Summary

- Use the UCSC table browser to generate a BED file containing the TSS and TTS
positions of every gene in the HG38 reference

- Create nextflow modules and update your script to perform the following tasks:

  1. Runs computeMatrix to generate a matrix containing the read coverage relative
  to the gene positions in the BED file
  
  2. Uses plotProfile to visualize the results generated by computeMatrix for 
  each of the two IP samples
  
  3. Utilizes HOMER to perform basic motif finding on your reproducible and 
  filtered peaks
  
## Week 4: ChIPseq

## Section Links

[Week 4 Overview](#week-4-overview)

[Objectives](#objectives)

[Use your already created jupyter notebook for the following analyses](#use-your-already-created-jupyter-notebook-for-the-following-analyses)

[Write a methods section](#write-a-methods-section)

[Comment on the sequence QC](#comment-on-the-sequence-qc)

[Read the original paper](#read-the-original-paper)

[Overlap your ChIPseq results with the original RNAseq data](#overlap-your-chipseq-results-with-the-original-rnaseq-data)

[Comparing key findings to the original paper](#comparing-key-findings-to-the-original-paper)

[Analyze the annotated peaks](#analyze-the-annotated-peaks)

[Address the provided discussion questions](#address-the-provided-discussion-questions)

[Week 4 Detailed Tasks Summary](#week-4-detailed-tasks-summary)

## Week 4 Overview

For the final week, you will be reading the original paper and interpreting
your results in the context of the publication's results. Specifically, you will
be focusing on reproducing the results shown in figure 2 with your own findings. 
This exercise is not meant to make any assertions as to the ground "truth" but
to encourage you think about reproducibility in science. 

**Reminder**

The tasks for this week will largely ask you to re-create the same figures found
in the original publication with your own results. Remember that this is not
meant to assert that one approach or one set of results are the only right answer.
In science, we are constantly making assumptions and subjective choices, ideally
based on sound logic and past knowledge, that will greatly impact the
interpretation of the results we obtain. The purpose of this exercise is to
explore the factors that contribute to reproducibility in bioinformatics and
develop an understanding of what it means for an experiment or publication to be
"reproducible".

## Objectives

- Read the original publication and focus specifically on the results and
discussion for figure 2

- Reproduce figures 2D, 2E and 2F from the paper

- Compare other key findings to the original publication

## Use your already created jupyter notebook for the following analyses

Use the jupyter notebook created last week for all of this week's analyses. 
Remember to choose the specified conda environment you created last week as the 
kernel for the notebook whenever you are working in it.

## Write a methods section

Using the style and guidelines discussed in class, write a methods section that
describes the analysis your nextflow pipeline performs. 

## Comment on the sequence QC

Use the multiqc report you generated (after you've rerun your workflow on the
full data) and write a brief paragraph commenting on the general quality of your
data and its suitability for analysis based on these metrics.

## Read the original paper

The original publication has been posted on blackboard. Please read through the
paper with a particular focus on the ChIP-Seq experiment presented in figure 2.

## Overlap your ChIPseq results with the original RNAseq data

In their publication find the link to their GEO submission. Read the methods
section of the paper and integrate **your** called ChIPSeq peaks with the results
from **their** differential expression RNAseq experiment. Use your set of
reproducible and filtered peaks, and use the publication's listed significance
thresholds for the RNAseq results.

1. You may do all of these steps in python using pandas or R using tidyverse /
ggplot. You may start by reading the RNAseq results and the annotated peak
results as dataframes.

2. Create a figure that displays the same information of figure 2F from the
original publication using your annotated peaks and the RNAseq results. The 
figure does not have to be the same style but must convey the same information
using your results.

3. In figures 2D and 2E, the authors identify and highlight two specific genes
that were identified in both experiments. Using your list of filtered and
reproducible peaks, a genome browser of your choice, and your bigWig files, please
re-create these figures with your own results (You do not need to include the
RNAseq data, but you should re-create the genomic tracks from your ChIPseq results)

4. In the notebook you created, please ensure you address the following questions:

  1. Focusing on your results for figure 2F:
    - Do you observe any differences in the number of overlapping genes from both
    analyses?
    - If you do observe a difference, explain at least two factors that
    may have contributed to these differences. 
    - What is the rationale behind combining these two analyses in this way? What
    additional conclusions is it supposed to enable you to draw?
    
  2. Focusing on your results for figures 2D and 2E:
    - From your annotated peaks, do you observe statistically significant peaks
    in these same two genes?
    - How similar do your genomic tracks appear to those in the paper? If you 
    observe any differences, comment briefly on why there may be discrepancies. 

## Comparing key findings to the original paper

Find the supplementary information for the publication and focus on supplementary
figure S2A, S2B, and S2C. 

1. Re-create the table found in supplementary figure S2A. Compare the results 
with your own findings. Address the following questions:

  - Do you observe differences in the reported number of raw and mapped reads?
  
  - If so, provide at least two explanations for the discrepancies. 
  
2. Compare your correlation plot with the one found in supplementary figure S2B. 

  - Do you observe any differences in your calculated metrics?
  
  - What was the author's takeaway from this figure? What is your conclusion
  from this figure regarding the success of the experiment?
  
3.  Create a venn diagram with the same information as found in figure S2C. 

  - Do you observe any differences in your results compared to what you see?
  
  - If so, provide at least two explanations for the discrepancies in the number
  of called peaks. 

## Analyze the annotated peaks

Use your annotated peaks list and perform an enrichment method of your choice. 
This is purposefully open-ended so you may consider filtering your peaks by
different categories before performing some kind of enrichment analysis. There are
a few peak / region based enrichment methods (GREAT) in addition to standard
methods used such as DAVID / Enrichr. 

1. In your created notebook, detail the methodology used to perform the enrichment.

2. Create a single figure / plot / table that displays some of the top results
from the analysis.

3. Comment briefly in a paragraph about the results you observe and why they 
may be interesting.

## Address the provided discussion questions

Answer any of the provided discussion questions in the notebook you created.
Please copy the questions and provide your answers in the same notebook you've
been performing your analyses. 

## Week 4 Detailed Tasks Summary

- Read the original publication with a particular focus on figure 2

- Write a methods section for the complete analysis workflow implemented by your
pipeline while adhering to the guidelines and style discussed in class

- Download the original publication's RNAseq results and apply their listed
significance threshold. Use this information to re-create figure 2F. 

- Re-create figures 2D and 2E and ensure you address the listed questions

- Find supplementary figure S2 and re-create or compare your findings to
supplementary figures 2A, 2B and 2C. Ensure you address any listed questions. 

- Perform an enrichment method using your annotated peaks and highlight the top
results

- Answer any provided discussion questions in your notebook

## Week 5: ChIPseq

## Discussion Questions

Please accept the github classroom link and do your best to answer the discussion
questions for project 2.

                https://classroom.github.com/a/5U-kGyNX

Please answer these questions to the best of your abilities. Most of these
questions are conceptual thought questions where we ask you to explain your
reasoning. Be brief! 

At the end, I've also asked you to display some of the key results / figures
generated from the workflow. This is more for me to assay how many of you were
able to successfully produce these results. You can compare on your own how well
you were able to reproduce the main biological findings from the original.

I will ask you to submit your answers by next week, after which, we will provide
you with feedback and comments in a timely manner. We will return this document
to you with this feedback, and ask you to resubmit your answers after another
week. If you address all of the comments and feedback in your resubmission, you
will receive full credit for this second project.

