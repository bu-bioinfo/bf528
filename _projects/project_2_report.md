---
title: "Project 2: RNAseq"
layout: single
---

# Purpose

In this project you will analyze an RNAseq experiment without knowing which
study it comes from. Working blind lets you form your own interpretation of the
data before you see what the authors concluded. The goal is not only to run the
pipeline correctly, but to evaluate what the data can and cannot tell you,
commit to an interpretation, and then compare it critically with the published
work.

This structure is not meant as a **gotcha** or to make the project harder. I want
you to explore the data and form your own conclusions without bias, rather than
deferring to what the paper stated was "interesting". Remember that every scientific
paper is a highly curated story of what the authors found significant or novel
based on their own research questions, interests, and the constraints of publication;
there may be other interesting results or findings that were not as remarked upon.
You are not expected to find something novel or something the authors missed; 
matching their findings is just as valid an outcome.

# Project structure

This project has two phases:

- **Phase 1 (blind analysis):** You will receive the data and sample metadata
only. You will process the data, evaluate its quality, perform differential
expression and enrichment analyses, and write your own interpretation of what
happened in this experiment.
- **Phase 2 (informed analysis):** Roughly halfway into the project (2 weeks in),
I will tell you the publication and experiment this data originated from. You will
then replicate figures from the paper and compare your findings with the authors'.
You should not revise your Phase 1 interpretation; it's simply meant
as a way for you to compare results.

# Working in an R Markdown notebook

For this project, since we are working with DESeq2, it will be easier to work
in an R Markdown notebook. R Markdown notebooks are highly similar to Jupyter
notebooks and allow you to write R code and markdown in the same file.

# Phase 1: Blind analysis

## Experimental Design (1 paragraph)

Using only the sample metadata you were given, describe the experiment:

- How many groups are there, and how many replicates per group?
- What covariates are provided (e.g. sex, batch, sequencing run)?
- What comparison(s) can this design support? What kinds of effects might it be
unable to detect?
- What potential confounders would you be concerned about, and can you account
for them with the information you have?

## Methods (as long as needed)

Please view the presentation here for guidelines: [methods]({{ site.baseurl }}/_lectures/accessory-slides.md)

The methods section should concisely describe which steps were taken in the
analysis of the data. Remember to adhere to our conventions for writing a
methods section, including specifying the software versions used and the
parameters for each step. If no parameters are changed, state that default
parameters were used. Remember that a methods section should include any details
that are necessary for someone else to replicate your analysis exactly. You can
exclude any details that should not affect the results, such as the exact file
paths used.

- Write a methods section for the pipeline you developed for project 2

## Read Quality Control (1-2 paragraphs)

