---
title: "Lab 08 — QC Pipeline with Singularity"
---

**Key concepts and tools**
- `mix` — interleaving two channels of the same type into one
- `container` directive, `-profile singularity` — Singularity on the SCC
- `withLabel` resource labels in `nextflow.config` — `process_single`, `process_low`, `process_medium`
- `withName` per-process `publishDir` and `ext.args` in config
- FastQC, Trimmomatic, MultiQC — standard short-read QC workflow
- QC report interpretation: per-base quality, GC content, adapter content, read length distribution, duplication

---

This lab assembles a complete short-read QC pipeline — FastQC on raw reads, adapter trimming with Trimmomatic, FastQC on trimmed reads, and MultiQC to summarise everything in a single HTML report. All processes run in Singularity containers, which is how all subsequent projects are run on the SCC. The one new Nextflow concept is `mix`, used to merge the pre-trim and post-trim FastQC channels so MultiQC sees both sets of reports and can produce a before/after comparison.

## Setup

```bash
module load miniconda
conda activate nextflow_latest
export NXF_SYNTAX_PARSER=v2
```

```bash
nextflow run main.nf -profile singularity,local    # local test
nextflow run main.nf -profile singularity,cluster  # submit to SCC
```

## Pipeline

```
samplesheet.csv
    ↓ channel.fromList
samples_ch ──┬──→ FASTQC ──────────────────────────→ pre_qc_ch ──┐
             │                                                      ├─ mix → combined_qc → flatMap → collect → MULTIQC
             └──→ TRIMMOMATIC → trim_ch → FASTQC → post_qc_ch ───┘
```

`mix` is the join point: it interleaves `pre_qc_ch` and `post_qc_ch` into a single channel so all six FastQC zip files (3 samples × pre + post) reach MultiQC together.

## Tasks

**Task 1 — Read `main.nf` and the modules**  
Before writing anything, answer: what field does TRIMMOMATIC add that FASTQC doesn't need? How many FASTQC tasks run for 3 samples? How does duck-typing allow `FASTQC(trim_ch)` to work when `trim_ch` carries a `log` field?

**Task 2 — Fill in the `mix` call**  
`main.nf` has one `???` placeholder. Replace it with:
```nextflow
combined_qc = pre_qc_ch.mix(post_qc_ch)
```
Verify with `-stub-run` (expect 10 tasks: 6 FASTQC + 3 TRIMMOMATIC + 1 MULTIQC).

**Task 3 — Run on the cluster**  
`nextflow run main.nf -profile singularity,cluster`. Open `results/multiqc/multiqc_report.html` and confirm both pre-trim and post-trim sections are present.

**Task 4 — Resource labels**  
Trace how `withLabel: process_low { cpus = 4 }` in `nextflow.config` becomes `-threads 4` in TRIMMOMATIC's `.command.sh`. Change the value and re-run with `-stub-run` to confirm it propagates.

**Task 5 — Interpreting the QC report**  
Working through five metrics: per-base quality, GC distribution, adapter content, read length distribution after trimming, duplication levels. Reference report: `exercise_3/provided_results/full_report.html`.
