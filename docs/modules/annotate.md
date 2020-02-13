# *annotate*

`CIRCexplorer2 annotate` integrates [CIRCexplorer](http://yanglab.github.io/CIRCexplorer/) into CIRCexplorer2. It annotates back-splicing junction reads with user provided gene annotations.

## Usage and option summary

### Usage:

```
CIRCexplorer2 annotate [options] -r REF -g GENOME -b JUNC [-o OUT]
```

### Options:

```
-h --help                      Show help message.
--version                      Show version.
-r REF --ref=REF               Gene annotation.
-g GENOME --genome=GENOME      Genome FASTA file.
-b JUNC --bed=JUNC             Input file.
-o OUT --output=OUT            Output file. [default: circularRNA_known.txt]
--no-fix                       No-fix mode (useful for species with poor gene annotations).
--low-confidence               Extract low confidence circRNAs.
```

## Notes about options

1. It would randomly report one circular RNA isoform for each back-splicing junction based on existed gene annotations.
2. If you set `--no-fix` options, [realignment step of fusion junction reads](http://www.sciencedirect.com/science/article/pii/S0092867414011118) will be skipped. It is useful for species with poor gene annotations, but the accuracy of circular RNA prediction would decrease.
3. `CIRCexplorer2 annotate` extracts fusion junction reads exactly matching the boundaries of exons of the same isoform by default. If you set the `--low-confidence`, it will also extract fusion junction reads matching the boundaries of exons of the different isofoms of the same gene, and output them in `low_conf_circularRNA_known.txt`.

## Input

`CIRCexplorer2 annotate` needs a gene annotation file, a reference genome sequence file and a `back_spliced_junction.bed` created by `CIRCexplorer2 parse` or `CIRCexplorer2 align`.

```
back_spliced_junction.bed
```

### Format of gene annotation file:

The file is in the format of [Gene Predictions and RefSeq Genes with Gene Names](https://genome.ucsc.edu/FAQ/FAQformat.html#format9) below. (See [example file](https://raw.githubusercontent.com/YangLab/CIRCexplorer2/master/test/data/ref.txt))

| Field       | Description                   |
| :---------: | :---------------------------- |
| geneName    | Name of gene                  |
| isoformName | Name of isoform               |
| chrom       | Reference sequence            |
| strand      | + or - for strand             |
| txStart     | Transcription start position  |
| txEnd       | Transcription end position    |
| cdsStart    | Coding region start           |
| cdsEnd      | Coding region end             |
| exonCount   | Number of exons               |
| exonStarts  | Exon start positions          |
| exonEnds    | Exon end positions            |


## Output

`CIRCexplorer2 annotate` will create a `circularRNA_known.txt` file by default. The `circularRNA_known.txt` contains the final circular RNA annotation information.

```
circularRNA_known.txt
low_conf_circularRNA_known.txt
```

* `circularRNA_known.txt`: Circular RNA annotation file.

*Format of `circularRNA_known.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of circular RNA                 |
| end         | End of circular RNA                   |
| name        | Circular RNA/Junction reads           |
| score       | Flag of fusion junction realignment   |
| strand      | + or - for strand                     |
| thickStart  | No meaning                            |
| thickEnd    | No meaning                            |
| itemRgb     | 0,0,0                                 |
| exonCount   | Number of exons                       |
| exonSizes   | Exon sizes                            |
| exonOffsets | Exon offsets                          |
| readNumber  | Number of junction reads              |
| circType    | Type of circular RNA                  |
| geneName    | Name of gene                          |
| isoformName | Name of isoform                       |
| index       | Index of exon or intron               |
| flankIntron | Left intron/Right intron              |

*Format of `low_conf_circularRNA_known.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of circular RNA                 |
| end         | End of circular RNA                   |
| name        | Circular RNA/Junction reads           |
| score       | Flag of fusion junction realignment   |
| strand      | + or - for strand                     |
| leftInfo    | Gene:Isoform:Index of left exon       |
| rightInfo   | Gene:Isoform:Index of right exon      |
