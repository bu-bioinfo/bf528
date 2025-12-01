---
title: Final Project
layout: single
---

The final project will ask you to develop and implement a full bioinformatics
pipeline for a real-world dataset, focusing on the prinicples of reproducibility
and portability we've discussed throughout the semester. 

You will have your choice of two options, the first being a publication
focused on chromatin accessiblity as assayed by ATACseq. You will be asked to 
generate an end-to-end pipeline for experiment and replicate some of their key
figures.

You may also choose to analyze a dataset of your own choosing, provided it meets
a few basic requirements:

1. It must be a dataset that has been published in a peer-reviewed journal
2. You must have access to the raw data
3. You must meet with me to discuss your project and get approval before proceeding
- This is largely to ensure that the work will be feasible and that you will be
doing roughly the same amount of work as the ATACseq project.

You will be given a rough outline of the steps your workflow should perform as
well as a list of deliverables to generate. When in doubt, you may refer back
to the original publication for additional details or guidance on specific steps.

# Universal Guidelines

No matter which project you choose, you will be asked to adhere to several 
guidelines following practices we've developed over the semester.

## Workflow Manager

1. You must use Nextflow to generate a working pipeline for your project. You
should use the same structure as each of the previous projects.

2. Each of your processes must be split into separate modules

3. Your workflow should be driven by either a samplesheet.csv or a directory of files
   using the `Channel.fromFilePairs` function. It should download the files as
   necessary.

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

The publication for this project is here: https://pubmed.ncbi.nlm.nih.gov/38829740/

**You only need to process the ATACseq data**


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
10. Annotation of differentially accessible peaks
11. Motif finding of differentially accessible peaks
12. Reproduce figures 6a-6f (it's only three distinct figures from two conditions)


## Deliverables

Your project should consist of:

1. A Nextflow workflow that implements the above steps in your github classroom repository
2. A README.md file in your github classroom repository that describes how to run your pipeline
3. A Jupyter notebook or Rmarkdown file that contains the analysis code
4. A report that addresses the deliverables outlined below.


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

4. Report how many differentially accessible regions your pipeline discovered
in each of the two conditions.

5. A figure showing the enrichment results of the differentially accessible
regions and a few sentences describing what the enrichment reveals.

6. A figure showing the motif enrichment results from the differential peaks and 
a few sentences describing the key motifs found.

7. Comment on the success of the reproductions of the panels from the original
publication. Do you think the results are consistent with the original publication?
What do your results show that is different from the original publication?


# Project 2: Your Choice

If choosing your own project, your workflow steps will look different and you should
determine the steps necessary to generate the results you want. You can of course
refer to the methods found in the original publication for guidance. 

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
3. You must produce *two* experiment specific QC metrics
- Alignment Statistics
- Sequence Quality Control
- Experiment-specific metrics (fingerprint plot, sample-sample distance matrix, etc.)

Comment, in no less than a paragraph, on each of your chosen two QC 
metrics and what they mean about the success of the experiment. 

4. Comment on the success of the reproductions of the panels from the original
publication. Do you think the results are consistent with the original publication?
What do your results show that is different from the original publication?

