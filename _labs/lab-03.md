---
title: "Lab 3 - Using the SCC and basic nextflow"
layout: single
---

Today we are going to extend the workflow we built last time by adjusting
our qsub script to request a certain amount of cores and memory to use. We will
then begin converting our basic workflow into a proper nextflow pipeline. I have
provided you with the scripts we used last time in the bin/ directory. 

# Lecture on SCC Resources (15 minutes) 

[Advanced SCC Usage]({{ site.baseurl }}/lectures/week-03/)

# Iteration 1 (15 minutes)

## Don't repeat yourself (DRY) - using third party tools (15 minutes)

Oftentimes, we will want to perform basic tasks in a workflow that have already
been implemented by someone else. DRY is a principle in software development that 
stands for "Don't Repeat Yourself" and is meant to reduce the repetition of code
and make it easier to maintain. We can apply this same idea to basic tasks in
bioinformatics. 

As it happens, Biopython is a well supported and maintained package that makes
a large number of tools for computational molecular biology available to us. In
particular, it has a number of functions for parsing bioinformatics data files, 
and performing common operations on them, such as calculating the length of a
sequence. 

**Your turn**

1. Adjust the calc_length.py script to use biopython to calculate the length of
the sequence in the fasta file.

## Resources for Computational Environments 

[Relevant XKCD](https://xkcd.com/2347/):

![xkcd]({{ site.baseurl }}/assets/images/dependency.png)

## Class Lecture
[Computational Environments]({{ site.baseurl }}/lectures/week-02/)

## Textbook Guide
[Conda Guide]({{ site.baseurl }}/guides/conda_guide/)

2. Create a conda environment in the envs/ directory called biopython_env.yml







## Add a process for running your python script

Now we are going to add a process for running the python script on the downloaded file. 
Please add the following lines to your script right underneath the DOWNLOAD process
and above the workflow block:

```bash
process CALCULATE_LENGTH {

    conda 'envs/biopython_env.yml'

    input:
    path(fasta)

    output:
    path("length.txt")

    script:
    """
    calculate_length.py -i $genome -o length.txt
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

Now try re-running your script with the following command:

```bash
nextflow run main.nf -profile conda
```

Find where the CALCULATE_LENGTH process executed and report the length
of the genome in the length.txt file.

# Iteration 2

By now, we have developed a very basic nextflow pipeline. However, we can 
improve upon this by adding a few features to make it more robust and easier to use.
Make a new text file called `improved_main.nf` and copy the contents of `main.nf` into it.

## Add values to your nextflow.config

You have already seen the nextflow.config file in the root of your directory. 
Notice in the params section, how we have defined a number of variables that we 
can use in our nextflow script. I have provided you with the value for the 
FTP link to download the genome we've been working with. 

**Your Turn:**

1. Adjust the process DOWNLOAD to reflect the following changes:

- Add an input to the process that takes in the ftp link (hint: use the `input` keyword and the `val` keyword to pass the value in params)
- Adjust the output to capture any `.fna.gz` files downloaded (hint: use the *` operator, it works the same as in bash)
- Adjust the script block to use the value provided in the input

2. Use the value in params (params.ftp_link) and pass it as an argument to the
DOWNLOAD process. 