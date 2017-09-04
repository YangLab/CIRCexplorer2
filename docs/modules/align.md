# *align*

`CIRCexplorer2 align` aligns fusion junction reads with TopHat2/TopHat-Fusion combined pipeline, followed by fetching non-colinear fusion junction reads.

## Usage and option summary

### Usage:

```
CIRCexplorer2 align [options] -G GTF (-g GENOME | -i INDEX1 -j INDEX2 | -i INDEX1 | -j INDEX1) -f FQ
```

### Options:

```
-h --help                      Show help message.
-v --version                   Show version.
-G GTF --gtf=GTF               Annotation GTF file.
-g GENOME --genome=GENOME      Genome fasta file.
-i INDEX1 --bowtie1=INDEX1     Index files for Bowtie1 (used for TopHat-Fusion).
-j INDEX2 --bowtie2=INDEX2     Index files for Bowtie2 (used for TopHat2).
-p THREAD --thread=THREAD      Running threads. [default: 10]
-f FQ --fastq=FQ               Input file.
-o OUT --output=OUT            Output directory. [default: alignment]
-b JUNC --bed=JUNC             Output file. [default: back_spliced_junction.bed]
--bw                           Create BigWig file.
--scale                        Scale to HPB.
--skip-tophat                  Skip TopHat mapping.
--skip-tophat-fusion           Skip TopHat-Fusion mapping.
```

## Notes about options

1. When offering reference genome, you could use genome sequence file (`-g GENOME`) or genome index files of bowtie1 and/or bowtie2 (`-i INDEX1` and/or `-j INDEX2`).
2. If you set `--bw` option, [BigWig](http://genome.ucsc.edu/FAQ/FAQformat.html#format6.1) file of TopHat2 alignment would be created automatically for visualization. It will not consider strand information of read alignment.
3. If you set `--scale` option, expression levels (for BigWig file) would be scaled to HPB (Hits per billion-mapped-bases
). More information about HPB could be found in [this paper](http://bmcgenomics.biomedcentral.com/articles/10.1186/1471-2164-14-206).
4. If you set `--skip-tophat`, TopHat2 alignment would be skipped. It is useful for some specific conditions, please see [FAQ](../about/faq.md) for details.
5. If you set `--skip-tophat-fusion`, TopHat-Fusion alignment would be skipped. It is useful for poly(A)+ RNA-seq.
6. You could offer multiple fastq files (or compressed files) separated or comma.
7. Only single-read RNA-seq is supported. It is recommended to convert paired-end RNA-seq to single-read RNA-seq before alignment.
8. It will overwrite the output directory and output file automatically, so please be careful when setting the path of output directory.
9. Because Tophat only supports Python2, you should ensure Python2 has been installed in your computer, even if you were running Python3 version of CIRCexplorer2.

## Output

`CIRCexplorer2 align` will create a folder(`alignment`) and a file(`back_spliced_junction.bed`). The `back_spliced_junction.bed` would be used by other modules of CIRCexplorer2 to further annotate and characterize circular RNAs.

```
back_spliced_junction.bed
alignment
├── bowtie1_index/
├── bowtie2_index/
├── tophat/
├── tophat_fusion/
├── tophat.log
└── tophat_fusion.log
```

* `bowtie1_index`: Index file folder for Bowtie1.
* `bowtie2_index`: Index file folder for Bowtie2.
* `tophat`: TopHat2 alignment folder.
* `tophat_fusion`: TopHat-Fusion alignment folder.
* `back_spliced_junction.bed`: Fusion junction information file.
* `tophat.log`: Log file of TopHat2 alignment.
* `tophat_fusion.log`: Log file of TopHat-Fusion alignment.

*Format of `back_spliced_junction.bed`:*

| Field       | Description              |
| :---------- | :----------------------- |
| chrom       | Chromosome               |
| start       | Start of fusion junction |
| end         | End of fusion junction   |
| name        | Fusion id/Junction reads |
| score       | No meaning               |
| strand      | No meaning               |
