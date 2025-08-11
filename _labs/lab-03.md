---
title: "Lab 3 - Using the SCC and basic nextflow"
layout: single
---

Today we are going to extend the workflow we built last time by adjusting
our qsub script to request a certain amount of cores and memory to use. We will
then begin converting our basic workflow into a proper nextflow pipeline. I have
provided you with the scripts we used last time in the bin/ directory. 

# Objectives

# Lecture on SCC Resources (15 minutes) 

[Advanced SCC Usage]({{ site.baseurl }}/lectures/week-03/)

# Don't repeat yourself - using third party tools (15 minutes)

Oftentimes, basic tasks that we want to accomplish in a workflow have already
been implemented by someone else. Additionally, some of these tools may implement
additional features and functionality over more basic scripts. 






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