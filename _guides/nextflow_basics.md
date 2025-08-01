---
title: "Nextflow Basics"
layout: single
--- 

# Setting up to run Nextflow on the SCC

We will be creating a single conda environment that contains only the nextflow
package. We will activate this environment every time we want to run Nextflow 
on the SCC.

Remember that when you first begin working on the SCC, you will need to load
the module for miniconda and either create the nextflow conda environment or 
activate it if it already exists. 

Just like for other conda environments, we will encode the environment 
specification in a YAML file. This will allow us to create the environment 
on any system that has conda installed. It also improves the reproducibility 
of your workflow by making all of the environment specifications explicit.

This environment should contain only the most up-to-date version of Nextflow. 
Other tools and packages will be specified in their own YAML files and the 
installation of each will be handled by Nextflow.

This series of steps will look something like below:

Create a YML file with the most recent version of nextflow installed:

```yml
name: nextflow_env
channels:
- conda-forge
- bioconda

dependencies:
- nextflow=25.04.6
```

Then you will need to create the environment using the following command:

```bash
conda env create -f nextflow_env.yml
``` 

And then activate it:

```bash
conda activate nextflow_env
``` 

If you've done these previous steps, you would simply do the following:

```bash
module load miniconda
conda activate nextflow_env
```

# Running Nextflow on the SCC

There are several ways to run Nextflow on the SCC using our different profiles.

The most common combinations will be:

## -profile local,conda

```bash
nextflow run main.nf -profile local,conda
```

This set of profile options will run nextflow on the interactive node where your
VSCode terminal is running. We will be using this particular running method
when we are troubleshooting the pipeline and when working with any subsets of
the data. Remember that although the VSCode terminal is running on a compute node,
we will still only be able to run relatively small tasks as our VSCode session
only requested a small amount of resources.

## -profile cluster,conda

```bash
nextflow run main.nf -profile cluster,conda
```

This set of profile options will run nextflow on the SCC compute nodes and also
instruct Nextflow to build or activate any conda environments specified in the
pipeline modules per task. Importantly, this will allow the pipeline to submit
multiple tasks to the SCC compute nodes and run them in parallel. The number of
jobs dispatched is controlled by the executor settings in the Nextflow config
file. You can see the $sge directive and the `queueSize` flag is by default
set to 8. This means that by default, Nextflow will submit up to 8 jobs to the SCC
compute nodes at the same time. You can adjust this number as needed but remember
that the SCC is a shared resource and that depending on your pipeline, there's only
so many jobs that can run in parallel.

## -profile cluster,singularity

```bash
nextflow run main.nf -profile cluster,singularity
```

This set of profile options will run nextflow on the SCC compute nodes and also
instruct Nextflow to pull the singularity container specified in the pipeline
modules per task. After project 1, this is the profile you will use going forward.
It will both submit jobs properly to the cluster with appropriate resources requests
and pull the singularity container specified in the pipeline modules per task.


# -stub-run

```bash
nextflow run main.nf <options> -stub-run
```

You may add the `-stub-run` flag to any of the above profile options to run the 
pipeline in stub mode. This will allow you to see what the pipeline will do without
actually running it. This is ideal for troubleshooting the actual channel logic
of your pipeline without waiting for the jobs to actually run on the SCC. You can
also use this stub-run even when you have not yet constructed the appropriate
command for each task in your pipeline. 

The stub modules in your processes have been pre-configured to mimic what the
output of each task should produce to enable you to develop the logic in your
main.nf.
