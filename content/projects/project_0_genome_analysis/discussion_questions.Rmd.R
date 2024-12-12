Week 1

3. Answer the following questions in the provided notebook:
  
  a. What is the advantage of using the most up-to-date versions of software? 
  
  b. What are some disadvantages?
  
  3. Take a look at the `nextflow.config` and look for the `profile` section. Answer
the following question in the provided notebook: 
  
  a. What do you think the option `-profile local,conda` is doing?
  
  
week 2




5. Answer the following questions in your provided docs/week2_tasks.Rmd:
  
  a. What does the option `label 'process_single'` specify? Can you find where
this value is described?
  
  b. What would happen if the values in our channel were switched?
  i.e. [path/to/genome, name_of_genome] Would this process still run? Would the
tool still run?
  
  4. Answer the following questions in your provided week2_tasks.Rmd when nextflow
has finished running:
  
  a. Where are the outputs from Prokka stored?
  
  b. You may have noticed a new directory has been created in your repo called
`work/`. What is in this directory? What do you think the advantages of 
generating directories this way are? What are the disadvantages?
  
  
  week 3

1. Navigate to the directory in `work/` where your Prokka process ran successfully. 
Answer the following question in the provided week3_tasks.Rmd:
  
  1. Explain the purpose of each file that you find in this directory. You may
need to look up concepts such as stdout and stderr. 

1. Navigate to your `results/` directory and find the outputs created by Prokka.
Open up the `<replace_with_your_name>.gff` file and answer the following questions:
  
  a. Does this file have a regularized format? How would you parse or read this
file?
  
  b. What information appears to be stored in this file?
  
  :::{.box .task}
In the provided week3_tasks.Rmd, please answer the following questions:
  
  1. How would you change this argparse code to accept a list of file inputs?
  
  2. Why are we going to the trouble of making a separate script and nextflow
module to run this specific code?
  
  :::
  
  
Rank the following quality control metrics for a 2x100nt PE illumina mRNAseq datraset

- Unequal Read Lengths
- Average PHRED score < 20 in the last 10 bases
- 15% of reads have identical sequences
- 50% of reads are multimapped after alignment to the appropriate genome
- 10% of reads are unmapped after alignment to the appropriate genome
- non-random nucleotide distribution in the first 6 bases
- Nucleotide frequences of ACTG are not equal over the entire read
- Unequal number of forward and reverse read.socket(
  
Order the following steps in a typical RNAseq pipeline
- count normalization
- Sequence QC
- Gene Set Enrichment Analysis
- Differential Expression
- Read Alignment
- Read Counting
)
  

:::{.box .task}

Please answer the following question in the provided Rmd:
  
  1. What are two reasons we are creating these two channels which contain the same 
information?
  
  :::
  
  

1. Draw the DAG for this sample snakemake workflow. Boxes indicate
the rules, and arrows indicate dependencies. Make this diagram in whatever
software you'd like and save it to this repo. Fill in the following code with the
name of the file you created and it will display it here in this markdown.

```













## RNAseq

1. List the major high-level steps of a basic RNAseq experiment to look for
differentially expressed genes. At each step, list what data you need to perform
each step and what format they are in (if applicable). At minimum, there are 4
essential steps.









2. Consider the following FastQC plot.

```{r}
knitr::include_graphics("fastqc_plot.png")
```


2a. What aspect of the data does this plot show?







2b. Make an interpretation of this plot assuming the data type was RNASeq.







2c. Do you think this plot indicates there was a problem with the dataset?
Explain your answer.






3. What is a splice-aware aligner? When is it important to use a splice-aware
aligner?







4. What does a “gene-level” count as produced by VERSE or any other counting
tool in a RNAseq experiment represent?






5. In your own words, briefly describe what information the matching GTF for a
reference genome stores.






6. When counting alignments using VERSE or any other utility, why do we need to
provide the matching reference genome GTF file?







7. Let’s pretend that this was a GSEA result from an experiment where we treated
293T cells with a drug and compared changes in gene expression to wild-type
cells treated with a vehicle control. The differential expression results are
relative to the control cells (i.e. a positive fold change means a gene is
upregulated upon treatment with the drug)

Assume the following result is statistically significant with a positive NES
(normalized enrichment score) and that it represents a GSEA experiment performed
on the entire list of genes discovered in the experiment ranked by
log2FoldChange (i.e. genes that are “upregulated” in the cells treated with drug
are on the “left” and genes that are “downregulated” due to treatment are on the
“right”).

```{r}
knitr::include_graphics("gsea_plot.png")
```


7a. Form a valid interpretation / conclusion of the results shown in the plot
given the above setup.





7b. Now consider that all of the genes driving the enrichment are all activators
of the inflammatory pathway. Does your interpretation change and if so, how?





7c. Finally, consider that all of the genes driving the enrichment all function
to inhibit inflammation. Does your interpretation change and if so, how?







---
title: "Project 2 Discussion Questions"
output: html_document
date: "2024-04-04"
---




**Methods and Quality Control**
  
  1. Include a full methods section for this project. You may simply combine
the individual methods sections you've written for each week.







2. Examine the figure provided below:
```{r, dup rate}
knitr::include_graphics("fastqc_sequence_counts_plot.png")
```
Notice the duplication rates between the IP and Input control samples.
Provide an explanation for why they are so different. Also make sure to note
whether you think this represents an issue with the dataset, and if so, why?.






2. Examine the figure provided below:
```{r, GC content}
knitr::include_graphics("fastqc_per_sequence_gc_content_plot.png")
```
Consider the GC plot for the IP and Input control samples. The two input samples
are represented by the red distributions, and the IP samples are the green
distributions.

Why do you think we see a difference in the GC distribution between our IP and
Input control samples? Also make sure to note whether you think this represents
an issue with the dataset and if so, why?






**Thought Questions on Publication**

The following questions will reference the original publication, which can be
found here: https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5071180/

3. First, please report the following results:
  
A. How many peaks were called in each of the biological replicates in your
results?
  
  
  
B. How many "reproducible" peaks did you end up with after applying your
bedtools intersect strategy on the two replicate peak sets?
     
     
     
C. How many "reproducible" peaks remained after filtering out any peaks found in
the hg38 blacklisted regions?
     


Consider Supplementary Figure S2C, do you obtain the same number of Runx1
peaks for each replicate experiment? Do you obtain the same number of
reproducible peaks? If not, provide at least three reasons why your results
differ.





4. Consider figure 2a, notice that around 1/3 of all of their reported
reproducible peaks are annotated to intergenic regions (regions of the genome
not associated with any known genes). Propose at least two experiments (or sets
of experiments) that would help you begin to understand whether these peaks are
biologically relevant.






5. Consider figure 2f, note that many of the genes that are differentially
expressed upon Runx1 knockdown do **not** have a proximal Runx1 binding peak.
Provide at least three reasons for why this might be the case.



How would you alter the qsub command to allow your job to run for 24hrs instead
of the default?

  



