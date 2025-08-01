---
title: "Troubleshooting Issues"
layout: single
---

# General Issues

While I am always here to assist, it is important to develop the skills to be 
able to resolve common issues on your own. This will serve you well in this class
and your future career. 

## Command not found

If you receive some sort of error saying "command not found", it is likely that
one of two things has occured:

1. You have not installed the required software 
2. You have misspelled the command

### Potential Fixes

In the case of issue #1, you will need to ensure that you are using the correct
environment in which to run your tool. 

In the case of issue #2, please ensure that you are following the manual or
documentation for the tool you are using. For the most part, many tools attempt
to obey [posix conventions](https://pubs.opengroup.org/onlinepubs/9699919799/basedefs/V1_chap12.html)
and will expect commands to be run in a specific way. 

However, more and more developers have started to deviate from these guidelines.
Make sure you are spelling the command right, and including the appropriate
arguments with the correct flags. 

## Task is taking a long time to complete

If you find that a task is taking a long time to complete, there *may* be an
issue. However, it is also possible that the task is simply taking a long time. 
Many bioinformatics operations are resource-intensive and many bioinformatics
datasets are quite large. 

### Potential Fixes

If you've confirmed there's an actual issue, you may consider trying the
following:


1. Did the task actually start?
    - If you're submitting to the cluster, is your job still in the queue?
    - If you're running locally, is your process using any CPU?

2. Find the output log (if any) and check for run information. Most tools will
    print some information to the console or a log file about what it is doing,
    progress updates, and any error messages. 

## Process Reaper

If you started to run a process locally on the SCC (on a head node), there are
automatic programs that are designed to kill any process that is using a significant
amount of resources automatically. This is designed to keep the head nodes from
becoming unresponsive. You will receive an automated email informing you that
your process has been "reaped". You are not in trouble (these messages are not
sent by a human) but you should avoid running processes locally on the SCC in 
the interest of being a responsible user. 

### Potential Fixes

Ensure you are submitting your processes to the cluster. Small operations like
file manipulation and tasks expected to use less than 15 minutes of wall time 
are allowed to be run on the head nodes. 


# Nextflow Troubleshooting

Some of the above issues you may encounter in tandem with nextflow issues. I 
will provide you some common guidelines for troubleshooting nextflow. 

## Syntax Issues

Nextflow error messages are not always the most helpful. I always encourage you
to google or search for the error message you receive. That being said, one of 
the most common culprits is a syntax error in your nextflow script. Nextflow is 
implemented in groovy, a java based language, and adheres to similar syntax as 
java. Be especially careful with semicolons, and indentations. 

### Potential Fixes

Nextflow has a built-in linter that can help you catch syntax errors. You can run
it using the following command:

```bash
nextflow lint your_script.nf
``` 

This command will lint nextflow scripts and config files, formats them if possible,
and provide you with a list of syntax errors and warnings. 

## Command not found

If you encounter a "command not found" error while running your pipeline with nextflow,
it is again likely that it is trying to execute the task in an environment that
does not have the required software installed. It may also mean you have misspelled
the command. 

### Potential Fixes

1. Ensure you are using the correct set of profile options for Nextflow. For 
    project 1, this will be `conda` and for subsequent projects, this will be `singularity`.

2. Make sure your process module has the correct environment specified using either
    `conda` or `singularity`.

3. Check your command against the documentation for the tool you are using. 

## Other errors

There are a multitude of other errors that can occur while running your pipeline. 
While I cannot address them all here, I can give you a general idea of what to do.

All of the running information from a nextflow process is stored in the `work` directory
where it executed. If you recall, each task is executed in a separate directory 
specified by a hash of the process name and the inputs. Inside this directory,
there are a number of files that can help you debug your issue. 

Let's pretend that you have a nextflow run that failed, and you want to check
if the actual process itself had an issue. 

Remember that when nextflow is invoked, it creates a "run name" that is used as
a short identifier for the run. 

You may see the runs by invoking the `nextflow log` command. The output of which
may look something like:

```bash
TIMESTAMP           DURATION        RUN NAME        STATUS  REVISION ID     SESSION ID                              COMMAND
2024-07-29 07:22:00 2.1s            amazing_ampere   ERROR   96eb04d6a4      af6adaaa-ad4f-48a2-9f6a-b121e789adf5    nextflow run main.nf -profile conda,cluster
```

We can see more details by using the `-f` flag to pull back specific fields from
the execution log:

```bash
nextflow log -f 'process,exit, hash, duration'
```

This will look something like this:

```bash
process exit hash duration
SORT 1 f2/96eb04d6   2.1s
```

The value in `hash` is the directory in work/ where that specific process
was executed. If you navigate to that directory, you can inspect some of the
log and output files to see what went wrong. 

It depends on the program, but most bioinformatics tools will output useful run
or log info to a few potential files. You can refer back to the [Nextflow Features](/guides/nextflow_features/)
section for more information all of these files. 

Commonly, you will find information sent to the following files:

- .command.err
- .command.log
- .command.out

Most tools will print out helpful run information as well as status updates
to these files. If you encounter an error, oftentimes the tool will provide a
specific and helpful error message that will identify the cause of the problem. 

# Resources available to you

I encourage you to work with your classmates, use Google or LLMs, and ask me for
help if you are having trouble. Keep in mind that while I make no restriction
on the use of LLMs, your reports must be entirely your own work. Please also
keep in mind that LLMs are not yet adept at many bioinformatics tasks and in general
should always be double-checked by a human.

1. A quick google search of the error message

2. A search through the issues section of the GitHub repository for the tool you are using

3. BioStars - a stack overflow-like forum for bioinformatics

4. LLMs - ChatGPT, Claude, etc.

5. The TAs and me