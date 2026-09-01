---
title: "Lab 05 — Sequencing Quality Control"
layout: single
---

**Key concepts and tools**
- FastQC: per-base quality (PHRED score), per-base sequence content, duplication
  levels, overrepresented sequences
- STAR alignment statistics: uniquely mapped, multi-mapped, and unmapped
  percentages
- RSeQC read distribution: CDS exons, UTRs, introns, intergenic regions
- MultiQC as a combined report across tools and across samples
- Poly-A selected mRNA-seq library prep and its expected biases
- Known contamination signatures: adapter, incomplete gDNA, rRNA,
  cross-species (bacterial, wrong-genome alignment)
- Distinguishing an expected library-prep artifact from a genuine
  experimental failure

---

This lab has two parts and no coding. In Part 1, in small groups, you will
rank a list of common sequencing artifacts and alignment statistics from most
to least concerning for a 2x100nt paired-end mRNA-seq experiment, reasoning
about which issues may be corrected downstream and which represent real problems
with the underlying data.

In Part 2, you will apply that same reasoning to six real QC reports (Case A
through Case F), each bundling FastQC, STAR, and RSeQC output plus a combined
MultiQC report. For each case you will cite specific statistics from all three
tools, match the case to one of six likely lab or alignment situations
(adapter contamination, gDNA contamination, bacterial contamination, rRNA
contamination, wrong-genome alignment, or a clean validated run), propose a
follow-up analysis to confirm the match, and make an explicit recommendation to
proceed or not proceed with the analysis.

Record both parts' answers in `worksheet_template.md`.

# Learning Objectives

## Interpret sequencing QC metrics by their impact on downstream analysis

> **Purpose - Why This Matters:** Understanding what per-base quality scores,
> duplication levels, per-base sequence content, and alignment statistics
> actually measure is foundational to reading any FastQC/STAR/RSeQC report
> correctly. Knowing which metrics can be mitigated, which represent known
> artifacts, and which represent experimental issues is critical for judging
> whether to proceed with an analysis or not.
>
> **Task - What you will do:** Rank a list of common sequencing artifacts and
> metrics from most to least concerning. Reason about the severity of each
> artifact and whether any downstream steps correct or mitigate for it.
>
> **Criteria - How you'll know you're succeeding:** You can place each metric
> into the context of the protocol that generated it. You can distinguish
> fundamental errors in data generation from artifacts that are inherent to
> the methodology.

## Apply knowledge of expected technical artifacts

> **Purpose - Why This Matters:** Many "abnormal-looking" QC signals are
> well-documented, expected artifacts of standard mRNA-seq library prep
> rather than genuine problems — a FastQC module can fail on a perfectly
> successful experiment. Common sequencing issues also have distinct
> signatures in these statistics. Telling the two apart avoids wasting effort
> re-sequencing data that's actually fine, or analyzing data that cannot be
> rescued.
>
> **Task - What you will do:** For each of the six cases, decide which
> flagged metrics are expected artifacts and which are genuine causes for
> concern.
>
> **Criteria - How you'll know you're succeeding:** Your Part 1 ranking and
> Part 2 case write-ups justify each artifact-vs-concern classification with
> a specific technical reason, such as library-prep chemistry or an aspect of
> the underlying biology.

## Analyze and evaluate a full QC report

> **Purpose - Why This Matters:** Real sequencing QC reports rarely have one
> metric that tells the whole story, and there are expected biases baked into
> the sequencing methodology itself. Drawing a sound conclusion requires
> weighing several statistics together across every step of the workflow —
> sequencing QC, alignment, and read distribution.
>
> **Task - What you will do:** For each case, synthesize at least 2-3 cited
> statistics per tool (FastQC, STAR, RSeQC) into a short paragraph judging the
> experiment's success.
>
> **Criteria - How you'll know you're succeeding:** Each case's paragraph
> draws a conclusion that follows from the *combination* of cited statistics,
> not from any single metric in isolation.

## Justify a decision to proceed or not proceed with the analysis

> **Purpose - Why This Matters:** Deciding whether to trust a dataset enough
> to commit further analysis time to it is a routine judgment call for any
> bioinformatics analyst, and one that must be defensible and remains the
> responsibility of the individual scientist.
>
> **Task - What you will do:** For each case, state whether you would proceed
> with further analysis and why. Match each case to its likely situation from
> the six given, and identify which case is the fully validated, high-quality
> experiment.
>
> **Criteria - How you'll know you're succeeding:** Each recommendation is
> unambiguous (proceed / do not proceed) and traceable to the statistics you
> cited for that case. For every case, you can suggest at least one follow-up
> analysis that would confirm your matched situation.

# AIAS Level Expectations

This entire lab is AIAS Level 1 (No AI). Judging whether sequencing data is
trustworthy enough to build an analysis on is a core scientific
responsibility that cannot be delegated to an LLM — if you publish
conclusions based on data an AI wrongly judged sound, that responsibility is
still yours. Work through both parts with your group using your own reasoning
about the statistics in front of you.
