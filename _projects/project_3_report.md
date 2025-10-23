---
title: "Project 3: ChIPseq"
layout: single
---

# Working in a Jupyter notebook

For this project, it will be easier to work in a jupyter notebook. Please
write all sections of the report in markdown blocks in your notebook and create
or display any plots there as well. Please create a **single** jupyter notebook.

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

- Write a methods section for the pipeline you developed for project 3

# Quality Control Evaluation (1-2 paragraphs)

Use the MultiQC report or the individual logs from FASTQC and TRIMMOMATIC to evaluate
the quality of the reads. Please make sure that at minimum you specifically mention the following (even if there's no issue, state that there is no issue):

- The range of the number of reads in all the samples
- Any potential issues with the reads as flagged by FASTQC
- Any overrepresented sequences, or adaptor contamination in the reads
- The alignment rate of the reads to the reference genome
- Based on your evaluation above, please state whether you believe the experiment
was of high quality and was suitable for downstream analysis. If not, please
state what you would do to improve the quality of the reads.


## Overlap your ChIPseq results with the original RNAseq data

In their publication find the link to their GEO submission. Read the methods
section of the paper and integrate **your** called ChIPSeq peaks with the results
from **their** differential expression RNAseq experiment. Use your set of
reproducible and filtered peaks, and use the publication's listed significance
thresholds for the RNAseq results. You may do all of these steps in python using pandas or R using tidyverse / ggplot. You may start by reading the RNAseq results and the annotated peak results as dataframes.

1. Create a figure that displays the same information of figure 2F from the
original publication using your annotated peaks and the RNAseq results. The 
figure does not have to be the same style but must convey the same information
using your results.

2. In figures 2D and 2E, the authors identify and highlight two specific genes
that were identified in both experiments. Using your list of filtered and
reproducible peaks, a genome browser of your choice, and your bigWig files, please
re-create these figures with your own results (You do not need to include the
RNAseq data, but you should re-create the genomic tracks from your ChIPseq results)

3. In the notebook you created, please ensure you address the following questions:

  1. Focusing on your results for figure 2F:
    - Do you observe any differences in the number of overlapping genes from both
    analyses?
    - If you do observe a difference, explain at least two factors that
    may have contributed to these differences. 
    - What is the rationale behind combining these two analyses in this way? What
    additional conclusions is it supposed to enable you to draw?
    
  2. Focusing on your results for figures 2D and 2E:
    - From your annotated peaks, do you observe statistically significant peaks
    in these same two genes?
    - How similar do your genomic tracks appear to those in the paper? If you 
    observe any differences, comment briefly on why there may be discrepancies. 

## Comparing key findings to the original paper

Find the supplementary information for the publication and focus on supplementary
figure S2A, S2B, and S2C. 

1. Re-create the table found in supplementary figure S2A. Compare the results 
with your own findings. Address the following questions:

  - Do you observe differences in the reported number of raw and mapped reads?
  
  - If so, provide at least two explanations for the discrepancies. 
  
2. Compare your correlation plot with the one found in supplementary figure S2B. 

  - Do you observe any differences in your calculated metrics?
  
  - What was the author's takeaway from this figure? What is your conclusion
  from this figure regarding the success of the experiment?
  
3.  Create a venn diagram with the same information as found in figure S2C. 

  - Do you observe any differences in your results compared to what you see?
  
  - If so, provide at least two explanations for the discrepancies in the number
  of called peaks. 

## Analyze the annotated peaks

Use your annotated peaks list and perform an enrichment method of your choice. 
This is purposefully open-ended so you may consider filtering your peaks by
different categories before performing some kind of enrichment analysis. There are
a few peak / region based enrichment methods (GREAT) in addition to standard
methods used such as DAVID / Enrichr. 

1. In your created notebook, detail the methodology used to perform the enrichment.

2. Create a single figure / plot / table that displays some of the top results
from the analysis.

3. Comment briefly in a paragraph about the results you observe and why they 
may be interesting.


# REMINDER TO CLEAN UP YOUR WORKING DIRECTORY

When you have successfully run your project 3 pipeline, please ensure that you 
fully delete your work/ directory and any large files that you may have published
to your results/ directory. 

You may use the following command:

```bash
rm -rf work/
```

These samples are very large and we have limited disk space. I will be checking
your working directories to ensure you do this. 