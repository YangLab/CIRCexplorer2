# *denovo*

`CIRCexplorer2 denovo` parses circular RNA *de novo* assembly results to identify novel circRNAs and characterize various of alternative splicing events.

## Usage and option summary

### Usage:

```
CIRCexplorer2 denovo [options] -r REF -g GENOME -b JUNC [-d CUFF] [-o OUT]
```

### Options:

```
-h --help                      Show help message.
--version                      Show version.
-r REF --ref=REF               Gene annotation.
--as=AS                        Detect alternative splicing and output.
--as-type=AS_TYPE              Only check certain type (CE/RI/ASS) of AS events.
--abs=ABS                      Detect alternative back-splicing and output.
-b JUNC --bed=JUNC             Input file.
-d CUFF --cuff=CUFF            assemble folder output by CIRCexplorer2 assemble. [default: '']
-m TOPHAT --tophat=TOPHAT      TopHat mapping folder.
-n PLUS_OUT --pAplus=PLUS_OUT  TopHat mapping directory for p(A)+ RNA-seq.
-o OUT --output=OUT            Output Folder. [default: denovo]
-g GENOME --genome=GENOME      Genome FASTA file.
--no-fix                       No-fix mode (useful for species with poor gene annotations).
--rpkm                         Calculate RPKM for cassette exons.
```

## Notes about options

1. If the `--cuff` is not set, `CIRCexplorer2 denovo` will only use existing gene annotations to parse alternative splicing with setting `--as` option. This way is not recommended, so please run `CIRCexplorer2 assemble` before `CIRCexplorer2 denovo`.
2. If you set `--abs` option, `CIRCexplorer2 denovo` will characteriza the alternative back-splicing of circular RNAs.
3. If you set `--as` option, it will characterize the alternative splicing of circular RNAs, including 'cassette exons', 'retained introns', 'A5SS' and 'A3SS'. In this mode, you should also offer the path of TopHat mapping directory for p(A)-/p(A)+ RNA-seq via `-m`/`-n` option. By default, after setting `--as` option, it will check all types of alternative splicing events. You could also indicate one type of alternative splicing events through the `--as-type` option ('CE': 'cassette exons', 'RI': 'retained introns', 'ASS': 'A5SS' and 'A3SS').
4. If you set `--no-fix` options, [realignment step of fusion junction reads](http://www.sciencedirect.com/science/article/pii/S0092867414011118) will be skipped. It is useful for species with poor gene annotations, but the accuracy of circular RNA prediction would decrease.
5. If `--rpkm` option is set, RPKM of cassette exons would be calculated.

## Input

The input files are similar to those in `CIRCexplorer2 annotate` command. See [Annotate](../modules/annotate.md) for more details.

## Output

`CIRCexplorer2 denovo` will create one `denovo` folder under the `<circ_dir>` folder.

```
denovo
├── combined_ref.txt
├── circularRNA_full.txt
├── annotated_circ.txt
└── novel_circ.txt
abs
├── a5bs.txt
└── a3bs.txt
as
├── all_exon_info.txt
├── all_intron_info.txt
├── all_A5SS_info.txt
└── all_A3SS_info.txt
```

* `combined_ref.txt`: combined gene annotation file (*de novo* assembled gene annotations and existing gene annotations).
* `circularRNA_full.txt`: Circular RNA annotation file. (same as relevant file in [Annotate](../modules/annotate.md)))
* `annotated_circ.txt`: CircRNAs with annotated back-splice sites.
* `a5bs.txt`: Alternative 5' back-splice site information file.
* `a3bs.txt`: Alternative 3' back-splice site information file.
* `novel_circ.txt`: CircRNAs with one or two novel back-splice site(s).
* `all_exon_info.txt`: Cassette exon information file.
* `all_intron_info.txt`: Retained intron information file.
* `all_A5SS_info.txt`: Alternative 5' splice site information file.
* `all_A3SS_info.txt`: Alternative 3' splice site information file.

