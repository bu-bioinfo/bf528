---
title: "Conventional Commits"
layout: single
---

> **Reference:** [conventionalcommits.org](https://www.conventionalcommits.org/en/v1.0.0/)

# Conventional Commits

A commit message is more than a note to yourself — it is the primary record of
why a change was made. Anyone reading the history of a repository (including
future you, six months from now) should be able to understand what happened and
why without having to read every line of code that changed.

Conventional Commits is a lightweight specification for writing commit messages
in a consistent, machine-readable format. The format is simple enough to type
in seconds, but structured enough that tools can parse it automatically to
generate changelogs, determine version numbers, and filter history by change type.

## The Format

A conventional commit message has three parts:

```
<type>[optional scope]: <description>

[optional body]

[optional footer]
```

The first line — `<type>[optional scope]: <description>` — is the most important
part and the one you will write most often. The body and footer are used for
longer explanations and metadata such as breaking change notices or issue references.

### Type

The type is a short keyword that categorizes what the commit does. The most
commonly used types are:

| Type | When to use |
|---|---|
| `feat` | Adds a new feature or capability |
| `fix` | Corrects a bug or incorrect behavior |
| `docs` | Changes to documentation only |
| `style` | Formatting changes that do not affect behavior (whitespace, semicolons) |
| `refactor` | Code restructuring that is neither a new feature nor a bug fix |
| `test` | Adding or correcting tests |
| `chore` | Maintenance tasks that don't touch production code (dependency updates, CI config) |
| `ci` | Changes to continuous integration configuration |

In bioinformatics workflows you will most commonly reach for `feat`, `fix`, and
`docs`. `refactor` is useful when you reorganize a pipeline without changing
what it does — for example, extracting a repeated block into a shared subworkflow.

### Scope

The scope is an optional word in parentheses that narrows the type to a specific
part of the codebase. It is helpful in larger projects where a commit might touch
one module among many:

```
feat(prokka): add --metagenome flag to annotation process
fix(trimmomatic): correct adapter path for paired-end samples
docs(readme): update cluster submission instructions
```

In a single-module project or a small lab repo, scope is often omitted.

### Description

The description is a short, imperative-mood summary of the change. Imperative
mood means you write it as a command: "add", "fix", "update", "remove" — not
"added", "fixed", "updating", or "removed".

Think of it as completing the sentence: *"If applied, this commit will..."*

- **Good:** `feat: add GC content calculation to genome stats process`
- **Good:** `fix: handle gzipped input in calc_length.py`
- **Less useful:** `updated the script`
- **Less useful:** `fixed bug`
- **Less useful:** `WIP`

Keep the description under 72 characters so it displays cleanly in `git log`.

## Examples

A minimal single-line commit:

```bash
git commit -m "feat: add jellyfish kmer counting process"
```

A commit with scope:

```bash
git commit -m "fix(samtools): remove duplicate fai index output field"
```

A commit with a body explaining the reasoning:

```bash
git commit -m "refactor: extract QC steps into shared reads_qc subworkflow

FASTQC and Trimmomatic were duplicated across project-2 and project-3.
Moving them to a shared subworkflow removes ~80 lines of repeated code
and ensures both projects stay in sync when parameters change."
```

A commit that documents a breaking change in the footer:

```bash
git commit -m "feat!: replace tuple inputs with typed record outputs

BREAKING CHANGE: process inputs now use record() destructuring.
Callers must update channel construction to supply named fields
instead of positional tuple elements."
```

The `!` after the type is shorthand for a breaking change. The
`BREAKING CHANGE:` footer makes it explicit for changelog tools.

## Why It Matters

### Readable history

When every commit follows the same format, `git log --oneline` becomes a
structured summary of the project's evolution rather than a stream of
free-text notes:

```
3f1a2c4 feat: add publishDir to GENOME_STATS process
b8e0d91 fix: correct shebang line in gc_content.py
a12c883 docs: update iteration_3 instructions with nextflow log commands
9d4f701 refactor: move biopython env spec to envs/ directory
```

You can immediately see what category of change each commit represents without
opening the diff.

### Filtering history

Because the type is always in the same position, you can search commit history
by change category:

```bash
git log --oneline --grep "^fix"    # show only bug fixes
git log --oneline --grep "^feat"   # show only new features
```

### Communicating intent to collaborators

In a shared repository — or when submitting work to an instructor — conventional
commit messages communicate not just what changed but why the change was
necessary. A `fix:` prefix signals that something was wrong. A `refactor:`
prefix signals that behavior is unchanged and the diff can be reviewed with less
scrutiny. A `feat:` signals new capability that a reviewer should test.

## Common Mistakes

**Using past tense.** Write "add support for gzipped input", not "added support
for gzipped input". The convention is imperative mood.

**Bundling unrelated changes.** If you fixed a bug and added a new process in
the same commit, the message cannot accurately describe both. Make two commits.
Small, focused commits are easier to review, easier to revert if something goes
wrong, and produce more useful history.

**Skipping the type.** A message like `"update main.nf"` is technically valid
git but provides no information about why the file changed. Requiring yourself
to choose a type forces you to think about what the change is — and sometimes
reveals that you are about to bundle two different kinds of changes into one.

**Over-specifying the description.** The description should say what the commit
does, not list every file touched. File names are visible in the diff; the
message should convey intent.

## Adopting Conventional Commits

You do not need any tooling to use conventional commits — it is just a writing
convention. The full specification at
[conventionalcommits.org](https://www.conventionalcommits.org/en/v1.0.0/)
defines additional rules for changelog generation and semantic versioning
tooling, but following the basic `type: description` format immediately improves
your commit history without any configuration.

For this course, using `feat`, `fix`, `docs`, `refactor`, and `chore` consistently
is sufficient. When in doubt, pick the type that best describes the primary intent
of the change.
