---
title: "Project Report Guidelines"
layout: single
---

# Project Report Guidelines

This document describes the lightweight specification and reporting format
used for pipeline-engineering projects in this course. Every project will be
given its own specification built from the sections below. For each section,
this page first describes what it should contain in general, then shows how
it reads in practice using a sample pipeline as an example. 

This spec should be included in your repo alongside the project and should be
done prior to any actual work on the pipeline. It will not be graded for 
"correctness" but you will be given feedback on how to improve the document.

## Specification sections

### Objective

**What to include:** A sentence or two stating what the pipeline takes as
input and what it produces, in plain terms — someone unfamiliar with the
project should be able to read this and know what it's for. Try to be as
specific as possible in terms of the experiment. As you can see below,
the sample specifically mentions paired-end data as the default input. 

**Example — Project:** A Nextflow pipeline that takes paired-end FASTQ
files and a reference genome, and produces per-sample alignment statistics
and a combined MultiQC report, flagging any sample that fails QC thresholds.

### Inputs

**What to include:** The exact files or data structures the pipeline
expects to receive, including format details (e.g. column names for a
samplesheet) needed to actually run it. Again, try to be as specific as
possible while thinking about best practices in making pipelines portable
and reproducible. For example, avoiding hardcoded paths or having a single
source of truth that drives the workflow (i.e. the CSV samplesheet).

**Example — Project:** Samplesheet (CSV: `sample_id`, `fastq_1`,
`fastq_2`), reference FASTA + GTF.

### Outputs

**What to include:** What the pipeline produces, split by whether it's
generated per-sample or combined across all samples.

**Example — Project:**
- Per-sample: FastQC reports, STAR alignment BAM + log, RSeQC read distribution
- Combined: one MultiQC HTML report across all samples

### Pipeline steps

**What to include:** A table listing each process, the type of input it
consumes, and the upstream process(es) it depends on (by name, or `None` if
it only consumes raw input). Naming dependencies by process rather than just
a linear reading order captures the actual DAG — including which steps have
no dependency on each other and can run in parallel.

**Example — Project 2:**

| Step | Input type | Depends on |
|---|---|---|
| `FASTQC` | Raw FASTQ | None |
| `STAR_ALIGN` | Raw FASTQ + reference genome | None |
| `RSEQC` | BAM | `STAR_ALIGN` |
| `MULTIQC` | FastQC reports, STAR logs, RSeQC output | `FASTQC`, `STAR_ALIGN`, `RSEQC` |

### Development workflow — build with stub-run first

**What to include:** Every process must define a `stub:` block producing
placeholder output files that match the real process's expected output
names and types. Students should implement and validate the entire pipeline
DAG using `nextflow run main.nf -stub-run` before running on real data —
this verifies channel wiring, process dependencies, and input/output shapes
in seconds rather than waiting on real compute. Every process needs a stub,
including any aggregation step at the end of the pipeline — without one,
`-stub-run` will still invoke that step for real against whatever
placeholder files the upstream stubs produced, which will error or produce
meaningless output rather than validating anything. Only after the
stub-run completes cleanly end-to-end should the pipeline be run without
`-stub-run` against real data.

**Example — Project:** A touch'd BAM for `STAR_ALIGN`, a placeholder text
file for `RSEQC`. `MULTIQC` must also have a stub — without one, `-stub-run`
would invoke real MultiQC against the upstream placeholder files instead of
validating the DAG. The stub-run must complete cleanly for all 3 samples
before running against real data.

### Environment & reproducibility

**What to include:** Every process must declare its software environment
explicitly — a container (Docker or Singularity image) or a conda/mamba
environment — pinning the exact tool version required. No process may rely
on tools already present on the executing machine's `PATH`. This is
independent of the executor profile (e.g. `-profile local`), which controls
*where* processes run; the environment directive controls *what software*
each process runs with, and must be declared regardless of executor.
Environment definitions (Dockerfiles, `environment.yml` files, or
Biocontainers/BioConda references) should be provided alongside the
pipeline code, not as a separate undocumented setup step.

In this course, this is achieved either through conda environments or
pre-built Singularity containers, depending on the project — see below.

**Example — Project (conda):** Conda environments defined per-tool in
`envs/*.yml` (e.g. `envs/flye.yml`), referenced via each process's `conda`
directive and invoked with `-profile cluster,conda`.

