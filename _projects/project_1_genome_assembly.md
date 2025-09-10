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

# Week 1 - Understanding channels

As we will discuss in class, hybrid assembly approaches combine the benefits of
both long and short read sequencing technologies. The long read sequencing
provides improved contiguity and longer reads, which can better capture regions
of the genome previously difficult to sequence using short reads. This is especially
useful during genome assembly, where the longer reads are more likely to span
all regions of the genome, greatly aiding in the assembly process. However,
short reads are still useful and are commonly utilized to "polish" the assembly
and remove systematic errors from the assembly of the long reads. 

We will be generating a nextflow pipeline that will perform the following steps:

1. Assembly of the nanopore reads
2. Polishing of the nanopore assembly with the Illumina reads
3. Quality Control of the polished assembly and comparison the reference genome
4. Annotation of the genome and visualization of genomic features

## Relevant Resources

- [Nextflow Operators](https://www.nextflow.io/docs/latest/reference/operator.html)
- [Nextflow Tutorial](https://training.nextflow.io/latest/hello_nextflow/)
- [CLI Resources]({{site.baseurl}}/guides/cli_resources/)
- [Computational Environments]({{site.baseurl}}/guides/computational_environments/)
- [Basic Conda]({{site.baseurl}}/guides/conda_guide/)
- [Nextflow Basics]({{site.baseurl}}/guides/nextflow_basics/)
- [Nextflow Channels]({{site.baseurl}}/guides/nextflow_channels/)

## Objectives 

For the first week, we will focus on creating channels with the files we are
going to process. You will also be asked to generate appropriate computational
environments and look into the commands required to run certain tools. From a 
pipeline standpoint, we will be performing quality control on the short reads,
quality control of the long reads, and then assembly of the long reads. 

## Setting up

For this week, I have provided you a fully working nextflow pipeline that will
let you see how it works while focusing just on learning a few key concepts
we will be using throughout the semester. 

To start, open a VSCode session in **your** directory under the BF528 project
(i.e. `/projectnb/bf528/students/<your_username>/`). Please replace the
`<your_username>` with your BU ID and no @bu.edu. So if your BU ID was `jstudent`
then your directory would be `/projectnb/bf528/students/jstudent/`

Remember to activate the conda environment you created for nextflow using the
following commands:

```bash
module load miniconda
conda activate nextflow_latest
```

1. Please clone the github repo for this project in your student folder - you may
find the link on blackboard. In your student directory, you may use the following
command to clone your repo after copying the **SSH** link from your repo made for
you on GitHub Classroom:

```bash
git clone <repo_url>
```

This will make clone the repo to your student directory and all of your work
for this week should be done in this directory. You will push your changes to
GitHub as you go, which will also enable us to evaluate your work and help
troubleshoot. 

2. Open this directory in your VSCode session. 

3. Familiarize yourself with the directory you are working in. Throughout the semester,
we will be using the same structure and organization in all of the projects.

## Tasks

### Creating a channel from a CSV file

1. Take a look at the channel_test.nf and run the following command in a terminal
with your nextflow environment active:

```bash
nextflow run channel_test.nf
```

2. Note what the output of the command is in your terminal window and remember
what we talked about in class about channels and tuples. 

3. Use the code in the channel_test.nf as an example and in the week1.nf, make
two channels that are a tuple containing the name of the sample and the path to
the long reads and short reads, respectively. Name the channels `longread_ch`
and `shortread_ch`, respectively. Since we have paired-end sequencing for the
short reads, the shortread_ch will be a tuple consisting of three elements while
the longread_ch will be a tuple with only two elements. 

If you view() the contents of these channels, they should look something like
below (the paths will be different from what you see below and the actual paths
will be their location on the SCC):

```bash
longread_ch
[Alteromonas_macleodii, /path/to/long_reads]
```

```bash
shortread_ch
[Alteromonas_macleodii, /path/to/short_reads1, /path/to/short_reads2]
```

These are both tuples where the first element is our sample identifier, and the
remaining elements are the paths to the files we want to process. 

Feel free to modify the code in the `channel_test.nf` and run it to view the 
contents of the channels as you're troubleshooting the logic to generate the
shortread_ch and longread_ch correctly.

### Specifying appropriate computational environments

This pipeline is fully specified in the week1.nf file, but you will need to 
specify the appropriate computational environments for each process. In general,
we will endeavor to always use the most up-to-date version of a tool. In the 
envs/ directory, you will find empty conda environment files for each tool already
created for you that you will need to complete.

1. Use the appropriate conda command to find the most recent version of each tool
available on bioconda and update the YML files accordingly. Keep in mind the 
following:

- The command is `conda search -c conda-forge -c bioconda <tool_name>`
- Use the most up-to-date version and specify it as so: `tool_name=<version>`, 
which will normally look like `samtools=1.17`. Conda will list all available
versions and the most-up-to-date version will be the last one in the list and
should be the numerically highest version. 

2. Only specify a single version of a tool in each YML file. While you can
specify multiple versions of a tool in a single YML file, we will try to 
minimize this as much as possible to avoid running into issues with conda being
unable to resolve the dependencies. 

3. Once you've filled in the YML files, add the relative path to the YML file
for each process after the line that begins with `conda` in the process. 

This will look something like below:

```
process EXAMPLE {
    label 'process_single'
    conda 'envs/<name_of_yml_file>.yml
    ...
}
```
Make sure to replace <name_of_yml_file> with the name of the YML file you created
and with no <> characters in the final replacement. Now when you run nextflow, it 
will build and load the appropriate conda environment for each process. 

Please note how the path is relative to where the week1.nf file is located. 

### Finding the appropriate commands for running each tool

You'll notice that the `script` block in each of the processes in the week1.nf
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

3. For FastQC and filtlonger, you may use the quick start command provided in
the documentation. For filtlonger, choose the command for running **without an
external reference**.

4. For Flye, the only arguments you should include in the command are `--nano-corr`
and the '-o .' to specify the output directory. 

A few hints:

- You will need to specify FASTQC to run on both the short read files (R1 and R2) 
by listing them one after another
- You can refer to files or variables passed in inputs using the `$` symbol. i.e.
`$read1` or `$read2`
- You can make strings by using string interpolation "${variable_name}.txt" will
create a string using the value of the variable_name variable - i.e. if 
variable_name is "test", then "${variable_name}.txt" will create the string "test.txt". 
- The file created by the tool should be specified in the `output` block of the process.

Once you have found the appropriate commands for running each tool, you will need
to fill in the `script` block in each process in the week1.nf file. 

When you believe you've finished this step, run the pipeline and observe if it
runs successfully. If it doesn't, you will need to go back and fix the commands
for running each tool. 

You may use the following command to run the pipeline:

```bash
nextflow run week1.nf -profile cluster,conda
```

Please note that if successful, this command may take around ~1 hour to run as
Flye is performing assembly using the long reads, which as we discussed, is a
computationally intensive process. Make sure not to end your VSCode interactive
session while the pipeline is running. You can however close your browser
window and your session will continue to run. 

## Week 1 Recap

- [ ] Clone the github repo for this project
- [ ] Familiarize yourself with the directory you are working in
- [ ] Use the code in the channel_test.nf to create two channels from a CSV file in 
your week1.nf
- [ ] Specify the appropriate computational environments for each process in the YML
file and add the path to each YML file in the appropriate process
- [ ] Find the appropriate commands for running each tool and fill them in
- [ ] Run the pipeline and observe if it runs successfully

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

Last week you were asked to run the pipeline with the `conda` and `cluster` profiles. 
If you look in the `nextflow.config` file, you'll notice that we have profiles
corresponding to these labels and a set of options specified. These options will
be automatically applied when you run the pipeline with the specified profile.
As we talked about in the lab, we will be using the SCC to run our pipelines and
nextflow will automatically submit each process as a separate job to the SCC using
the appropriate qsub commands if specified. 

This week, we will be running significantly more resource intensive processes and
we will need to now make use of the resource available to us on the SCC. You will
be asked to determine the most appropriate set of resources for each of your
processes. 

As a reminder, you should run your pipelines with the following command:

```bash
nextflow run main.nf -profile cluster,conda
```

Keep in mind that this will submit each of your processes as separate jobs to
different compute nodes on the cluster. This may take significantly longer to run
as your job will potentially need to wait in the queue for resources to become
available, processes may also take longer as they are more complex and certain
processes may need to wait until others finish. 

### Modularize the remaining processes in the week2.nf

Before you begin, take a note of the week2.nf file you've been provided and the
modules/ directory. If you've been following along, you'll notice that we've
changed how we have organized our pipeline. The same code from our week 1 pipeline
is there, but we have now separated each process into different modules You can see
that code largely in the modules/ directory. We now import our processes into
the week2.nf script to make them available using the `include` keyword. You can 
think of this as akin to when you import a library in python. 

1. Take the code for the processes MEDAKA, BOWTIE2_INDEX, BOWTIE2_ALIGN, SAMTOOLS_SORT,
and PILON found in the week2.nf and split them out into modules the 
way I have already done for you with last week's code. 

2. Follow the same pattern where you make a new directory in modules/ with the
name of the process and the file itself called main.nf.

### Connect the processes in the week2.nf

1. Look at the inputs and outputs of each module and try to construct the
workflow by passing the correct channels to each process. You will need to understand
the order of operations and the dependencies between the processes to construct
the workflow. If you find it useful, I have included a visual representation of
the DAG for the workflow in these directions and in your repository. 

- Remember that you may access the outputs of a process using the <PROCESS>.out()
notation. For example, if you have a process called `FASTQC`, you can access
the output of the process using `FASTQC.out()`. If you have named different
outputs, you refer to them by the named defined in the `emit` block of the process.
For example, if you have a process called `FASTQC` that emits two different output
channels called `html` and `zip`, you can access them using
`FASTQC.out.html` and `FASTQC.out.zip`.

If you complete this successfully, you should have a working pipeline that should
run last week's tasks as well as the steps from this week that will assemble
the reads, polish the assembly with the long reads, align the short reads to the
long read polished assembly, and use the short reads to further polish the
assembly. 

Before you run the pipeline, please complete the next section.

### Use the report and the list of SCC resources to give each process an appropriate label

In the repo, I have provided you a HTML report that can be obtained from running
nextflow with the `-with-report` flag (i.e. `nextflow run week2.nf -profile cluster,conda -with-report`). 
This report shows you the amount of resources used per process. Use this information
and the guide for [requesting SCC resources]({{site.baseurl}}/guides/requesting_scc_resources/)
to give each process an appropriate label. 

1. Look at the report and try to give each process an appropriate label. Focus
on the amount of VMEM (virtual memory) required for each task and ensure that
your label requests the appropriate amount of RAM. You want to look at the 
virtual memory usage tab of the memory section in the report. See [here](https://nextflow.io/docs/latest/tutorials/metrics.html#metrics-page) for more details. 

2. Edit your `nextflow.config` to add the appropriate label specifications. I
have provided you a sample label in the config file that you can use as a model
for the ones you create. Please create labels called `process_low`, and `process_medium`.

You can see an example of where I've added a label to a process in the FLYE
process. You'll also notice that in the command, I have to specify the option
specific to FLYE for using multiple threads, `--threads` and I use the `$task.cpus`
variable in nextflow to automatically fill in the number of cpus requested for
the selected label. If you look in the nextflow.config, you can see that the
label 'process_high' requests 16 cpus, which also reserves 128GB of memory. 

3. For the other processes, please specify an appropriate label and ensure you
add the right flag to each command to make use of the resources requested. 

## Week 2 Recap

- [ ] Modularize the remaining processes in the week2.nf
- [ ] Connect the processes in the week2.nf
- [ ] Create labels in your nextflow.config for `process_low` and `process_medium`
- [ ] Use the report and the list of SCC resources to give each process an appropriate label -
ensuring that each process has requested a node with enough memory.

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
appropriately. I will ask you to put together a single nextflow process to run 
prokka. You will have to determine the right inputs and outputs as well as the
appropriate running command. You will once again be provided a visual diagram of
the workflow and you will need to figure out the order of operations and dependencies
between the processes to construct the workflow. 

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

Use the instructions found in the guide for [Using Conda with VSCode and Jupyter Notebooks]({{site.baseurl}}/guides/notebooks_computational_envs/) for the following tasks.

1. Create a conda environment with the PyCirclize and ipykernel packages installed

2. Make a jupyter notebook by opening a new text file and naming it with the .ipynb extension

3. Open your notebook and select the conda environment you created in the previous step
to use as the kernel for your notebook

4. Use the sample code found [here](https://moshi4.github.io/pyCirclize/circos_plot/)
to create a circos plot from the GFF file

### Finalize the project report for project 1

Follow the instructions found below to make a final report for this project.

## Week 3 Recap

- [ ] Connect the processes
- [ ] Use the output from Prokka and create a circos plot from the GFF file
- [ ] Finalize the project report for project 1
