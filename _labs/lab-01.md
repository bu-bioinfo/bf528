---
title: "Lab 1 - Setting up"
layout: single
---


Today we're going to spend most of our time getting setup with all of the tools
we'll be using throughout the semester. While we're going through these various
activities, please check off the different tasks after you've completed them 
and at the end, you'll push your changes to your github repo. 

# Objectives
- Get familiar with the SCC OnDemand and VSCode interfaces
- Setup your SSH key on the SCC with GitHub
- Edit your ~/.condarc file to change where your conda packages are stored
- Install the required VSCode plugins  
- Confirm your email and Github ID in the provided form

## Computational Pipeline Strategies

**Lecture (30 mins)**

## SCC and SCC OnDemand

**Lecture (10 minutes)**
[Computational Skills Primer](https://docs.google.com/presentation/d/1FbAWxSftB0tWXEKVv17yU6luyYoJ4PlQsx8qsz6kDHE/present?usp=sharing)

**Activity (5 minutes)**

Ensure you can do the following in VSCode:

- [ ] Open a terminal
- [ ] Create new files and directories
- [ ] Open a new directory as the working directory


## git / github

**Lecture (10 minutes)**
[git / GitHub](https://docs.google.com/presentation/d/17a8OwDCTyIhzgNgsJkEBWzEu2CPm9x3QKy9ZHR5tyxA/present?usp=sharing)

**Activity (10 minutes)**

We will walk through it together live but if you're more comfortable following
written instructions, please setup a SSH key by following the directions [here](https://www.bu.edu/tech/support/research/system-usage/connect-scc/access-and-security/using-scc-with-github-2fa/#AUTH)

This SSH key will pair your SCC account and github repo and allow you to perform
basic git operations (push and pull) from the command line without having to 
enter a password every time.

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


After you have completed the above tasks, please run the following command
to create your first conda environment:

```bash
conda env create -f envs/nextflow_env.yml
```

As you can see, you must run this command from the root directory of your repo
and it will build a conda environment from the provided to you. 

This will make a conda environment named "nextflow_latest" which you will be using
throughout the semester. 

## Objectives for today

- [ ] Confirm your email and Github ID in the provided form
- [ ] Familiarize yourself with SCC OnDemand and VSCode
- [ ] Setup your SSH key on the SCC with GitHub
- [ ] Edit your ~/.condarc file to change where your conda packages are stored
- [ ] Make a change to your repo and push it to GitHub

Install the following VsCode plugins:
- [ ] R extension for Visual Studio Code (REditorSupport)
- [ ] Jupyter (ms-toolsai)
- [ ] Nextflow (nextflow)
- [ ] Python (ms-python)
- [ ] Snakemake Language (snakemake)

Check off the boxes and push your changes to your remote repo.