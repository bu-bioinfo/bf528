---
title: "Project 3: ChIPseq"
layout: single
---

# Purpose

In this project you will analyze a ChIPseq experiment without knowing which
study it comes from. As in Project 2, working blind lets you form your own
interpretation of where this factor binds and what it might be doing before you
see what the authors concluded. The goal is not only to run the pipeline
correctly, but to evaluate what the data can and cannot tell you, commit to an
interpretation, and then compare it critically with the published work.

This structure is not meant as a **gotcha** or to make the project harder. I want
you to explore the data and form your own conclusions without bias, rather than
deferring to what the paper stated was "interesting". Remember that every
scientific paper is a highly curated story of what the authors found significant
or novel based on their own research questions, interests, and the constraints
of publication; there may be other interesting results or findings that were
not as remarked upon. You are not expected to find something novel or something
the authors missed; matching their findings is just as valid an outcome.

# Project structure

This project has two phases:

- **Phase 1 (blind analysis):** You will receive the data and sample metadata
only. You will process the data, evaluate its quality, call and filter peaks,
perform motif and enrichment analyses, and write your own interpretation of
what this factor is doing in these cells.
- **Phase 2 (informed analysis):** Roughly halfway into the project, I will
tell you the publication this data originated from. You will then compare your
results with the authors', replicate figures from the paper, and integrate your
peaks with their RNAseq results. You should not revise your Phase 1
interpretation; it's simply meant as a way for you to compare results.

# Working in a Jupyter notebook

For this project, it will be easier to work in a Jupyter notebook. Please write
all sections of the report in markdown blocks in your notebook and create or
display any plots there as well. Please use the provided Jupyter notebook for
all of your analyses, writing, and plots. 

# Phase 1: Blind analysis

## Experimental Design (1 paragraph)

Using only the sample metadata you were given, describe the experiment:

- How many IP samples and how many input (control) samples are there? How many
replicates?
- What questions can this design support? Can it tell you anything about
*changes* in binding, or only about where binding occurs?
- What potential confounders or limitations would you be concerned about (e.g.
antibody specificity, number of replicates, sequencing depth), and can you
account for them with the information you have?

## Methods (as long as needed)

Please view the presentation here for guidelines: [methods]({{ site.baseurl }}/lectures/accessory-slides/)

The methods section should concisely describe which steps were taken in the
analysis of the data. Remember to adhere to our conventions for writing a
methods section, including specifying the software versions used and the
parameters for each step. If no parameters are changed, state that default
parameters were used. Remember that a methods section should include any details
that are necessary for someone else to replicate your analysis exactly. You can
exclude any details that should not affect the results, such as the exact file
paths used.

- Write a methods section for the pipeline you developed for project 3
- Some of this information will come from your `specifications.md`.

## Read Quality Control (1-2 paragraphs)

Use the MultiQC report or the individual logs from FastQC, Trimmomatic, and 
samtools flagstats to evaluate the quality of the reads and alignments. Please
make sure that at minimum you specifically mention the following (even if there's
no issue, state that there is no issue):

- The range of the number of reads in all the samples
- The proportion of reads that survived trimming
- Any potential issues with the reads as flagged by FastQC
- Any overrepresented sequences, or adapter contamination in the reads
- The alignment rate of the reads to the reference genome
- The duplication rate and GC content distribution, and whether they differ between IP and input samples
- Based on your evaluation above, please state whether you believe the
experiment was of high quality and was suitable for downstream analysis. If
not, please state what you would do to improve the quality of the reads.

## Sample Quality Control (2 paragraphs)

Evaluate your samples before calling peaks. These plots tell you whether your
downstream results can be trusted.

- Display your correlation plot of the genome-wide signal across all samples
- Justify your choice of either pearson or spearman correlation
- Display the fingerprint plots of all IP and INPUT samples
    - Describe the shape of each curve in your fingerprint plot. How far do your
      IP samples deviate from the inputs, and do your inputs approach the 
      uniform distribution you would expect?
    - What would you expect each of these plots to look like for a failed IP?
      For a successful one?

- Do the IP replicates resemble each other more than they resemble the inputs?
Are any samples outliers?
- What would you expect this plot to look like for a failed IP? For a
successful one?
- Based only on these plots, would you proceed to peak calling with all samples
as they are?

## Peak Calling and Filtering (1-2 paragraphs)

Please describe how you called peaks and how you produced your final set of
reproducible, filtered peaks.

- State the number of peaks called in each replicate, the number in your
reproducible set, and the number remaining after filtering from the blacklist
- Describe the method you used to determine reproducibility and any filtering
you applied (e.g. blacklisted regions), and justify in a paragraph why you
chose to do it this way


## Signal Coverage Plot (1-2 paragraphs)

Display your signal coverage plot and address the following:

- Explain briefly what the plot represents
- Provide a biological interpretation or hypothesis that the plot supports
about where this factor binds
- What can this plot not tell you about the factor's binding?

## Motif Finding (1-2 paragraphs)

Use the results from HOMER findMotifsGenome and address the following:

- Create a single figure or plot (you may take a screenshot) of the top results
from the knownResults output from HOMER
- What are some of the top motifs? What might that imply about the identity of
the factor that was being tested (the IP)?
- Do any of the other enriched motifs suggest co-factors or binding partners?
What would you need to show to support that?

