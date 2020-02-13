## FAQ

Q: Comparied with other circular RNA identification tools, what is the performance of CIRCexplorer2?

A: CIRCexplorer2 is based on our previous circular RNA identification tool CIRCexplorer, and it inherits all the advantages of CIRCexplorer such as high accuracy, good sensitivity and low memory consumption. and it performs well single-handedly and the combination with other circRNA identification algorithm only results in subtle improvements. [[1](http://nar.oxfordjournals.org/content/44/6/e58.abstract)][[2](http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1005420)][[3](https://www.frontiersin.org/articles/10.3389/fcell.2018.00020/full)]

Q: CIRCexplorer2 is too slow with large data. How could I improve it?

A: The rate-limiting step of CIRCexplorer2 is the alignment step. The default aligner TopHat2/TopHat-Fusion would be very slow for some cases. If you use [Annotating pipeline](../tutorial/pipeline.md), you could use [STAR](https://github.com/alexdobin/STAR) or [BWA](https://github.com/lh3/bwa) instead, and they are extremely fast. Please refer [here](../tutorial/parsing.md) for how to integrate CIRCexplorer2 with other aligners.

Q: Which types of sequencing data are supported by CIRCexplorer2? Single-read or paired-end sequencing?

A: CIRCexplorer2 now (after v2.2.0) supports paired-end reads. Please refer to [Alignment](../tutorial/alignment.md) and [Parsing](../tutorial/parsing.md). On the other hand, paired-end reads could also be converted to single reads, and then used in CIRCexplorer2. However, in this way, you should be careful in calculation RPM (Reads Per Million mapped reads) for circular RNAs, because the number of total mapped reads may have some misestimation after converted to single reads.

Q: Which treatments are required for RNA-seq?

A: If you only use the [annotating pipeline](../tutorial/pipeline.md), the [poly(A)−/ribo− RNA-seq](http://genomebiology.com/2011/12/2/R16) is recommended. If you want to enrich circular RNAs, [RNase R treatment](http://www.sciencedirect.com/science/article/pii/S109727651300590X) could be performed. RNA-seq with only rRNA depletion is acceptable, but it is not the best choice. If you want to use the [characterization pipeline](../tutorial/pipeline.md), only poly(A)−/ribo− w/o RNase R RNA-seq is acceptable. In addition, poly(A)+ RNA-seq is also required.

Q: What is the criterion to define high-expressed/high-confidence circular RNAs.

A: There is no common rule to define which circular RNAs belong to high-expressed/high-confidence circular RNAs. In practice, we use circular RNA fusion junction cutoff (**RPM≥0.1**, RPM: Reads Per Million mapped reads) to define them. This cutoff was used in our previous [Cell paper](http://www.sciencedirect.com/science/article/pii/S0092867414011118), and it works well for our current research. A new pipeline [CLEAR](https://github.com/YangLab/CLEAR) was developped to help better quantify and compare the expression of circRNAs.

Q: which aligner should I use when aligning circular RNA fusion junction reads?

A: CIRCexplorer2 now supported 5 different aligners (TopHat2/TopHat-Fusion, STAR, MapSplice, BWA, and segemehl). Each of them has its own pros and cons. We have offered some example alignment parameters of them for circular RNA fusion junction read alignment (see [tutorial](../tutorial/alignment.md) for details). However, if you want to use CIRCexplorer2 to identification novel circular RNAs or novel alternative (back-)splicing events in circular RNAs, `CIRCexplorer2 assemble` is required, and it relies on TopHat and Cufflinks. So, in this way, TopHat/TopHat-Fusion is recommended for circular RNA fusion junction read alignment.

Q: If I have aligned fastq with TopHat2 in advance and don't want to align them again with `CIRCexplorer2 align`, what should I do?

A: You should first convert `unmapped.bam` in TopHat2 output folder into fastq format (e.g. `unmapped.fq` through tools like [bedtools bamtofastq](http://bedtools.readthedocs.io/en/latest/content/tools/bamtobed.html)). Then, you could set the `--skip-tophat` option and use `unmapped.fq` as `<fastq>` in `CIRCexplorer2 align` command.

Q: Why is there the TopHat2 alignment step in `CIRCexplorer2 align`? Is this step necessary?

A: We first align reads onto genome and transcriptome using TopHat2 to reduce false positive reads aligned in the TopHat-Fusion alignment step. It is optional to skip the TopHat2 alignment step simply through set the `--skip-tophat` option in in `CIRCexplorer2 align` command.

Q: Does CIRCexplorer2 support Python3?

A: From version 2.3.0, the source codes of CIRCexplorer2 are compatible with Python3. However, because TopHat2 only supports Python2, you should be careful when you run `CIRCexplorer2 align`. It will call TopHat2 and require Python2 to be installed in your computer.
