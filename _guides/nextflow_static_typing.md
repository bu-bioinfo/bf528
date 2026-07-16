---
title: "Nextflow Static Typing"
layout: single
---

# Static Typing in Nextflow

Nextflow 26.04 introduced support for static typing. This guide explains what
static typing means in the context of Nextflow, why it was added to the
language, and what you need to do to use it.

## Background: How Nextflow Has Evolved

Nextflow has gone through several significant changes since it was first
released. Understanding this progression helps explain why static typing looks
the way it does.

### DSL1 and DSL2

The original Nextflow language (sometimes called DSL1) embedded pipeline logic
directly inside process definitions. DSL2, introduced as the standard in
Nextflow 22.x, separated processes into standalone modules that could be
imported and reused. This is the `include { PROCESS } from './modules/...'`
pattern you have already seen.

DSL2 was a major improvement for code organization, but it left much of the
channel wiring logic loosely defined. Channels carried values of any type, and
it was easy to pass a tuple in the wrong order or call a deprecated operator
without any warning.

### The Strict Syntax

Nextflow 26.04 enables a stricter variant of the DSL2 syntax by default. The
strict syntax removes several patterns that were previously allowed but known
to cause problems:

- Using `Channel` (uppercase) to access channel factories
- Using the implicit `it` closure parameter
- Using `set` or `tap` to assign channels
- Composing logic with `|` and `&`
- Accessing process outputs via `.out`

These are not arbitrary restrictions. Each of these patterns makes it difficult
or impossible for Nextflow to understand the types of values flowing through
your pipeline, which is required for type checking to work.

If you have code written in an older style, the `nextflow lint` command will
flag these patterns before you try to run anything.

### Static Typing

Static typing builds on the strict syntax by allowing you to annotate your
code with type information. Instead of a channel that carries "something",
you can declare a channel that carries `Channel<Sample>` — a channel of `Sample`
records with specific named fields.

When type annotations are present, the Nextflow language server can validate
them during development. It can tell you, before you run a single task, that a
channel of `Sample` records is compatible with a process expecting `id: String`
and `fastq_1: Path`. This is the same kind of feedback that a linter or
compiler gives you in other typed languages.

## Enabling Static Typing

Static typing requires two things.

First, the strict syntax parser must be active. In Nextflow 26.04 it is enabled
by default. If you are on an earlier version, you can activate it explicitly:

```bash
export NXF_SYNTAX_PARSER=v2
```

You only need to set this once per shell session. A good place to put it is in
your `.bashrc` or the activation script for your Nextflow conda environment.

Second, each script that uses typed processes or typed workflows must declare
the preview feature flag at the top of the file:

```bash
nextflow.preview.types = true
```

This flag goes in the script itself, not in the config file, and it must be
present in every `.nf` file that uses typed syntax — including module files,
not just `main.nf`.

**N.B.** The `params {}` block and the `output {}` block work without this flag.
You only need `nextflow.preview.types = true` in files that contain typed
process inputs, typed process outputs, or typed workflow `take:`/`emit:`
declarations.

## What Type Checking Does

The type checker runs inside the Nextflow language server, which is the backend
used by the VS Code Nextflow extension. As you edit your pipeline, the language
server continuously checks the types of channels as they flow between processes
and operators.

For example, if you define a process that expects a `Path` input but you pass
it a `String`, the language server will underline the mismatch in the editor
and show you the error before you run anything.

This is useful for catching several common mistakes:

- Passing a channel of the wrong record type to a process
- Forgetting to include a required field in a record
- Using an operator that is not statically typed (and therefore breaks the
  type checker's ability to validate downstream code)

The type checker does not run as part of `nextflow lint` or as part of a normal
`nextflow run`. It is a development-time tool. Running the pipeline will not
fail on type errors alone — but having the language server flag them while you
are writing code means you fix problems earlier and more cheaply.

## Why Some Operators Are Not Statically Typed

Not every Nextflow operator can be given a precise return type. Operators like
`splitCsv`, `groupTuple`, and `branch` can return different types depending on
their arguments, and the type checker cannot always determine which type applies.

When you use one of these operators, the type checker treats the resulting
channel as having an unknown type, which means it cannot validate anything
downstream of that operator. The core operators — `map`, `filter`, `flatMap`,
`join`, `collect`, and others — all have precise types and are fully supported.

This is the primary reason why patterns like `Channel.fromFilePairs` followed
by `splitCsv` are replaced in typed pipelines. Those patterns produce channels
with unknown types. The replacement — a typed `List<Sample>` parameter loaded
from a CSV samplesheet — gives the channel a precise type that the checker can
follow through every downstream operator and process.

See [Using operators with static typing]() and the Operators (typed) reference
for more detail on which operators are fully supported.

## Static Typing Is Optional

Existing pipelines do not need to be migrated. All DSL2 syntax continues to
work. You can also adopt static typing progressively: you might add a typed
`params {}` block first, then migrate individual processes, then migrate
workflows, without needing to change everything at once.

The one constraint is that you should not mix typed and legacy syntax within
the same workflow. If a workflow is declared as typed — using annotated `take:`
and `emit:` — then all of the patterns restricted by the strict syntax must be
absent from that workflow.

## Summary

| Feature | Available since | Requires flag |
|---|---|---|
| Typed `params {}` block | 25.10 | No |
| Typed `output {}` block | 25.10 | No |
| Typed process inputs/outputs | 26.04 | `nextflow.preview.types = true` |
| Typed workflow `take:`/`emit:` | 26.04 | `nextflow.preview.types = true` |
| Strict syntax parser | 26.04 (default) | `NXF_SYNTAX_PARSER=v2` on older versions |
