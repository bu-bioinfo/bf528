---
title: "Lab 2 - Workflow Basics"
layout: single
---

Today we are going to construct a very basic workflow that downloads a microbial
genome from the NCBI FTP server, and write a script that calculates the length
of the sequence. We will build this workflow from a primitive version
that we run on the command line and iteratively add features to it to make it
more robust, reproducible, and easy to use.  

I encourage you to make judicious use of the internet, LLMs, and your classmates
on the coding sections of this lab. All of the operations we will be doing are 
relatively simple and have already been implemented by others. We are simply
building a workflow from the ground up to understand the components that make
up a proper reproducible and robust workflow. 

# Objectives

- Understand FTP links and `wget`
- Gain experience with argument parsing using `argparse`
- Understand nextflow basics

# Setup (5 minutes)

1. Before we start, please open a VSCode interactive session on the SCC in your
student folder in the /projectnb/bf528/students/<your-bu-username> directory. 

2. Accept the github classroom assignment for this lab and clone the repo to 
your directory.

# Background

A FTP link is a web address that points to a file or directory on a server. It is
a standard protocol for transferring files from a server to a client. The NCBI
hosts a number of resources that we can download and analyze. For example,
today we will be downloading the genomic sequence of Escherichia coli and writing
a small python script to calculate the length of the sequence. 

# First Iteration (5 minutes)

1. Open a terminal and download the following file using this command:

```bash
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz
```

2. Run the script:

In your terminal, run the following command:

```bash
python calc_length.py
```

## Discussion of this approach

While this approach is straightforward and works, it would rapidly become 
unmanageable as the workflow begins to scale. In addition, since we ran these
commands on the terminal, there is no record of what we did and there would be
no easy way to share with others what we did. 

Advantages:
- Simple and fast

Disadvantages:
- Not reproducible
- No record of what was run your terminal history will be lost once you close it)
- Working locally on a single machine
- Script is hardcoded to work on a specific file


# Second Iteration - Qsub script

**Lecture (10 minutes)**

[Basic SCC Usage]({{ site.baseurl }}/lectures/week-02/)

**Your Turn (5 minutes)**

1. Make a new text file called `download_script.sh` that has the following lines:

```bash
#!/bin/bash -l

#$ -P bf528

wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz
```

2. Run the script using `qsub download_script.sh`

3. Check the status of the job using `qstat -u <your-bu-username>`

4. Do the same for your python script by making a new script called `calc_length_script.sh`

5. You may also submit this via `qsub calc_length_script.sh`

## Discussion of this approach

Advantages:
- Record of what was run
- Submits a job to the cluster

Disadvantages:
- Has to be run manually
- No easy way to determine if it worked
- Not very reproducible

# Third Iteration - Nextflow (5 minutes)

Above would be the simplest example of a bioinformatics pipeline. Nextflow is a
workflow management tool that will help us connect and automate the above 
components into a single pipeline. 

Navigate to the iteration_3/ directory and take a look at the main.nf file. Inside,
you will see some of the same commands but wrapped in a nextflow script. For now,
the important thing to take note of are:

Within the `process` block 
1. The `output` block - this specifies the file that will be created or exist
at the end of the process

2. The `script` block - this is where the commands are executed

Within the `workflow` block
1. The `DOWNLOAD()` function calls the DOWNLOAD process

## Activate the nextflow environment we made in the first lab

1. Load the miniconda module using `module load miniconda`

2. Activate the nextflow environment using `conda activate nextflow_env`

3. Run the nextflow script using `nextflow run main.nf`

Notice that nextflow created a `work` directory and stored the output there. 
During your run, you will see the name of the process and a series of letters or
numbers indicating the hash of the process. 

![nextflow run information]({{ site.baseurl }}/assets/images/nextflow_run.png)

If you now navigate into your `work/` directory, you will see a directory with
the first two characters of the hash and a subdirectory with the remaining characters of the hash. 

From our above example, the directory would be `work/ab/2496183aa8f126aac4b6a083de6ade/`.
That is where the outputs of the DOWNLOAD process were stored. 

# Fourth Iteration - Nextflow with multiple processes (20 minutes)

You'll notice that the workflow only downloads the file, but doesn't do anything
with it. We are going to run a python script to calculate the length of the 
genome. First, we will need to update our script to use argparse to accept
input and output file names on the command line. Navigate to the bin/ directory
and modify the calc_length.py script.

## Argparse Resources

[Argparse Guide]({{ site.baseurl }}/guides/argparse_guide/)

[Argparse Documentation](https://docs.python.org/3/library/argparse.html)

## Use argparse to accept input and output file names on the command line (15 minutes)
**Your Turn:**

1. Adjust the python script to use argparse to accept input and output file names on the command line.
- You should have two arguments: one for the input file and one for the output file.

Once finished, the script should be runnable via the following command:

```bash
python calc_length.py -i <fasta_file> -o <length_file>
```

2. Make the script executable using `chmod +x bin/calc_length.py` (assuming you
are in the root directory of your repo)

## Update your nextflow script (10 minutes)

Go into your main.nf and add the following underneath the download process and above the workflow block:

```bash
process CALCULATE_LENGTH {

    input:
    path(fasta)

    output:
    path("length.txt")

    script:
    """
    calc_length.py -i $fasta -o length.txt
    """
}
```

Now in your workflow block, add the following line so that it resembles below:

```bash
workflow {
    DOWNLOAD()
    CALCULATE_LENGTH(DOWNLOAD().out)
}
```

## Run your nextflow script (5 minutes)

1. Run the nextflow script using `nextflow run main.nf`
2. Check the output in the `work/` directory for the CALCULATE_LENGTH process

Take note of a few things about this basic workflow:

1. The DOWNLOAD process downloads the file specified and we can pass it to the
next process using the `DOWNLOAD().out` syntax. This is a channel that contains
the output of the DOWNLOAD process.

2. The CALCULATE_LENGTH process takes the output of the DOWNLOAD process as its
input `path(fasta)` and calls the calc_length.py script on it.

3. Our calc_length.py script parses this input and writes the output to the file
length.txt

4. You can see that in the input of CALCULATE_LENGTH, we refer to the value
passed in with a variable name fasta. This allows us to generalize and avoid
hardcoding the file name in the script. $fasta is a placeholder for the value
passed in with the variable name fasta, in this case, the output of the DOWNLOAD
process - GC_000005845.2_ASM584v2_genomic.fna.gz. When the process is run, the
fasta variable is replaced with this value. 

















# Resources for Computational Environments 

[Relevant XKCD](https://xkcd.com/2347/):

![xkcd]({{ site.baseurl }}/assets/images/dependency.png)

## Class Lecture
[Computational Environments]({{ site.baseurl }}/lectures/week-02/)

## Textbook Guide
[Conda Guide]({{ site.baseurl }}/guides/conda_guide/)