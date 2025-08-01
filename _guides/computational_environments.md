---
title: "Computational Environments Guide"
layout: single
---

A software tool / program / package is at its core just code in a programming
language that usually performs a certain function. In bioinformatics
specifically, many of these tools will perform various statistical tests or data
transformations or data manipulation.

## Don't reinvent the wheel!
Many of the analyses in bioinformatics have already been implemented in a
variety of software packages maintained and released for general use. Whenever
possible, we should make efficient use of the tools available in order to solve
our problems, especially if someone has already solved it!

## Computational Environments
The ability to install and use these different software tools will largely
depend upon three main factors related to the concept of computational
environments:

  1. Hardware / Operating System: Both the physical hardware and the operating
  system you are working with may affect the tools you are able to install and
  utilize. You likely have noticed that many programs and software you already
  use require you to choose specific versions tailored to an operating system or
  in some niche cases, hardware (i.e Apple silicon computers vs. intel-based,
  windows, linux).
  
  2. Dependencies: Software dependencies are other libraries or tools or code
  that the program in question *depend* on in order to work. Many software tools
  / packages reuse existing code and tools and build upon their functionality. 
  Certain tools may have hundreds of dependencies that enable them to function 
  and any changes in those dependencies may potentially change the behavior
  of the program and its operations.
  
  3. Versioning: Many commonly used software tools are regularly maintained and
  updated. In addition to bug fixes, newer versions often contain updated or
  novel features that expand the scope and functionality of the original tool.
  In many cases, these new versions may require newer versions of their
  dependencies and updates may unintentionally change the outputs from
  complicated algorithms or calculations.

## Why is this important?
Science is built on the principle of reproducibility and that results that
reveal to us the ground "truth" should be able to be reproduced in the future by
those performing the experiments and others. Bioinformatics analyses are often
complex, multi-faceted analysis pipelines that utilize a combination of many
different computational and mathematical approaches to transform, manipulate and
analyze data.

This presents a few challenges to reproducibility:

  1. We often have to make certain choices on how we manipulate or transform the
  data that will lead to radically different conclusions.
  
  2. Some of the algorithms and techniques we use are not fully deterministic and 
  may produce slightly different results when repeated. 
  
  3. Systemic changes in the underlying code of software tools or their
  dependencies may propagate across updates and versions, leading to slight
  differences in their behavior and output.
  
Below, we will discuss the various strategies we have for defining a computational
environment that will allow us to use these various tools and how we can ensure
that we (and others) can reproduce any results generated from them.

## Working locally

One strategy for using and installing a tool is to simply download and install
it to your local desktop or laptop. You will need to download the appropriate
version for your system architecture and hope that the installation process
includes any necessary dependencies.

**When you might want to do this**:

- You want to very quickly analyze data or perform a task

- You want to troubleshoot or learn how a certain tool works

**Disadvantages**

- The installation is specific to your exact hardware and operating system

- Difficult to keep track of version and dependencies if you need to report or publish them in a paper

- May not be reproducible outside of your specific environment

- Limited by your personal hardware specifications

## SCC Modules

The SCC IT team has very conveniently pre-installed many different, commonly
used scientific packages and tools directly on the cluster. You may simply type
`module avail` when signed in to a terminal connected to the SCC to see the
available list of tools and their versions available. You may then use the
`module load name_of_tool` command, which will allow you to use the tool and all
of its functionalities. The module system will handle any dependencies and add
the tool to your path for your use.

**When you might want to do this**

- You want to very quickly analyze data or perform a task

- You want to troubleshoot or learn how a certain tool works

- The package isn't available through conda or docker

**Disadvantages**

- You are limited to only the versions pre-installed on the SCC (you may request updates but the SCC team is very busy)

- You are still tied to a specific system architecture (SCC)

- Difficult to keep track of version and dependencies if you need to report or 
  publish them in a paper
  
- May not be reproducible outside of your specific environment

## Miniconda

Miniconda is a software package that provides package, dependency and
environment management for all of the common platforms. Miniconda will allow you
to create separate environments, each containing their own packages and package
dependencies. Miniconda will handle resolving all of the different versions and
package dependencies needed for the requested tools.

**When you might want to do this**

- Miniconda (conda) should be the default environment management tool used if better solutions
like containers are unavailable (more below)

**Disadvantages**

- Still tied to system architecture - conda environments may install system architecture
specific packages

- Miniconda will often break and not be able to resolve package dependencies
for particularly complicated environments

## Containers

