# *denovo*

`CIRCexplorer2 denovo`

## Usage and option summary

### Usage:

```bash
CIRCexplorer2 denovo [options] -r REF -g GENOME <circ_dir>
```

### Options:

```bash
-h --help                      Show this screen.
--version                      Show version.
-r REF --ref=REF               Gene annotation.
--as                           Detect alternative splicing.
-a PLUS_OUT --pAplus=PLUS_OUT  TopHat mapping directory for pAplus RNA-seq.
-g GENOME --genome=GENOME      Genome FASTA file.
--tophat-dir=TOPHAT_DIR        TopHat mapping directory for pAminus RNA-seq.
--no-fix                       No-fix mode (useful for species with poor gene annotations)
--rpkm                         Calculate RPKM for specific exons.
```
