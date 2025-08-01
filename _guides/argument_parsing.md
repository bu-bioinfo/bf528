---
title: "Argument Parsing"
layout: single
---

# Introduction

For this class, when we write third party scripts, we will be using argument parsing
utilities to make our scripts more user-friendly and extensible. We will be primarily
be working in python, so we will be using the `argparse` module to parse arguments. However,
most argument parsing utilities will provide similar functionality.

By now, you've seen that when you run command line tools or utilities, you are often asked
to provide certain inputs or variables. For example, when you run a BLAST search, you might 
be asked to provide a query file, a database to search against, and a name for the results file. 
Such a command might look something like this:

```bash
blastp -query <query.fasta> -db <database> -out <results.txt>
```

In this case, the `<query.fasta>`, `<database>`, and `<results.txt>` are the arguments
passed to the BLAST command. Internally, the BLAST command will parse these arguments
and use them to execute the BLAST search while substituting in the right values provided
on the command line by the user.

If you've used sys.argv before, you may be familiar with the idea of argument parsing. However,
the use of argument parsing libraries provides a more robust way to handle this problem. 

## Using argparse

The `argparse` module is a built-in python module that provides a way to parse command line arguments. 

The basic structure of an argparse script is as follows:

```python
#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser(description='Description of your script')
parser.add_argument('-i', dest='input', help='Description of input', required=True)
parser.add_argument('-o', dest='output', help='Description of output', required=True)
args = parser.parse_args()

print(args.input)
print(args.output)
```

If this code was encapsulated in a script, you could run it using the following command:

```bash
script.py -i input.txt -o output.txt
```

And it would print out the arguments provided on the command line. This is a simple example
that shows you how you can provide arguments and values on the command line and use them
in your script. 

The values you see if you ran this script would be

```bash
input.txt
output.txt
```


## Using argparse with Nextflow

When we develop scripts for our workflow, we will be using argparse to parse arguments 
and provide the values to our scripts in nextflow. This will enable us to easily re-use our script
for different datasets.

Let's pretend we have a simple python script that calculates the GC content of a FASTA file. This script
might look something like below (code not guaranteed to work):

```python
#!/usr/bin/env python
import argparse

parser = argparse.ArgumentParser(description='Calculate length of a sequences in a FASTA file')
parser.add_argument('-i', dest='input', help='FASTA File as input', required=True)
parser.add_argument('-o', dest='output', help='Name of output txt file containing sequence lengths', required=True)
args = parser.parse_args()

with open(args.input, 'r') as f, open(args.output, 'w') as o:
    for line in f:
        if line.startswith('>'):
            continue
        else:
            sequence_length = len(line)
            o.write(f'{sequence_length}\n')

```

To use this script in a nextflow process, we would first need to make it executable and then place it in the bin/ 
directory of our project. 

Then if we had a process that used this script, it might look something like below:     

```bash
process SEQUENCE_LENGTH {

    label 'process_low'
    conda 'envs/python_env.yml'


    input:
    tuple val(meta), path(fasta)

    output:
    tuple val(meta), path("${meta}.length.txt")

    script:
    """
    calculate_sequence_length.py -i $fasta -o $meta.length.txt
    """
}
```

As you can see, we are passing the values from the nextflow channel to the appropriate arguments in the python script.
This will be a common pattern we utilized in order to make our scripts re-usable for other files. We could run this script
on multiple files by simply providing a different nextflow input channel. 