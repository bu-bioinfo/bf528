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

# Week 1 - Quality Control

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

## Relevant Resources

- [Nextflow Operators](https://www.nextflow.io/docs/latest/reference/operator.html)
- [Nextflow Tutorial](https://training.nextflow.io/latest/hello_nextflow/)
- [CLI Resources]({{site.baseurl}}/guides/cli_resources/)
- [Computational Environments]({{site.baseurl}}/guides/computational_environments/)
- [Basic Conda]({{site.baseurl}}/guides/conda_guide/)
- [Nextflow Basics]({{site.baseurl}}/guides/nextflow_basics/)
- [Nextflow Channels]({{site.baseurl}}/guides/nextflow_channels/)

## Objectives 

For the first week, we will be performing QC on the all of the sequencing reads
and you will be asked to focus on understanding how to read data from a CSV file
into a nextflow channel and pass it to a process. You will also be asked to
generate appropriate computational environments and look into the commands
required to perform QC on the sequencing data. 

## Setting up

For this week, I have provided you a fully working nextflow pipeline that will
let you see how it works while focusing just on learning a few key concepts
we will be using throughout the semester. 

To start, open a VSCode session in your project directory (/projectnb/bf528/students/<your_username>/)

Remember to activate the conda environment you created for nextflow using the
following commands:

```bash
module load miniconda
conda activate nextflow_latest
```

1. Please clone the github repo for this project in your student folder - you may
find the link on blackboard.

2. In your student directory, you may use the following command to clone your
repo:

```bash
git clone <repo_url>
```

You should now have a directory called `project-1-genome-assembly-<your_username>`
in your student directory. 

3. Open this directory in your VSCode session. 

4. Familiarize yourself with the directory you are working in. Throughout the semester,
we will be using the same structure and organization in all of the projects.

## Tasks

### Creating a channel from a CSV file

1. Take a look at the channel_test.nf and run the following command:

```bash
nextflow run channel_test.nf -profile local,conda
```

2. Note what the output of the command is in your terminal window. 

3. Use the code in the channel_test.nf and move it to the specified location in
the main.nf file. Look at the nextflow documentation for an operator that will 
assign the values from the CSV to a channel and name this channel `bac_ch`. This 
operator should replace the view() operator. 

### Specifying appropriate computational environments

This pipeline is fully specified in the main.nf file, but you will need to 
specify the appropriate computational environments for each process. In general,
we will endeavor to always use the most up-to-date version of a tool. In the 
envs/ directory, please find the appropriate conda environment files for each
process. 

1. Use the appropriate conda command to find the most recent version of each tool
available on bioconda and update the YML files accordingly. Keep in mind the 
following:

- Use the most up-to-date version and specify it as so: `tool_name=<version>`, 
which will normally look like `samtools=1.17`. 

2. Only specify a single version of a tool in each YML file. While you can
specify multiple versions of a tool in a single YML file, we will try to 
minimize this as much as possible to avoid running into issues with conda being
unable to resolve the dependencies. 

3. Once you've filled in the YML files, add the appropriate path to each YML
file in the appropriate process (envs/<process_name>.yml)

### Finding the appropriate commands for running each tool

You'll notice that the `script` block in each of the processes in the main.nf
are blank. You will need to find the appropriate commands for running each tool
and fill them in. 

There are several ways to figure out the appropriate commands for running each tool. 

1. In an environment where you have the tool installed, you can use the help
flag, which is usually `-h` or `--help` to see the appropriate command for running
the tool. i.e. `tool_name -h` or `tool_name --help`

2. Many of the well-supported tools host either a GitHub repository or a wiki
page where you can find the appropriate commands for running the tool as well as
examples of how to use the tool. They will often have a `Usage` section that 
contains a quick basic example of how to use the tool. 

A few hints:

- You will need to specify FASTQC to run on both the short read files (R1 and R2)
- Nanoplot, Filtlonger, and Flye should only run on the nanopore reads
- You can refer to files or variables passed in inputs using the `$` symbol. i.e.
`$fasta`

Once you have found the appropriate commands for running each tool, you will need
to fill in the `script` block in each of the processes in the main.nf file. 

When you believe you've finished this step, run the pipeline and observe if it
runs successfully. If it doesn't, you will need to go back and fix the commands
for running each tool. 

You may use the following command to run the pipeline:

```bash
nextflow run main.nf -profile local,conda
```

## Week 1 Recap

- Clone the github repo for this project
- Familiarize yourself with the directory you are working in
- Use the code in the channel_test.nf to create a channel from a CSV file in 
your main.nf
- Specify the appropriate computational environments for each process in the YML
file and add the path to each YML file in the appropriate process
- Find the appropriate commands for running each tool and fill them in
- Run the pipeline and observe if it runs successfully

# Week 2 - Modularizing our pipeline and polishing our assembly

You may have noticed from the first week that our pipeline is becoming 
increasingly complex and slightly onerous to read in a single file. In this week,
we are going to refactor our workflow to make it more modular and easier to read.
This modularity will have the secondary benefit of making it easier to reuse
components of the pipeline in future projects or even share it with others. 

From a bioinformatics standpoint, this week we will add several steps to our
pipeline. We will polish the assembly we created last week with our long reads and
our short Illumina reads. Long read polishing will require the assembly as well
as the long reads. In order to polish with the Illumina reads, we will first 
need to align the illumina reads to the draft assembly using bowtie2. We can then
provide the aligned reads to Pilon to polish the assembly. 

## Relevant Resources

- [Requesting SCC Resources]({{site.baseurl}}/guides/requesting_scc_resources/)
- [Nextflow Modules]({{site.baseurl}}/guides/nextflow_modules/)
- [Connecting Inputs and Outputs]({{site.baseurl}}/guides/connecting_inputs_and_outputs/)
- [Nextflow Features]({{site.baseurl}}/guides/nextflow_features/)

## Objectives

For this week, you will again be given a working pipeline but this time, I will
ask you to focus on connecting the processes by filling out the nextflow workflow.
You will need to look at the inputs and outputs of the processes, and connect
them appropriately. 

## Setting up

1. Clone the github repo for this project - you may find the link on blackboard

## Tasks

### Changing the way we run our processes

Last week you were asked to run the pipeline with the `conda` and `local` profiles. 
If you look in the `nextflow.config` file, you'll notice that we have profiles
corresponding to these labels and a set of options specified. These options will
be automatically applied when you run the pipeline with the specified profile.

This week, we will be running significantly more resource intensive processes and
we will need to now make use of the resource available to us on the SCC. We will
use the `cluster` profile to run our processes on the SCC.

Your new nextflow running command should now look like below:

```bash
nextflow run main.nf -profile cluster,conda
```

Keep in mind that this will submit each of your processes as separate jobs to
different compute nodes on the cluster. This may take significantly longer to run
as your job will potentially need to wait in the queue for resources to become
available, processes may also take longer as they are more complex and certain
processes may need to wait until others finish. 

### Modularize the remaining processes in the week2.nf

Before you begin, take a note of the new main.nf you've been provided and the
modules/ directory. If you've been following along, you'll notice that we've
changed how we have organized our pipeline. The same code from our week 1 pipeline
is there, but we have now separated each process into different modules. We also
now import our processes into the main.nf script to make them available. You can
think of this as akin to when you import a library in python. 

1. Take the new code found in the main.nf and split them out into modules the 
way I have already done for you with last week's code. 

### Connect the processes in the week2.nf

1. Look at the inputs and outputs of each module and try to construct the
workflow by passing the correct channels to each process. You will need to understand
the order of operations and the dependencies between the processes to construct
the workflow. If you find it useful, I have included a visual representation of
the DAG for the workflow in these directions and in your repository. 

2. Run the pipeline and observe if it runs successfully. If it doesn't, you will
need to go back and fix the workflow. 

If you complete this successfully, you should have a working pipeline that should
run last week's tasks as well as the steps from this week that will assemble
the reads, polish the assembly with the long reads, align the short reads to the
long read polished assembly, and use the short reads to further polish the
assembly. 

## Week 2 Recap

- Modularize the remaining processes in the week2.nf
- Connect the processes in the week2.nf

# Week 3 - Wrapping up and evaluating our assembly

For the final week, we will be evaluating our assembly and comparing it to a 
reference genome. As we briefly discussed in class, there are several important 
criteria we can use to evaluate our assembly, including contiguity, completeness
and correctness. We will be performing several analyses to look at the quality
of our genome. 

## Relevant Resources

- [Using Conda with VSCode and Jupyter Notebooks]({{site.baseurl}}/guides/notebooks_computational_envs/)
- [Report Guidelines]({{site.baseurl}}/guides/project_report_guidelines/)

## Objectives

As with last week, I will provide you working modules and task you with 
connecting them to form a working pipeline. Please focus on understanding how
inputs and output channels are passed between processes and how to connect them
appropriately. I will once again provide you a visual diagram of the workflow
and you will need to figure out the order of operations and dependencies between
the processes to construct the workflow. 

You should also use the remaining time to put together your
writeup for project 1 if you haven't already.

## Setting up

1. Clone the github repo for this project - you may find the link on blackboard

## Tasks

### Connect the processes

1. Look at the inputs and outputs of each module and try to construct the
workflow by passing the correct channels to each process. You will need to understand
the order of operations and the dependencies between the processes to construct
the workflow. If you find it useful, I have included a visual representation of
the DAG for the workflow in these directions and in your repository. 

2. Run the pipeline and observe if it runs successfully. If it doesn't, you will
need to go back and fix the workflow. 

You should use the following command:

```bash
nextflow run main.nf -profile cluster,conda
```

### Use the output from Prokka and create a circos plot from the GFF file

Use the instructions found in the Using Conda with VSCode and Jupyter Notebooks
for the following tasks.

1. Create a conda environment with the PyCirclize and ipykernel packages installed

2. Make a jupyter notebook by opening a new text file and naming it with the .ipynb extension

3. Open your notebook and select the conda environment you created in the previous step
to use as the kernel for your notebook

4. Use the sample code found [here](https://moshi4.github.io/pyCirclize/circos_plot/)
to create a circos plot from the GFF file

### Finalize the project report for project 1

Follow the instructions found in the Report Guidelines to create a report for this project.

## Week 3 Recap

- Connect the processes
- Use the output from Prokka and create a circos plot from the GFF file
- Finalize the project report for project 1
