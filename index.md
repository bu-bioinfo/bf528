---
link-citations: true
---

CURRENTLY UNDER CONSTRUCTION

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
- [AI Use in This Course](#ai-use-in-this-course)
- [Project Grading](#project-grading)
- [Course Schedule](#course-schedule)

## Course Objectives
By the end of this course, you will be able to:

Skills

- Design and build computational workflows that process raw sequencing data 
  end-to-end with a focus on best practices in reproducibility and portability
- Evaluate the quality and appropriateness of bioinformatics analyses at each
  stage
- Use AI tools deliberately and responsibly by generating precise prompts, 
  critically evaluating the output, and documenting its use in a methodical fashion

Knowledge

- Explain how RNAseq, ChIPseq, ATACseq, and single cell RNAseq work at the molecular
  level and how various aspects of the method shape the interpretation of the analysis
- Identify the major steps in each analysis step and recognize common failures in
  genomic data analysis including violated assumptions, or misused tools

Why it matters

These are skills that are used by practicing computational biologists regularly.
The goal is not just to be able to build a pipeline, but also to share your work
in a way that enables others to be able to verify and reproduce your results. The 
ability to critically evaluate and interpret computational results in a biological
context, whether developed manually or by AI, is what enables you to trust your own
work or for others to trust yours. Developing responsible and principled
habits around validation, testing, and agentic coding will be transferrable to 
any domain. 


Topics covered include:

- High Throughput Sequencing Technologies (RNAseq, ChIPseq, scRNAseq)
  and various omics technologies (Proteomics, Metabolomics, etc.)
- Computational Workflow Tools (Snakemake, Nextflow)
- Reproducibility and Replicability Tools (Git, Docker, Conda)
- Bioinformatics Databases and File Formats
- Responsible use of LLMs

## Course Description

This course covers modern bioinformatics with a specific focus on the
analysis of next generation sequencing data. Lectures cover a mix of
biological and computational topics necessary for the technical and
conceptual understanding of current high-throughput genomics
techniques, including the molecular mechanisms of the assays, basic
data analysis workflows, and translating results into biological
conclusions.

Students build computational workflows that perform end-to-end
analyses of sequencing data from RNA-sequencing, ChIP-sequencing, and
single-cell RNA-sequencing experiments. The course emphasizes
reproducibility and portability throughout. AI tools are treated as
part of that workflow: used deliberately, evaluated critically, and
documented with the same rigor as any other methodological choice.

Labs focus on practical activities with the tools and technologies
needed to analyze and interpret sequencing data.

## Prerequisites

Basic understanding of biology and genomics. Any of these courses are
adequate prerequisites: BF527, BE505/BE605. Students should have some
experience programming in a modern language (R, Python, C, Java,
etc.).

Working familiarity with Git and the command line is strongly
recommended.

## Required Software

All you need is a laptop. Course computing runs on BU's Shared
Computing Cluster (SCC), accessed via a browser-based VSCode session
— no local installation of bioinformatics tools is required. You will
be automatically provided with access to the shared computing cluster.

If you do not currently have a GitHub account, please make one prior
to the start of the first class. It is free and one of the most
widely used platforms for hosting git repositories.

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
sex, sexual orientation, gender identity, and nationality is welcome
in this course. Disrespectful language, discrimination, or harassment
of any kind are not tolerated and may result in removal from class or
the University. Incidents can be reported to the instructor, the
Bioinformatics Program leadership, or the BU Equal Opportunity Office.

**Collaboration.**
Collaboration is encouraged. You may work with others, share ideas
and code, and use any resources available to you — including the
internet. Your written reports must reflect your own analysis,
interpretation, and understanding of the results.

**Attendance.**
Lab attendance is tracked through Git commits. Each lab session has
associated tasks that should be committed to your repository during
or shortly after the session. Regular commit activity is expected and
counts toward the 20% participation grade.

**AI and LLM tools.**
AI tools (ChatGPT, GitHub Copilot, Claude, etc.) are a legitimate and
expected part of this course. Used critically, transparently, and
with appropriate skepticism, they will be a significant asset to your
skillset in this course and beyond. Each assignment has an explicit
AI use level that tells you what is permitted and why. See the AI Use
in This Course section for the full framework.

**Flexibility.**
If something comes up that affects your ability to participate, let
me know and we'll work it out. You don't need to share details you're
not comfortable sharing. BU Student Health Services is available if
you need additional support.

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
  perform motif enrichment analysis, and compare binding profiles
  across conditions.
- **Final Project:** An open-ended analysis of a dataset and question
  of your choosing, integrating methods from across the course.

All pipelines are built with Nextflow and run on the SCC using
Singularity containers, with results version-controlled in Git.

**A note on lab numbering:** Labs are numbered by topic rather than
chronological order. Some labs appear in the schedule out of numerical
sequence — each number is a stable topic reference, not a position
indicator.

## AI Use in This Course

This course uses the **AI Assessment Scale (AIAS)** (Perkins, Furze, Roe and MacVaugh, 2024)
to make AI policy transparent and consistent across all assignments. The AIAS 
describes five levels of AI involvement in assessment, from no AI to full
AI-human collaboration. Rather than a single blanket policy, each
component of this course has an assigned level that reflects its
learning goals. The level tells you both what level of use is expected
and why that choice was made.

The goal is to use AI in ways that serve your learning rather than
substitute for it.

### AIAS Levels at a Glance

| Level | Name | What it means |
|---|---|---|
| 1 | **No AI** | Completed entirely without AI assistance |
| 2 | **AI Planning** | AI may support brainstorming and structuring; not present in final submission |
| 3 | **AI Collaboration** | AI assists in developing and refining work; human judgment directs and evaluates output |
| 4 | **Full AI** | AI used throughout; all AI-generated content must be cited and critically evaluated |
| 5 | **AI Exploration** | Open-ended co-design with AI; boundaries defined collaboratively |

For Level 4 work, AI use is structured around test-driven development
— specifications and verification plans come before prompting.
Details are in the Final Project section below.

### Assignments and Their Levels

**Labs — Level 1–3**
Labs are participation exercises, not graded assignments. Each lab
has an assigned AI level that reflects its goals. When appropriate,
you are encouraged to use AI tools freely to work through the
material. Pushing changes to your repo is how participation is
tracked.

**Projects 1 & 2 — Level 2 (AI Planning)**
These early projects ask you to build foundational skills by working
through pipelines largely by hand. You may use AI for brainstorming,
planning, and debugging small well-defined subtasks but the pipeline
logic, parameter choices, and written analysis should be yours. The
idea is to develop confidence and the ability to evaluate an analysis
before leaning on tools that can do it for you. Developing and running
a pipeline you've built yourself, whose parameters you have chosen and
whose outputs you have questioned, will give you the intuition to
recognize when an LLM-generated version is subtly wrong. Importantly,
it also builds the vocabulary to ask for the right thing in the first
place by generating precise, well-grounded prompts stemming from an understanding
of the problem to be solved. 

Each submission includes a trust map: a table of every pipeline step
annotated with a trust level (high / medium / low) and a rationale.
At this stage, most of your pipeline is hand-built, so the trust map
is primarily an exercise in articulating why you believe each step is
correct. "It ran without errors" is not a rationale.

**Projects 3 & 4 — Level 3 (AI Collaboration)**
By this point you have enough hands-on experience to use AI as a
genuine collaborator. You may use AI tools more broadly for drafting
code, exploring methods, and structuring your write-up but your
critical evaluation of the output is the work. Each submission
includes a trust map and verification evidence: for every step you
flag as medium or low trust, a specific verification method carried
out and documented. Not "I will check the output" but "I confirmed
the number of significantly DE genes is plausible for this
experimental design, and I verified the fold change direction for
three known marker genes against a primary database."

**Final Project — Level 4 (Full AI)**
AI use is not just permitted here; it is expected. The trust map
and verification practice from earlier projects now governs the full
AI-assisted workflow. Note that Level 4 applies to the project as a
whole; individual components carry their own levels. The specification
document and trust map are Level 1. They must be completed without
AI assistance. Their value depends entirely on representing your own
thinking before any AI interaction occurs.

Your submission has four components:

**1. Specification document — Level 1 (No AI)**
Written before any AI interaction. For each step in your pipeline,
describe what a correct output looks like: its format, expected value
ranges, and any properties you could check programmatically. This is
your test suite. Writing it first forces you to understand the
analysis before you ask AI to help build it, and gives you a concrete
standard against which to evaluate what comes back.

**2. Trust map — Level 1 (No AI)**
A table of every pipeline step annotated with a trust level
(high / medium / low) and a rationale. The trust level reflects how
likely AI-generated output is to be subtly wrong at that step, and
why. A step with a high trust level still needs a rationale and
"it looked right" is not one. Steps involving experimental design
choices, biological interpretation, or tool flags that depend on your
specific data are almost always low trust.

**3. Verification evidence — Level 3 (AI Collaboration)**
For every step flagged as medium or low trust, a specific
verification method carried out and documented. Unit tests, manual
spot checks, and cross-references against published results all
count.

**4. Scientific writeup — Level 3 (AI Collaboration)**
Your interpretation of the results. Where your verification evidence
changed a conclusion or caught an error, that must be reflected here.
The argument, what your results mean, why they are or are not what
you expected, what caveats apply must remain yours. 

All AI-generated content must be cited. Your self-assessment for this
project should address where your trust map turned out to be wrong
and what that tells you about calibrating this kind of judgment in
future work.

**Self-assessments — Level 1 (No AI)**
Self-assessments are the one place where AI use is not permitted.
The honest reflection *is* the work. Using AI to write or refine your
self-assessment defeats its entire purpose.

## Project Grading

Each project asks you to write sections of a scientific publication,
produce relevant figures and visualizations, and explore discussion
questions designed to extend your thinking beyond the immediate
analysis. The emphasis throughout is on growth, not performance.

**Feedback, not scores.**
After each project you will receive detailed written feedback tied to
the learning objectives for that report. You will also receive an
indicative grade, but treat that number as a rough signal, not the
point. The feedback is the point.

**Growth model.**
No project grade is final until the end of the semester. Grades
improve as you demonstrate that you have incorporated feedback from
earlier reports into later ones. A weak Project 1 followed by clear
improvement carries more weight than a strong Project 1 followed by
stagnation.

**Self-assessment.**
Each submission includes a self-assessment (AIAS Level 1 — see
above). This is not graded on content. It is graded on depth and
honesty. The questions are simple: where did you meet the learning
objectives? Where do you still have gaps? What would you do
differently? These reflections are the primary record of your
learning across the semester. My hope is that this structure frees you to engage
with AI tools transparently, focus on the material, and reflect honestly on your
own growth without the grade getting in the way.

**Final weights.**
Projects account for 80% of your final grade; lab participation
accounts for 20%.

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


## A note on AI use in this syllabus

This syllabus was developed in keeping with the same principles
outlined above. All content was initially drafted by me; Claude
(Anthropic) was subsequently used to refine language, improve
clarity, and suggest structural edits. Every element was reviewed,
revised, and approved by me before inclusion.

The AI Assessment Scale sections were drafted with AI assistance
and reviewed against the primary literature. Citations and framework
descriptions reflect my own reading of that literature and should
be verified against the original sources.

This syllabus was produced at approximately **Level 3 (AI
Collaboration)**: AI assisted in developing and refining the
content while my judgment directed and evaluated the output
throughout. Nearly all of the content was manually drafted first before
integrating suggestions and edits from a LLM. 

Unless otherwise specified, all other course materials including labs,
projects, and supporting documents were produced at approximately
**Level 2–3 (AI Planning to AI Collaboration)**. I initially generated all drafts
by myself without the use of AI and AI was used only for structure, organization,
formatting, and further brainstorming. All of the technical content, biological
framing, and pedagogical decisions remain my own.

In short, this document is my own work, produced with AI as a collaborator and
not as a substitute for my judgment.