# Alignment for Circular RNA Fusion Junction Reads

CIRCexplorer2 supports TopHat2/TopHat-Fusion and other aligners (STAR, segemehl, BWA and MapSplice). Although different aligners showed slightly different in circular RNA identification, TopHat2/TopHat-Fusion has a perfect match with Cufflinks. As a result, TopHat2/TopHat-Fusion is recommended in alignment step, especially for [circular RNA characterization pipeline](../tutorial/pipeline.md).


## TopHat2/TopHat-Fusion

Because TopHat2 needs gene annotation file for better alignment, you could select one GTF file from `hg19_ref.gtf`, `hg19_kg.gtf` and `hg19_ens.gtf`. In addition, TopHat2 needs genome index files for bowtie2, and TopHat-Fusion require indices for bowtie1, so you could index the genome sequence in advance or let `CIRCexplorer2 align` to do it from scratch. (See [Setup](../tutorial/setup.md))

* From index files (`bowtie1_index` is the prefix for bowtie1 index files, and `bowtie2_index` is the prefix for bowtie2 index files):
```
CIRCexplorer2 align -G hg19_kg.gtf -i bowtie1_index -j bowtie2_index RNA_seq.fastq > CIRCexplorer2_align.log
```

* Or from genome sequence:
```
CIRCexplorer2 align -G hg19_kg.gtf -g hg19.fa RNA_seq.fastq > CIRCexplorer2_align.log
```

### Note

1. Because Cufflinks is well compatible with TopHat2/TopHat-Fusion, it is recommended to use TopHat2/TopHat-Fusion alignment for [characterization pipeline](../tutorial/pipeline.md).
2. `CIRCexplorer2 align` will create a directory `circ_out` by default, and the BED file `fusion_junction.bed` under this directory is required for following analysis. You could also check `tophat.log` and `tophat_fusion.log` file for detailed logs of Tophat2 and TopHat-Fusion alignment.
3. See [Align](../modules/align.md) for detailed information about `CIRCexplorer2 align`.
4. If you have already had alignment results with TopHat2/TopHat-Fusion, you could use `CIRCexplorer2 parse` to convert their results compatible with CIRCexplorer2. For the alignment parameters of TopHat2/TopHat-Fusion, you could refer to [CIRCexplorer manual](https://github.com/YangLab/CIRCexplorer#tophat--tophat-fusion).
```
CIRCexplorer2 parse -t TopHat-Fusion tophat_fusion/accepted_hits.bam > CIRCexplorer2_parse.log
```

## Other aligners

1 Align sequencing reads to the reference genome. Commands for different aligners for detecting fusion junction reads are listed below, and you could modify them according to your different requirements.

* STAR (See [STAR manual](https://github.com/alexdobin/STAR/blob/master/doc/STARmanual.pdf) for more information)
```
STAR --chimSegmentMin 10 --runThreadN 10 --genomeDir hg19_STAR_index --readFilesIn RNA_seq.fastq
```

* MapSplice (See [MapSplice](http://www.netlab.uky.edu/p/bioinfo/MapSplice2UserGuide) for more information)
```
mapsplice.py -p 10 -k 1 --non-canonical --fusion-non-canonical --min-fusion-distance 200 -c hg19_dir -x bowtie1_index --gene-gtf hg19_kg.gtf -1 RNA_seq.fastq
```

* BWA (See [BWA](http://bio-bwa.sourceforge.net/bwa.shtml) for more information)
```
bwa mem -T 19 -t 10 hg19_bwa_index RNA_seq.fastq > RNA_seq_bwa.sam
```

* segemehl (See [segemehl manual](http://www.bioinf.uni-leipzig.de/Software/segemehl/segemehl_manual_0_1_7.pdf) for more information)
```
segemehl.x -q RNA_seq.fastq -d hg19.fa -i hg19_segemehl.idx -S -M 1 -t 10 -o RNA_seq.sam
testrealign.x -d hg19.fa -q RNA_seq.sam -n
```

2 Use `CIRCexplorer2 parse` to parse and convert fusion junction information.

* STAR
```
CIRCexplorer2 parse -t STAR Chimeric.out.junction > CIRCexplorer2_parse.log
```

* MapSplice
```
CIRCexplorer2 parse -t MapSplice mapsplice_out/fusions_raw.txt > CIRCexplorer2_parse.log
```

* BWA
```
CIRCexplorer2 parse -t BWA RNA_seq_bwa.sam > CIRCexplorer2_parse.log
```

* segemehl
```
CIRCexplorer2 parse -t segemehl splicesites.bed > CIRCexplorer2_parse.log
```

### Note

1. You could align raw sequencing reads or unmapped reads from TopHat2 alignment (`circ_out/tophat/unmapped.fastq`).
2. `CIRCexplorer2 parse` will create a directory `circ_out` by default, and the BED file `fusion_junction.bed` under this directory is required for following analysis.
3. See [Parse](../modules/parse.md) for detailed information about `CIRCexplorer2 parse`.
