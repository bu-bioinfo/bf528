---
title: "Lab 05 — Nextflow Cardinality"
layout: single
---

**Key concepts and tools**
- Channel cardinality: how many separate emissions a channel produces
- Implicit parallelization: one process task per channel emission
- `channel.of(...)` with separate arguments vs. a single list argument
- `record(...)` and dot notation for named fields
- `.view()` and `.count().view()` for inspecting channel contents
- `channel.fromPath(...).splitCsv(header: true)` and `LinkedHashMap` rows
- `.map {}` — 1:1 transformation, cardinality unchanged
- `.flatMap {}` — unpack lists into separate emissions, cardinality grows (or shrinks on empty lists)
- `.combine()` — cross product, N x M emissions
- `.collect()` — gather N emissions into a single list emission
- `.join()` — key-based pairing across two channels, order-independent
- `List<Path>` typed process inputs, `${files.join(' ')}` interpolation in `script:`
- `nextflow run`, `-profile local,conda`

---

This lab focuses on one of the most important, concepts in Nextflow:
**cardinality**, or how many separate values a channel emits. You write a 
pipeline as if it handles a single sample, and Nextflow decides how many tasks
to launch from the number of emissions in the input channel. Getting a channel's 
shape wrong rarely causes an error. 

In Part 1 you will read eight small scripts in `view_cases/`, predict how
each operator changes a channel, and check your predictions with `.view()`
and `.count()`. Record your predictions and results in `ANSWERS.md`. In
Part 2 you will apply `map`, `flatMap`, `combine`, `collect`, and `join`
to finish small pipelines modeled on common bioinformatics tasks: running
FastQC per file, sweeping k-mer sizes across assemblies, merging per-sample
count files into one matrix, and pairing reads with their matching
reference genome.

# Learning Objectives

## Determine the cardinality of a channel and predict how operators change it

> **Purpose - Why This Matters:** Every process in a Nextflow pipeline runs
> once per emission of its input channel. If you can't tell how many
> emissions a channel holds, you can't predict how many tasks your pipeline
> will launch, or whether a process will see one file or all of them.
>
> **Task - What you will do:** For each script in `view_cases/`, read the
> code *before* running it and predict how many lines `.view()` will print
> and whether a single emission is a bare value, a list, or a record. Then
> run the script, add a `.count().view()` call on the same channel, and
> compare the result to your prediction and to the provided diagrams.
>
> **Criteria - How you'll know you're succeeding:** Your predictions in
> `ANSWERS.md` match the observed counts, and when a prediction is wrong you
> can explain why. You can explain why `channel.of('a', 'b')` and
> `channel.of(['a', 'b'])` behave differently, and why brackets in `.view()`
> output are not a reliable way to count emissions.

## Apply channel operators to reshape data for real bioinformatics workflows

> **Purpose - Why This Matters:** Real pipelines constantly change the shape
> of their data. Per-sample steps run in parallel, paired-end files are split
> for independent QC, parameter sweeps multiply work, and results are merged
> for a final summary. Choosing the right operator decides whether a process
> runs with the correct inputs the correct number of times.
>
> **Task - What you will do:** Complete the `main.nf` in each of the `map/`,
> `flatMap/`, `collect/`, and `join/` directories, and verify the already
> wired-up `combine/` example, so that each workflow runs successfully with
> the intended number of tasks.
>
> **Criteria - How you'll know you're succeeding:** Each pipeline runs to
> completion, and the number of tasks for each process matches what you
> expect: one per file for FastQC, N x M for `KMER_COUNT`, exactly one for
> `CONCAT`, and one per sample (not N x M) for `ALIGN`.

## Distinguish between operators that preserve, expand, multiply, collapse, or pair emissions

> **Purpose - Why This Matters:** Several operators look alike but have very
> different effects on cardinality. Mixing up `combine` and `join`, or `map`
> and `flatMap`, is a common silent bug that can produce wrong results
> without any error message.
>
> **Task - What you will do:** Compare how each operator transformed the
> channels in Parts 1 and 2, including edge cases such as `flatMap` over an
> empty list and chaining `flatMap` with `map`.
>
> **Criteria - How you'll know you're succeeding:** Given an input channel
> and an operator, you can state the output cardinality (1:1, 1:many, N x M,
> N to 1, or matched by key) and choose the right operator for a described
> pipeline step.

# AIAS Level Expectations (AIAS Level 2)

As this is a foundational lab, try to complete most of the tasks on your own.
In particular, make your Part 1 predictions yourself *before* running any
code or asking an LLM. The point of the exercise is to build your own
intuition for channel shapes. You may consult LLMs to explain operators or
concepts, but write and debug the Part 2 channel logic yourself.
