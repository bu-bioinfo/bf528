---
title: "Nextflow Features"
layout: single
---

In lecture, we will have covered the basics of how nextflow works conceptually. 
In this guide, we'll cover a few extra features of nextflow that are useful
for workflow development and execution. 

## Basic Nextflow Directory for BF528

The basic nextflow directory will look something like this:

```
project/
├── bin/
│   └── python_script.py
├── envs/
│   └── tool_env.yml
├── modules/
│   └── module1/
│       └── main.nf
├── main.nf
├── data/
│   └── test_data.csv
├── nextflow.config
└── samplesheet.csv
```

### bin/

The bin directory is where we will place any accessory scripts that we will use
in our nextflow pipeline. Nextflow automatically includes this directory in
the PATH environment variable, so you can refer to these scripts using their
names without having to provide the full path or provide the files directly. 
You will need to make the script executable using the following command:

```bash
 chmod +x <name-of-script>
``` 

You will then be able to call a script by using the following syntax in any nextflow
process:

```bash
shell:
"""
<name-of-script> <arguments>
"""
```

or more descriptively:

```bash
shell:
"""
parse_gtf.py -i <arg> -o <arg>
"""
```

Ensure that the script has the correct shebang line at the top of the file. For example:

```bash
#!/usr/bin/env python
``` 

We will also be using an argument parser to parse any arguments passed to the script. 
In python, you can use the `argparse` module to do this or in R, you can use the `argparser` package.

 
### envs/

The envs directory is where we will place any conda environments that we will use
in our nextflow pipeline. Per our class guidelines, we will make conda environments
using YML files according to the following conventions in the computational environments
guide found [here]({{ baseSite }}/guides/computational_environments/).

### modules/

Eventually we will develop our nextflow processes in the modules directory. This practice will
allow us to keep our modules separate and reuse them across different worfklows by simply
copying them into a new project directory. 

When using modules this way, in your nextflow workflow `main.nf` you will need to include
the following line:

```bash
include "./modules/<module_name>/main.nf"

workflow {
    <module_name>()
}   

```

As you can see, this is conceptually similar to the way we call a function or import a module
in python. 


## Nextflow Working Directory

By default, nextflow assumes the working directory is the directory where the
main.nf file is located. This means that you can refer to files in the working
directory using relative paths. 

For example, in our main.nf, when we are using `INCLUDE` to import a module,
we can refer to files in the working directory using relative paths. 

```bash
include "./modules/<module_name>/main.nf"
```

This assumes the working directory structure we set up above. 

In each module, we can also use relative paths when referring to other files. For
example, if we are using a conda environment, we can refer to the environment
YML file using the following path:

```bash

process INDEX {
    label 'process_high'
    conda 'envs/star_env.yml'
    ...

}
``` 

Note that the path is a relative path as nextflow resolves against the workflow
launching directory (where the main.nf file is located). If we wanted to be more
careful, we could encode the path to the environment YML file using the `$projectDir`
variable in the nextflow.config file.

## $projectDir

As a good practice, we will use the `$projectDir` variable to refer to the
root directory of the project. This is a variable that is automatically
assigned by nextflow and points to the directory where the main.nf file is
located. 

For example, if your project directory looks like this:

```
project/
├── main.nf
├── data/
│   └── test_data.csv
└── nextflow.config
```

You can refer to the test data file using the following path:

```yml
test_data = "$projectDir/data/test_data.csv"
```

If our full path was `/home/user/project/data/test_data.csv`, then the variable
`$projectDir` would resolve to `/home/user/project` and the variable
`$projectDir/data/test_data.csv` would resolve to `/home/user/project/data/test_data.csv`.
This allows us to avoid hardcoding the full path to the file and makes it easier to
move the project to a different location without having to update the path in the config file.  

## Nextflow Config 

### params

We will be using the config file to store static values, files and variables
that will be used in the workflow. This is important because it allows us to
specify these values once and use them throughout the workflow without having
to change each instance if we update one.

For example, you can see a sample config file below:

```yml
params {

    test_data = "$projectDir/data/test_data.csv"
    ref_genome = "$projectDir/data/ref_genome.fa"
    

}
```

This config file above stores the paths to the test data and reference genome
as variables that can be used throughout the workflow. We can reference these 
variables elsewhere using the `params.variable_name` syntax. 

For example, we could use the test_data value in a process like this:

```
params.test_data
```

### Profiles

If you look in the nextflow.config file at the top-level of the directory,
you will see a number of profiles defined. These profiles correspond to 
preset options that will be automatically applied when you run the workflow. 

For example, if you run the workflow using the following command:

```bash
nextflow run main.nf -profile test
```

The `test` profile will be applied and the workflow will be run with the 
preset options defined in that profile.

For a more realistic test case, you will often see the following command:

```bash
nextflow run main.nf -profile conda,cluster
```

This will instruct nextflow to use the pre-defined options in the `conda` and `cluster`
profiles. These profiles specify a number of important options for nextlow to use
conda and submit jobs appropriately to the SCC. 

