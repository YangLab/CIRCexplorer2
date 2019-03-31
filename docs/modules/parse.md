# *parse*

`CIRCexplorer2 parse` parses fusion junction information from results of different aligners to prepare necessary files for following analysis.

## Usage and option summary

### Usage:

```
CIRCexplorer2 parse [options] -t ALIGNER <fusion>
```

### Options:

```
-h --help                      Show help message.
--version                      Show version.
-t ALIGNER                     Aligner (TopHat-Fusion, STAR, MapSplice, BWA, segemehl).
-b JUNC --bed=JUNC             Output file. [default: back_spliced_junction.bed]
--pe                           Parse paired-end alignment file (only for TopHat-Fusion).
-f                             Statistics fragment numbers rather than read numbers.
```

## Notes about options

1. `CIRCexplorer2 parse` could accept results derived from TopHat-Fusion, STAR, MapSplice, BWA and segemehl.
2. For the alignment parameters of each aligner, some examples have been offered in the [tutorial](../tutorial/alignment.md). You could also adjust relevant parameters according to your requirements.
3. The `back_spliced_junction.bed` file has the same format with `back_spliced_junction.bed` created by the [align](../modules/align.md) module, and would be used by other modules of CIRCexplorer2 to further annotate and characterize circular RNAs.
4. It will overwrite the output file `back_spliced_junction.bed` directly, so please be careful when setting the path of output directory.
5. For paired-end results, you can add `--pe` option to get more strict fusion reads by considering the mate reads.
6. For different aligner, the `<fusion>` is different.

| ALigner       | Fusion file                           |
| :------------ | :------------------------------------ |
| TopHat-Fusion | accepted_hits.bam                     |
| STAR          | Chimeric.out.junction                 |
| MapSplice     | fusions_raw.txt                       |
| BWA           | output sam file                       |
| segemehl      | splicesites.bed                       |


## Output

`CIRCexplorer2 parse` will create a `back_spliced_junction.bed`.

``` 
back_spliced_junction.bed
```
