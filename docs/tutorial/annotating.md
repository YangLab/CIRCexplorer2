# Annotating for Circular RNAs

This step is a clone and integration of [CIRCexplorer](http://yanglab.github.io/CIRCexplorer/) to make CIRCexplorer2 inherit all the functions from CIRCexplorer. Please see our previous [Cell paper](http://www.sciencedirect.com/science/article/pii/S0092867414011118) for detailed information.

## Command

```
CIRCexplorer2 annotate -r hg19_ref_all.txt -g hg19.fa -b back_spliced_junction.bed -o circularRNA_known.txt > CIRCexplorer2_annotate.log
```

### Note:
1. It will compare `back_spliced_junction.bed` (See [Alignment](../tutorial/alignment.md)) and gene annotation file (`hg19_ref_all.txt`) to determine the boundaries of circular RNAs, and also carries out realignments to fix some mis-alignments.
2. `CIRCexplorer2 annotate` will create a output file `circularRNA_known.txt` containing circRNA informations.
3. See [Annotate](../modules/annotate.md) for detailed information about `CIRCexplorer2 annotate`.
