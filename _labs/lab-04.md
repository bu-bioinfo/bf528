---
title: "Lab 04 — Channel Operators and Scaling Up"
---

**Key concepts and tools**
- `Channel.fromPath`, `Channel.fromFilePairs`
- `map`, `join`, `collect`, `combine`, `branch`, `flatten`, `transpose`
- `view` — inspecting channel contents
- `mix`
- Containers vs. conda: `container` directive, Singularity
- `-profile singularity,local`, `-profile singularity,cluster`
- `process.withLabel`, resource labels (`process_single`, `process_low`)
- FastQC, Trimmomatic, MultiQC

---

Channel operators are how Nextflow pipelines reshape, merge, and route data between processes. This lab is a series of exercises — each one isolates a common channel manipulation pattern (grouping, joining, collecting, branching, combining) and asks you to apply it both in a standalone `test.nf` and inside a real multi-sample pipeline. You also transition away from conda to Singularity containers, which is how all subsequent projects are run. By the end you should be comfortable building the input channel for any standard bioinformatics pipeline.
