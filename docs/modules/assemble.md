# *assemble*

`CIRCexplorer2 assemble` carries out *de novo* assembly for circular RNA based on RABT method.

## Usage and option summary

### Usage:

```
CIRCexplorer2 assemble [options] -r REF <circ_dir>
```

### Options:

```
-h --help                      Show help message.
-v --version                   Show version.
-r REF --ref=REF               Gene annotation file.
-p THREAD --thread=THREAD      Running threads. [default: 10]
--bb                           Convert assembly results to BigBed.
--tophat-dir=TOPHAT_DIR        TopHat mapping directory.
--chrom-size=CHROM_SIZE        Chrom size file for converting to BigBed.
--remove-rRNA                  Ignore rRNA during assembling (only for human hg19).
--max-bundle-frags=FRAGMENTS   Cufflinks --max-bundle-frags option.
```

## Notes about options

1. `CIRCexplorer2 assemble` require to use alignment results of TopHat2 to *de novo* assemble circular RNA transcripts. So if the TopHat2 result folder is not under `<circ_dir>`, you could specify its path using `--tophat-dir`.
2. `CIRCexplorer2 assemble` will search for the chrom size file in TopHat2 result folder, and you could also specify its path using `--chrom-size`. If you have used `CIRCexplorer2 align` to align RNA-seq data, the chrom size file would be existed in the TopHat2 result folder.
3. Assembly for rRNA would be very time-consuming. If you set `--remove-rRNA` option, it would skip assembly for rRNA. To be noted, this option is only suitable for **hg19**. If the assembly step is still very slow, you could set `--max-bundle-frags` with a small number. Please see [Cufflinks protocol](http://www.nature.com/nprot/journal/v7/n3/fig_tab/nprot.2012.016_T2.html) for more details about `--max-bundle-frags` option.
4. If you set `--bb` option, the BigBed file of assembled transcripts would be created.

## Output

`CIRCexplorer2 assemble` will create one `cufflinks` folder under the `<circ_dir>` folder. It will also create `cufflinks.log` under `<circ_dir>` folder. The `transcripts_ref.txt` would be used to do alternative splicing analysis for circular RNAs, and it has the same format with [refFlat format](http://genome.ucsc.edu/FAQ/FAQformat.html#format9).

```
cufflinks
├── filtered_junction.gtf
├── filtered_junction.txt
├── genes.fpkm_tracking
├── isoforms.fpkm_tracking
├── skipped.gtf
├── transcripts.gtf
├── transcripts.txt
├── transcripts_ref.txt
├── transcripts_ref.bed
├── transcripts_ref_sorted.bed
└── transcripts_ref_sorted.bb
```

* `filtered_junction.gtf` and `filtered_junction.txt`: Filtered gene annotation files.
* `genes.fpkm_tracking`, `isoforms.fpkm_tracking`, `skipped.gtf` and `transcripts.gtf`: Cufflinks result files.
* `transcripts_ref.txt`, `transcripts_ref.bed` and `transcripts_ref_sorted.bed`: Circular RNA transcript files.
* `transcripts_ref_sorted.bb`: BigBed file of Circular RNA transcripts.
