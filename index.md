---
link-citations: true
---

**Semester**: Fall 2026

**Meeting time:** Mon/Fri - 10:10-11:55am, Wed - 9:05-9:55am

**Location:** 

Mon/Fri: CDS B62

Wed: SAR103

Zoom: Posted on blackboard

**Office hours:**
By appointment - contact information on blackboard

Joey
Wednesdays, 10-11am LSEB 101

Monday, 3-4pm LSEB 101

## Contents

- [Course Objectives](#course-objectives)
- [Course Description](#course-description)
- [Course Values and Policies](#course-values-and-policies)
- [Course Schedule](#course-schedule)
- [Prerequisites](#prerequisites)
- [Instructor and TAs](#instructor-and-tas)
- [Projects Overview](#projects-overview)
- [Project Grading](#project-grading)
- [Course Schedule](#course-schedule)

## Course Objectives

- Learn the molecular mechanisms and basic data analysis steps that underly common next-generation sequencing experiments

- Develop proficiency in creating bioinformatics workflows with an emphasis on reproducibility and portability

- Gain experience generating and interpreting bioinformatics analyses in a biological context

Below you will find a selection of some of the prominent biological and computational topics that will be covered in the course:

- High Throughput Sequencing Technologies (RNAseq, ChIPseq, scRNAseq) and various omics technologies (Proteomics Metabolomics, etc)
- Computational Workflow Tools (snakemake, nextflow)
- Reproducibility and Replicability Tools (Git, Docker, Conda)
- Bioinformatics Databases and File Formats

## Course Description

This course will expose students to modern bioinformatics studies with 
a specific focus on the analysis of next generation sequencing data. Lectures will
cover a mix of both biological and computational topics necessary for the
technical and conceptual understanding of current high-throughput genomics
techniques. This will include brief discussions of the molecular mechanisms of
the assays, basic data analysis workflows, and translating these results into
biological conclusions.

Students will get hands-on experience developing computational workflows that
perform an end-to-end analysis of sequencing data from ubiquitous NGS
technologies including RNA-sequencing, ChIP-sequencing, and Single Cell
RNA-sequencing. The course emphasizes the importance of reproducibility, and
portability in modern bioinformatics.

Classes will be traditional lectures exploring the variety of topics regarding
next generation sequencing and labs will focus on practical activities meant
to develop experience working with the tools and technologies needed for the
analysis and interpretation of sequencing data.

## Course Values and Policies

**Everyone is welcome.** 
Every background, race, color, creed, religion, ethnic
origin, age, sex, sexual orientation, gender identity, nationality is welcome
and celebrated in this course. Everyone deserves respect, patience, and
kindness. Disrespectful language, discrimination, or harassment of any kind are
not tolerated, and may result in removal from class or the University.  The
instructors deem these principles to be inviolable human rights. Students should
feel safe reporting any and all instances of discrimination or harassment to the
instructor, to any of the Bioinformatics Program leadership, or the BU Equal
Opportunity Office 

**Everyone brings value.** 
Each of us brings unique experiences,
skills, and creativity to this course. Our diversity is our greatest asset.
Collaboration is highly encouraged. All students are encouraged to work together
and seek out any and all available resources when completing projects in all
aspects of the course, including sharing both ideas and code as well as those
found on the internet. Any and all available resources may be brought to bear.
However, consistent with BU policy, your reports should be written in your own
words and represent your own work and understanding of the material. 

**Life happens.** 
Your mental, physical and emotional health is far more
important than any class. Make sure to take care of yourself and reach out to
someone you trust (mentor, family member, or friend) if you ever feel you need
to talk to someone. BU offers a number of resources through Student Health
Services for managing situations involving grief, anxiety and depression,
stress, homesickness and other common issues. I am also always here to listen
without judgment and help you find any other resources. On a related note, if 
you need to miss class because of private matters, you do not need to disclose 
anything you aren’t comfortable sharing, please just let me know and I will work
with you to help you catch up when you return. Your family, friends, and health 
should always come first.

## Prerequisites
Basic understanding of biology and genomics. Any of these courses are adequate prerequisites for this course: BF527, BE505/BE605. Students should have some
experience programming in a modern programming language (R, python, C, Java, etc).

Working familiarity with Git and command line interfaces is also heavily
recommended. 

## Instructor and TAs
Joey Orofino

Contact information available on Blackboard

It should go without saying that our class is composed of people from a diverse
set of backgrounds. Everyone will treat one another with respect and consideration
at all times or be asked to leave the classroom. 

As instructor, I will:

1. Learn and correctly pronounce everyone’s preferred name/nickname
2. Use preferred pronouns for those who wish to indicate this to me/the class
3. Work to accommodate/prevent language related challenges (for instance I will
   do my best to avoid the use of idioms and slang)

## Projects Overview

- Project 1: Genome Assembly
- Project 2: RNAseq
- Project 3: ChIPseq
- Project 4: Final Project

In order to generate reproducible, and portable
NGS analysis workflows, we will be employing a combination of technologies
including Nextflow, git, Conda, Docker, and HPC.

Subsequent projects will gradually add more complexity and tasks once you've
gained experience with the fundamentals. Simultaneously, the amount of scaffolding
and direct instructions will also be reduced. 


## Project Grading

Your final report for each project will ask you to write various sections of a 
scientific publication as well as produce certain figures and visualizations.

The grading system for this class works on a growth model. You will receive an 
unofficial grade per report, and be given detailed feedback on where to incorporate
changes and edits. This grade is temporary and will improve or remain the same as
long as you incorporate the feedback from each previous report or maintain the 
the same consistency. 

If you want to think about it in terms of percentage, projects will account for
80% of your grade and participation in class / lab will account for the remaining
20%.

## Course Schedule

| Day | Date  | Week | Class    | Topic                                                                | Project                         |
| --- | ----- | ---- | -------- | -------------------------------------------------------------------- | ------------------------------- |
| Wed | 9/2   | [1]({{ site.baseurl }}/lectures/week-01/)    | Lecture  | Introduction                                                         |                                 |
| Fri | 9/4   | [1]({{ site.baseurl }}/lectures/week-01/)    | Lab      | Lab 01 — Setup                                                       |                                 |
| Mon | 9/7   |      | NO CLASS | Labor Day                                                            |                                 |
| Wed | 9/9   | [2]({{ site.baseurl }}/lectures/week-02/)    | Lecture  | Genomics, Genes, and Genomes<br>Next Generation Sequencing           | P1 assigned                     |
| Fri | 9/11  | [2]({{ site.baseurl }}/lectures/week-02/)    | Lab      | Lab 02 — Workflow Basics                                             |                                 |
| Mon | 9/14  | [3]({{ site.baseurl }}/lectures/week-03/)    | Lecture  | Sequence Analysis Fundamentals                                       |                                 |
| Wed | 9/16  | [3]({{ site.baseurl }}/lectures/week-03/)    | Lab      | Writing a Methods Section<br>Lab 03 — Nextflow Practice              |                                 |
| Fri | 9/18  | [3]({{ site.baseurl }}/lectures/week-03/)    | Lab      | Lab 04 — Argparse and CLI Tools                                      |                                 |
| Mon | 9/21  | [4]({{ site.baseurl }}/lectures/week-04/)    | Lecture  | Genomic Variation and SNP Analysis                                   |                                 |
| Wed | 9/23  | [4]({{ site.baseurl }}/lectures/week-04/)    | Lecture  | Long Read Sequencing                                                 |                                 |
| Fri | 9/25  | [4]({{ site.baseurl }}/lectures/week-04/)    | Lab      | Lab 05 — Nextflow Tooling                                            |                                 |
| Mon | 9/28  | [5]({{ site.baseurl }}/lectures/week-05/)    | Lecture  | Sequence Analysis — RNA-Seq 1                                        |                                 |
| Wed | 9/30  | [5]({{ site.baseurl }}/lectures/week-05/)    | Lecture  | Sequence Analysis — RNA-Seq 2                                        |                                 |
| Fri | 10/2  | [5]({{ site.baseurl }}/lectures/week-05/)    | Lab      | Lab 06 — Containers (Docker)                                         |                                 |
| Mon | 10/5  | [6]({{ site.baseurl }}/lectures/week-06/)    | Lecture  | P1 Check-In and Review                                               |                                 |
| Wed | 10/7  | [6]({{ site.baseurl }}/lectures/week-06/)    | Lecture  | Biological Databases<br>Gene Sets and Enrichment                     |                                 |
| Fri | 10/9  | [6]({{ site.baseurl }}/lectures/week-06/)    | Lab      | Lab 07 — Scaling Up and the SCC                                      | P1 due — P2 assigned            |
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
| Wed | 12/2  | [14]({{ site.baseurl }}/lectures/week-14/)   | Lab      | Lab 16 — Single Cell Pseudobulk                                      |                                 |
| Fri | 12/4  | [14]({{ site.baseurl }}/lectures/week-14/)   | Lab      | Single Cell Integration                                              |                                 |
| Mon | 12/7  | [15]({{ site.baseurl }}/lectures/week-15/)   | Lab      | Final Project Work                                                   |                                 |
| Wed | 12/9  | [15]({{ site.baseurl }}/lectures/week-15/)   | Lab      | Feedback                                                             |                                 |
|     | 12/14 |      |          | Final Exams Begin                                                    | Final Project Due               |