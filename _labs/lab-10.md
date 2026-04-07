---
title: "Lab 10 — Snakemake"
layout: single
---

**Key concepts and tools**
- `Snakefile`, `rule`, `input`, `output`, `shell`
- `rule all` — declaring target outputs
- Wildcards (`{sample}`) — generalization across samples
- `expand()` — generating lists of expected outputs
- `snakemake --workflow-profile` — cluster submission
- `conda:` directive per rule
- DAG: directed acyclic graph of rules
- `samtools sort`, `samtools index`

---

Snakemake is an alternative workflow manager that reasons backward from desired output files rather than forward from inputs. This lab starts with a single-rule example to establish the syntax, then moves to a multi-sample pipeline that uses wildcards to generalize across samples without repeating code. You will fill in `samtools sort` and `samtools index` rules and specify their file dependencies, observe how Snakemake constructs the execution DAG, and run the pipeline on the cluster using a profile. The goal is not to replace Nextflow but to understand how a file-centric workflow manager thinks differently about the same problem.

---

## Setup

Create the Snakemake conda environment from the provided YAML:

```bash
conda env create -f envs/snakemake_env.yml
conda activate snakemake_env
```

## Part 1 — single/

Look at the `Snakefile`. It closely resembles the example from lecture: a `rule all` that declares the final target, and individual rules that specify how to produce each file.

```bash
snakemake -s Snakefile
```

Observe what is created and where. Snakemake checks for the existence of declared output files after each rule executes.

## Part 2 — multi/

Look at the files in `samples/`. Note what portion of each filename is shared and what portion is unique.

Snakemake generalizes across samples using **wildcards** — any string in curly braces `{sample}` that it infers from the filesystem:

```python
rule samtools_sort:
    input:
        bam = 'samples/{sample}.bam'
    output:
        sorted_bam = 'results/{sample}.sorted.bam'
    shell:
        'samtools sort {input.bam} > {output.sorted_bam}'
```

**Tasks:**

1. Declare the two final target files in `rule all`:
   - `results/sampleA.sorted.bam.bai`
   - `results/sampleB.sorted.bam.bai`

2. Fill in the rules for `samtools_sort` and `samtools_index`:
   - `samtools_sort` input: the starting BAM files; output: redirect sorted output to a new file
   - `samtools_index` input: the output of `samtools_sort`; output: the `.bai` index (same name + `.bai`)

3. Run with the cluster profile:

```bash
snakemake -s Snakefile --workflow-profile profile/
```

## Part 3 — advanced/

Extends the multi-sample pipeline to handle paired-end reads. Explore how `expand()` generates lists of expected outputs and how the profile specifies cluster resource requests per rule.

## Key differences from Nextflow

| | Snakemake | Nextflow |
|---|---|---|
| Reasoning direction | Backward from outputs | Forward from inputs |
| Parallelism unit | Rule × wildcard combination | Process × channel element |
| Data representation | File paths | Channels |
| Language | Python | Groovy / DSL2 |
| Config | `config.yaml` | `nextflow.config` |
