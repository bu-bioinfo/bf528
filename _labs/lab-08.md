---
title: "Lab 08 — Differential Expression with DESeq2"
layout: single
---

**Key concepts and tools**
- R Markdown documents: running chunks in order, knitting to HTML
- Tidyverse basics: `select()`, `filter()`, `mutate()`, `arrange()`, `group_by()` + `summarize()`, and the pipe `%>%`
- Reading delimited files with `read_tsv()` / `read_csv()` into tibbles
- Wide vs. long tables with `pivot_longer()` and `separate()`
- `ggplot()` + `aes()` + `geom_*()` layers for basic plots
- The sample table (`colData`) and factor reference levels
- `DESeqDataSetFromMatrix()` and the design formula
- Filtering low-count genes before testing
- `vst()`, `plotPCA()`, and sample-distance heatmaps with `pheatmap()`
- `DESeq()` and `results()`: log2 fold change, p-value, and adjusted p-value (`padj`)
- Interpreting a result with few or no significant genes
- Revising a design formula when new sample information becomes available
- Joining gene symbols onto results with `left_join()`
- Ranked gene lists for FGSEA and significant gene lists for DAVID / Enrichr
- Reviewing generated plotting code critically

---

This lab walks through a complete bulk RNA-seq differential expression analysis
in R using **DESeq2**. The data are from a real experiment consisting of gene
counts from 8 mice, 4 wild-type (WT) and 4 knockout (KO), produced by a pipeline
like the one you built earlier in the course. We want to know which genes are
differentially expressed between KO and WT. 

You don't need to know any R beforehand. Part 0 of `Lab_DESeq2.Rmd` covers the
basics of R and the tidyverse. You will then load and tidy the count matrix,
build a sample table, explore the samples with PCA and a sample-distance
heatmap, and run DESeq2. The result will not be what the researchers expected.

After the class discussion, Part 2 (`Re-analysis.Rmd`) gives you the missing
piece of information. You will add it to the analysis, compare the results to
your first attempt, and look closely at the genes that change. The last section
previews tasks you will need for Project 2: adding gene symbols, building ranked
and significant gene lists, running FGSEA, and checking plots.

# Learning Objectives

## Read, reshape, and plot tabular data in R using the tidyverse

> **Purpose - Why This Matters:** Nearly every step of a downstream analysis,
> from loading counts to filtering results to preparing gene lists, is a
> table operation. Being able to select, filter, reshape, and join tables lets
> you get your data into the form that each tool expects, and check it along
> the way.
>
> **Task - What you will do:** Work through Part 0 and Part 1 of
> `Lab_DESeq2.Rmd`. Practice the core tidyverse verbs on a small example table,
> then use them to clean the real count matrix, reshape it from wide to long,
> plot counts for individual genes, and build the sample table.
>
> **Criteria - How you'll know you're succeeding:** You can explain what each
> step of a pipe does to the table, predict the number of rows after
> `pivot_longer()`, and write your own short pipe that filters and sorts a
> table.

## Build and run a DESeq2 differential expression analysis

> **Purpose - Why This Matters:** DESeq2 is one of the most widely used tools
> for bulk RNA-seq differential expression. Knowing what goes into a
> `DESeqDataSet` (counts, sample information, and a design formula) and what
> comes out of `results()` is the foundation for interpreting any DE analysis.
>
> **Task - What you will do:** Build a `DESeqDataSet` from the count matrix
> and sample table, filter low-count genes, run `DESeq()`, and turn the
> results into a sorted tibble. Use the DESeq2 vignette to find the functions
> you need for the TODO chunks.
>
> **Criteria - How you'll know you're succeeding:** Your notebook knits
> without errors. You can explain what the reference level does to the sign of
> a fold change, why genes are filtered before testing, and the difference
> between `pvalue` and `padj`.

## Use exploratory plots to assess sample quality and structure

> **Purpose - Why This Matters:** Statistical tests only answer the question
> you ask them. PCA and sample-distance heatmaps show you what the dominant
> sources of variation in your data actually are, which may or may not be the
> variable you are testing.
>
> **Task - What you will do:** Apply a variance-stabilizing transformation,
> make a PCA plot and a sample-distance heatmap, and describe which samples
> group together.
>
> **Criteria - How you'll know you're succeeding:** You can state what PC1
> separates, whether that matches genotype, and write down a hypothesis for
> the structure you see.

## Reason about an unexpected result and revise the analysis

> **Purpose - Why This Matters:** A result with few or no significant genes does
> not mean "no effect". It can come from biology, from poor-quality samples,
> or from an analysis that does not match how the experiment was done. Telling
> these apart, and knowing what information to ask your collaborators for,
> is a core skill in real analyses.
>
> **Task - What you will do:** Discuss with your classmates what might explain
> the first result, using only the counts and the sample table. In Part 2,
> incorporate the new information into the design, re-run DESeq2, and compare
> the two models gene by gene.
>
> **Criteria - How you'll know you're succeeding:** You can explain in a few
> sentences why the two models give different results, use plots of individual
> genes to show why, and describe how the experiment could have been designed
> to avoid the problem.

# AIAS Level Expectations (AIAS Level 2)

As this is a foundational lab, try to complete most of the tasks on your own.
In particular, form your own hypothesis for the Part 1 discussion *before*
asking an LLM. The point of the exercise is to practice reading your own data
critically. You may consult LLMs to explain R syntax, DESeq2 functions, or
statistical concepts, but write the analysis code yourself, using the DESeq2
vignette as your main reference. Generating plotting code with an LLM is
acceptable, as long as you review it as described in the Plotting section of
`Re-analysis.Rmd`.
