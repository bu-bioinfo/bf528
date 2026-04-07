---
title: "Lab 03 — Nextflow Practice"
layout: single
---

**Key concepts and tools**
- `Channel.fromPath`
- `params`, `$projectDir`
- `set { channel_name }`
- Process `input`, `output`, `script` blocks
- `publishDir`
- `split`, `tr` — Unix text utilities

---

A short, open-ended lab that reinforces core Nextflow concepts through a minimal example. You first perform the task manually in the shell — splitting a file into chunks and uppercasing the contents — then rebuild the same logic as a Nextflow workflow.

## Part 1 — Manual (cli_workflow/)

```bash
cat starting_file.txt | split -l 1 - chunk_
cat chunk_aa | tr '[a-z]' '[A-Z]' > new_chunk_aa.txt
cat chunk_ab | tr '[a-z]' '[A-Z]' > new_chunk_ab.txt
```

## Part 2 — Nextflow (nextflow/)

```bash
module load miniconda
conda activate nextflow_latest
```

1. Run `channel.nf` to see how `Channel.fromPath` and `params.starting_file` work together. `$projectDir` resolves to the directory containing `main.nf`, keeping paths portable.
2. Copy the channel code into `main.nf`, replacing the final `view()` with `set { file_ch }`.
3. Write a process that takes the channel as input, runs `split` and `tr`, and publishes the results with `publishDir`.
4. Run: `nextflow run main.nf`

The emphasis is on constructing a channel from a file param, passing it through a process, and collecting output — without the distraction of bioinformatics tool flags.
