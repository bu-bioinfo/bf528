---
title: "Lab 2 - Workflow Basics"
layout: single
---

Today we are going to construct a very basic workflow that downloads a microbial
genome from the NCBI FTP server, and runs a script that calculates some simple
statistics about the genome. We will build this workflow from a primitive version
that we run on the command line and iteratively add features to it to make it
more robust, reproducible, and easy to use. As we do this, I will point out various
features in nextflow that provide many quality-of-life improvements to our workflow.

All of the operations we will be doing are relatively simple and have already been
implemented by others. We are simply building a workflow from the ground up to
understand the components that make up a proper reproducible and robust workflow. 

Feel free to discuss with your classmates, consult google or LLMs, or ask me
questions if you get stuck. We will walk through these exercises together. 

# Setup

1. Open a VSCode interactive session on the SCC in your
student folder in the /projectnb/bf528/students/<your-bu-username> directory. 
Replace the <your-bu-username> with your BU ID and no @bu.edu.

2. Accept the github classroom assignment for this lab and clone the repo to 
your directory.

3. This lab will be completed in a series of iterations. Each iteration will build
on the previous one and add new features to make the workflow more robust, 
reproducible, and easy to use. Please open a terminal and navigate to the 
iteration_X/ directory for each iteration.

4. Make sure to activate the conda environment we created in the first lab using
the following commands:

```bash
module load miniconda
conda activate nextflow_latest
```

This will become second nature to you as we progress through the semester, but
you will want to run this series of commands every time you open a new VSCode
session.

# Background

A FTP link is a web address that points to a file or directory on a server. It is
a standard protocol for transferring files from a server to a client. The NCBI
hosts a number of resources that we can download and analyze. For example,
today we will be downloading the genomic sequence of Escherichia coli and running
a small python script to calculate the length of the sequence. 

# First Iteration - Simplest workflow

Navigate to the iteration_1/ directory in a terminal and perform the following:

1. Download the E. Coli genome using this command:

```bash
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz
```

2. Run the script:

```bash
python calc_length.py
```

- [ ] Download the E. Coli genome 
- [ ] Run the script to print out the length of the genome

# Second Iteration - Submitting jobs to the cluster

**Lecture (10 minutes)**

[Basic SCC Usage]({{ site.baseurl }}/lectures/week-02/)

**Your Turn**

Navigate to the iteration_2/ directory in a terminal and perform the following:

1. Make a new text file called `download_script.sh` that has the following lines:

```bash
#!/bin/bash -l

#$ -P bf528

wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz
```

2. Run the script using `qsub download_script.sh`

3. Check the status of the job using `qstat -u <your-bu-username>`

4. Do the same for your python script by making a new script called `calc_length_script.sh`.
This should look the same as the download script but with the python command in place
of the wget command.

5. Wait until the file has finished downloading and then run the `calc_length_script.sh`
using `qsub calc_length_script.sh`

6. Check the status of the job using `qstat -u <your-bu-username>`

- [ ] Make a qsub script that downloads the genome
- [ ] Make a qsub script that runs the python script
- [ ] Check the status of your submitted jobs using `qstat`

# Third Iteration - Basic Nextflow workflow

Above would be the simplest example of a bioinformatics pipeline. Nextflow is a
workflow management tool that will help us connect and automate the above 
components into a single pipeline. I have provided you a new script that will 
calculate the GC content of a FASTA file. The previous script `calc_length.py` 
and the `wget` command worked because the base environment on the SCC already
had the necessary tools installed. This will not always be the case, but we can
use conda environments to create custom environments for our workflow with the
packages we want installed. 

Navigate to the iteration_3/ directory in a terminal and take note of the following:

**In the main.nf**

*Within the `process`*
-The `output` - this specifies the file that will be created or exist
at the end of the process

- Note how we specify `path` in the output to indicate that we expect a file
to be created. You can also specify `val` to indicate that we expect a value,
or even tuple to indicate that we expect multiple elements to be created. 

- The `script` - this is where the commands are executed and you can see the
same wget command we ran earlier on the terminal

*Within the `workflow`*
- The `DOWNLOAD()` calls the DOWNLOAD process

