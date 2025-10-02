---
title: "Project 2: RNAseq"
layout: single
---

# REMINDER TO CLEAN UP YOUR WORKING DIRECTORY

When you have successfully run your project 2 pipeline, please ensure that you 
fully delete your work/ directory and any large files that you may have published
to your results/ directory. 

You may use the following command:

```bash
rm -rf work/
```

These samples are very large and we have limited disk space. I will be checking
your working directories to ensure you do this. 

# Working in a Rmarkdown notebook

For this project, since we are working with DESeq2, it will be easier to work
in a Rmarkdown notebook. Rmarkdown notebooks are highly similar to Jupyter
Notebooks and allow you to write R code and markdown in the same file.


# Introduction (1 paragraph)

- What is the biological background of the study?
- Why was the study performed?
- Why did the authors use the bioinformatic techniques they did?

# Methods (as long as needed)

The methods section should concisely describe which steps were taken in the
analysis of the data. Remember to adhere to our conventions for writing a
methods section, including specifying the software versions used and the
parameters for each step, if no parameters are changed, state that default
parameters were used. Remember that a methods section should include any details
that are necessary for someone else to replicate your analysis exactly. You can
exclude any details that should not affect the results, such as the exact file
paths used. 

- Write a methods section for the pipeline you developed for project 2

# Quality Control Evaluation (1-2 paragraphs)

Use the MultiQC report or the individual logs from FASTQC and STAR to evaluate
the quality of the reads. Please make sure that at minimum you specifically mention the
following (even if there's no issue, state that there is no issue):

- The range of the number of reads in all the samples
- Any potential issues with the reads as flagged by FASTQC
- Any overrepresented sequences, or adaptor contamination in the reads
- The alignment rate of the reads to the reference genome
- Based on your evaluation above, please state whether you believe the experiment
was of high quality and was suitable for downstream analysis. If not, please
state what you would do to improve the quality of the reads.

# Filtering the counts matrix (1 paragraph)

Please describe the filtering process you used to filter the counts matrix. 

- Ensure that you include the two plots that show the distribution of counts before and after filtering
- State the number of genes present before and after filtering

# Differential Expression Analysis (3-4 paragraphs)

- Create a table of the top 10 differentially expressed genes and the statistics
provided by DESeq2 as ranked by adjusted p-value
- Choose a padj threshold and report the number of significant genes at this threshold
- Use the thresholded results to perform a DAVID or ENRICHR analysis on the significant genes at your chosen padj threshold. 
- Perform a GSEA analysis using [fgsea](https://bioconductor.org/packages/release/bioc/html/fgsea.html on your RNAseq results using the C2 canonical pathways MSIGDB dataset and log2 fold change as the ranking metric
- Choose a padj threshold for the fgsea analysis and create a plot of your choice
that displays the top most significantly enriched pathways
- Comment briefly on the results of the DAVID or ENRICHR analysis and the table
you created and what it indicates about the biological processes that might be
affected by the treatment.
- Comment briefly on the results of the fgsea analysis
- Compare the results from your DAVID/ENRICHR analysis and your fgsea analysis
and comment on any similarities or differences you observe

# RNAseq Quality Control (2 paragraphs)

- Follow the instructions in the DESeq2 vignette, and normalize the counts by
using the rlog transformation or the variance-stabilizing transformation

- Perform PCA on the normalized counts matrix and overlay the sample
information in a biplot of PC1 vs. PC2

- Create a heatmap or graphic of the sample-to-sample distances for the experiment

- Comment briefly on both the PCA plot and the sample-to-sample distance matrix
and what these plots may suggest about the success of the experiment and the
analysis as a whole.


# Replicate figure 3C and 3F (3-4 paragraphs)

- Create a volcano plot similar to the one seen in figure 3c. 
- Use your DAVID or GSEA results and create a plot resembling figure 3F but with
your findings - you do not need to use the same pathways as they did
- Read their discussion of their results and specifically address the following
in your provided notebook:

1. Compare how many significant genes are up- and down-regulated in their
findings and yours (using their significance threshold). Ensure you list how 
many you find vs. how many they report. 

2. Compare their enrichment results with your DAVID and GSEA analysis. Comment
on any differences you observe and why there are discrepancies.

