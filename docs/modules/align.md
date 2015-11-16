# *align*

`CIRCexplorer2 align` aligns fusion junction reads with TopHat2/TopHat-Fusion combined pipeline, followed by fetching non-colinear fusion junction reads.

## Usage and option summary

### Usage:

```bash
CIRCexplorer2 align [options] -G GTF (-g GENOME | -i INDEX1 -j INDEX2) <fastq>...
```

### Options:

```bash
-h --help                      Show help message.
-v --version                   Show version.
-G GTF --gtf=GTF               Annotation GTF file.
-g GENOME --genome=GENOME      Genome fasta file.
-i INDEX1 --bowtie1=INDEX1     Index files for Bowtie1.
-j INDEX2 --bowtie2=INDEX2     Index files for Bowtie2.
-p THREAD --thread=THREAD      Running threads. [default: 10]
-o OUT --output=OUT            Output directory. [default: circ_out]
--bw                           Create BigWig file.
--scale                        Scale to HPB.
--no-tophat-fusion             No TopHat-Fusion mapping.
```
