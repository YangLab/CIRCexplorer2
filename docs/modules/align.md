# *align*

`CIRCexplorer2 align` aligns fusion junction reads with TopHat2/TopHat-Fusion combined pipeline, followed by fetching non-colinear fusion junction reads.

## Usage and option summary

### Usage:

```
CIRCexplorer2 align [options] -G GTF (-g GENOME | -i INDEX1 -j INDEX2 | -i INDEX1 | -j INDEX1) <fastq>...
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
-o OUT --output=OUT            Output directory. [default: circ_out]
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
6. You could offer multiple fastq files (or compressed files) separated by spaces or comma.
7. Only single-end RNA-seq is supported. It is recommended to convert paired-end RNA-seq to single-end RNA-seq before alignment.
8. It will overwrite the output directory automatically, so please be careful when setting the path of output directory.

## Output

`CIRCexplorer2 align` will create multiple folders and log files under `circ_out` (you could change output folder using `-o`) folder. The `fusion_junction.bed` would be used by other modules of CIRCexplorer2 to further annotate and characterize circular RNAs.

```
circ_out
├── bowtie1_index/
├── bowtie2_index/
├── tophat/
├── tophat_fusion/
├── fusion_junction.bed
├── tophat.log
└── tophat_fusion.log
```

* `bowtie1_index`: Index file folder for Bowtie1.
* `bowtie2_index`: Index file folder for Bowtie2.
* `tophat`: TopHat2 alignment folder.
* `tophat_fusion`: TopHat-Fusion alignment folder.
* `fusion_junction.bed`: Fusion junction information file.
* `tophat.log`: Log file of TopHat2 alignment.
* `tophat_fusion.log`: Log file of TopHat-Fusion alignment.

*Format of `fusion_junction.bed`:*

| Field       | Description              |
| :---------- | :----------------------- |
| chrom       | Chromosome               |
| start       | Start of fusion junction |
| end         | End of fusion junction   |
| name        | Fusion id/Junction reads |
| score       | No meaning               |
| strand      | No meaning               |
