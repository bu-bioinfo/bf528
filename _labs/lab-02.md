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
- Recognize the advantages and disadvantages of the various iterations of our
workflow
- Gain experience with argument parsing using `argparse`

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

2. In VSCode, create a new file called `calculate_length.py` and add the following code:

```python
#!/usr/bin/env python3

import gzip

with gzip.open("GCF_000005845.2_ASM584v2_genomic.fna.gz", "rt") as f:
    for line in f:
        if line.startswith(">"):
            continue
        print(len(line.strip()))

```

3. Run the script:

In your terminal, run the following command:

```bash
python calculate_length.py
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
- No record of what was run (your terminal history will be lost once you close it)
- Working locally on a single machine
- Script is hardcoded to work on a specific file

# Second Iteration (10 minutes)

1. Delete the downloaded file using a quick `rm` command

2. Copy the download command above into a new text file called `download.sh`

```bash
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz
```

3. Call the script using `bash download.sh`

**Your Turn:**

1. Adjust your script to also write out the results to a txt file.

2. Use the textbook guide on [argparse]({site.baseurl}/guides/argument_parsing/) 
or the [argparse](https://docs.python.org/3/library/argparse.html) documentation or LLMs
to add arguments to your python script to make it more flexible. 

- Add an argument for the input file name
- Add an argument for the output file name

## Discussion of this second iteration

We have made some progress, all of the code we ran is now documented in external
files and we can run them from the command line. However, there are still a few
disadvantages to this approach. 

An old adage in software development is "Don't Repeat Yourself" or DRY. This means
that we should avoid writing the same code multiple times and make use of the
many tools and resources available to us. There are many different libraries
that already exist that will parse a genome file and calculate various statistics
for us. The most prominent in python being the `BioPython` library, which has an
enormous amount of pre-built functions for common bioinformatics operations.

We are also currently relying on the native python interpreter to run our script. 
We are lucky that the we have a python interpreter installed on the SCC, but we
cannot always make that assumption. In the future, we would like to control exactly
what packages are installed and used. This will allow us to ensure that our scripts
run the same way on any machine.

# Resources for Computational Environments 

[Relevant XKCD](https://xkcd.com/2347/):

![xkcd]({{ site.baseurl }}/assets/images/dependency.png)

## Class Lecture
[Computational Environments]({{ site.baseurl }}/lectures/week-02/)

## Textbook Guide
[Conda Guide]({{ site.baseurl }}/guides/conda_guide/)

# Third Iteration (20 minutes)

For the final iteration, we will create a conda environment containing the
biopython package and use the built-in function to parse the file and return
the length. 

**Your Turn:**

1. Load the miniconda module using `module load miniconda`
2. In VSCode, make a new text file called `biopython_env.yml` and add the following content:

```yml
name: biopython_env
channels:
  - conda-forge
  - bioconda
packages:
  - biopython=1.79
```

3. Create the environment using the following command:

```bash
conda env create -f biopython_env.yml
```

4. Activate the environment using `conda activate biopython_env`

5. Revise your script to utilize the Biopython library to parse the file
and calculate the length.

- Your script should still utilize argparse to take in the input and output file names


# Final Iteration (remaining time)

For the final step, we will now wrap your python script in a qsub script that
would allow it to be submitted to the SCC cluster. Currently, your script is
running locally on the same machine where your VSCode instance is running. We can
take advantage of the SCC to run this script on a remote machine. The strengths
of this approach will become apparent once we start working with larger datasets.

**Your Turn:**

1. Make a new txt file called `qsub_script.sh` and add the following content:

```bash
#!/bin/bash -l

#$ -P bf528

module load miniconda
conda activate biopython_env
python calculate_length.py <input_file> <output_file>
```

2. Submit the job using `qsub qsub_script.sh` in a terminal

3. Check the status of your job using `qstat -u <your_bu_username>`

4. Inspect the output file to ensure it finished correctly

5. Take note of the qsub_script.sh.e and qsub_script.sh.o files. These are the 
standard error and output files that are generated by your script. In all likelihood,
these files will be blank, but they will often contain useful information about
the status of your job if it fails or when running other tools. 

## Wrap-up

Today, you have constructed a small workflow that downloads a microbial genome
from the NCBI FTP server, and write a script that calculates the length of the
sequence. The numerous iterations we went through allowed us to make the workflow
more robust, reproducible, and easy to use. 

Next week, we will make one final modification to this workflow before moving
on to using Nextflow to generate a bioinformatics pipeline that replicates this
one. You will see how Nextflow integrates all of these different features we've
learned into a single, easy-to-use pipeline management sytem. 