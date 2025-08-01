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


Your workflow should do the following:



## Deliverables


# Project 2: Long-read sequencing and alternative splicing analysis

The publication for this project is here:

Your workflow should do the following:


## Deliverables

