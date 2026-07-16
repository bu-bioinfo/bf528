---
title: "Lab 06 — Subworkflows and Pipeline Architecture"
layout: single
---

**Key concepts and tools**
- Named record types as shared type contracts between files
- `params {}` block with `List<RecordType>` and automatic CSV samplesheet parsing
- Modules: one process per file, `include { PROCESS } from './modules/...'`
- Process directives: `label`, `conda`, `publishDir`
- `nextflow.config`: `profiles {}`, resource labels, `withName:`, `ext.args`
- Channel operators: `.map`, `.mix`, `.flatMap`, `.collect`
- Subworkflows: typed `take:` / `emit:`, imported with `include`
- Re-exporting record types from a subworkflow file
- Duck-typing: the minimum-fields contract that enables module reuse

---

This lab builds a four-step reads QC pipeline — FastQC, Trimmomatic, FastQC again, MultiQC — through five successive refactoring steps. Each step introduces one architectural layer from the lecture and articulates the design choice it embodies. The result is a pipeline with typed parameters, modular processes, a configuration file, operator-driven channel wiring, and a reusable subworkflow — every layer from the slides, in one working pipeline. No real FASTQ files or tool installations are required; every checkpoint runs in stub mode.

## Setup

```bash
module load miniconda
conda activate nextflow_latest
export NXF_SYNTAX_PARSER=v2
```

Create a working directory and placeholder input files:

```bash
mkdir -p lab06 && cd lab06
mkdir -p data modules/fastqc modules/trimmomatic modules/multiqc subworkflows
for s in ctl_rep1 ctl_rep2 trt_rep1 trt_rep2; do
    touch data/${s}_R1.fastq.gz data/${s}_R2.fastq.gz
done
```

## Goal structure

```
main.nf
samplesheet.csv
nextflow.config
subworkflows/
  reads_qc.nf
modules/
  fastqc/main.nf
  trimmomatic/main.nf
  multiqc/main.nf
```

---

## Task 1 — Typed params and samplesheet

**Design choice:** Separate *what* the pipeline processes from *how* it processes it. A samplesheet CSV is the standard interface for multi-sample input. Declaring it as `List<RecordType>` gives Nextflow a schema to validate each row against at startup — before any task is submitted.

Create `samplesheet.csv`:

```csv
id,fastq_1,fastq_2
ctl_rep1,data/ctl_rep1_R1.fastq.gz,data/ctl_rep1_R2.fastq.gz
ctl_rep2,data/ctl_rep2_R1.fastq.gz,data/ctl_rep2_R2.fastq.gz
trt_rep1,data/trt_rep1_R1.fastq.gz,data/trt_rep1_R2.fastq.gz
trt_rep2,data/trt_rep2_R1.fastq.gz,data/trt_rep2_R2.fastq.gz
```

Create `main.nf`:

```nextflow
nextflow.preview.types = true

record Sample {
    id:      String
    fastq_1: Path
    fastq_2: Path
}

params {
    samplesheet: List<Sample> = 'samplesheet.csv'
    outdir:      Path         = 'results'
}

workflow {
    samples_ch = channel.fromList(params.samplesheet)
    samples_ch.view { s -> "${s.id}: ${s.fastq_1}" }
}
```

```bash
nextflow run main.nf -profile local -stub-run
```

You should see four lines, one per sample. The `record Sample` declaration acts as the CSV schema — column names must match field names exactly. A missing column or wrong type is caught here, before any compute resources are requested.

---

## Task 2 — Modules with typed I/O

**Design choice:** One process per file. Each module declares the *minimum* fields it needs — any richer record that supplies those fields satisfies the contract (duck-typing). This lets the same `FASTQC` module accept raw samples and trimmed samples without modification.

Create `modules/fastqc/main.nf`:

```nextflow
nextflow.preview.types = true

process FASTQC {
    label 'process_low'
    conda "${moduleDir}/../../envs/fastqc.yml"

    input:
    record(id: String, reads: List<Path>)

    output:
    record(
        id:   id,
        zip:  files("*_fastqc.zip"),
        html: files("*_fastqc.html")
    )

    script:
    """
    fastqc ${reads.join(' ')} --threads ${task.cpus}
    """

    stub:
    """
    touch ${id}_R1_fastqc.zip ${id}_R1_fastqc.html
    touch ${id}_R2_fastqc.zip ${id}_R2_fastqc.html
    """
}
```

Create `modules/trimmomatic/main.nf`:

```nextflow
nextflow.preview.types = true

process TRIMMOMATIC {
    label 'process_medium'
    conda "${moduleDir}/../../envs/trimmomatic.yml"

    input:
    record(id: String, fastq_1: Path, fastq_2: Path)

    output:
    record(
        id:       id,
        reads:    files("${id}_{1,2}P.fastq.gz"),
        trim_log: file("${id}.trim.log")
    )

    script:
    def args = task.ext.args ?: ''
    """
    trimmomatic PE -threads ${task.cpus} \
        ${fastq_1} ${fastq_2} \
        ${id}_1P.fastq.gz ${id}_1U.fastq.gz \
        ${id}_2P.fastq.gz ${id}_2U.fastq.gz \
        -trimlog ${id}.trim.log \
        ${args}
    """

    stub:
    """
    touch ${id}_1P.fastq.gz ${id}_2P.fastq.gz ${id}.trim.log
    """
}
```

