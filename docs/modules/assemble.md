# *assemble*

`CIRCexplorer2 assemble`

## Usage and option summary

### Usage:

```bash
CIRCexplorer2 assemble [options] -r REF <circ_dir>
```

### Options:

```bash
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
