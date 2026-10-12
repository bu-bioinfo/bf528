---
title: "Lab 07 — Docker and Containers"
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

---

# Learning Objectives

## Use pre-built images from a public registry

> **Purpose - Why This Matters:** For most common bioinformatics tools,
> someone has already built and published an image. Pulling an existing image
> is often the fastest way to get a working tool. Choosing a specific tag
> rather than relying on `latest` is what makes that environment reproducible
> months or years later.
>
> **Task - What you will do:** Pull the `latest` and a pinned `slim` version
> of the official python image from Docker Hub. Start a container from each
> and check the installed python version. Compare the image sizes.
>
> **Criteria - How you'll know you're succeeding:** You can explain what an
> untagged pull actually retrieves. You can explain why a pinned tag is more
> reproducible than `latest`. You can account for the size difference between
> a full and a `slim` image.

## Write and build a Dockerfile using core instructions

> **Purpose - Why This Matters:** A Dockerfile is the written, version-controlled
> recipe for a computational environment. Knowing what each core instruction
> does lets you read the containers other people publish and write your own
> when a pre-built image doesn't exist or doesn't fit your needs.
>
> **Task - What you will do:** Build an image from the provided `simple/`
> Dockerfile and inspect the resulting environment interactively. Then
> complete the partially written `advanced/` Dockerfile and conda environment
> file to produce a working FastQC image.
>
> **Criteria - How you'll know you're succeeding:** You can state what `FROM`,
> `RUN`, `COPY`, `WORKDIR`, and `CMD` each contribute to the final image. You
> can explain why the `Dockerfile` itself does not appear inside the container.
> Your FastQC image builds successfully and `fastqc --version` runs inside it.

## Explain and exploit the Docker build cache

> **Purpose - Why This Matters:** Images are built as a stack of cached
> layers. Instruction order determines whether a one-line edit to a script
> rebuilds in seconds or reinstalls every dependency. When you are iterating
> on a pipeline, this difference adds up quickly.
>
> **Task - What you will do:** Rebuild an unchanged image, then edit
> `script.py` and rebuild again. Observe which steps are marked `CACHED`
> and which re-run.
>
> **Criteria - How you'll know you're succeeding:** You can predict which
> layers will be invalidated by a given change. You can justify ordering
> Dockerfile instructions from least to most frequently changed.

## Run containers non-interactively and interactively

> **Purpose - Why This Matters:** Containers are used in two distinct modes.
> They run a fixed command inside an automated workflow, and they open an
> interactive shell when you need to debug or explore the environment.
> Knowing how `docker run` flags and the `CMD` interact lets you move
> between these modes deliberately.
>
> **Task - What you will do:** Run a container that executes its default
> `CMD` and exits. Resolve a container-name conflict. Then launch an
> interactive, self-removing container with `-it --rm` and a command override.
>
> **Criteria - How you'll know you're succeeding:** You can explain why a
> container exits once its command finishes. You can explain why a stopped
> container still holds its name. You can describe how passing `bash`
> overrides the default `CMD`.

## Persist container outputs to the host with a bind mount

> **Purpose - Why This Matters:** By default, files written inside a
> container are isolated from the host and are lost when the container is
> removed. Any analysis that produces results you intend to keep depends on
> connecting the container's filesystem to persistent storage. Nextflow does
> exactly this on your behalf.
>
> **Task - What you will do:** Run FastQC in a container without a mount and
> look for the output. Then rerun it with `--volume $(pwd):/app` and
> retrieve the HTML report.
>
> **Criteria - How you'll know you're succeeding:** You can explain where the
> output went in each run. You can interpret the `<host_path>:<container_path>`
> syntax. You can explain why the mount only works when the input file exists
> in the host directory, since the mount replaces the image's `/app`.

## Evaluate design choices that keep images lightweight and pipeline-ready

> **Purpose - Why This Matters:** Images built for shared pipelines have
> different requirements than images built for one-off use. They need to be
> small enough to pull and convert repeatedly, secure enough to run on shared
> infrastructure, and flexible enough for a workflow manager to call any
> command. The containers used throughout this course reflect these
> trade-offs.
>
> **Task - What you will do:** Read the `class_containers/` Dockerfile and
> environment file. Answer the guided questions about the base image, cleanup
> steps, user switching, and the absence of a `CMD`. Manage and remove the
> images and containers you created during the lab.
>
> **Criteria - How you'll know you're succeeding:** For each of the
> following, you can give a specific technical reason for the choice:
> choosing `micromamba` over `miniconda3`, cleaning caches within the same
> `RUN` layer, switching between `root` and `$MAMBA_USER`, and omitting
> `CMD` for Nextflow use.

## (Optional) Publish an image to the GitHub Container Registry

> **Purpose - Why This Matters:** An image only becomes reusable by
> collaborators and pipelines once it lives in a registry. This is the same
> mechanism behind every `container 'ghcr.io/bu-cds-bf528/...'` line in your
> Nextflow processes.
>
> **Task - What you will do:** Authenticate to GHCR, tag an image with the
> full registry path, push it, make the package public, then delete your
> local copy and pull it back.
>
> **Criteria - How you'll know you're succeeding:** You can explain why both
> tags share one IMAGE ID. You can explain why already-pushed layers are
> skipped during upload. Your image can be pulled and run from GHCR with no
> local copy present.