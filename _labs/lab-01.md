---
title: "Lab 01 — Environment Setup"
layout: single
---

**Key concepts and tools**
- `git`, `git clone`, `git push`, `git pull`
- SSH key authentication
- GitHub and GitHub Classroom
- `conda`, `conda env create -f`, `.condarc`
- `module load miniconda`, `conda activate`
- SCC OnDemand, VSCode on a compute node
- HPC concepts: head node vs. compute node, home directory vs. project directory

---

This lab covers the foundational tooling used throughout the semester. You will configure your SCC account, set up a GitHub SSH key so you can push code without a password, and redirect your conda package storage to `/projectnb/bf528/students/<username>` to avoid filling up your home directory quota. You will install the required VSCode extensions (R, Jupyter, Nextflow, Python, Snakemake) and create the `nextflow_latest` conda environment from the provided YAML — this environment will be activated at the start of every subsequent lab.

## Setup checklist

- [ ] Familiarize yourself with SCC OnDemand and VSCode
- [ ] Set up an SSH key and link it to GitHub
- [ ] Edit `~/.condarc` to redirect conda package storage:

```bash
envs_dirs:
    - /projectnb/bf528/students/<your_loginname>/.conda/envs
pkgs_dirs:
    - /projectnb/bf528/students/<your_loginname>/.conda/pkgs
```

- [ ] Create the course Nextflow environment:

```bash
module load miniconda
conda env create -f envs/nextflow_env.yml
conda activate nextflow_latest
nextflow -h   # confirm it installed correctly
```

- [ ] Accept the GitHub Classroom link, clone the repo, make a change, and push it
- [ ] Submit your BU email and GitHub username via the course form

## Resources

- [Nextflow Hello World training](https://training.nextflow.io/latest/hello_nextflow/) — complete on your own time
- [SCC SSH + GitHub 2FA guide](https://www.bu.edu/tech/support/research/system-usage/connect-scc/access-and-security/using-scc-with-github-2fa/#AUTH)
- [SCC conda setup](https://www.bu.edu/tech/support/research/software-and-programming/common-languages/python/python-software/miniconda-modules/#Conda%20Modules)
