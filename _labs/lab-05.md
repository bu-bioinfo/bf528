---
title: "Lab 05 — Typed Channel Operators"
layout: single
---

**Key concepts and tools**
- `.map` — transform or extend a record
- `.filter` — keep records matching a condition
- `.join(ch, by: 'field')` — merge two channels by a shared field name
- `.combine(field: ch)` — cartesian product with a named field appended
- `.flatMap` — expand one record into many
- `.collect()` — aggregate all channel items into a single list
- Operator chaining
- Distinction between operators (driver) and processes (compute nodes)

---

Channel operators transform the streams of records flowing between processes without consuming cluster resources. This lab works through six operators in isolation — first on fake records so the behavior is clear, then on the real bioinformatics patterns they underpin. Each exercise is a short `.nf` script with a `???` placeholder; fill it in and run the script to verify your answer.

## Setup

```bash
module load miniconda
conda activate nextflow_latest
export NXF_SYNTAX_PARSER=v2
```

Run any exercise with:
```bash
nextflow run exercises/01_map.nf -profile local
```

## Exercises

| Exercise | Operator | Fake scenario | Bioinformatics pattern |
|---|---|---|---|
| 01 | `map` | Add a letter grade to student records | Add `reads: List<Path>` to paired-end sample records |
| 02 | `filter` | Keep experiments that passed QC | Keep only treatment samples before differential analysis |
| 03 | `join` | Merge color and weight channels by id | Merge FASTA + FAI channels by sample name for `samtools faidx subset` |
| 04 | `combine` | Pair each sample with three thresholds | Pair each genome with kmer sizes 17/21/25 for jellyfish |
| 05 | `flatMap` | Expand team records into individual member records | Expand multi-replicate samplesheet rows into per-file records |
| 06 | `collect` | Aggregate per-sample measurements for a summary process | Collect FastQC reports for MultiQC |

## Key distinctions

**`join` vs `combine`:**  
`join` matches records one-to-one by a shared field value — it merges parallel outputs from two different processes into a single record. `combine` is a cartesian product — every left record paired with every right value, typically used for parameter sweeps.

**`map` vs `flatMap`:**  
`map` always emits exactly one output per input. `flatMap` emits a list per input — all list elements are emitted individually — so the output channel can be longer than the input.

**`collect` timing:**  
`collect` waits for all upstream items to arrive before emitting. Any process fed by a collected channel will not start until every sample upstream has finished. Use it only when a process genuinely needs all samples at once (e.g. MultiQC).

## Optional challenges

1. Chain `filter` and `map` on the student channel from exercise 01: keep only failing students, then add a `retake: Boolean` field set to `true`.
2. In exercise 03, add a fourth item to `ch_colors` without adding a match in `ch_weights`. Observe that it is dropped. Add `remainder: true` to `.join()` and observe what changes.
