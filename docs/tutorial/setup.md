# Installation and Setup

This part will guide you to install CIRCexplorer2 and setup all the required stuff step by step.

## Prerequisites

### Softwares and Packages

* Software
    - TopHat & TopHat-Fusion
        + [TopHat](http://ccb.jhu.edu/software/tophat/index.shtml) (>=2.0.9)
        + [TopHat-Fusion](http://ccb.jhu.edu/software/tophat/fusion_index.html) (included in TopHat)
    - [Cufflinks](http://cole-trapnell-lab.github.io/cufflinks/) (>=2.1.1)
    - [BEDTools](http://bedtools.readthedocs.org/en/latest/)
    - [UCSC Utilities](http://hgdownload.soe.ucsc.edu/admin/exe/)
        + genePredToGtf
        + gtfToGenePred
        + bedGraphToBigWig (*optional*)
        + bedToBigBed (*optional*)
    - STAR or MapSplice or BWA or segemehl (*optional*)
        + [STAR](https://github.com/alexdobin/STAR) (>=2.4.0j)
        + [MapSplice](http://www.netlab.uky.edu/p/bioinfo/MapSplice2) (>=2.1.9)
        + [BWA](http://bio-bwa.sourceforge.net) (>=0.6.2-r126)
        + [segemehl](http://www.bioinf.uni-leipzig.de/Software/segemehl) (>=0.2.0)
* Package (python 2.7 +)
    - [pysam](http://pysam.readthedocs.org/en/latest/) (>=0.8.4)
    - [pybedtools](http://daler.github.io/pybedtools/) (require [pandas](http://pandas.pydata.org) if pybedtools>=0.7.6)
    - [docopt](http://docopt.org)
    - [scipy](http://www.scipy.org) (only used in [denovo](../modules/denovo.md) module)

### RNA-seq

The [poly(A)−/ribo− RNA-seq](http://genomebiology.com/2011/12/2/R16) is recommended. If you want to enrich circular RNAs, [RNase R treatment](http://www.sciencedirect.com/science/article/pii/S109727651300590X) could be performed. RNA-seq with only rRNA depletion is acceptable, but it is not the best choice.

## Installation

### Install latest release using *pip*

CIRCexplorer2 is on [PyPI](https://pypi.python.org/pypi), so you can install via pip like most Python packages. Depending on your Python installation, this may require admin rights:
```
pip install circexplorer2
```

### Install latest release via *conda*

CIRCexplorer2 has installation recipe on [Bioconda](https://bioconda.github.io), so you can install via conda from Bioconda channel:
```
conda install circexplorer2 --channel bioconda
```

### Install latest release from source codes

Firstly, you should successfully install softwares required for fusion junction read alignment and *de novo* assembly, and add relevant pathes to your `$PATH`.

Secondly, install required python packages and CIRCexplorer2:
```
git clone https://github.com/YangLab/CIRCexplorer2.git
cd CIRCexplorer2
pip install -r requirements.txt
### install scipy according to http://www.scipy.org/install.html
python setup.py install
```

## Setup

CIRCexplorer2 requires the gene annotation file and the reference genome sequence file to annotate circular RNAs. The gene annotation file should be in the format of [Gene Predictions and RefSeq Genes with Gene Names](https://genome.ucsc.edu/FAQ/FAQformat.html#format9), and the reference genome sequence file contains all the genome sequences with respective chromosome ID. All the chromosome IDs in the gene annotation file must be included in the reference genome sequence file, otherwise the inconsistence between these two files may cause undetectable errors when running CIRCexplorer2.

*Format of 'Gene Predictions and RefSeq Genes with Gene Names':*

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

We could use `fetch_ucsc.py` script to download all the essential gene annotation and reference genome sequence files for circular RNA identification.

`fetch_ucsc.py` is a small python script included in CIRCexplorer2 to help users to prepare relevant stuff for CIRCexplorer2. It could download and format the gene annotation file (RefSeq, KnownGenes or Ensembl) and the reference genome sequence file for two species (Human: hg19, hg38; Mouse: mm9, mm10). All these files will be fetched from the latest release of [UCSC](http://hgdownload.soe.ucsc.edu/downloads.html).

Command line of `fetch_ucsc.py`:
```
fetch_ucsc.py hg19/hg38/mm9/mm10 ref/kg/ens/fa out
```

Examples:

1 Download human RefSeq gene annotation file
```
fetch_ucsc.py hg19 ref hg19_ref.txt
```

2 Download human KnownGenes gene annotation file
```
fetch_ucsc.py hg19 kg hg19_kg.txt
```

3 Download human Ensembl gene annotation file
```
fetch_ucsc.py hg19 ens hg19_ens.txt
```

4 Download human reference genome sequence file
```
fetch_ucsc.py hg19 fa hg19.fa
```

5 Convert gene annotation file to GTF format (require [genePredToGtf](http://hgdownload.soe.ucsc.edu/admin/exe/))
```
cut -f2-11 hg19_ref.txt|genePredToGtf file stdin hg19_ref.gtf
# or
cut -f2-11 hg19_kg.txt|genePredToGtf file stdin hg19_kg.gtf
# or
cut -f2-11 hg19_ens.txt|genePredToGtf file stdin hg19_ens.gtf
```

###Notes:

1 hg38 and mm10 only have RefSeq and KnownGenes (GENCODE) gene annotations, and does not support Ensembl gene annotations.

2 You could select one gene annotation file among `hg19_ref.txt`, `hg19_kg.txt` or `hg19_ens.txt` at your choice. In addition, you could concatenate all these gene annotation file as a single file for CIRCexplorer2.
```
cat hg19_ref.txt hg19_kg.txt hg19_ens.txt > hg19_ref_all.txt
```

3 CIRCexploer2 TopHat2/TopHat-Fusion pipeline requires [Bowtie](http://bowtie-bio.sourceforge.net/index.shtml) and [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml) index files for reference genome. You could use `bowtie-build` and `bowtie2-build` to index relevant genome. Or you could use `CIRCexplorer2 align` to automatically index the genome file (See [Alignment](../tutorial/alignment.md)).
```
# index genome for Bowtie
bowtie-build hg19.fa bowtie1_index
# index genome for Bowtie2
bowtie2-build hg19.fa bowtie2_index
```

4 If you analyze circular RNAs in mouse, you should download mouse relevant files (use mm10 for example).
```
# mouse RefSeq gene annotation file
fetch_ucsc.py mm10 ref mm10_ref.txt
# mouse KnownGenes gene annotation file
fetch_ucsc.py mm10 kg mm10_kg.txt
# mouse Ensembl gene annotation file
fetch_ucsc.py mm10 ens mm10_ens.txt
# mouse reference genome sequence file
fetch_ucsc.py mm10 fa mm10.fa
```