Create `modules/multiqc/main.nf`:

```nextflow
nextflow.preview.types = true

process MULTIQC {
    label 'process_low'
    conda "${moduleDir}/../../envs/multiqc.yml"

    input:
    record(qc_files: List<Path>)

    output:
    record(report: file("multiqc_report.html"))

    script:
    """
    multiqc .
    """

    stub:
    """
    touch multiqc_report.html
    """
}
```

`FASTQC` takes `reads: List<Path>`, not `fastq_1` and `fastq_2`. The module treats the reads as an ordered list; it does not care that they come in pairs. `TRIMMOMATIC`, by contrast, takes `fastq_1` and `fastq_2` explicitly because the tool's interface distinguishes them. The module's input record reflects the tool's interface, not the samplesheet's structure — keeping these concerns separate is what makes each module independently reusable.

Add `include` statements to `main.nf` after the `params {}` block:

```nextflow
include { FASTQC }      from './modules/fastqc'
include { TRIMMOMATIC } from './modules/trimmomatic'
include { MULTIQC }     from './modules/multiqc'
```

---

## Task 3 — Configuration: profiles, labels, and ext.args

**Design choice:** Keep execution details out of modules. A module declares *what* it needs (CPU/memory via `label`, tool flags via `task.ext.args`); `nextflow.config` decides *how much* and *which flags*. A module that encodes resource numbers or tool parameters cannot be shared across projects with different hardware or analysis requirements.

Create `nextflow.config`:

```groovy
profiles {
    local {
        process.executor = 'local'
    }
    cluster {
        process.executor       = 'sge'
        process.clusterOptions = '-P bf528'
    }
    conda {
        conda.enabled = true
    }
    singularity {
        singularity.enabled    = true
        singularity.autoMounts = true
    }
}

process {
    withLabel: 'process_low' {
        cpus   = 2
        memory = '4 GB'
    }
    withLabel: 'process_medium' {
        cpus   = 8
        memory = '16 GB'
    }

    withName: 'TRIMMOMATIC' {
        ext.args = 'SLIDINGWINDOW:4:15 MINLEN:36'
    }
    withName: 'MULTIQC' {
        publishDir = [path: "${params.outdir}/qc", mode: 'copy']
    }
}
```

`ext.args` flows into the module via `task.ext.args ?: ''` in the script block. Changing trimming parameters is a one-line config edit, not a module edit. A module shared across three projects means all three benefit from every improvement — and a change to the module affects all three. `ext.args` is the mechanism that lets project-specific tuning live in the project config while the module stays generic.

`publishDir` is set in config rather than in the module for the same reason: two projects may organize outputs differently. A module that hardcodes `publishDir` cannot be reused as-is by a project with a different directory layout.

---

## Task 4 — Flat pipeline wiring

**Design choice:** Operators transform channel records on the driver node — no cluster jobs, no wait time. All reshaping and aggregation logic belongs in the workflow block, not inside modules. This keeps modules stateless and reusable; the caller decides how to connect them.

Update the `workflow {}` block in `main.nf`:

```nextflow
workflow {
    samples_ch = channel.fromList(params.samplesheet)

    // Reshape samplesheet record → FASTQC's (id, reads: List<Path>) form
    raw_ch = samples_ch.map { s -> record(id: s.id, reads: [s.fastq_1, s.fastq_2]) }

    pre_qc  = FASTQC(raw_ch)
    trimmed = TRIMMOMATIC(samples_ch)

    // The _post suffix distinguishes pre/post samples in the MultiQC report
    post_qc = FASTQC(trimmed.map { s -> record(id: "${s.id}_post", reads: s.reads) })

    // Gather all QC files — collect() waits for all samples before MultiQC starts
    all_qc_ch = pre_qc
        .map { r -> r.zip + r.html }
        .mix(post_qc.map { r -> r.zip + r.html })
        .flatMap { fs -> fs }
        .collect()
        .map { files -> record(qc_files: files) }

    MULTIQC(all_qc_ch)
}
```

Run the flat pipeline:

```bash
nextflow run main.nf -profile local,conda -stub-run
```

Expect 13 tasks: 4 `FASTQC` (pre-trim), 4 `TRIMMOMATIC`, 4 `FASTQC` (post-trim), 1 `MULTIQC`. The MULTIQC task does not start until all eight FASTQC tasks finish — `.collect()` enforces this by withholding its output until the upstream channel closes.

Visualize the dependency graph:

```bash
nextflow run main.nf -profile local -stub-run -with-dag dag.html
```