Containers package applications and their dependencies in a virtual container that
allows it to run on any platform (linux, windows, macOS). They are isolated,
lightweight and the best method to ensure reproducibility of your computational
environments. We will be using Singularity, a containerization solution, that
is able to run on shared computing environments like the SCC.

**When you might want to do this**

- Whenever possible, containers are the most reproducible and portable method
for ensuring standardization of packages and dependencies

**Disadvantages**

- Docker, a common containerization solution, requires root permissions, which
are unavailable to users on the SCC and most shared clusters. 

## Using Conda on the SCC

To use miniconda on the SCC, we will need to perform a few steps. **Every** time
you wish to use miniconda, you will need to first open a terminal and load the
module for miniconda.

```bash
module load miniconda
```

The **first** time you load miniconda, you will want to perform the following
steps as described
[here](https://www.bu.edu/tech/support/research/software-and-programming/common-languages/python/python-software/miniconda-modules/#Conda%20Modules).
The setup_scc_condarc.sh script will automatically run and edit the conda config
file stored in your home directory, ~/.condarc. 

It will change the location where conda installs all of its packages to a
directory specified. By default, it would install these packages into your home
directory which is only allotted 10gb of storage space.

You should choose to save your environments to your student folder 
/projectnb/bf528/students/<your_username>/. If you manually inspect your .condarc
file (~/.condarc) with `cat` or a text editor, it should look like below:

```bash
envs_dirs:
    - /projectnb/bf528/students/your_bu_username/.conda/envs
    - ~/.conda/envs
pkgs_dirs:
    - /projectnb/bf528/students/your_bu_username/.conda/pkgs
    - ~/.conda/pkgs
env_prompt: ({name})
```

When you have successfully loaded miniconda, you should see a (base) appended
before your username in your terminal. This means conda is active and may be used.

## Best Practices for conda environments / containers for BF528

In order to ensure reproducibility and portability of our computational environments,
we will use the following conventions:

1. Each tool should be installed into its own separate environment / container
    - This ensures the environment / container is lightweight
    - It greatly reduces the chance of version or dependency conflicts between tools
      (e.g. two tools need different versions of the same package) and allows us to 
      use the most up-to-date version of the tool

2. The environment specification for the environment / container should be clear
and transparent. For conda environments, we will encode the environment
description into a YML file named appropriately. YAML files are commonly used
for configuration files as YAML is a human-readable serialization language. For
containers, we will use up-to-date containers hosted on standard registries.

3. We ensure that we specify the exact version of the tool we want installed
For instance, if wanted to create a conda environment to run and use Samtools,
we would create a YML file in our project directory named descriptively
(samtools_env.yml) and use the `conda env create -f samtools_env.yml` to
generate an environment using the specification contained within. That YML file
may look something like the following:
  
```yaml
channels:
- conda-forge
- bioconda

dependencies:
- samtools=1.19.2
```

You'll notice that in addition to setting the appropriate channel priority,
conda-forge first and bioconda second, we directly specify the exact version of
samtools that we want installed. You'll notice we did not specify the versions of
any dependencies as Conda will handle this particular process. We will keep this
YML file contained within the repository in which it is being used. This would allow
us or others to exactly recreate the environment in which the analysis was run. 

N.B. Pinning a specific version does make your environment specification potentially
less portable to other architectures or operating systems if the software maintainers
release different updates for different systems. However, pinning the version is more
important in order to ensure reproducibility of your analysis by using the same version
of the tool. 

You may find which tools and versions are available on conda by using the command:

```bash
`conda search -c conda-forge -c bioconda <tool_name>`.
```

## How we are going to use conda environments / containers

For the most part, we are not going to be directly utilizing these environments
or containers. One of the advantages of nextflow and other workflow managers is 
that they can automatically make use of these conda YML environment specification
files or containers for individual tasks by specifying them in each of the modules.
Nextflow will automatically create these conda environments or download the container
images necessary. 

We will create a single, small conda environment that we will use directly that
contains both Nextflow. Otherwise, we will simply specify the exact conda environments
we'd like created in YML files or a path to a container image, and nextflow will seamlessly
 incorporate it into our workflows.

For project 1, you will be using conda environments that you specify. After
project 1, you will be provided pre-built container images that have the
necessary tool installed. These containers have been built using micromamba as a
base and are hosted on the Github Container Registry.

You will also get experience building Docker containers from scratch and making
them available for use.

You may view all of the containers available for the class here: [BF528 Containers](https://github.com/BF528/pipeline_containers)
