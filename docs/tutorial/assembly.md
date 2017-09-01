# *De Novo* Assembly for Circular RNA Transcripts

CIRCexplorer2 employs Cufflinks to carry out *de novo* assembly for circular RNA transcripts, and charaterizes alternative splicing based on the assembled results. So it is the key step before analyzing the landscape of alternative back-splicing and alternative splicing of circular RNAs.

## Command

```
CIRCexplorer2 assemble -r hg19_ref_all.txt -m tophat -o assemble > CIRCexplorer2_assemble.log
```

### Note:
1. It will use Cufflinks to assemble circular RNA transcripts with the alignment result (`tophat`) of poly(A)−/ribo− RNA-seq (See [Alignment](../tutorial/alignment.md)).
2. `CIRCexplorer2 assemble` will create a directory `assemble` by default. All the assembly information of circular RNA transcripts will be created under the directory `assemble`. You could also check `cufflinks.log` file for detailed logs of Cufflinks assembly.
3. See [Assemble](../modules/assemble.md) for detailed information about `CIRCexplorer2 assemble`.