**Example — Project (Singularity):** Pre-built containers at
`ghcr.io/bf528/<tool>:latest` (e.g. `ghcr.io/bf528/star:latest`),
referenced via each process's `container` directive and invoked with
`-profile singularity,local`. Tool versions: Nextflow 24.x, STAR 2.7.x,
FastQC 0.12.x, RSeQC 5.x, MultiQC 1.2x.

### Resource requirements

**What to include:** Each process must declare `cpus` and `memory`
directives sized appropriately for its workload. Declaring resource
limits — even generous ones — is part of the assignment, not just making
the pipeline run.

**Example — Project:** `STAR_ALIGN` is memory-intensive when loading a
genome index.


### Success criteria

**What to include:** Split into a stub-run milestone (validates DAG wiring
only) and a full-run milestone (validates actual results), so students have
a concrete, checkable definition of "done" at each stage.

**Example — Project:**
- **Stub-run milestone:** `nextflow run main.nf -stub-run -profile local`
  completes end-to-end for all 3 samples without errors, producing
  correctly-named placeholder outputs at every step (including `MULTIQC`).
- **Full-run milestone:** Pipeline runs end-to-end on the 3-sample test set
  with `-profile local` without manual intervention; MultiQC report opens
  and shows all 3 samples

### Out of scope

**What to include:** Explicitly name what the pipeline is *not* expected to
do, so students don't over-build or assume missing steps are an oversight.
For each item, include a short justification for why it's excluded. Out of
scope means for the pipeline work only, not the overall project.

**Example — Project:** Differential expression (performed manually in a
Jupyter notebook), adapter trimming (STAR soft-clips adapter contamination
from reads).

## Deliverables & submission

**What to include:** All work for a project lives in a single GitHub
repository. At minimum, this repo should contain:

- [ ] The pipeline itself — you'll be given a template to build on, so this
      is just whatever the template needs to run (`main.nf`,
      `nextflow.config`, `modules/`, environment definitions)
- [ ] The specification document from above, saved as `specifications.md`
      at the top level of the repo. This is written before you start
      building, and updated as you go. At the time of submission, it should
      contain:
  - [ ] A completed validation table — one row per analysis stage (e.g.
        "Sequencing quality control", "Alignment"), not necessarily one row
        per Nextflow process; a stage may bundle several processes, unlike
        the process-level DAG table above. Include any milestones named in
        the spec's success criteria as their own rows. For each row:
        - **Parameter justification:** why you chose the specific parameter
          values or thresholds used at that stage — the reasoning behind
          the choice, not a restatement of what the parameter does.
        - **Confidence:** self-rated (e.g. High/Medium/Low).
        - **Validation:** the concrete check you actually ran to confirm
          that stage works — a specific comparison, inspection, or test you
          can run to verify success. As the workflow manager handles
          whether the process ran correctly, this should reflect how you'd
          verify the output from an analysis perspective.
- [ ] The project report, usually a `.ipynb` or `.Rmd`
- [ ] `README.md` with a short description of the repo

**Example — Project `specifications.md` table:** the entries below are
illustrative sample values only, meant to show the level of specificity
expected — your own pipeline's justifications, confidence, and validation
checks will be different.

| Step | Parameter justification *(sample)* | Confidence *(sample)* | Validation *(sample)* |
|---|---|---|---|
| Sequencing quality control | Default FastQC parameters; adapter trimming skipped since STAR soft-clips at alignment | High | Per-base quality >Q30 across all cycles, all 3 samples |
| Alignment | Default STAR parameters, appropriate for 100bp paired-end reads | Medium | 88-92% uniquely-mapped across samples |
| Post-alignment QC | Default RSeQC settings; no strandedness flag since library prep is unstranded | Medium | >80% of reads in CDS exons + UTRs, consistent with poly-A selection |
| QC aggregation & reporting | Default MultiQC settings; no custom config needed | High | All 3 samples present in every module of the report |

## Scientific deliverables

The checklist above covers the pipeline as an engineering artifact — it
does not by itself constitute the project. Each project will separately
specify the scientific/biological deliverables expected of it (e.g.,
specific figures, tables, or biological interpretation produced from the
pipeline's output). Consult the individual project description for what's
required there, in addition to the engineering deliverables above.