Use the MultiQC report or the individual logs from FastQC and STAR to evaluate
the quality of the reads. Please make sure that at minimum you specifically
mention the following (even if there's no issue, state that there is no issue):

- The range of the number of reads in all the samples
- Any potential issues with the reads as flagged by FastQC
- Any overrepresented sequences, or adapter contamination in the reads
- The alignment rate of the reads to the reference genome
- Multimapping rate
- Identify the single metric that concerns you most, even if nothing failed,
and state what value of that metric would have made you stop the analysis
- Based on your evaluation above, please state whether you believe the
experiment was of high quality and was suitable for downstream analysis. If
not, please state what you would do to improve the quality of the reads.

## Filtering the Counts Matrix (1-2 paragraphs)

Please describe the filtering process you used to filter the counts matrix.

- Ensure that you include the two plots that show the distribution of counts
before and after filtering
- State the number of genes present before and after filtering
- Justify in a paragraph why you chose to filter in this way

## Sample Quality Control (2 paragraphs)

Evaluate your samples before performing differential expression. These plots
tell you whether your downstream results can be trusted.

- Follow the instructions in the DESeq2 vignette, and normalize the filtered
counts by using the rlog transformation or the variance-stabilizing
transformation
- Perform PCA on the normalized counts matrix and overlay the sample
information in a biplot of PC1 vs. PC2
- Create a heatmap or graphic of the sample-to-sample distances for the
experiment
- Do the samples cluster by experimental group? Are any samples outliers? Do
any covariates appear to explain the variation better than the experimental
groups?
- Based only on these plots, would you proceed to differential expression with
all samples as they are? If not, what would you change, and why?

## Differential Expression Analysis (3-4 paragraphs)

- Create a table of the top 10 differentially expressed genes and the
statistics provided by DESeq2 as ranked by adjusted p-value
- Choose a padj threshold and report the number of significant genes at this
threshold, separated into up- and downregulated
- Rerun your analysis with one alternative choice: either a different padj
threshold or a different filtering strategy. Report how the number of
significant genes and your top enrichment results change in a short table.
Comment on whether your conclusions are robust to this choice.
- Use the thresholded results to perform a DAVID or Enrichr analysis on the
significant genes at your chosen padj threshold
    - State the background gene set you used and justify it
    - State whether you submitted up- and downregulated genes together or
    separately, and why
- Perform a GSEA analysis using [fgsea](https://bioconductor.org/packages/release/bioc/html/fgsea.html)
on your RNAseq results using the C2 canonical pathways MSigDB dataset and log2
fold change as the ranking metric
    - State whether you used shrunken log2 fold changes, and why
    - Briefly comment on what might change if you had ranked genes by the
    DESeq2 test statistic instead
- Choose a padj threshold for the fgsea analysis and create a plot of your
choice that displays the top most significantly enriched pathways
- Comment briefly on the results of the DAVID or Enrichr analysis and the
table you created and what it indicates about the biological processes that
might differ between groups
- Comment briefly on the results of the fgsea analysis
- Compare the results from your DAVID/Enrichr analysis and your fgsea analysis
and comment on any similarities or differences you observe

## Interpretations (2-3 paragraphs)

Using the number and direction of your DE genes, along with your pathway and
enrichment results, please do the following:

- Speculate broadly on the major changes caused by the experimental condition
- Which results most strongly support your speculation?

## Your Conclusions and Follow-up

- Propose two to three additional experiments you might do to validate your
findings. You do not have to do them, just propose them and anticipate what
they would show you if your findings held, and what result would convince you
that your findings were wrong.

- Propose at least two follow-up experiments that would extend or expand on
your findings

# Phase 2: Informed analysis

## Introduction (1 paragraph)

- What is the biological background of the study?
- Why was the study performed?
- Why did the authors use the bioinformatic techniques they did?

## Replicate Figures 3C and 3F (3-4 paragraphs)

- Create a volcano plot similar to the one seen in figure 3C
- Use your DAVID/Enrichr or fgsea results and create a plot resembling figure
3F but with your findings. You do not need to use the same pathways as they did.
- Read their discussion of their results and specifically address the
following in your provided notebook:

1. Compare how many significant genes are up- and downregulated in their
findings and yours (using their significance threshold). Ensure you list how
many you find vs. how many they report.

2. Compare their enrichment results with your DAVID/Enrichr and fgsea
analyses. Comment on any differences you observe.

3. List the candidate sources of discrepancy between your results and theirs
(e.g. genome and annotation versions, aligner, filtering, normalization,
thresholds, multiple testing correction). Using the paper's methods as
evidence, comment on at least two candidate sources you believe contribute the most
to the differences you observe.
   - For each candidate source, please provide a follow-up analysis or experiment
   that would reveal whether it was the likely source of the differences. **You
   do not need to actually do this analysis, just propose how.**    

## Comparing Interpretations (2-3 paragraphs)

Return to your first interpretations about the major biological pathways implicated
in the results:

- Did the authors emphasize any genes or pathways that were weak or absent in
your results? How strongly do you think their data support those claims?

- Which of your findings agree with the authors'? Does reaching the same result
through a different pipeline make you more or less confident in it, and why?

## Conclusions (1-2 paragraphs)

Please address the following:

- Compare your first conclusions with those made by the paper. Did they propose
any follow-up experiments or perform any validation? What was different between
what you proposed and what they did or proposed in the text?