## Annotation and Enrichment Analysis (2-3 paragraphs)

Use your annotated peaks list and perform an enrichment method of your choice.
This is purposefully open-ended, so you may consider filtering your peaks by
different categories (e.g. promoter vs. distal) before performing some kind of
enrichment analysis. There are region-based enrichment methods (GREAT) in
addition to standard gene-based methods such as DAVID / Enrichr.

- Detail the methodology used to perform the enrichment
    - State how you assigned peaks to genes (if you did), and what assumptions
    that assignment makes
    - State the background set you used and justify it
- Create a single figure / plot / table that displays some of the top results
from the analysis
- Comment briefly on the results you observe and what they indicate about the
biological processes this factor might be involved in

## Interpretations (2-3 paragraphs)

Using your peak locations, coverage plot, motif results, and enrichment results,
please do the following:

- Speculate broadly on the role this factor plays in these cells
- Which results most strongly support your speculation?

## Your Conclusions and Follow-up

- Propose two to three additional experiments you might do to validate your
findings. You do not have to do them, just propose them and anticipate what
they would show you if your findings held, and what result would convince you
that your findings were wrong.

- Propose at least two follow-up experiments that would extend or expand on
your findings. 

# Phase 2: Informed analysis

## Introduction (1 paragraph)

- What is the biological background of the study?
- Why was the study performed?

## Comparing Sequencing and Peak Results (3-4 paragraphs)

Find the supplementary information for the publication and focus on
supplementary figures S2A, S2B, and S2C.

1. Re-create the table found in supplementary figure S2A and compare it with
your own results.
    - Do you observe differences in the reported number of raw and mapped reads?
    Ensure you list the numbers you find vs. the numbers they report.

2. Compare your correlation plot with the one found in supplementary figure S2B.
    - Do you observe any differences in your calculated metrics?
    - What was the authors' takeaway from this figure? Does it agree with the
    conclusion you reached in your Phase 1 Sample Quality Control section?

3. Create a Venn diagram with the same information as found in figure S2C.
    - Compare the number of peaks called in each replicate and in the overlap
    with what they report. Ensure you list how many you find vs. how many they
    report.

4. List the candidate sources of discrepancy between your results and theirs
(e.g. genome version, trimming, aligner, duplicate handling, peak caller and
its parameters, reproducibility method, filtering). Using the paper's methods
as evidence, comment on at least two candidate sources you believe contribute
the most to the differences you observe.
    - For each candidate source, please provide a follow-up analysis that would
    reveal whether it was the likely source of the differences. **You do not
    need to actually do this analysis, just propose how.**

## Integrating Your Peaks with Their RNAseq Results (3-4 paragraphs)

In their publication, find the link to their GEO submission. Read the methods
section of the paper and integrate **your** called ChIPseq peaks with the
results from **their** differential expression RNAseq experiment. Use your set
of reproducible and filtered peaks, and use the publication's listed
significance thresholds for the RNAseq results. You may do all of these steps
in python using pandas or R using tidyverse / ggplot.

1. Create a figure that displays the same information as figure 2F from the
original publication using your annotated peaks and the RNAseq results. The
figure does not have to be the same style but must convey the same information
using your results.

2. In figures 2D and 2E, the authors highlight two specific genes that were
identified in both experiments. Using your list of filtered and reproducible
peaks, a genome browser of your choice, and your bigWig files, re-create these
figures with your own results. (You do not need to include the RNAseq data, but
you should re-create the genomic tracks from your ChIPseq results.)

3. Address the following:
    - Compare the number of overlapping genes in your figure 2F with theirs.
    Ensure you list how many you find vs. how many they report.
    - Do you observe statistically significant peaks in the two genes from
    figures 2D and 2E? How similar do your tracks appear to theirs?
    - List the candidate sources of any discrepancies (consider the peak-to-gene
    assignment in addition to the sources above) and comment on at least two you
    believe contribute the most.
    - What is the rationale behind combining these two analyses in this way? What
    conclusions does it enable that neither experiment supports alone, and what
    can it still not establish?

## Comparing Interpretations (2-3 paragraphs)

Return to your Phase 1 interpretations of the role this factor plays:

- Did the authors emphasize any genes, motifs, or pathways that were weak or
absent in your results? How strongly do you think their data support those
claims?

- Which of your findings agree with the authors'? Does reaching the same result
through a different pipeline make you more or less confident in it, and why?

- Did integrating the RNAseq data support, refine, or contradict the
speculation you made from binding data alone?

## Conclusions (1-2 paragraphs)

Please address the following:

- Compare your Phase 1 conclusions with those made by the paper. Did they
propose any follow-up experiments or perform any validation? What was different
between what you proposed and what they did or proposed in the text?

# REMINDER TO CLEAN UP YOUR WORKING DIRECTORY

When you have successfully run your project 3 pipeline, please ensure that you
fully delete your work/ directory and any large files that you may have
published to your results/ directory.

You may use the following command:

```bash
rm -rf work/
```

These samples are very large and we have limited disk space. I will be checking
your working directories to ensure you do this.