You can see the options defined in each profile by looking at the `nextflow.config` 
file.

### Nextflow Labels

Nextflow labels are a way to assign labels to processes in the workflow. These labels can be used to 
pre-assign any default values to specific processes. We will primarily use labels to assign processes
a different set of computational resources to request when submitting to the SCC. 

This requires the label to be defined in two places:

1. In the `nextflow.config` file
2. In the process definition in the module `main.nf` file

In the nextflow.config, these labels will look like below:

```yml
withLabel: process_high {
    cpus = 16
}
```

If we had a sample process with this label, it would look like below:

```bash
process INDEX {
    label 'process_high'
    conda 'envs/star_env.yml'

    ...
    
}
```

Whenever we submit a job to the SCC, nextflow will automatically assign the 
values defined in the label to the process. For this process INDEX, it will
appropriately request 16 CPUs in the qsub command. These labels will allow
us to dynamically request different amounts of resources for different processes
without having to manually specify every time. This has the 
benefit of ensuring that we are not requesting more resources than we need for 
simple tasks and requesting enough to make complex tasks run faster or at all. 
Remember that the SCC is a shared resource and we want to be respectful of the other 
users. Also, keep in mind that requesting nodes with more resources will likely increase
the amount of time our jobs spend in the queue before they begin running as there are less
nodes available with these resources and they are in high demand. 

## $task.cpus

Remember that we have several layers to our resource requests. 

1. We must request the appropriate amount of resources in nextflow.
    - We accomplish this with the `label` found in both the process and the nextflow.config file.
    - Each process should have a label and the nextflow.config file should define the resources for that label.

2. We must ensure that the tool is instructed to use the appropriate amount of resources.
    - We accomplish this with the `$task.cpus` variable in the shell script.
    - Check each tool's documentation for how to specify how many resources the process should use.

We will most often by using multiple cores or cpus to accelerate our computational
processes. 

Remember that you need to match the amount you request via qsub with the amount
you instruct the program to utilize in the shell script. 

You may use the `$task.cpus` variable in the shell script to access the values
assigned in the nextflow.config file. Note in the following example that several
directives are missing for clarity. 

```bash
#!/usr/bin/env nextflow

process ALIGN {
    label 'process_high'

    script:
    """
    STAR --runThreadN $task.cpus <other directives>
    """
}
```

At runtime, nextflow will replace the `$task.cpus` variable with the value assigned
in the nextflow.config file, specifically the value in the process_high label under
the "cpus" directive. 

You can specify memory in a similar way by setting the memory directive under a
label in the nextflow.config file. 

## String interpolation

Nextflow allows for string interpolation using the `${}` syntax. This allows us to 
include variables in strings dynamically. For example:

```bash
#!/usr/bin/env nextflow

process ALIGN {
    label 'process_high'
    conda 'envs/star_env.yml'
    publishDir params.outdir, pattern: "*.Log.final.out"

    input:
    tuple val(meta), path(reads)
    path(index)

    output:
    tuple val(meta), path("${meta}.Aligned.out.bam"), emit: bam
    tuple val(meta), path("${meta}.Log.final.out"), emit: log

    script:
    """
    STAR --runThreadN $task.cpus --genomeDir $index --readFilesIn $reads --readFilesCommand zcat --outFileNamePrefix $meta. --outSAMtype BAM Unsorted
    """
}
```

You can see that we are using the `${meta}` variable to specify the sample name in the output 
file name. The file generated will have the value of meta substituted in the file name
and end with `.Aligned.out.bam`. This value is the first element of the tuple passed 
in the input channel and is typically the name or identifier of the sample. This
is a common pattern in nextflow and allows us to dynamically generate file names based
on the name passed in the input channel tuple.

### String functions (.baseName)

Groovy also has a few built-in functions that we can use to generate file names. For example, we can use the `basename` 
function to extract the base name of a file path. This is useful when we want to remove the file extension from a file path.

```bash
#!/usr/bin/env nextflow
process BOWTIE2_BUILD {
    label 'process_high'
    container 'ghcr.io/bf528/bowtie2:latest'

    input:
    path(genome)
    
    output:
    path('bowtie2_index'), emit: index
    val genome.baseName, emit: name
    
    shell:
    """
    mkdir bowtie2_index
    bowtie2-build --threads $task.cpus $genome bowtie2_index/${genome.baseName}
    """
}
```
In this example, we are using the `baseName` function to extract the base name of the genome file path. Bowtie2 requires us
to provide the base name of the index files as an argument without the extensions. This is a common pattern in nextflow and 
is another method that allows us to dynamically generate file names based on the name passed in the input channel tuple.

## (*) and (**) patterns

Nextflow also supports the bash `*` glob pattern to match any number of files in a directory. For example, we could use the following

```bash
output:
    path('*.fastq.gz')
```

The above line would instruct nextflow to match any file ending in `.fastq.gz` in the current directory and emit them in the
output channel.

You can also use the `**` to recurse through directories. For example, we could use the following:

