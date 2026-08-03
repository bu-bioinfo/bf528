---
title: "Nextflow Channels"
layout: single
---

# Nextflow Channels

Nextflow channels are the key data dstructure that allow data to flow between
dependencies or processes in a workflow. Though there are more technical details,
you can think of channels as queues or lists of values that can be passed between
processes. For our workflows, these channels will contain lists of the files and
their metadata that we want to process.

## Queue Channel

A queue channel *emits* an asynchronous sequence of values. The values in a queue
channel cannot be accessed directly. A queue channel can be made from various
channel factories. 

## Value Channels

A value channel is *bound to an asynchronous value. A value channel can be created
with the channel.value factory and certain operators and processes. 

# Channel Factories

Channel factories are functions that create channels from values. There are 
several that will be commonly used.

**N.B.** Channel factories live in the lowercase `channel` namespace
(`channel.fromPath`, `channel.of`, etc.), not the uppercase `Channel`. Under
static typing, the uppercase `Channel` namespace is one of the legacy patterns
the strict syntax parser removes — see
[Nextflow Static Typing]({{ site.baseurl }}{% link _guides/nextflow_static_typing.md %}).

## channel.fromPath

This will create a channel emitting one more file paths. Please note that
this does not check if the file exists or not. It will simply emit the path.

This can be used simply with a single file path:

```bash
channel.fromPath("/path/to/file")
```

.fromPath also supports the use of the `*` wildcard character to emit multiple files:

```bash
channel.fromPath("/path/to/files/*.fastq")
```

This would create a channel and emit as many `Path` items as there are files
matching that pattern.

You can also use the `**` to recurse through directories.

## channel.fromFilePairs

This channel factory was made specifically for bioinformatics use cases. It is
similar to `channel.fromPath` but is designed to handle paired-end reads. The
exact definition of paired end reads is not important yet, but essentially this
function handles the case where two files are associated with a single sample and
need to be used in conjunction with each other.

Imagine we had the following files:

```bash
/path/to/files/SRRA_1.fastq
/path/to/files/SRRA_2.fastq
/path/to/files/SRRB_1.fastq
/path/to/files/SRRB_2.fastq
```

```bash
channel.fromFilePairs("/path/to/files/SRR*_{1,2}.fastq")
| view()
```

This channel would look like the following:

```bash
[SRRA, [SRRA_1.fastq, SRRA_2.fastq]]
[SRRB, [SRRB_1.fastq, SRRB_2.fastq]]
```

**N.B.** As a best practice, prefer a samplesheet over matching file pairs
directly with a glob pattern like this. A glob has no static type, can
silently pick up the wrong files if naming isn't perfectly consistent across
samples, and can't be validated before the run starts. See
[Nextflow Typed Parameters]({{ site.baseurl }}{% link _guides/nextflow_typed_params.md %})
for loading samples from a samplesheet into a typed `List<Sample>` parameter
instead.

## channel.of

channel.of creates a channel that emits the arguments provided to it 

```bash
channel.of(1..23, X, Y)
| view()
```

This would print the range from 1-23 and the string X and Y.

```bash
1
2
3
.
X
Y
```

# Operators

Operators are functions that consume, produce and manipulate channels. These 
will often be employed to arrange the channels to make them flow between different
processes. The core operators covered below — `map`, `filter`, `join`, `collect`,
and others — are all fully supported under static typing.

## view

The simplest operator will simply print the contents of a channel to stdout.

```bash
channel.of(A, B, C)
| view()
```

## Assigning a channel to a variable

Older Nextflow code used the `set` (or `tap`) operator to store the contents
of a channel in a variable:

```bash
// legacy
channel.of(A, B, C)
| set { letter_ch }
```

Under static typing, `set` and `tap` are removed by the strict syntax parser.
Assign the channel directly instead:

```bash
letter_ch = channel.of(A, B, C)
```

This is shorter, and it makes clear that `letter_ch` is just a normal variable
holding a channel — not a special construct.

## map

The map operator applies a function to each item from a channel passed to it.

```bash
channel.of(a, b, c)
| map { letter -> letter.toUpperCase() }
| view()
```

This would print the uppercase letters A, B, and C. `letter` is the name of
the parameter representing the item being processed. You can think of it as
being akin to the python equivalent i in a for loop.

```python
for i in [a, b, c]:
    print(i.upper())
```

**N.B.** Under static typing, `map` no longer discards `null` values
automatically. If your mapping closure can return `null`, chain a `filter`
afterward to remove them explicitly:

```bash
ch.map { r -> r.id }.filter { id -> id != null }
```

## splitCsv

This operator parses information from a CSV file. It will often be used together
with `map` to build a channel of tuples containing the information from the CSV file.

For example if we have the following CSV file:

```csv
sample,fastq
SRRA,/path/to/files/SRRA_1.fastq
SRRB,/path/to/files/SRRB_1.fastq
```

```bash
sample_ch = channel.fromPath("/path/to/file.csv")
    | splitCsv(header: true)
    | map { row -> tuple(row.sample, row.fastq) }
```

If we ran `view()` on this channel, it would print the following:

```bash
[SRRA, /path/to/files/SRRA_1.fastq]
[SRRB, /path/to/files/SRRB_1.fastq]
```

**N.B.** Reading a CSV by hand with `splitCsv` and `map` predates static
typing and produces a channel with no type information. Once your pipeline
uses a typed `params {}` block, prefer declaring a `List<Sample>` parameter
and letting Nextflow load and validate the samplesheet automatically instead
— see
[Nextflow Typed Parameters]({{ site.baseurl }}{% link _guides/nextflow_typed_params.md %}).
`splitCsv` is still useful for parsing CSV content that isn't a samplesheet.

## collect

This operator will collect all items into a list and emit a single item.

```bash
channel.of(A, B, C)
| collect()
| view()
```

This would print the list [A, B, C].

We will often use this to force a process to wait for all previous processes to 
complete before running. There are many occasions in bioinformatics where we will
gather or combine the output of multiple processes before running a downstream
process.

**N.B.** Under static typing, `collect` behaves like `toList`: values are
never flattened, and an empty source channel emits an empty list rather than
emitting nothing.

## join

The join operator emits the inner product of two channels when matching on a key.
We will typically need to use this when we wish to combine the output of two
processes for a single sample. The sample serves as the key in this case.

For example,

```bash
output1_ch = channel.of( [SampleA, output1], [SampleB, output1] )
output2_ch = channel.of( [SampleA, output2], [SampleB, output2] )
```

```bash
output1_ch
| join(output2_ch)
| view()
```

This would print the following:

```bash
[SampleA, output1, output2]
[SampleB, output1, output2]
```

**N.B.** Under static typing, the `by` option is required — either an integer,
to join tuples by index, or a string, to join records by field name:

```bash
left = channel.of(
    record(id: 'X', a: 1),
    record(id: 'Y', a: 2)
)
right = channel.of(
    record(id: 'X', b: 4),
    record(id: 'Y', b: 5)
)

left.join(right, by: 'id').view()

// [id: X, a: 1, b: 4]
// [id: Y, a: 2, b: 5]
```

Joining records this way also means the `failOnDuplicate` and `failOnMismatch`
options are not available — duplicate matches are emitted individually, and
unmatched records are dropped unless you pass the `remainder` option.

## Additional Operators
For more information on all operators, see the [Nextflow documentation](https://www.nextflow.io/docs/latest/operator.html). The ones covered on this page are the most commonly used in this class. `groupBy` is worth knowing about separately — it is the statically typed replacement for the legacy `groupTuple` operator.
