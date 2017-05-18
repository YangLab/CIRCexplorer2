#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage:
    fast_circ.py parse -r REF -g GENOME -t ALIGNER [--pe] [-o OUT] <fusion>
    fast_circ.py annotate -r REF -g GENOME -G GTF [-p THREAD] [-o OUT] \
<fastq>...
    fast_circ.py denovo -r REF -g GENOME -G GTF [-a PLUS_OUT] [-p THREAD] \
[-o OUT] <fastq>...

Options:
    -h --help                      Show help message.
    -r REF --ref=REF               Gene annotation.
    -g GENOME --genome=GENOME      Genome FASTA file.
    -G GTF --gtf=GTF               Annotation GTF file.
    -t ALIGNER                     Aligner (TopHat-Fusion, STAR, MapSplice, \
BWA, segemehl).
    --pe                           Parse paired-end alignment file (only for \
TopHat-Fusion).
    -a PLUS_OUT --pAplus=PLUS_OUT  TopHat mapping directory for p(A)+ RNA-seq.
    -p THREAD --thread=THREAD      Running threads. [default: 10]
    -o OUT --output=OUT            Output directory. [default: circ_out]
'''

import sys
from docopt import docopt

__author__ = 'Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn)'


def main():
    options = docopt(__doc__)
    command_log = 'fast_circ.py parameters: ' + ' '.join(sys.argv)
    if options['parse']:
        # parse fusion reads from <fusion> file
        parse_command(options, command_log)
        # annotate circular RNAs
        annotate_command(options, command_log)
    elif options['annotate']:
        # align fusion reads
        align_command(options, command_log)
        # annotate circular RNAs
        annotate_command(options, command_log)
    elif options['denovo']:
        # align fusion reads
        align_command(options, command_log)
        # de novo assemble circular RNAs
        assemble_command(options, command_log)
        # fetch AS events of circular RNAs
        denovo_command(options, command_log)


def parse_command(options, command_log):
    from parse import parse
    parse(options, command=command_log, name='parse')


def align_command(options, command_log):
    from align import align
    options['--bw'] = True
    options['--scale'] = True
    options['--skip-tophat'] = False
    options['--skip-tophat-fusion'] = False
    align(options, command=command_log, name='align')


def annotate_command(options, command_log):
    from annotate import annotate
    options['--no-fix'] = False
    options['--low-confidence'] = False
    options['<circ_dir>'] = options['--output']
    annotate(options, command=command_log, name='annotate')


def assemble_command(options, command_log):
    from assemble import assemble
    options['--bb'] = False
    options['--tophat-dir'] = None
    options['--chrom-size'] = None
    options['--remove-rRNA'] = False
    options['--max-bundle-frags'] = None
    options['<circ_dir>'] = options['--output']
    assemble(options, command=command_log, name='assemble')


def denovo_command(options, command_log):
    from denovo import denovo
    if options['--pAplus']:
        options['--as'] = True
        options['--rpkm'] = True
    else:
        options['--as'] = False
        options['--rpkm'] = False
    options['--as-type'] = None
    options['--tophat-dir'] = None
    options['--no-fix'] = False
    options['<circ_dir>'] = options['--output']
    denovo(options, command=command_log, name='denovo')


if __name__ == '__main__':
    main()
