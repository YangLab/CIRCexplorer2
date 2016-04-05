# Annotating for Circular RNAs

This step is a clone and integration of [CIRCexplorer](http://yanglab.github.io/CIRCexplorer/) to make CIRCexplorer2 inherit all the functions from CIRCexplorer. Please see our previous [Cell paper](http://www.sciencedirect.com/science/article/pii/S0092867414011118) for detailed information.

## Command

```
CIRCexplorer2 annotate -r hg19_ref_all.txt -g hg19.fa circ_out > CIRCexplorer2_annotate.log
```

### Note:
1. It will compare `fusion_junction.bed` (See [Alignment](../tutorial/alignment.md)) and gene annotation file (`hg19_ref_all.txt`) to determine the boundaries of circular RNAs, and also carries out realignments to fix some mis-alignments.
2. `CIRCexplorer2 annotate` will create a directory `annotate` under the `circ_out` directory by default. All the annotation information of circular RNAs will be created under the directory `annotate`.
3. See [Annotate](../modules/annotate.md) for detailed information about `CIRCexplorer2 annotate`.