*Format of `annotated_circ.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of circular RNA                 |
| end         | End of circular RNA                   |
| name        | Circular RNA/Junction reads           |
| score       | Flag of fusion junction realignment   |
| strand      | + or - for strand                     |
| geneName    | Name of gene                          |

*Format of `a5bs.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of circular RNA                 |
| end         | End of circular RNA                   |
| strand      | Strand of circular RNA                |
| absSite     | Alternative back-splice site          |
| absCount    | back-spliced read counts              |
| PCU         | Percent Circularized-site Usage       |

*Format of `a3bs.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of circular RNA                 |
| end         | End of circular RNA                   |
| strand      | Strand of circular RNA                |
| absSite     | Alternative back-splice site          |
| absCount    | back-spliced read counts              |
| PCU         | Percent Circularized-site Usage       |

*Format of `novel_circ.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of circular RNA                 |
| end         | End of circular RNA                   |
| name        | Circular RNA/Junction reads           |
| score       | Flag of fusion junction realignment   |
| strand      | + or - for strand                     |
| leftLabel   | Label of circRNA start                |
| rightLabel  | Label of circRNA end                  |

*Format of `all_exon_info.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of cassette exon                |
| end         | End of cassette exon                  |
| name        | Exon label                            |
| score       | No meaning                            |
| strand      | + or - for strand                     |
| geneName    | Name of gene                          |
| isoformName | Name of isoform                       |
| read        | CircRNA fusion junction reads         |
| psiCirc     | PSI in circular RNAs                  |
| psiLinear   | PSI in linear RNAs                    |
| pValue1     | P value (circular RNAs vs linear RNAs)|
| pValue2     | P value (linear RNAs vs circular RNAs)|
| inCirc      | Inclusion reads in circular RNAs      |
| exCirc      | Exclusion reads in circular RNAs      |
| inLinear    | Inclusion reads in linear RNAs        |
| exLinear    | Exclusion reads in linear RNAs        |
| rpkmCirc    | RPKM of cassette exon in circular RNAs|
| rpkmLinear  | RPKM of cassette exon in linear RNAs  |

*Format of `all_intron_info.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of retained intron              |
| end         | End of retained intron                |
| name        | Intron label                          |
| score       | No meaning                            |
| strand      | + or - for strand                     |
| geneName    | Name of gene                          |
| isoformName | Name of isoform                       |
| read        | CircRNA fusion junction reads         |
| pirCirc     | PIR in circular RNAs                  |
| pirLinear   | PIR in linear RNAs                    |
| pValue1     | P value (circular RNAs vs linear RNAs)|
| pValue2     | P value (linear RNAs vs circular RNAs)|
| riCirc      | Retained intron reads in circular RNAs|
| juncCirc    | Junction reads in circular RNAs       |
| intronCirc  | Intron reads in circular RNAs         |
| riLinear    | Retained intron reads in linear RNAs  |
| juncLinear  | Junction reads in linear RNAs         |
| intronLinear| Intron reads in linear RNAs           |

*Format of `all_A5SS_info.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of circular RNA                 |
| end         | End of circular RNA                   |
| strand      | + or - for strand                     |
| readCirc    | 5' splice reads in circular RNAs      |
| totalCirc   | Total splice reads in circular RNAs   |
| psuCirc     | PSU in circular RNAs                  |
| readLinear  | 5' splice reads in linear RNAs        |
| totalLinear | Total splice reads in linear RNAs     |
| psuLinear   | PSU in linear RNAs                    |

*Format of `all_A3SS_info.txt`:*

| Field       | Description                           |
| :---------- | :------------------------------------ |
| chrom       | Chromosome                            |
| start       | Start of circular RNA                 |
| end         | End of circular RNA                   |
| strand      | + or - for strand                     |
| readCirc    | 3' splice reads in circular RNAs      |
| totalCirc   | Total splice reads in circular RNAs   |
| psuCirc     | PSU in circular RNAs                  |
| readLinear  | 3' splice reads in linear RNAs        |
| totalLinear | Total splice reads in linear RNAs     |
| psuLinear   | PSU in linear RNAs                    |
