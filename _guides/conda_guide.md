---
title: "Conda"
layout: single
---

# Overview

Conda is a package manager and environment manager that allows you to manage 
your packages and environments. Conda enables you to create isolated environments
with particular versions of packages installed. Conda also handles the 
dependencies of packages automatically, ensuring that you have the packages and
most importantly, the right versions of the packages you need to run your code.

## Conda Channels

Conda channels are repositories of packages that can be installed using conda.
Developers and maintainers will often contribute their packages to channels
so that others can easily install them. 

In bioinformatics, there are two main channels we will be utilizing:

1. conda-forge
2. bioconda

You will often need to specify these channels when installing bioinformatics
packages via conda to prevent conflicts with other packages or dependencies. 

**N.B.** The order of these channels is important! The order determines the priority
of the channels and where conda will attempt to install the packages from first. 
In bioinformatics, conda-forge should always be specified first, followed by bioconda.

## How we will use conda

For the most part, we will be allowing Nextflow to handle the conda environments
for us. We will simply define the environments we want created in a YML file
and Nextflow will handle the rest. However, it is useful to know a few basic
features and commands for conda. 

You will always be using a single conda environment that has Nextflow installed
whenever you are working on the SCC. 

# Basic Conda Workflow on the SCC (we will not often use this)

Although I have used the term conda, we will actually be using *miniconda* on the SCC.
Miniconda is a stripped-down version of anaconda/conda that only includes the basic functionality
we need to manage our environments. Miniconda on the SCC is available via a module.

The basic workflow for using miniconda is as follows:

1. Load the miniconda module
2. Create a conda environment
3. Activate the environment

## Step 1: Load the miniconda module

```bash
module load miniconda
```

This will load the miniconda module and make the conda commands available to you.

## Step 2: Create a conda environment

```bash
conda create -n nextflow_env -c conda-forge -c bioconda nextflow
```

This will create a new conda environment named `nextflow_env` with Nextflow installed.
Conda will also determine any needed dependencies and install them automatically.

## Step 3: Activate the environment

```bash
conda activate nextflow_env
```

This will activate the environment and make the environment with Nextflow installed
available to you. To the left of your terminal prompt, you should see the name of the
environment you are using (e.g. `nextflow_env`).

# Basic Conda Workflow on the SCC (use this one)

1. Load the miniconda module
2. Activate your environment with Nextflow installed

```bash
module load miniconda
conda activate <name of nextflow environment>
```

Once you've done this, you will simply run Nextflow and as we will discuss later,
it will handle the rest for you. 

# Conda conventions for this class

In this class, you will always define a conda environment by creating a YML file.
This practice will make it transparent exactly what packages and versions were 
used in each analysis. The YML files essentially contain some of the same information
seen in the above conda create command.

You can see an example of a YML file here: 

```yml
name: nextflow_env
channels:
  - conda-forge
  - bioconda
packages:
  - nextflow=24.04.6
```

You can then create the environment using the following command:

```bash
conda env create -f nextflow_env.yml
```

This will create an environment just as the above command would, but with the added
benefit of transparency and documentation of the exact command run. You will 
also notice that we have specified a version of Nextflow to install using the `=`.
We will always be specifying the exact version of the package we want to install.
You can see the same information in this YML file as we saw in the conda create command
and if you needed, you could manually activate this environment after it's made just
as you would with the basic conda workflow.

We will store these YML files in our GitHub repositories which allows anyone to
see what environments were used in our analysis and would enable them to easily
recreate these environments by running the same command we used. 

# Conda and Nextflow

Most workflow managers allow you to define separate environments for each of your
processes. Nextflow in particular allows you to define conda environments with
YML files and specify a different conda environment for each of your processes. 
Nextflow will automatically handle building the environment and activating it 
appropriately for each process. 

Whenever you sign on to work on the SCC, you will need to load the miniconda module
and activate your single conda environment that only has Nextflow installed. 

For your pipelines, you will define YML files that describe your conda environments
for each task and refer to them in the nextflow process. When Nextflow is invoked
with the `-profile conda,<profile_name>` flag, it will automatically take care
of the rest if you've specified conda environments in your processes. 

# Conda Commands

## Create an environment from a YML file

```bash
conda env create -f <env_name>.yml
```

## Create a new environment

```bash
conda create -n <env_name> -c conda-forge -c bioconda <package_name>
```

## List all environments

```bash
conda env list
```

## Remove an environment

```bash
conda env remove -n <env_name> --all
```

## List packages in an environment (environment must be activated)

```bash
conda list
```

## Activate an environment

```bash
conda activate <env_name>
```

## Deactivate an environment

```bash
conda deactivate
```

## Search for available packages

```bash
conda search -c conda-forge -c bioconda <package_name>
```

You will often use this command to see what versions of a package are available,
this is also the command that will show you which version you want to specify, which
will typically be the latest. 

You may also find information on software package versions by looking at the tool's 
documentation (often on GitHub or the tool's website).