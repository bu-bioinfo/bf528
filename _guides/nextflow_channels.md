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

## Channel.fromPath

This will create a channel emitting one more file paths. Please note that
this does not check if the file exists or not. It will simply emit the path.

This can be used simply with a single file path:

```bash
Channel.fromPath("/path/to/file")
```

.fromPath also supports the use of the `*` wildcard character to emit multiple files:

```bash
Channel.fromPath("/path/to/files/*.fastq")
```

This would create a channel and emit as many `Path` items as there are files
matching that pattern.

You can also use the `**` to recurse through directories.

## Channel.fromFilePairs

This channel factory was made specifically for bioinformatics use cases. It is
similar to `Channel.fromPath` but is designed to handle paired-end reads. The
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
Channel.fromFilePairs("/path/to/files/SRR*_{1,2}.fastq")
| view()
```

This channel would look like the following:

```bash
[SRRA, [SRRA_1.fastq, SRRA_2.fastq]]
[SRRB, [SRRB_1.fastq, SRRB_2.fastq]]
```

## Channel.of

Channel.of creates a channel that emits the arguments provided to it 

```bash
Channel.of(1..23, X, Y)
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
processes. 

## view

The simplest operator will simply print the contents of a channel to stdout.

```bash
Channel.of(A, B, C)
| view()
```

## set  

The set operator will store the contents of a channel in a variable.

```bash
Channel.of(A, B, C)
| set { letter_ch }
```

This will allow you to refer to the contents of this channel by the variable
`letter_ch`.

## map

The map operator applies a function to each item from a channel passed to it.

```bash
Channel.of(a, b, c)
| map { it -> it.toUpperCase() }
| view()
```

This would print the uppercase letters A, B, and C. The `it` is a placeholder for
the item being processed. You can think of it as being akin to the python equivalent
i in a for loop.

```python
for i in [a, b, c]:
    print(i.upper())
```

## splitCsv

This operator parses information from a CSV file. It will often be used together
with `map` and `set` to create a channel of tuples containing the information
from the CSV file.

For example if we have the following CSV file:

```csv
sample,fastq
SRRA,/path/to/files/SRRA_1.fastq
SRRB,/path/to/files/SRRB_1.fastq
```

```bash
Channel.fromPath("/path/to/file.csv")
| splitCsv(header: true)
| map { row -> tuple(row.sample, row.fastq) }
| set { sample_ch }
```

If we ran `view()` on this channel, it would print the following:

```bash
[SRRA, /path/to/files/SRRA_1.fastq]
[SRRB, /path/to/files/SRRB_1.fastq]
```

## collect

This operator will collect all items into a list and emit a single item.

```bash
Channel.of(A, B, C)
| collect()
| view()
```

This would print the list [A, B, C].

We will often use this to force a process to wait for all previous processes to 
complete before running. There are many occasions in bioinformatics where we will
gather or combine the output of multiple processes before running a downstream
process.

## join

The join operator emits the inner product of two channels when matching on a key.
We will typically need to use this when we wish to combine the output of two
processes for a single sample. The sample serves as the key in this case.

For example,

```bash
Channel.of ( [SampleA, output1], [SampleB, output1])
| set { output1_ch }

Channel.of ( [SampleA, output2], [SampleB, output2])
| set { output2_ch }
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
## Additional Operators
For more information on all operators, see the [Nextflow documentation](https://www.nextflow.io/docs/latest/operator.html). The ones covered on this page are the most commonly used in this class. 