**In the bin/ directory:**

- The gc_content.py script is located in the bin/ directory - nextflow 
automatically makes any scripts in the bin/ directory available to any process. 
This means that we do not need to pass the script into the process and can 
call it by name in the process as long as we make it executable.

**In the envs/ directory:**

- The biopython_env.yml file is located in the envs/ directory. This should
look exactly like the file used to create your nextflow conda environment. 

- Keep in mind that we do not need to do anything with this file ourselves. Nextflow
will automatically build this environment and activate it for us provided we use
the correct commands. 

**Your Turn:**

1. Use the following command in a terminal to make the script in the bin/ 
directory executable:

```bash
chmod +x bin/gc_content.py
```

Making a script executable allows it to be run as a command in the terminal. It
also allows us to avoid having to specify which interpreter to use to run the
script (as long as it's specified in the script). 

It will also let us call it from a terminal with the following command:

```bash
gc_content.py
```

Notice how we are not required to specify `python` to run the script. 

2. In the `main.nf`, make a new process called GC_CONTENT that takes the 
output of the DOWNLOAD process as input and runs the gc_content.py script on it. 
Structure it with similar syntax as the DOWNLOAD process.

- Make sure to check the script to see what file it creates and set that as the
output

- At the same indentation level as `input`, `output`, or `script`, please add a
line that looks like: 

```bash
conda 'envs/biopython_env.yml'
```

3. In the workflow block of the `main.nf`,Use `DOWNLOAD.out` to pass the output
of the DOWNLOAD process to the GC_CONTENT process.

- Call the GC_CONTENT process the same way the DOWNLOAD process was called

4. Run the nextflow script using `nextflow run main.nf -profile conda,local`

- Note this may take several minutes as Nextflow is creating the conda environment

Notice that when it finished, nextflow created a new directory called `work` and 
stored the output there. As nextflow is running, you will see the name of the process
and a series of letters or numbers indicating the hash of the process. 

![nextflow run information]({{ site.baseurl }}/assets/images/nextflow_run.png)

If you now navigate into your `work/` directory, you will see two directories with
the first two characters of the hash and a subdirectory with the remaining characters of the hash. 

From our above example, the directory would be `work/ab/2496183aa8f126aac4b6a083de6ade/`.
That is where the outputs of the DOWNLOAD process were stored. The terminal 
output only shows the first six unique characters of the hash, but the full hash
is used to identify the process. Your directory location will be different than the one
shown above. 

Every nextflow process will execute in these isolated directories that Nextflow automatically
creates for you. These directories will be populated with any files passed in the
process and will not have access to any other files. 

In this workflow, we are only running two processes and so it's relatively trivial
to determine in what directory our process executes. When we are running many, we will
take advantage of several built-in functionalities in nextflow. 

You may have noticed that when you run nextflow, you can see an often whimsical code name
of two vaguely related science words separated by an underscore. These are run names that
nextflow randomly generates every time you invoke a nextflow workflow. After you have run
this workflow, please use the following command:

```bash
nextflow log
```

This will print out all of the recorded runs tracked by nextflow. Locate the RUN NAME and
now run the following command (remove the <> before running):

```bash
nextflow log <RUN NAME> -f hash,name,exit,status
```

This will print out the hash, name, exit code and status of every process that was executed
by the workflow run. This will enable you in the future to figure out in what directory was
each process executed in. 

- [ ] Write a process that calls the python script provided in the bin/ directory
- [ ] Specify a conda environment for a specific process to use
- [ ] Understand how to find the outputs of specific processes
- [ ] Understand the idea of staging directories
- [ ] Use various commands to find the output directory for any process from a nextflow run
- [ ] Learn how to use profiles to specify options at runtime

# Fourth Iteration - Updating our script to use argparse

Navigate to the iteration_4/ directory.

You may have noticed that the python script we provided in the bin/ directory is not
very flexible. It is hardcoded to work on a specific file and write the output to a specific file.
We will update the script to use argparse to accept input and output file names on the command line.
As you've seen with other command line tools or scripts, we will often pass arguments to a script
on the command line using what are sometimes referred to as flags. These flags usually look like `-i` or `--input`
and are followed by the value of the argument. For example, we might run a script using:

```bash
gc_content.py -i <fasta_file> -o <length_file>
``` 
The values on the command line passed after the arguments will be read by the script,
stored in variables, and used to run the script with the values provided.

This is a common pattern that will enable our scripts to be more flexible and 
reusable. 

## Argparse Resources

[Argparse Guide]({{ site.baseurl }}/guides/argument_parsing/)

[Argparse Documentation]

**Your Turn:**

1. Adjust the python script to use argparse to accept input and output file names on the command line.

- You should have two arguments: one for the input file and one for the output file.

- If you are struggling with this, please use the example script provided in the
directory. It is not in the bin/ directory and you should be able to run it on
the command line using `python argparse_example.py`. Read the message that is
printed to the terminal to understand how to use the script. Look at the script
itself and it should become clear how we use argparse in python scripts.

2. Make the script executable using `chmod +x bin/gc_content.py`

Once finished, the script should be runnable via the following command:

```bash
gc_content.py -i <fasta_file> -o <length_file>
```

3. Go into your main.nf and create a new process that calls the gc_content.py script.

- The process should take the output of the DOWNLOAD process as input and pass it
to the gc_content.py script

- Pass the appropriate files on the command line to the python script. Remember
that you may access values in the input and output of a nextflow process. Values
in the input may be accessed using the $ symbol. 

4. Update the workflow block to call the new process like in the last exercise

5. Run the nextflow script using `nextflow run main.nf -profile conda,cluster`

- [ ] Adjust the python script to use argparse
- [ ] Make the script executable
- [ ] Create a new process that calls the gc_content.py script
- [ ] Update the workflow block to call the new process
- [ ] Run the nextflow script  

# Fifth Iteration - Specifying multiple outputs in a process

Sometimes we will want to have a process that creates multiple outputs and pass
the outputs to different processes. Nextflow provides a way to do this using the
`emit` keyword. 

Navigate to the iteration_5/ directory and you'll notice a few differences:

1. Look at the script in the bin/ directory. This script now creates two files and 
writes the output to them - gc_content.txt and length.txt. 

2. The main.nf file now has four processes: DOWNLOAD, GENOME_STATS, PRINT_GC, and PRINT_LENGTH.

3. Pay attention to the `output block` of the GENOME_STATS process. It has two outputs:

```bash
output:
    path("gc_content.txt"), emit: gc_content
    path("length.txt"), emit: length
```

By using `emit`, we can pass different outputs to different processes by calling
the separate outputs by the name we give them in `emit`. We can individually 
access different outputs using the <PROCESS NAME>.out.<EMIT NAME> notation. For
our example, we can access the gc_content.txt file using `GENOME_STATS.out.gc_content`
and the length.txt file using `GENOME_STATS.out.length`.

4. Add a line underneath the `conda` line in this process:

```bash
publishDir params.outdir
```

5. Look at the contents of the genome_stats.py script and properly fill out the
`script` block with the appropriate commands to run the script.

6. Send the appropriate outputs of the GENOME_STATS process to the PRINT_GC and PRINT_LENGTH
processes in the workflow.

7. Once finished, run the nextflow script using the following command:

```bash
nextflow run main.nf -profile conda,cluster
```

- [ ] Learn how emit lets us name outputs and pass them to other processes
- [ ] Use publishDir to publish outputs to a directory outside of work/
- [ ] Inspect the work/ directory to see where the outputs are stored and the
various log files that are created
- [ ] Send the appropriate outputs of the GENOME_STATS process to the PRINT_GC and PRINT_LENGTH
processes in the workflow
- [ ] Run the nextflow script   

# Optional

If you have been able to do all of the above, you can try to do the following:

1. Instead of using `wget`, develop a nextflow workflow that instead utilizes
the `ncbi-datasets-cli` tool to download the E. coli genome.

2. Keep the rest of the workflow the same as iteration_5 and run the `genome_stats.py`
script on the downloaded E. Coli genome.

*Hint*
You may want to try running the ncbi datasets command on the terminal to see what
options are available and what file is downloaded. 