---
title: "Project 1: Genome Assembly"
layout: single
---


## Project Overview

For this first project, you will be developing a nextflow pipeline to assemble
a bacterial genome from long and short read sequencing data. You will be provided
a scaffold of the nextflow pipeline and asked to implement the various steps
outlined in the pipeline. You will not have to complete the entire pipeline, but
will instead be asked to focus on various aspects of the workflow as we progress
and get more comfortable with the tools and concepts.

## Section Links

[Week 1 Overview](#week-1-overview)

[Objectives](#objectives)


## Week 1 Overview

For this project, you will be assembling a bacterial genome from both nanopore 
and Illumina sequencing data. As we discussed in class, the long read sequencing
provides improved contiguity and longer reads, which can better capture regions
of the genome previously difficult to sequence using short reads. This is especially
useful during genome assembly, where the longer reads are more likely to span
all regions of the genome, greatly aiding in the assembly process. However,
short reads are still useful and are commonly utilized to "polish" the assembly
and remove systematic errors from the assembly of the long reads. 

We will be generating a nextflow pipeline that will perform the following steps:

1. Quality Control of the sequencing data
2. Assembly of the nanopore reads
3. Polishing of the nanopore assembly with the Illumina reads
4. Quality Control of the polished assembly and comparison the reference genome
5. Annotation of the genome and visualization of genomic features

## Week 1 Objectives

For the first week, we will be performing QC on the all of the sequencing reads
and you will be asked to focus on understanding how to read data from a CSV file
into a nextflow channel and pass it to a process. You will also be asked to 



