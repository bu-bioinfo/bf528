---
title: "Project 1: Genome Assembly"
layout: single
---

# Project Overview

For this first project, you will be developing a nextflow pipeline to assemble
a bacterial genome from long and short read sequencing data. You will be provided
a scaffold of the nextflow pipeline and asked to implement the various steps
outlined in the pipeline. You will not have to complete the entire pipeline, but
will instead be asked to focus on various aspects of the workflow as we progress
and get more comfortable with the tools and concepts. This project is broken up
into weeks and each week will focus on different tasks. Future projects you will
be working in a more open-ended manner and will be asked to implement the entire
pipeline on your own. 

For this week, you will be given a scaffolded nextflow pipeline and every week,
we will continue to update and refine it until it resembles a final pipeline. 
The weeks after the first will include the previous week's pipeline as well as
additional improvements. 

# Week 1 Overview

As we will discuss in class, hybrid assembly approaches combine the benefits of
both long and short read sequencing technologies. The long read sequencing
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
generate appropriate computational environments and look into the commands
required to perform QC on the sequencing data. YOu will then finish by running 
an assembly algorithm to assemble the reads into a consensus sequence. 

## Week 1 - Setting up

For this week, I have provided you a fully working nextflow pipeline that will
let you see how it works while focusing just on learning a few key concepts
we will be using throughout the semester. 

1. Please clone the github repo for this project - you may find the link on blackboard

2. Familiarize yourself with the directory you are working in. Throughout the semester,
we will be using the same structure and organization in all of the projects. 




# Week 2 - Modularizing our pipeline

You may have noticed from the first week that our pipeline is becoming 
increasingly complex and slightly onerous to read in a single file. In this week,
we are going to refactor our workflow to make it more modular and easier to read.
This modularity will have the secondary benefit of making it easier to reuse
components of the pipeline in future projects or even share it with others. 

## Week 2 Objectives

For this week, you will again be given a working pipeline but this time, I will
ask you to focus on connecting the processes by filling out the nextflow workflow.
You will need to 
