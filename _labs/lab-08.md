---
title: "Lab 08"
layout: single
---

# Lab 08 - Genome Browsers

## Objectives

- Develop a nextflow workflow to align using both bowtie2 and STAR, sort and index the BAMs, and generate bigWig coverage tracks
- Use IGV to visualize the alignments and compare the difference between splice-aware and splice-unaware aligners on mRNAseq data

## Directions

Copy the /projectnb/bf528/materials/lab07_template/visualization/ directory to your directory here, we will use
it later. 

I have provided you with modules and a config file that should enable you to perform the required tasks.
You will need to put together the workflow portion in order to do the following:

1. Build indexes for the sequence from human (hg38) chr16 using bowtie2 and STAR
2. Align the sample named bowtie2 (bowtie2_R1, bowtie2_R2) using bowtie2 and the
   sample named star (star_R1, star_R2) using STAR (There is an operator for this)
3. Sort and index the two resulting BAM files
4. Generate a bigWig coverage track for both of the BAM files

The samples have been made smaller so you may run this workflow with singularity
locally. (-profile singularity,local)

## Genome Browser - IGV

Do your best to get your workflow working to do the above steps. However, in case things are still running,
you may find the results from this workflow here: /projectnb/bf528/materials/lab07_template/visualization/.

You may copy that entire directory here. 

We are going to use the Desktop interactive session on SCC to utilize the browser app of IGV to look at the
alignments and coverage track we generated. 
