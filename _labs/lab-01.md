---
title: "Lab 1 - Setting up"
layout: single
---

Today we're going to spend most of our time getting setup with all of the tools
we'll be using throughout the semester. While we're going through these various
activities, please check off the different tasks after you've completed them 
and at the end, you'll push your changes to your github repo. 

There are extra folders and files here just to get you accustomed to the directory
setup we will be using throughout the semester. For more details on what each 
will be used for, please read through the directory_structure.md.

# Objectives
- Get familiar with the SCC OnDemand and VSCode interfaces
- Setup your SSH key on the SCC with GitHub
- Edit your ~/.condarc file to change where your conda packages are stored
- Install the required VSCode plugins  
- Confirm your email and Github ID in the provided form


## SCC and SCC OnDemand

**Lecture (10 minutes)**

[Computational Skills Primer](https://docs.google.com/presentation/d/1FbAWxSftB0tWXEKVv17yU6luyYoJ4PlQsx8qsz6kDHE/present?usp=sharing)

**Activity (5 minutes)**

Ensure you can do the following in VSCode:

- [ ] Open a terminal
- [ ] Create new files and directories
- [ ] Open a new directory as the working directory

Install the following VsCode plugins:

- [ ] R extension for Visual Studio Code (REditorSupport)
- [ ] Jupyter (ms-toolsai)
- [ ] Nextflow (nextflow)
- [ ] Python (ms-python)
- [ ] Snakemake Language (snakemake)

## git / github

**Lecture (10 minutes)**

[git / GitHub](https://docs.google.com/presentation/d/17a8OwDCTyIhzgNgsJkEBWzEu2CPm9x3QKy9ZHR5tyxA/present?usp=sharing)

**Activity (10 minutes)**

We will walk through it together live but if you're more comfortable following
written instructions, please setup a SSH key by following the directions [here](https://www.bu.edu/tech/support/research/system-usage/connect-scc/access-and-security/using-scc-with-github-2fa/#AUTH)

This SSH key will pair your SCC account and github repo and allow you to perform
basic git operations (push and pull) from the command line without having to 
enter a password every time.

You will need to remember to make sure you clone the repo using the appropriate
SSH link, **not** the https protocol. 

- [ ] Successfully setup a SSH key
- [ ] Accept and clone the github classroom link
- [ ] Follow along and make a change to your github repo


## Conda

**Lecture (10 minutes)**

[Computational environments and conda](https://docs.google.com/presentation/d/1VohllvTaP7Ok77ttB2HStDJPtC3LSu-x3Y652AqBfLo/present?usp=sharing)

**Activity (10 minutes)**

We will walk through this together live but if you more comfortable following
written instructions, please edit your .condarc according to the directions 
[here](https://www.bu.edu/tech/support/research/software-and-programming/common-languages/python/python-software/miniconda-modules/#Conda%20Modules)

- [ ] Changed where conda stores packages from your home directory to your
space on /projectnb/bf528/

By the end of this, the .condarc file in your home directory (~/.condarc)
should look like below:

```bash
envs_dirs:
    - /projectnb/bf528/students/<your_loginname>/.conda/envs
    - ~/.conda/envs
pkgs_dirs:
    - /projectnb/bf528/students/<your_loginname>/.conda/pkgs
    - ~/.conda/pkgs
env_prompt: ({name})
```
Please make sure to replace <your_loginname> with your BU username.

After you have completed the above tasks, please run the following commands
to create your first conda environment (wait until each command has finished
successfully):

```bash
module load miniconda
conda env create -f envs/nextflow_env.yml
conda activate nextflow_latest
```

As you can see, you must run this command from the root directory of your repo
and it will build a conda environment from the provided to you. 

This will make a conda environment named "nextflow_latest" which you will be using
throughout the semester. 

The conda environment you just created is active and your terminal should now look 
something like below:

```bash
(nextflow_latest)[your-username@scc-wl2 lab_01]
```

The environment name in parentheses is a reminder that this environment is active in this
shell session. **N.B.** The @scc-wl2 will likely be different as this denotes what node your
session is running on, which is assigned automatically via the queue.

With your environment active, try running nextflow with the `-h`command to see if it
was properly installed:

```bash
 nextflow -h
```

This should print out the help information for running nextflow. 

You can also run the following command to see what packages are installed in your
environment:

```bash
conda list
```

## Computational Pipeline Strategies

**Lecture (30 mins)**

[Nextflow](https://docs.google.com/presentation/d/1ibyJSkFIzO08XsZaa7VQr6FfYwapnwS3tPWvxNIlx7k/present?usp=sharing)

## Tasks for today

- [ ] Confirm your email and Github ID in the provided form
- [ ] Familiarize yourself with SCC OnDemand and VSCode
- [ ] Setup your SSH key on the SCC with GitHub
- [ ] Edit your ~/.condarc file to change where your conda packages are stored
- [ ] Make a change to your repo and push it to GitHub


**Add a check mark to each box and push your changes to your github repo**

You may add a check mark to a box in markdown by using a x (`- [x]`):

- [x] This is a checked off box


**Try to complete the basic hello nextflow training on your own time**
[Nextflow Tutorial](https://training.nextflow.io/latest/hello_nextflow/)

**Please complete the rest of the steps on your own if we run out of time in class**
