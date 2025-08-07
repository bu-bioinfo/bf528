---
title: Final Project
layout: single
---

The final project will ask you to develop and implement a full bioinformatics
pipeline for a real-world dataset, focusing on the prinicples of reproducibility
and portability we've discussed throughout the semester. 

You will have your choice of two datasets stemming from published work that
focused on chromatin accessiblity and alternative splicing, respectively. You 
will be asked to generate an end-to-end pipeline for each dataset, including
reproducing several of their key results and figures. 

You will be given a rough outline of the steps your workflow should perform as
well as a list of deliverables to generate. When in doubt, you may refer back
to the original publication for additional details or guidance on specific steps.

# Universal Guidelines

No matter which dataset you choose, you will be asked to adhere to several 
guidelines following practices we've developed over the semester.

## Workflow Manager

1. You must use Nextflow to generate a working pipeline for your project. You
should use the same structure as each of the previous projects.

You may see a template repo here: https://github.com/bf528/final_project_template

2. Each of your processes must be split into separate modules

3. Your workflow should be driven by either a samplesheet.csv or a directory of files
   using the `Channel.fromFilePairs` function

## Environment Management

You must use either conda or singularity to manage your environments.

1. If you choose to use conda:
- Each tool should have its own conda environment and YML file
- You should pin the most recent version of each tool

2. If you choose to use singularity:
- Each tool should have its own singularity image
- Containers should be from the class repo or another vetted source (biocontainers, etc.)

## Github Repository

Your entire workflow must be stored in a github repository provided to you 
by the GitHub Classroom link for the final project. Your repo should **not**
contain any data or large files, but your entire workflow and analysis code. Any
analysis code should be contained within either a Rmarkdown or Jupyter notebook.

Your repo must contain a README.md file with the following information:

- A description of the source of the data and publication
- How to run your pipeline
- The deliverables required for the project


# Project 1: ATAC-seq and Differential Chromatin Accessibility

The publication for this project is here:


Your workflow at a high-level should do the following:

1. Download the data from the publication
2. Sequence quality control on the raw reads
3. Adapter trimming (if necessary) and quality filtering
4. Alignment to the reference genome using ATACseq specific parameters
5. Remove any alignments aligning to mitochondrial DNA
6. Correct the alignemnts by shifting +4/-5 for the positive and negative strand
respectively 
7.*OPTIONAL* Split your dataset into the nucleosome-free (NFR) and nucleosome-bound
(NBR) fractions. If you choose to do this, please justify why and make it clear 
which fraction you are working with for each subsequent analysis. 
8. Peak calling
9. Differential chromatin accessibility analysis
10. Annotation of called peaks
11. Motif finding of differential peaks


## Deliverables

Your project should consist of:

1. A Nextflow workflow that implements the above steps in your github classroom repository
2. A README.md file in your github classroom repository that describes how to run your pipeline
3. A Jupyter notebook or Rmarkdown file that contains the analysis code
4. A report that addresses the deliverables outlined in the [Project Report Guidelines]({{ site.baseurl }}/project_report_guidelines/)


The specific deliverables pertaining to the results for this project that should
be included in your report are:

1. A brief discussion (1 paragraph) of the sequencing quality control results and
any steps taken to address any identified issues
2. A brief discussion (1 paragraph) of the alignment statistics, and what they
mean for your analysis
3. You must produce *two* ATAC-seq specific QC metrics from the following list:

- TSS enrichment score
- Fragment Size Distribution
- Heatmap of signal across TSS split between NFR and NBR
- Fraction of Reads in Peak (FRiP)

Comment, in no less than a paragraph, on each of your chosen two ATAC-seq QC 
metrics and what they mean about the success of the experiment. 







# Project 2: Long-read sequencing and alternative splicing analysis

The publication for this project is here:

Your workflow should do the following:


## Deliverables

