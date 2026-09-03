---
title: "Lab 02 — Workflow Basics"
layout: single
---

**Key concepts and tools**
- `wget`, FTP downloads from NCBI
- `qsub`, `qstat`, SGE cluster submission
- Nextflow `process` block: `input`, `output`, `script`
- `workflow` block, typed process inputs/outputs as record fields
- `conda` directive, `envs/` YAML files
- `bin/` directory, `chmod +x`, shebang lines (`#!/usr/bin/env python`)
- `argparse` in Python
-  output publishing
- `nextflow run`, `-profile conda,local`, `-profile conda,cluster`
- `nextflow log <run-name> -f hash,name,exit,status`

---

This lab will walk you through several iterations of workflows and will motivate
why workflow managers are **essential** to performing reproducible and documented
bioinformatics analyses. 

You will be intentionally asked to perform a small set of tasks in non-ideal ways 
to illustrate the different pain points that workflow managers solve. 

# Learning Objectives

## Evaluate and compare the same workflow using either primarily command line interfaces or a workflow manager

> **Purpose - Why This Matters:** To understand why workflow managers were
> invented, it is best to experience how pipelines used to be run to expose
> all of the different failure modes that prevented proper reproducibility
> and portability in computational analyses. 
>
> **Task - What you will do:** Run iterations of the same core tasks
> (downloading a genome, and running a small script) using the command line
> before comparing the behavior when run through a structured workflow
> manager.
>
> **Criteria - How you'll know you're succeeding:** You can state clearly
> what each iteration attempts to fix about the previous one. You observe
> and demonstrate workflow caching by re-running the iteration unchanged and
> observing every process marked as successfully completed.

## Build a multi-process Nextflow pipeline with typed record inputs/outputs and publish reproducible results

> **Purpose - Why This Matters:** Real pipelines are rarely a single
> command — outputs from one step become inputs to the next, and Nextflow's
> typed record system lets the language server catch mismatches before you
> ever submit a job. Keeping final outputs organized outside of `work/` is
> what makes results usable by you and others after the run finishes.
>
> **Task - What you will do:** Refactor a script to accept inputs via
> `argparse` and place it in `bin/` so Nextflow can call it by name. Split a
> single process into two connected processes that pass a typed `record`
> between them. Publish the results of the pipeline to `results/` instead
> of `work/`
>
> **Criteria - How you'll know you're succeeding:** Your pipeline runs
> end-to-end with the download and stats steps as separate processes linked
> by a typed record. Final output files appear in your specified `outdir`
> without needing to search through `work/`.

# AIAS Level Expectations (AIAS Levels 2)

As this is a foundational lab, try to complete most of the tasks on your own.
You may consult LLMs and have them explain concepts but please gain experience
actually performing the tasks manually for this lab. 