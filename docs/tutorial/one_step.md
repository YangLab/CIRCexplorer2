# Run CIRCexplorer2 via One Command

CIRCexplorer2 contains 5 modules and offers flexibility for multiple circular RNA analysis tasks. However, It would confuse many people who are not very familiar with CIRCexplorer2 and blocks people from making good use of it. As a result, we wrote the `fast_circ.py` script to integrate different combinations of modules to complete different tasks.

## Usage and option summary

### Usage:

```
fast_circ.py parse -r REF -g GENOME -t ALIGNER [--pe] [-o OUT] <fusion>
fast_circ.py annotate -r REF -g GENOME -G GTF [-p THREAD] [-o OUT] -f FQ
fast_circ.py denovo -r REF -g GENOME -G GTF [-n PLUS_OUT] [-p THREAD] [-o OUT] -f FQ
```

### Options:

```
-h --help                      Show help message.
-r REF --ref=REF               Gene annotation.
-g GENOME --genome=GENOME      Genome FASTA file.
-G GTF --gtf=GTF               Annotation GTF file.
-t ALIGNER                     Aligner (TopHat-Fusion, STAR, MapSplice, BWA, segemehl).
--pe                           Parse paired-end alignment file (only for TopHat-Fusion).
-f FQ --fastq=FQ               Input file.
-n PLUS_OUT --pAplus=PLUS_OUT  TopHat mapping directory for p(A)+ RNA-seq.
-p THREAD --thread=THREAD      Running threads. [default: 10]
-o OUT --output=OUT            Output directory. [default: .]
```

## How to use it?

`fast_circ.py` could perform all the circular RNA analysis pipelines mentioned in [Pipelines](../tutorial/pipeline.md).

### Annotating pipeline

* If you have mapped RNA-seq reads using one of listed aligners (TopHat2/TopHat-Fusion, STAR, segemehl and MapSplice, see [here](../tutorial/alignment.md) for recommended parameters of different aligners), you should use `fast_circ.py parse` with gene annotation file (via `-r`) and reference genome sequence file (via `-g`). Meanwhile, you should also indicate its aligner (via `-t`) and whether reads are paired-end or not (via `--pe`). Last but not least, the fusion junction file (`<fusion>`) should be correct. This command is just like [CIRCexplorer](https://github.com/YangLab/CIRCexplorer). See [here](../tutorial/setup.md) for the format of gene annotation file and [there](../tutorial/parsing.md) for the information about how to parse different aligners.
* If you only have raw RNA-seq reads, you could use `fast_circ.py annotate` to align RNA-seq reads with TopHat2/TopHat-Fusion. You should offer it gene annotation file (via `-r`), gene annotation GTF file (via `-G`), reference genome sequence file (via `-g`) and the raw read fastq file(via `-f`). See [here](../tutorial/setup.md) for the format of gene annotation file.

### Characterization pipeline

* `fast_circ.py denovo` would align raw RNA-seq reads with TopHat2/TopHat-Fusion, and de novo assemble circular RNA transcripts with Cufflinks, and last extract alternative (back-)splicing events. Some options are same with `fast_circ.py annotate`.

* If you offer a TopHat mapping directory for p(A)+ RNA-seq (via `-n`), `fast_circ.py denovo` will fetch all the alternative splicing events. Otherwise, It only fetches alternative back-splicing events. See [here](../modules/denovo.md) for more details.
