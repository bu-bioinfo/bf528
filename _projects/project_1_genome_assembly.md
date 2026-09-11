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

We will talk in much greater detail about the concepts behind this project in
class. For now, please focus on understanding what the pipeline is doing at
a high-level and the nextflow concepts being introduced. 

# Week 1 - Understanding channels

As we will discuss in class, hybrid assembly approaches combine the benefits of
both long and short read sequencing technologies. The long read sequencing
provides improved contiguity and longer reads, which can better capture regions
of the genome previously difficult to sequence using short reads. This is especially
useful during genome assembly, where the longer reads are more likely to span
all regions of the genome, greatly aiding in the assembly process. However,
short reads are still useful and are commonly utilized to "polish" the assembly
and remove systematic errors from the assembly of the long reads.

We will talk in more detail about short and long reads as well as genome assembly.
Focus for now on the specific concepts and tools in nextflow.

We will be generating a nextflow pipeline that will perform the following steps:

1. Assembly of the nanopore reads
2. Polishing of the nanopore assembly with the Illumina reads
3. Quality Control of the polished assembly and comparison the reference genome
4. Annotation of the genome and visualization of genomic features

## Relevant Resources

- [Nextflow Operators](https://docs.seqera.io/nextflow/tutorials/static-types-operators)
- [Nextflow Tutorial](https://training.nextflow.io/latest/hello_nextflow/)
- [CLI Resources]({{site.baseurl}}/guides/cli_resources/)
- [Computational Environments]({{site.baseurl}}/guides/computational_environments/)
- [Basic Conda]({{site.baseurl}}/guides/conda_guide/)
- [Nextflow Basics]({{site.baseurl}}/guides/nextflow_basics/)
- [Nextflow Channels]({{site.baseurl}}/guides/nextflow_channels/)

## Objectives

For the first week, we will focus on understanding how channels work in
Nextflow and how they connect the processes in a pipeline together. You will
annotate the provided `week1.nf` pipeline to explain what each channel
operation is doing, complete the `specifications.md` file to describe the
pipeline at a higher level, generate the appropriate computational
environments for each tool, and fill in the commands for the two simpler
tools in the pipeline, FastQC and filtlong. From a pipeline standpoint, we
will be performing quality control on the short reads, quality control of the
long reads, and then assembly of the long reads.

## Setting up

For this week, I have provided you with a mostly complete nextflow pipeline
that will let you see how it works while focusing just on learning a few key
concepts we will be using throughout the semester.

To start, open a VSCode session in **your** directory under the BF528 project
(i.e. `/projectnb/bf528/students/<your_username>/`). Please replace the
`<your_username>` with your BU ID and no @bu.edu. So if your BU ID was `jstudent`
then your directory would be `/projectnb/bf528/students/jstudent/`

Ensure that you have selected `miniconda` in the Additional Modules to load
section of the VSCode OnDemand interface.

When your session has launched, remember to activate the conda environment
you created for nextflow using the following command:

```bash
conda activate nextflow_latest
```

1. Please clone the github repo for this project in your student folder - you may
find the link on blackboard. In your student directory, you may use the following
command to clone your repo after copying the **SSH** link from your repo made for
you on classroom50:

```bash
git clone <repo_url>
```

This will make a clone of the repo to your student directory and all of your work
for this week should be done in this directory. You will push your changes to
GitHub as you go, which will also enable us to evaluate your work and help
troubleshoot.

2. Open this directory in your VSCode session.

3. Familiarize yourself with the directory you are working in. Throughout the semester,
we will be using the same structure and organization in all of the projects.

## Tasks

### Understanding the channels

1. Open `week1.nf`. This is a fully working pipeline, already wired up
to run end to end. Feel free to look up these terms in the nextflow documentation,
the internet, the website, or any other resources. Add a comment above each of 
the following explaining, in plain English, what it is doing:

Single line comments in Groovy / Nextflow start with `//` and multi line begin with
`/*` and end with `*/`

- The `record` block definitions (`AssemblyReads`, `FastqRead`, `FastqcReport`)
  - How many fields does each record type have, and what type is each field?
  - Which record type represents a single read file, and which represents an
  entire sample's set of reads (long + paired short reads)?

- The `read_pairs_ch` assignment (what does `splitCsv` do, and what does the
`map` produce for each row of the CSV?)
  - Given the number of rows in `bac_samples.csv`, how many items will be
  emitted into `read_pairs_ch`?
  - How many fields does each item in `read_pairs_ch` have?

- The `fastqc_ch` assignment (why is `flatMap` used here instead of `map`, and
how does the shape of `fastqc_ch` differ from `read_pairs_ch`?)
  - For every one item that comes out of `read_pairs_ch`, how many items does
  `fastqc_ch` produce? Why that number specifically?
  - If `bac_samples.csv` had 5 rows instead of 1, how many total items would
  flow through `fastqc_ch`?

- The `input:` and `output:` blocks of each process (what type is expected in,
and what is being produced out?)
  - How many named outputs does each process declare, and how many actual
  files on disk does each output correspond to?
  - How many times will `FASTQC` run, and how does that relate to the number
  of items in `fastqc_ch`?
  - Does the output type of `FILTLONGER` match the input type expected by
  `FLYE`? How do you know they can be connected directly?

- The use of `$reads.read` (in `FASTQC`'s script block) and `${reads.name}`
(in `FILTLONGER`'s and `FLYE`'s output/script blocks)
  - What field of the record is being accessed in each case, and why does
  that field need to exist on the record type declared in that process's
  `input:` block?
  - Why does `${reads.name}` need curly braces while `$reads.read` doesn't —
  what would `$reads.name.filtered.fastq.gz` (no braces) be interpreted as
  instead?

You don't need to modify any of the logic here as your goal is to demonstrate
that you can read Nextflow code and explain what each channel operation is doing.
You'll be writing this kind of logic yourself later in the class.

### Specifying appropriate computational environments

The channel and process logic for this pipeline is already written in the
week1.nf file, but you will need to specify the appropriate computational
environments for each process. In general, we will endeavor to always use
the most up-to-date version of a tool. In the envs/ directory, you will find
empty conda environment files for each tool already created for you that you
will need to complete.

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

```groovy
process EXAMPLE {
    label 'process_single'
    conda 'envs/<name_of_yml_file>.yml'
    ...
}
```

Make sure to replace <name_of_yml_file> with the name of the YML file you created
and with no <> characters in the final replacement. Now when you run nextflow, it
will build and load the appropriate conda environment for each process.

Please note how the path is relative to where the week1.nf file is located.

### Completing specifications.md

Open `specifications.md` in the root of the repo. This document describes the
full pipeline we'll be building over the course of the semester, independent
of any particular week's code.

1. Fill in the **Pipeline Steps** table with one row per process in the final
pipeline (not just what's implemented in `week1.nf` so far), using the
Objective and Outputs sections above it as a guide. This will help you understand
dependencies and what processes can happen in parallel and which must wait for the
outputs of other steps.

2. Fill in the **Environment and Reproducibility** table, noting whether each
tool's conda environment pins an exact version.

This document should give someone unfamiliar with the code a clear sense of
what the pipeline does and how you'd know it worked correctly, even without
reading `week1.nf` itself. Eventually, this will serve as scaffolding for
you and potentially agentic coding harnesses to understand and implement
the project at a high level.

### Finding the appropriate commands for FastQC and filtlong

You'll notice that the `script` block for the `FASTQC` and `FILTLONGER`
processes in week1.nf are blank. Flye's command is already provided for you,
since it's a more complex, computationally expensive step to iterate on — but
you will need to find the appropriate commands for FastQC and filtlong and
fill them in yourself.

1. For FastQC, you may use the quick start command provided in the
documentation.

2. For filtlong, you may use the quick start command provided in the
documentation. Choose the command for running **without an external
reference**.

A few hints:

- You can refer to a field on a record using the `$` symbol followed by the
variable name and the field, since we typically save the whole record to one
named variable in `input:` rather than unpacking it into separate variables.
i.e. if the input is declared as `reads: FastqRead`, you'd refer to its file
with `$reads.read`.
- You can make strings by using string interpolation "${variable_name}.txt"
will create a string using the value of the variable_name variable - i.e. if
variable_name is "test", then "${variable_name}.txt" will create the string
"test.txt".
- The file created by the tool should be specified in the `output` block of
the process.

Once you have found the appropriate commands, fill in the `script` block for
each of the two processes in week1.nf.

Once you've filled in your environments, wired up the `conda` paths, and
written the FastQC and filtlong commands, run the pipeline with the `-stub`
flag to confirm the pipeline logic and channel wiring are correct:

```bash
nextflow run week1.nf -stub
```

This command should finish nearly instantaneously, since a `-stub` run
executes each process's `stub:` block (the placeholder `touch` commands)
instead of its real `script:` block, and doesn't require building the conda
environments. That means a successful stub run only tells you that your
channels and processes are wired together correctly and producing outputs
named the way downstream steps expect — it does **not** confirm that your
conda environments resolve or that the FastQC/filtlong commands you wrote are
actually correct. If you want to sanity check those separately, you can test
a command directly in a terminal with the appropriate environment activated.
Later in the semester, once we're confident in the full pipeline, we'll
switch to running it for real.

## Week 1 Recap

- [ ] Clone the github repo for this project
- [ ] Familiarize yourself with the directory you are working in
- [ ] Annotate the channel logic in week1.nf
- [ ] Complete the Pipeline Steps, Environment and Reproducibility in specifications.md
- [ ] Specify the appropriate computational environments for each process in the YML
file and add the path to each YML file in the appropriate process
- [ ] Find the appropriate commands for FastQC and filtlong and fill them in
- [ ] Run the pipeline with `-stub` and confirm it completes successfully

# Week 2 - Modularizing our pipeline and polishing our assembly

You may have noticed from the first week that our pipeline is becoming
increasingly complex and slightly onerous to read in a single file. In this
week, we are going to refactor our workflow to make it more modular and
easier to read. This modularity will have the secondary benefit of enabling
us to reuse components of the pipeline in future projects or even share them
with others.

From a bioinformatics standpoint, this week we will add several steps to our
pipeline. We will first generate a genome index from the assembly and align
the illumina reads to the draft assembly using bowtie2. We can then sort the
aligned reads and provide them to Pilon to polish the assembly and fix any
potential errors.

## Relevant Resources

- Requesting SCC Resources
- Nextflow Modules
- Nextflow Features

## Objectives

For this week, you will again be given a working pipeline but this time, I
will ask you to focus on connecting the processes by filling out the
nextflow workflow. You will need to look at the inputs and outputs of the
processes, and connect them appropriately.

## Setting up

1. Clone the github repo for this project - you may find the link on
blackboard

## Tasks

### Always confirm your workflow with a `-stub` run first

Last week you confirmed your channel wiring was correct by running
`nextflow run week1.nf -stub` instead of building conda environments and
executing every tool for real. We'll continue that same habit this week: as
you modularize and connect the processes below, verify each change with

```bash
nextflow run week2.nf -stub
```

A `-stub` run executes each process's `stub:` block (the placeholder
`touch` commands) instead of its real `script:` block, so it finishes
almost instantly and doesn't require building conda environments or
submitting a single job to the SCC. That means a successful stub run only
tells you that your channels and processes are wired together correctly and
producing outputs named the way downstream steps expect - it does **not**
confirm that your real commands, resource labels, or conda environments are
correct.

If you look in the `nextflow.config` file, you'll notice that we also have
`conda` and `cluster` profiles defined, corresponding to the SCC and the
qsub-based job submission we discussed in lab. This week's processes are
significantly more resource intensive than last week's, so once you are
confident your pipeline is wired correctly via repeated `-stub` runs, and
only once your instructor tells you to do so, you would run for real with:

```bash
nextflow run week2.nf -profile cluster,conda
```

This submits each process as a separate job to the SCC and may take
considerably longer as jobs wait in the queue. For this week's tasks,
however, you should not need to leave `-stub` mode - the resource report you
need for the labeling section below has already been generated for you.

### Modularize the remaining processes in the week2.nf

Before you begin, take note of the `week2.nf` file you've been provided and
the `modules/` directory. If you've been following along, you'll notice that
we've changed how we have organized our pipeline. The same code from our
week 1 pipeline is there, but we have now separated each process into a
different module located in a named directory in `modules/`. This allows us
to remove the processes from the `week2.nf` file and import them into the
`week2.nf` file using the `include` keyword. You can think of this as akin
to when you import a library in python to make certain functions available
for use.

1. Take the code for the processes `BOWTIE2_INDEX`, `BOWTIE2_ALIGN`,
`SAMTOOLS_SORT`, and `PILON` found in the `week2.nf` and separate them out
into modules the way I have already done for you with last week's code. You
should remove this code from the `week2.nf` file and place them in new text
files following the same format as last week's modules. When finished, your
`week2.nf` should begin with the `include` statements and end with the
workflow block.

2. Follow the same pattern where you make a new directory in `modules/`
with the name of the process and the file itself called `main.nf`.

3. Just as I've done for you with last week's processes, at the top of your
`week2.nf` file before the workflow block, you should use the `include`
keyword to import the processes you have created new modules for. Follow
the same syntax and style that is already there.

### Connect the processes in the week2.nf

1. Look at the inputs and outputs of each module and try to construct the
workflow by passing the correct channels to each process. You will need to
understand the order of operations and the dependencies between the
processes to construct the workflow. If you find it useful, refer to the
`specifications.md`. You should add the processes to the workflow in the order
they should be run and with the right dependencies. A dependency in this context
is simply a process that must be run and finish before the next process can
begin.

If you complete this successfully, you should have a working pipeline that
should run last week's tasks as well as the steps from this week that will
assemble the reads, align the short reads to the assembly, sort the
alignments, and use the short reads to polish the assembly.

You'll notice that when we go to align reads to the reference sequence, we
first have to build an index. We will discuss more in-class about this
step, but essentially, most aligners need to build a data structure that
allows them to quickly and efficiently align reads to the reference
sequence and locate where they align. You can think of a genome index as
akin to a table of contents, which allows you to determine what page a
chapter is located on, without having to read through the entire book. Most
traditional aligners will need to build an index for the reference sequence
before they can align reads to it, and most indexes need to be built with
the same tool as the aligner.

Before you run the pipeline, please complete the following section.

### Use the report and the list of SCC resources to give each process an appropriate label

In the repo, I have provided you a HTML report that was obtained by running
nextflow for real with the `-with-report` flag:

```bash
nextflow run week2.nf -profile cluster,conda -with-report
```

You will not need to run this command yourself - the report is already
included in the repo. This report shows you the amount of resources used
per process. Use this information and the guide for requesting SCC
resources to give each process an appropriate label.

1. Look at the report and try to give each process an appropriate label.
Focus on the amount of VMEM (virtual memory) required for each task and
ensure that your label requests the appropriate amount of RAM. You want to
look at the virtual memory usage tab of the memory section in the report.

2. Edit your `nextflow.config` to add the appropriate label specifications.
I have provided you a sample label in the config file that you can use as a
model for the ones you create. Please create labels called `process_low`,
and `process_medium` that specify a different number of CPUs to request.

You can see an example of where I've added a label to a process in the
`FLYE` process. You'll also notice that in the command, I have to specify
the option specific to FLYE for using multiple threads, `-t`, and I use the
`$task.cpus` variable in nextflow to automatically fill in the number of
cpus requested for the selected label. If you look in the
`nextflow.config`, you can see that the label `process_high` requests 16
cpus, which also reserves 128GB of memory.

3. For the other processes, please specify an appropriate label like in the
`FLYE` process and ensure you add the right flag to each command to make
use of the resources requested. You will need to use the `$task.cpus`
variable in nextflow to automatically fill in the number of cpus requested
for the selected label in the command as well as find the right flag to use
for each tool by looking at their documentation.

4. Certain processes like building an index or aligning reads to the
reference benefit greatly from using multiple threads / cores. You can use
a higher number of threads / cores for these processes if you have the
resources available and it will greatly speed up the process. You may
choose to use a greater number of threads for these processes even if you
don't technically need more memory reserved.

5. Some tools may not be able to use multiple threads / cores, but you
should still use the provided report to specify an appropriate label so
that your job properly reserves the right amount of memory.

## Week 2 Recap

- [ ] Modularize the remaining processes in the week2.nf
- [ ] Connect the processes in the week2.nf
- [ ] Create labels in your nextflow.config for `process_low` and
`process_medium`
- [ ] Use the report and the list of SCC resources to give each process an
appropriate label - ensuring that each process has requested a node with
enough memory
- [ ] Run the pipeline with `-stub` and confirm it completes successfully


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

As with last week, I will provide you with working modules for most of this
week's new steps - `BUSCO`, `NCBI_DATASETS`, `QUAST`, and `BUSCO_PLOT` - and
task you with connecting them to form a working pipeline. Please focus on
understanding how inputs and output channels are passed between processes and
how to connect them appropriately. Unlike those modules, I will ask you to put
together the `PROKKA` module yourself: you will have to determine the right
inputs and outputs as well as the appropriate running command. You will once
again be provided a description of the workflow and will need to figure
out the order of operations and dependencies between the processes to
construct the workflow. 

You should also use the remaining time to put together your
writeup for project 1 if you haven't already.


## Setting up

1. Clone the github repo for this project - you may find the link on blackboard

## Tasks

### Always confirm your workflow with a `-stub` run first

As in the previous two weeks, verify each change you make below by running

```bash
nextflow run week3.nf -stub
```

A `-stub` run executes each process's `stub:` block (the placeholder `touch`
commands) instead of its real `script:` block, so it finishes almost
instantly and doesn't require building conda environments or submitting jobs
to the SCC. That means a successful stub run only tells you that your
channels and processes are wired together correctly and producing outputs
named the way downstream steps expect - it does **not** confirm that the
command you write for `PROKKA`, or the real commands in the other modules,
are actually correct.


### Write the PROKKA module

Unlike this week's other new modules, `modules/prokka/main.nf` is left for
you to write from scratch.

1. Create the `PROKKA` process in `modules/prokka/main.nf`, following the
same structure as the other modules in `modules/` (`label`, `conda`,
`publishDir`, `input:`, `output:`, `script:`, and a `stub:` block).

2. This process should take a genome assembly (the same way `BUSCO` and
`QUAST` do) as input and produce Prokka's annotation output.

3. Look up Prokka's documentation for the appropriate command, making sure
to specify an appropriate label and use `$task.cpus` in the command for the
number of threads.

### Connect the processes

1. Look at the inputs and outputs of each module - including the `PROKKA`
module you just wrote - and try to construct the workflow by passing the
correct channels to each process. You will need to understand the order of
operations and the dependencies between the processes to construct the
workflow. If you find it useful, I have included a visual representation of
the DAG for the workflow in these directions and in your repository.

Note that `QUAST` is imported twice in `week3.nf` - once as `QUAST` and once
aliased as `QUAST_UNPOLISHED` - so that you can reuse the same process to
compare both the polished and unpolished assemblies against a reference.
Under the `// THIS WEEK` comment in the `workflow` block, you'll need to:

- Annotate the polished assembly with `PROKKA`.
- Run `BUSCO` on the polished assembly to assess its completeness.
- Use `NCBI_DATASETS` to download the reference genome named in
`params.ref_genome` (set in `nextflow.config`), so you have something to
compare your assembly against.
- Run `QUAST` comparing the **polished** assembly to the downloaded reference.
- Run `QUAST_UNPOLISHED` comparing the **unpolished** assembly to the same
reference, so you can see what Pilon's polishing step actually improved.
- Run `BUSCO_PLOT` on the `BUSCO` output to visualize its completeness
results.

*Please note that while you can alter the inputs / outputs, you should
be able to run the pipeline successfully by simply passing the correct outputs
to the correct processes. If you do change the inputs / outputs, you will need
to ensure that the pipeline still runs successfully.* 

2. Once your `-stub` runs succeed, run the pipeline for real and observe if
it runs successfully. If it doesn't, you will need to go back and fix the
workflow. 

You should use the following command:

```bash
nextflow run week3.nf -profile cluster,conda
```

### Finalize the project report for project 1

Follow the [Project 1 Report Guidelines]({{site.baseurl}}/guides/project_report/) to make a final report for this project.

## Week 3 Recap

- [ ] Write the `PROKKA` module (inputs, outputs, and script)
- [ ] Connect `PROKKA`, `BUSCO`, `NCBI_DATASETS`, `QUAST`, `QUAST_UNPOLISHED`,
and `BUSCO_PLOT` into the workflow
- [ ] Run the pipeline with `-stub` and confirm it completes successfully
- [ ] Run the pipeline for real with `nextflow run week3.nf -profile cluster,conda`
- [ ] Finalize the project report for project 1
