# Parsing for Circular RNA Fusion Junction Reads

CIRCexplorer2 can parse the alignment results separably rather than together with alignment by `CIRCexplorer2 align` in one step. In this way, it can support many [aligners](./alignment.md) and support paired-end data.

If you have aligned reads with `CIRCexplorer2 align`, you could **skip** this step.

# For different aligners

* TopHat2/TopHat-Fusion
```
CIRCexplorer2 parse -t TopHat-Fusion tophat_fusion/accepted_hits.bam > CIRCexplorer2_parse.log
```

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

1. `CIRCexplorer2 parse` will create a directory `circ_out` by default, and the BED file `fusion_junction.bed` under this directory is required for following analysis.
2. See [Parse](../modules/parse.md) for detailed information about `CIRCexplorer2 parse`.

# For paired-end datas

* TopHat-Fusion
```
CIRCexplorer2 parse -p -t TopHat-Fusion tophat_fusion/accepted_hits.bam > CIRCexplorer2_parse.log
```

### Note

1. `CIRCexplorer2 parse` will create a directory `circ_out` by default, and the BED file `fusion_junction.bed` under this directory is required for following analysis.
2. Now `CIRCexplorer2 parse` only support paired-end data aligned by TopHat-Fusion in one step as mentioned in [alignment tutorial](./alignment.md).
3. See [Parse](../modules/parse.md) for detailed information about `CIRCexplorer2 parse`.
