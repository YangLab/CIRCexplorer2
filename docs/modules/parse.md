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
-t ALIGNER                     Aligner (STAR, MapSplice, segemehl).
-o OUT --output=OUT            Output directory. [default: circ_out]
```

## Notes about options

1. `CIRCexplorer2 parse` only accept results derived from STAR, MapSplice, segemehl.
2. The `fusion_junction.bed` file has the same format with `fusion_junction.bed` created by the [align](../modules/align.md) module, and would be used by other modules of CIRCexplorer2 to further annotate and characterize circular RNAs.

## Output

`CIRCexplorer2 parse` will create a `circ_out` (you could change output folder using `-o`) folder, and format and convert relevant fusion information into decent file compatible with CIRCexplorer2.

```
circ_out
└── fusion_junction.bed
```
