# Characterization of Circular RNA Alternative Splicing

CIRCexplorer2 will systematically characterize two types of alternative back-splicing events (alternative 5' back-splice site and alternative 3' back-splice site) and four types of alternative splicing events (cassette exon, intron retention, alternative 5' splice site and alternative 3' splice site) for circular RNAs.

## Command

```
CIRCexplorer2 denovo -r hg19_ref_all.txt -g hg19.fa -b back_spliced_junction.bed --abs abs --as as -m tophat -n pAplus_tophat -o denovo > CIRCexplorer2_denovo.log
```

### Notes:
1. It requires alignment results (set with `-n`) of poly(A)+ RNA-seq derived from the same source of corresponding poly(A)−/ribo− RNA-seq (set with `-m`) so that it will extract circular RNA predominate alternative (back-)splicing events after comparing poly(A)−/ribo− RNA-seq with poly(A)+ RNA-seq.
2. `CIRCexplorer2 denovo` will create three directory `denovo`, `as` and `abs` by default. All the alternative (back-)splicing information of circular RNAs will be created under these directory. Each alternative (back-)splicing event has a series of metrics to evaluate, and you could sort out relevant events according to your requirements.
3. See [denovo](../modules/denovo.md) for detailed information about `CIRCexplorer2 denovo`.