---

## Task 5 — Extract the READS_QC subworkflow

**Design choice:** A subworkflow bundles a recurring multi-process pattern into a named, typed unit with an explicit contract. The FASTQC → TRIMMOMATIC → FASTQC sequence appears in both project 2 and project 3; writing it once means one place to fix bugs and one place to tune parameters. The typed `take:` / `emit:` annotations are checked by the language server at parse time — a mismatch between what the subworkflow emits and what the caller expects is caught before the pipeline runs.

Create `subworkflows/reads_qc.nf`:

```nextflow
nextflow.preview.types = true

include { FASTQC }      from '../modules/fastqc'
include { TRIMMOMATIC } from '../modules/trimmomatic'

record Sample {
    id:      String
    fastq_1: Path
    fastq_2: Path
}

record TrimmedSample {
    id:       String
    reads:    List<Path>
    trim_log: Path
}

record QCResult {
    id:   String
    zip:  List<Path>
    html: List<Path>
}

workflow READS_QC {
    take:
    samples_ch: Channel<Sample>

    main:
    raw_ch  = samples_ch.map { s -> record(id: s.id, reads: [s.fastq_1, s.fastq_2]) }
    pre_qc  = FASTQC(raw_ch)
    trimmed = TRIMMOMATIC(samples_ch)
    post_qc = FASTQC(trimmed.map { s -> record(id: "${s.id}_post", reads: s.reads) })

    emit:
    trimmed: Channel<TrimmedSample> = trimmed
    pre_qc:  Channel<QCResult>      = pre_qc
    post_qc: Channel<QCResult>      = post_qc
}
```

Record types are defined in the subworkflow file — not duplicated in `main.nf`. Any caller imports the type alongside the workflow name:

```nextflow
include { READS_QC, Sample } from './subworkflows/reads_qc'
```

Callers access named emit outputs as fields on the return value: `qc.trimmed`, `qc.pre_qc`, `qc.post_qc`. This is the same field-access pattern used for typed process outputs.

Replace `main.nf` with the final composed version:

```nextflow
nextflow.preview.types = true

include { READS_QC, Sample } from './subworkflows/reads_qc'
include { MULTIQC }          from './modules/multiqc'

params {
    samplesheet: List<Sample> = 'samplesheet.csv'
    outdir:      Path         = 'results'
}

workflow {
    samples_ch = channel.fromList(params.samplesheet)

    qc = READS_QC(samples_ch)

    all_qc_ch = qc.pre_qc
        .map { r -> r.zip + r.html }
        .mix(qc.post_qc.map { r -> r.zip + r.html })
        .flatMap { fs -> fs }
        .collect()
        .map { files -> record(qc_files: files) }

    MULTIQC(all_qc_ch)
}
```

Run the final pipeline:

```bash
nextflow run main.nf -profile local,conda -stub-run
```

The task count and graph are identical to Task 4. The refactoring is structural: `main.nf` now reads as a high-level orchestration — load samples, run QC, aggregate and report. Adding the alignment step would be a single `ALIGN(qc.trimmed)` call followed by its own subworkflow, with no changes to the QC logic.

---

## Design summary

| Layer | Where it lives | What it expresses |
|---|---|---|
| Data schema | `record Sample {}` in `subworkflows/reads_qc.nf` | Shape and types of each samplesheet row |
| Parameters | `params {}` in `main.nf` | What the pipeline accepts, with types and defaults |
| Processes | `modules/*/main.nf` | One tool, one task, typed I/O, minimum-fields contract |
| Environment | `label`, `conda` in modules | What software each process needs |
| Execution | `profiles {}` in `nextflow.config` | Where jobs run (local vs. cluster) |
| Resources | `withLabel:` in `nextflow.config` | CPU and memory per resource tier |
| Tool flags | `ext.args` in `nextflow.config` | Per-process options without module edits |
| Output location | `publishDir` in `nextflow.config` | Where final results are copied |
| Reusable pattern | `subworkflows/reads_qc.nf` | Named, typed, multi-process analysis unit |
| Pipeline | `workflow {}` in `main.nf` | High-level composition of subworkflows |

## Optional

1. Add a fifth sample to `samplesheet.csv` and re-run with `-resume`. Only the three new tasks (pre-QC, trim, post-QC for the new sample) execute; MultiQC re-runs because `.collect()` output changed.

2. Override TRIMMOMATIC quality thresholds from the command line without editing any `.nf` file:
   ```bash
   nextflow run main.nf -profile local -stub-run \
     -c 'process { withName: "TRIMMOMATIC" { ext.args = "SLIDINGWINDOW:4:20 MINLEN:50" } }'
   ```

3. Extract the `all_qc_ch` wiring and `MULTIQC` call into a `MULTIQC_REPORT` subworkflow under `subworkflows/`. The final `main.nf` workflow block becomes three lines: load samples, call `READS_QC`, call `MULTIQC_REPORT`.
