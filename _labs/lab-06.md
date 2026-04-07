---
title: "Lab 06 — Docker and Containers"
layout: single
---

**Key concepts and tools**
- `docker pull`, `docker run`, `docker images`, `docker build`
- `Dockerfile`: `FROM`, `RUN`, `COPY`, `WORKDIR`, `CMD`
- Image tags and versioning
- Interactive (`-it`) vs. non-interactive container execution
- Bind mounts (`-v host:container`)
- Build cache and layer ordering
- GitHub Container Registry (`ghcr.io`), `docker push`
- Singularity and its relationship to Docker
- FastQC, Trimmomatic, MultiQC — sequencing QC workflow

---

Containers solve the "works on my machine" problem by packaging a tool and all its dependencies into a portable, reproducible image. This lab runs in GitHub Codespaces rather than the SCC so you have access to the Docker daemon. You will pull existing images, inspect them interactively, write a Dockerfile from scratch, build and tag an image, and use a bind mount to persist output files back to the host. The final section introduces GitHub Container Registry, which is where the course container images live and how Singularity pulls them on the cluster.

---

# Part 1 — Sequence Quality Control

Raw sequencing reads always require quality assessment before any downstream analysis. Systematic quality issues — adapter contamination, low-quality tails, GC bias, overrepresented sequences — can propagate silently through a pipeline and distort biological conclusions.

## Workflow

```
FASTQC (raw) → TRIMMOMATIC → FASTQC (trimmed) → MULTIQC
```

Run FastQC on raw reads first. After trimming, run FastQC again to confirm issues are resolved. MultiQC aggregates both sets of reports so you can compare before and after side by side.

## Reading a MultiQC report

- **Per-base sequence quality** — flag if median quality drops below Q28 at the 3' end
- **Per-sequence GC content** — a sharp peak offset from the expected distribution indicates contamination
- **Adapter content** — any adapter signal above ~1% warrants trimming
- **Sequence duplication levels** — high duplication in RNA-seq may indicate over-amplification; in ChIP/ATACseq it is expected

## Trimmomatic

```bash
trimmomatic PE \
    -threads $task.cpus \
    $read1 $read2 \
    ${sample}_R1_paired.fastq.gz ${sample}_R1_unpaired.fastq.gz \
    ${sample}_R2_paired.fastq.gz ${sample}_R2_unpaired.fastq.gz \
    ILLUMINACLIP:TruSeq3-PE.fa:2:30:10 \
    LEADING:3 TRAILING:3 SLIDINGWINDOW:4:15 MINLEN:36
```

Key options:
- `ILLUMINACLIP` — adapter sequence file and mismatch tolerances
- `SLIDINGWINDOW:4:15` — trim when average quality in a 4-base window drops below Q15
- `MINLEN:36` — discard reads shorter than 36 bp after trimming

---

# Part 2 — Docker and Containers

## Why containers?

Conda environments solve many reproducibility problems, but they can fail when a tool has non-Python system dependencies, when the tool is not packaged for conda, or when you need to run on infrastructure without conda. Containers bundle an entire Linux filesystem — OS libraries, tool binaries, and your conda environment — into a single portable image.

## Docker concepts

| Concept | Description |
|---|---|
| Image | A read-only template built from a Dockerfile |
| Container | A running instance of an image |
| Layer | Each `RUN` instruction adds a filesystem layer; layers are cached |
| Registry | Remote storage for images (`docker.io`, `ghcr.io`) |

## Basic commands

```bash
docker pull python:3.11-slim           # download an image
docker images                           # list local images
docker run -it python:3.11-slim bash   # interactive shell inside container
docker run python:3.11-slim python --version  # non-interactive
docker build -t myimage:latest .        # build from Dockerfile in current dir
docker push ghcr.io/org/myimage:tag    # push to registry
```

## Dockerfile structure

```dockerfile
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    samtools \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /data
```

Key instructions:
- `FROM` — base image (always first)
- `RUN` — execute a shell command and commit the result as a new layer
- `COPY` — add files from the build context into the image
- `WORKDIR` — set the working directory for subsequent instructions and container startup
- `CMD` — default command when the container starts

## Bind mounts

Containers have their own isolated filesystem. To read files from or write files to the host, use a bind mount:

```bash
docker run -v /host/path:/container/path myimage command
```

Files written to `/container/path` inside the container appear at `/host/path` on the host after the container exits.

## Singularity on the SCC

The SCC does not allow Docker (it requires root). Singularity provides the same isolation with user-level permissions. Nextflow pulls Singularity images automatically when you use `-profile singularity`. Docker images from `ghcr.io` are converted on the fly.

```bash
nextflow run main.nf -profile singularity,cluster
```
