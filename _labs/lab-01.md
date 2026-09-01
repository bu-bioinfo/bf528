---
title: "Lab 01 — Environment Setup"
layout: single
---

**Key concepts and tools**
- `git`, `git clone`, `git add`, `git commit`, `git push`, `git pull`, `git log`
- SSH key authentication (SCC and laptop)
- GitHub as a shared remote — push from one machine, pull on another
- `conda`, `conda env create -f`, `.condarc`
- `module load miniconda`, `conda activate`
- `NXF_SYNTAX_PARSER=v2` — strict Nextflow syntax parser required for
  static typing
- SCC OnDemand, VSCode on a compute node
- HPC concepts: head node vs. compute node, home directory vs. project directory

---

This lab covers the foundational tooling used throughout the semester. You
will configure your SCC account, set up GitHub SSH keys on both
the SCC and your laptop, and redirect your conda package storage to
`/projectnb/bf528/students/<username>` to avoid filling up your home
directory quota. You will install the required VSCode extensions and create
the `nextflow_latest` conda environment (Nextflow) — this environment will
be activated at the start of every subsequent lab.

The git activity demonstrates the core model: GitHub is a shared remote, not
a copy of your code. You push commits from one machine so another machine
can pull them. You will make a change on the SCC, push it to GitHub, clone
the repo on your laptop, then push a second change from the laptop and pull
it back on the SCC. You will follow-up by intentionally introducing a small
merge conflict and learning how to resolve it using the merge editor.

# Learning Objectives

## Perform a complete edit–commit–push–pull cycle across two machines using git

> **Purpose - Why This Matters:** Every subsequent lab and project assumes you
> can move code between instances without losing work or overwriting changes
> unnecessarily
>
> **Task - What you will do:** Set up an SSH key on the SCC and link it to
> GitHub for easy authentication. Practice editing and committing changes in
> a GitHub repository across multiple instances.
>
> **Criteria - How you'll know you're succeeding:** You can explain the
> purpose of each of the commonly used git commands. You understand the
> basics of pushing, and pulling by resolving a simple merge conflict.

## Set up a portable, reproducible conda environment on the SCC

> **Purpose - Why This Matters:** While many of these steps are specific to
> our SCC architecture, their underlying concepts are agnostic and
> universally important. Understanding how to set up a basic conda
> environment to provide an isolated instance of a software package and all
> of the associated setup will be translatable to other HPC and development
> environments.
>
> **Task - What you will do:** Direct conda to store downloaded packages and
> files to dedicated project disk space outside of your home directory.
> Create a basic conda environment containing the latest version of Nextflow
> for use throughout the semester.
>
> **Criteria - How you'll know you're succeeding:** When the conda
> environment is activated, you can run a basic nextflow command
> (nextflow -h) to demonstrate its proper installation. All conda related
> packages are stored in a directory you create in the project disk space,
> not your home directory (you can manually check your ~/.condarc file).

# AIAS Level Expectations

You may use AI freely for this lab at anywhere from levels AIAS 1-5 depending
on your background. The specifics of this lab are not important as every
environment setup will be slightly different: the important takeaways are
the high-level concepts of how these tools allow for reproducibility and
portability and why we care to use them. 


# Additional Resources

- [Nextflow Hello World training](https://training.nextflow.io/latest/hello_nextflow/)
  — complete on your own time
- [SCC SSH + GitHub 2FA guide](https://www.bu.edu/tech/support/research/system-usage/connect-scc/access-and-security/using-scc-with-github-2fa/#AUTH)
- [SCC conda setup](https://www.bu.edu/tech/support/research/software-and-programming/common-languages/python/python-software/miniconda-modules/#Conda%20Modules)
- [GitHub SSH key setup (local machine)](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)