---
title: "Lab 02b — Nextflow Tooling"
layout: single
---

**Key concepts and tools**
- `stub` block, `-stub` flag
- `ext.args`, `task.ext.args ?: ''`
- `withName:` process selector in `nextflow.config`
- `-with-report`, `-with-timeline`, `-with-dag`
- `nextflow log`, `-f` fields, `-filter` expressions
- `.command.sh`, `.command.err`, `.exitcode` in the work directory
- `nextflow lint`, `nf-core lint`, `nextflow inspect`
- `nextflow fmt`

---

This lab focuses on the development and debugging features that make Nextflow practical to use on real pipelines. Working with a pre-built FastQC → fastp → MultiQC workflow, you will run the pipeline in stub mode to test channel logic without executing real tools, configure per-tool flags through `ext.args` in the config file, generate HTML execution reports and timelines, and use `nextflow log` to locate work directories and read the exact commands that were run. A final section covers linting and formatting tools that catch mistakes before a job is submitted.
