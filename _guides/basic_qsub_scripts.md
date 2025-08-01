---
title: "Basic Qsub Scripts"
layout: single
---

# Introduction to Qsub

Qsub scripts are a way to submit jobs to the SCC. `qsub` is a specific command from the
Open Grid Engine (OGE) queueing system. There are other queueing systems available, such as Slurm,
but the SCC utilizes OGE and `qsub` is the primary command used to submit jobs to the SCC.

## Basic Qsub Script

A qsub script is often created as a shell script. The first line of the script should be the shebang line, which
specifies the interpreter to use to execute the script. In this case, we will be using bash.

The next line will be the qsub directives, which will be used to specify the project, and other
parameters. The only required directive is the project name, which is specified using the `-P` option and 
will be `bf528` for our class.

```bash
#!/bin/bash

# -P bf528

python myscript.py
```

To submit this script, you would run the following:

```bash
qsub myscript.sh
```

## Using Modules

If you check the computational environments guide [here](/guides/computational_environments/), you will see that we 
can make use of pre-installed software packages on the SCC using modules. Although we discourage you from using
modules in your own scripts, it is important to be aware of this functionality as it may be useful in certain   
situations. 

```bash
#!/bin/bash -l

# -P bf528
module load python/3.12

python myscript.py
```

The `-l` flag is important for using modules in qsub scripts.

## Common Directives

The most commonly used directives are:

`-l h_rt`: hard run time limit in hh:mm:ss format. Default, 12 hrs. 

`-P`: The project to which jobs are assigned. This option is *mandatory* for all
      users and used for accounting purposes.

`-l mem_per_core=#G`: Request a specific amount of memory per core. 

`-pe omp N`: Request multiple slots for Shared Memory applications

It is important to note that you cannot change the time limit of a job once it has
been submitted. 

# Managing your batch jobs on the SCC
 
## qstat

Please see this [resource](https://www.bu.edu/tech/support/research/system-usage/running-jobs/tracking-jobs/) from BU SCC IT for detailed information on tracking
your batch jobs using `qstat`

After you've submitted a batch job, you will be able to check the status of any
job by using the following command:

```bash
qstat -u <your-BU-userid>
```

To get detailed information about the resources a job is utilizing, you may use
the following command:

```bash
qstat -j <job ID>
```

This [resource](https://www.bu.edu/tech/support/research/system-usage/running-jobs/allocating-memory-for-your-job/)
from the BU SCC IT group describes briefly the output of the above command. One
of the important metrics to note is the `maxvmem` output, which displays the
maximum amount of virtual memory used during the CPU runtime of the job. This
value should enable you to determine how much memory to request for similar
operations on similarly sized data. 

## qdel

If you wish to delete a job from the queue, you may use the following command:

```bash
qdel <job-id>
```

The job ID for a specific job may be found by using the above `qstat` command

If you wish to delete all of the jobs associated with your username, you may
use the following command:

```bash
qdel -u <your-BU-userid>
```

# Nextflow and qsub

For the most part, you will not need to manually use qsub scripts in your own Nextflow pipelines. 
The profiles we will be using in this class will handle this for you. On the backend, nextflow
is submitting qsub scripts for you, and you can see some of the directives used in the qsub
command in the `nextflow.config` file and the actual qsub script in the work/ directory the process
executes in. See nextflow features [here](/guides/nextflow_features/#nextflow-work-directory) for 
more information.

You may use the same commands to manage and track your jobs as above as all
nextflow processes are submitted as qsub jobs on the backend. 