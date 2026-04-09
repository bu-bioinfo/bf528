---
link-citations: true
---

**Semester**: Fall 2026

**Meeting time:** Mon/Fri - 10:10-11:55am, Wed - 9:05-9:55am

**Location:**

Mon/Fri: CDS B62

Wed: SAR103

Zoom: Posted on Blackboard

**Office hours:**
By appointment — contact information on Blackboard

Joey
Wednesdays, 10-11am LSEB 101

Monday, 3-4pm LSEB 101

## Contents

- [Course Objectives](#course-objectives)
- [Course Description](#course-description)
- [Prerequisites](#prerequisites)
- [Required Software](#required-software)
- [Instructor and TAs](#instructor-and-tas)
- [Course Values and Policies](#course-values-and-policies)
- [Projects Overview](#projects-overview)
- [Project Grading](#project-grading)
- [Course Schedule](#course-schedule)

## Course Objectives

- Learn the molecular mechanisms and basic data analysis steps that
  underlie common next-generation sequencing experiments
- Develop proficiency in creating bioinformatics workflows with an
  emphasis on reproducibility and portability
- Gain experience generating and interpreting bioinformatics analyses
  in a biological context

Topics covered include:

- High Throughput Sequencing Technologies (RNAseq, ChIPseq, scRNAseq)
  and various omics technologies (Proteomics, Metabolomics, etc.)
- Computational Workflow Tools (Snakemake, Nextflow)
- Reproducibility and Replicability Tools (Git, Docker, Conda)
- Bioinformatics Databases and File Formats

## Course Description

This course covers modern bioinformatics with a specific focus on the
analysis of next generation sequencing data. Lectures cover a mix of
biological and computational topics necessary for the technical and
conceptual understanding of current high-throughput genomics techniques,
including the molecular mechanisms of the assays, basic data analysis
workflows, and translating results into biological conclusions.

Students build computational workflows that perform end-to-end analyses
of sequencing data from RNA-sequencing, ChIP-sequencing, and Single Cell
RNA-sequencing experiments. The course emphasizes reproducibility and
portability throughout.

Labs focus on practical activities with the tools and technologies needed
to analyze and interpret sequencing data.

## Prerequisites

Basic understanding of biology and genomics. Any of these courses are
adequate prerequisites: BF527, BE505/BE605. Students should have some
experience programming in a modern language (R, Python, C, Java, etc.).

Working familiarity with Git and the command line is strongly recommended.

## Required Software

All you need is a laptop. Course computing runs on BU's Shared Computing
Cluster (SCC), accessed via a browser-based VSCode session — no local
installation of bioinformatics tools is required. You will need a BU SCC
account (obtainable through the Research Computing help desk) and a
GitHub account before the first lab.

## Instructor and TAs

Joey Orofino

Contact information available on Blackboard

As instructor, I will:

1. Learn and correctly pronounce everyone's preferred name/nickname
2. Use preferred pronouns for those who wish to indicate this to me
3. Work to accommodate language-related challenges (I will do my best
   to avoid idioms and slang)

## Course Values and Policies

**Respect.**
Every background, race, color, creed, religion, ethnic origin, age,
sex, sexual orientation, gender identity, and nationality is welcome in
this course. Disrespectful language, discrimination, or harassment of
any kind are not tolerated and may result in removal from class or the
University. Incidents can be reported to the instructor, the
Bioinformatics Program leadership, or the BU Equal Opportunity Office.

**Collaboration.**
Collaboration is encouraged. You may work with others, share ideas and
code, and use any resources available to you — including the internet.
Your written reports must reflect your own analysis, interpretation, and
understanding of the results.

**Attendance.**
Lab attendance is tracked through Git commits. Each lab session has
associated tasks that should be committed to your repository during or
shortly after the session. Regular commit activity is expected and
counts toward the 20% participation grade.

**AI and LLM tools.**
AI tools (ChatGPT, GitHub Copilot, Claude, etc.) may be used to help
write and debug code. Written reports must be your own — submitting
AI-generated text as your own scientific writing is not permitted.

**Flexibility.**
If something comes up that affects your ability to participate, let me
know and we'll work it out. You don't need to share details you're not
comfortable sharing. BU Student Health Services is available if you need
additional support.

## Projects Overview

Each project asks you to build a Nextflow pipeline that performs an
end-to-end analysis of a real sequencing dataset, then write up the
results as sections of a scientific publication. Projects increase in
complexity and decrease in scaffolding as the semester progresses.

- **Project 1 — Genome Assembly:** Assemble a bacterial genome from
  long reads, assess assembly quality, and annotate predicted genes.
- **Project 2 — RNA-seq:** Quantify gene expression from paired-end
  RNA-seq data, identify differentially expressed genes, and interpret
  the results in a biological context.
- **Project 3 — ChIP-seq:** Call transcription factor binding peaks,
  perform motif enrichment analysis, and compare binding profiles across
  conditions.
- **Final Project:** An open-ended analysis of a dataset and question
  of your choosing, integrating methods from across the course.

All pipelines are built with Nextflow and run on the SCC using
Singularity containers, with results version-controlled in Git.

**A note on lab numbering:** Labs are numbered by topic rather than
chronological order. Some labs appear in the schedule out of numerical
sequence — each number is a stable topic reference, not a position
indicator.

## Project Grading

Each project report asks you to write sections of a scientific
publication and produce relevant figures and visualizations.

Grading works on a growth model. You will receive an unofficial grade
per report along with detailed feedback. That grade is temporary — it
will improve as long as you incorporate the feedback from each previous
report. Projects account for 80% of your final grade; participation in
class and lab accounts for the remaining 20%.

## Course Schedule

| Day | Date  | Week | Class    | Topic                                                                | Project                         |
| --- | ----- | ---- | -------- | -------------------------------------------------------------------- | ------------------------------- |
| Wed | 9/2   | [1]({{ site.baseurl }}/lectures/week-01/)    | Lecture  | Introduction                                                         |                                 |
| Fri | 9/4   | [1]({{ site.baseurl }}/lectures/week-01/)    | Lab      | Lab 01 — Setup                                                       |                                 |
| Mon | 9/7   |      | NO CLASS | Labor Day                                                            |                                 |
| Wed | 9/9   | [2]({{ site.baseurl }}/lectures/week-02/)    | Lecture  | Genomics, Genes, and Genomes<br>Next Generation Sequencing           | P1 assigned                     |
| Fri | 9/11  | [2]({{ site.baseurl }}/lectures/week-02/)    | Lab      | Lab 02 — Workflow Basics                                             |                                 |
| Mon | 9/14  | [3]({{ site.baseurl }}/lectures/week-03/)    | Lab      | Lab 03 — Nextflow Tooling                                            |                                 |
| Wed | 9/16  | [3]({{ site.baseurl }}/lectures/week-03/)    | Lecture  | Sequence Analysis Fundamentals                                       |                                 |
| Fri | 9/18  | [3]({{ site.baseurl }}/lectures/week-03/)    | Lab      | Lab 04 — Multi-Sample Pipelines                                      |                                 |
| Mon | 9/21  | [4]({{ site.baseurl }}/lectures/week-04/)    | Lecture  | Genomic Variation and SNP Analysis                                   |                                 |
| Wed | 9/23  | [4]({{ site.baseurl }}/lectures/week-04/)    | Lecture  | Long Read Sequencing                                                 |                                 |
| Fri | 9/25  | [4]({{ site.baseurl }}/lectures/week-04/)    | Lab      | Lab 05 — Typed Channel Operators                                     |                                 |
| Mon | 9/28  | [5]({{ site.baseurl }}/lectures/week-05/)    | Lecture  | Sequence Analysis — RNA-Seq 1                                        |                                 |
| Wed | 9/30  | [5]({{ site.baseurl }}/lectures/week-05/)    | Lecture  | Sequence Analysis — RNA-Seq 2                                        |                                 |
| Fri | 10/2  | [5]({{ site.baseurl }}/lectures/week-05/)    | Lab      | Lab 06 — Containers (Docker)                                         |                                 |
| Mon | 10/5  | [6]({{ site.baseurl }}/lectures/week-06/)    | Lab      | Lab 07 — QC Pipeline with Singularity                                |                                 |
| Wed | 10/7  | [6]({{ site.baseurl }}/lectures/week-06/)    | Lecture  | Biological Databases<br>Gene Sets and Enrichment                     |                                 |
| Fri | 10/9  | [6]({{ site.baseurl }}/lectures/week-06/)    | Lecture  | P1 Check-In and Review                                               | P1 due — P2 assigned            |
| Mon | 10/12 |      | NO CLASS | Indigenous People's Day                                              |                                 |
| Tue | 10/13 | [7]({{ site.baseurl }}/lectures/week-07/)    | Lecture  | Genome Editing — CRISPR-Cas9<br><em>(Monday schedule substitute)</em>|                                 |
| Wed | 10/14 | [7]({{ site.baseurl }}/lectures/week-07/)    | Lecture  | Sequence Analysis — ChIP-Seq                                         |                                 |
| Fri | 10/16 | [7]({{ site.baseurl }}/lectures/week-07/)    | Lab      | Lab 11 — RNAseq and DESeq2                                           |                                 |
| Mon | 10/19 | [8]({{ site.baseurl }}/lectures/week-08/)    | Lecture  | Sequence Analysis — ATAC-Seq                                         |                                 |
| Wed | 10/21 | [8]({{ site.baseurl }}/lectures/week-08/)    | Lecture  | P2 Check-In                                                          |                                 |
| Fri | 10/23 | [8]({{ site.baseurl }}/lectures/week-08/)    | Lab      | Lab 09 — CRISPR Guide Design                                         |                                 |
| Mon | 10/26 | [9]({{ site.baseurl }}/lectures/week-09/)    | Lecture  | Microbiome: 16S and Metagenomics                                     |                                 |
| Wed | 10/28 | [9]({{ site.baseurl }}/lectures/week-09/)    | Lecture  | Metabolomics                                                         |                                 |
| Fri | 10/30 | [9]({{ site.baseurl }}/lectures/week-09/)    | Lab      | Lab 12 — Differential Peak Analysis (ATACseq)                        | P2 due — P3 assigned            |
| Mon | 11/2  | [10]({{ site.baseurl }}/lectures/week-10/)   | Lecture  | Single Cell Analysis Part 1                                          |                                 |
| Wed | 11/4  | [10]({{ site.baseurl }}/lectures/week-10/)   | Lecture  | Single Cell Analysis Part 2                                          |                                 |
| Fri | 11/6  | [10]({{ site.baseurl }}/lectures/week-10/)   | Lab      | Lab 08 — Snakemake                                                   |                                 |
| Mon | 11/9  | [11]({{ site.baseurl }}/lectures/week-11/)   | Lecture  | Single Cell Analysis Part 3                                          |                                 |
| Wed | 11/11 | [11]({{ site.baseurl }}/lectures/week-11/)   | Lecture  | Spatial Transcriptomics                                              |                                 |
| Fri | 11/13 | [11]({{ site.baseurl }}/lectures/week-11/)   | Lab      | Lab 10 — Genome Browsers                                             |                                 |
| Mon | 11/16 | [12]({{ site.baseurl }}/lectures/week-12/)   | Lecture  | P3 Check-In                                                          |                                 |
| Wed | 11/18 | [12]({{ site.baseurl }}/lectures/week-12/)   | Lecture  | Single Cell Analysis Part 4 / Extended Topics                        |                                 |
| Fri | 11/20 | [12]({{ site.baseurl }}/lectures/week-12/)   | Lab      | Lab 13 — Single Cell Setup                                           | P3 due — Final assigned         |
| Mon | 11/23 | [13]({{ site.baseurl }}/lectures/week-13/)   | Lab      | Lab 14 — Single Cell QC                                              |                                 |
|     | 11/25 |      | NO CLASS | Thanksgiving Recess                                                  |                                 |
|     | 11/28 |      | NO CLASS | Thanksgiving Recess                                                  |                                 |
| Mon | 11/30 | [14]({{ site.baseurl }}/lectures/week-14/)   | Lab      | Lab 15 — Single Cell Preprocessing                                   |                                 |
| Wed | 12/2  | [14]({{ site.baseurl }}/lectures/week-14/)   | Lab      | Final Project Work Session                                           |                                 |
| Fri | 12/4  | [14]({{ site.baseurl }}/lectures/week-14/)   | Lab      | Lab 16 — Single Cell Pseudobulk                                      |                                 |
| Mon | 12/7  | [15]({{ site.baseurl }}/lectures/week-15/)   | Lab      | Single Cell Integration                                              |                                 |
| Wed | 12/9  | [15]({{ site.baseurl }}/lectures/week-15/)   | Lab      | Feedback                                                             |                                 |
|     | 12/14 |      |          | Final Exams Begin                                                    | Final Project Due               |