```bash
#!/usr/bin/env nextflow
process NCBI_DATASETS_CLI {
    label 'process_single'
    conda "envs/ncbidatasets_env.yml"

    input:
    tuple val(name), val(GCF)

    output:
    tuple val(name), path('dataset/**/*.fna')

    shell:
    """
    datasets download genome accession $GCF --include genome
    unzip ncbi_dataset.zip -d dataset/
    """
```

The above line would instruct nextflow to match any file ending in `.fna` in the `dataset`   directory and any subdirectories
and emit them in the output channel. This is useful in cases where processes create multiple output files in different directories or
deeply nested directories. The above example demonstrates this by downloading a genome from the NCBI datasets CLI and emitting the 
FASTA file in the `dataset` directory. By default, NCBI datasets CLI will download a `ncbi_dataset.zip` file with the requested files
and we unzip it to the `dataset` directory. The files provided are in a nested directory structure, so we use the `**` glob pattern to match
any file ending in `.fna` in the `dataset` directory and any subdirectories while avoiding hardcoding the exact path to the file.


## Nextflow work/ directory

Nextflow automatically creates a work directory where it stores the output of each process. 
Nextflow creates a hash of the process name and the input files to create a unique directory for each process.
When a task is run, nextflow will stage any input files into these directories and each process will run
in its own directory. These directories are located in the work/ directory and if we ran a single task
the directory structure would look something like this:

```bash
work/
├── 03
│   └── c746ec9f000f7b3f9bbccebd1dca3d/
│       └── .command.begin
│       └── .command.err
│       └── .command.log
│       └── .command.out
│       └── .command.run
│       └── .command.sh
│       └── .command.trace
│       └── .exitcode
│       └── staged files
│       └── output files

```

This work directory will generate a number of different .files that contain information about the
execution of each process. These files include:

- .command.begin: A script that is run before the process starts
- .command.err: The standard error output of the process
- .command.log: The log output of the process
- .command.out: The standard output of the process
- .command.run: The script that is run to execute the process
- .command.sh: The shell script that is run to execute the process
- .command.trace: A trace of the process execution
- .exitcode: The exit code of the process

Any files that are staged into the process directory will be copied into the work directory and
all output files will be generated in this directory as well. One of the advantages of this
strategy is that each process is completely self-contained and cannot be affected by other processes.
This also means that we can refer to any files generated in a process with relative paths. For instance,
we can create directories in each process and refer to them with relative paths. For example, we can create
a directory and then run a command that generates a file in that directory.

```bash
process INDEX {
    label 'process_high'
    conda 'envs/star_env.yml'

    input:
    path genome
    path gtf

    output:
    path "star", emit: index

    script:
    """
    mkdir star
    STAR --runThreadN $task.cpus --runMode genomeGenerate --genomeDir star --genomeFastaFiles $genome --sjdbGTFfile $gtf --genomeSAindexNbases 11
    """

}
```

In this example, we create a directory called `star` and then run a command that generates a file in that directory. Specifically,
we create the `star` directory and then the `--genomeDir` option points to that directory. We can then refer to the file with a relative path.


### Nextflow Log

The nextflow log command shows information about executed pipelines. This is helpful
for showing you the various exit statuses of the processes in your pipeline. A sample command
may look like the following:

```bash
nextflow log <run_name> -f hash,name,exit,status
```

This will show you the hash of the process, the name of the process, the exit status, and the status of the process. 
Which will look something like this:

```bash
hash	name	exit	status
03/c746ec 	INDEX	0   COMPLETED
```

Although the work/ directory strategy has a number of advantages, it can be a bit of a pain to navigate and manage. This
nextflow log command is an easy way to see where each process is located and what its exit status was. If you need to
manually inspect the output of a process, you can use the hash value to navigate to the directory where you can view all
of the running information for that process, input files, and output files. 

### Nextflow PublishDir 

Nextflow also has a publishDir option that allows you to specify a directory where you want to publish the output of a process.
This is helpful for gathering final output files from a process and storing them in a single location. You may also wish to
use publishDir to share any QC or log output files from each process. 

```bash
process INDEX {
    label 'process_high'
    conda 'envs/star_env.yml'
    publishDir params.outdir, pattern: "*.Log.final.out"
    ...
    
}
``` 

This will publish the output of the align process to the directory specified in the `params.outdir` parameter. The `pattern` 
option allows you to specify a pattern to match the output files that you want to publish. In this case, we are only
publishing a file that matches the pattern and ends with `.Log.final.out`.

Typically, we will make the publishDir location, here params.outdir, a directory in this same repository called results/.

## Nextflow report  

Nextflow can create a html report that summarizes the execution of a pipeline. This is helpful for documentation purposes
and for examining some runtime metrics for each process. 

This can be achieved by adding the following flag to the command:

```bash
nextflow run <main.nf> -with-report [file name]
```

One of the more helpful features of this report will be the Resource Usage section where you can see the amount of memory
and CPU Usage for each process. This can be helpful for determining how many resources to request for a given process.





