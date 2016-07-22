# *annotate*

`CIRCexplorer2 annotate` integrates [CIRCexplorer](http://yanglab.github.io/CIRCexplorer/) into CIRCexplorer2. It annotates back-splicing junction reads with user provided gene annotations.

## Usage and option summary

### Usage:

```
CIRCexplorer2 annotate [options] -r REF -g GENOME <circ_dir>
```

### Options:

```
-h --help                      Show help message.
--version                      Show version.
-r REF --ref=REF               Gene annotation.
-g GENOME --genome=GENOME      Genome FASTA file.
--no-fix                       No-fix mode (useful for species with poor gene annotations).
--low-confidence               Extract low confidence circRNAs.
```

## Notes about options

1. It would randomly report one circular RNA isoform for each back-splicing junction based on existed gene annotations.
2. If you set `--no-fix` options, [realignment step of fusion junction reads](http://www.sciencedirect.com/science/article/pii/S0092867414011118) will be skipped. It is useful for species with poor gene annotations, but the accuracy of circular RNA prediction would decrease.
3. `CIRCexplorer2 annotate` extracts fusion junction reads exactly matching the boundaries of exons of the same isoform by default. If you set the `--low-confidence`, it will also extract fusion junction reads matching the boundaries of exons of the different isofoms of the same gene, and output them in `low_circ_fusion.txt`.

## Output

`CIRCexplorer2 annotate` will create one `annotate` folder under the `<circ_dir>` folder. The `circ_fusion.txt` contains the final circular RNA annotation information.

```
annotate
├── annotated_fusion.txt
├── circ_fusion.txt
└── low_circ_fusion.txt (if set the '--low-confidence' option)
```

* `annotated_fusion.txt`: Annotated fusion junction information file.
* `circ_fusion.txt`: Circular RNA annotation file.

*Format of `circ_fusion.txt`:*

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

*Format of `low_circ_fusion.txt`:*

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
