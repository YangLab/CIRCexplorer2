#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage:
    fast_circ.py parse -r REF -g GENOME -t ALIGNER [--pe] [-o OUT] <fusion>
    fast_circ.py annotate -r REF -g GENOME -G GTF [-p THREAD] [-o OUT] \
-f FQ
    fast_circ.py denovo -r REF -g GENOME -G GTF [-n PLUS_OUT] [-p THREAD] \
[-o OUT] -f FQ

Options:
    -h --help                      Show help message.
    -r REF --ref=REF               Gene annotation.
    -g GENOME --genome=GENOME      Genome FASTA file.
    -G GTF --gtf=GTF               Annotation GTF file.
    -t ALIGNER                     Aligner (TopHat-Fusion, STAR, MapSplice, \
BWA, segemehl).
    --pe                           Parse paired-end alignment file (only for \
TopHat-Fusion).
    -f FQ --fastq=FQ               Input file.
    -n PLUS_OUT --pAplus=PLUS_OUT  TopHat mapping directory for p(A)+ RNA-seq.
    -p THREAD --thread=THREAD      Running threads. [default: 10]
    -o OUT --output=OUT            Output directory. [default: .]
'''

import sys
from docopt import docopt
from .dir_func import create_dir

__author__ = [
    'Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn)',
    'Xu-Kai Ma (maxukai@picb.ac.cn)'
]


def main():
    options = docopt(__doc__)
    command_log = 'fast_circ.py parameters: ' + ' '.join(sys.argv)
    work_dir = options['--output']
    if work_dir != '.' and 'work_dir' != './':
        create_dir(work_dir)

    if options['parse']:
        # parse fusion reads from <fusion> file
        options['--bed'] = '%s/back_spliced_junction.bed' % work_dir
        parse_command(options, command_log)
        # annotate circular RNAs
        options['--output'] = '%s/circularRNA_known.txt' % options['--output']
        annotate_command(options, command_log)
    elif options['annotate']:
        # align fusion reads
        options['--output'] = '%s/alignment' % work_dir
        options['--bed'] = '%s/back_spliced_junction.bed' % work_dir
        align_command(options, command_log)
        # annotate circular RNAs
        options['--output'] = '%s/circularRNA_known.txt' % options['--output']
        annotate_command(options, command_log)
    elif options['denovo']:
        # align fusion reads
        options['--output'] = '%s/alignment' % work_dir
        options['--bed'] = '%s/back_spliced_junction.bed' % work_dir
        align_command(options, command_log)
        # de novo assemble circular RNAs
        options['--tophat'] = '%s/alignment/tophat' % work_dir
        options['--output'] = '%s/assemble' % work_dir
        assemble_command(options, command_log)
        # fetch AS events of circular RNAs
        options['--output'] = '%s/denovo' % work_dir
        options['--abs'] = '%s/abs' % work_dir
        denovo_command(options, work_dir, command_log)


def parse_command(options, command_log):
    from .parse import parse
    parse(options, command=command_log, name='parse')


def align_command(options, command_log):
    from .align import align
    options['--bw'] = True
    options['--scale'] = True
    options['--skip-tophat'] = False
    options['--skip-tophat-fusion'] = False
    align(options, command=command_log, name='align')


def annotate_command(options, command_log):
    from .annotate import annotate
    options['--no-fix'] = False
    options['--low-confidence'] = False
    annotate(options, command=command_log, name='annotate')


def assemble_command(options, command_log):
    from .assemble import assemble
    options['--bb'] = False
    options['--chrom-size'] = None
    options['--remove-rRNA'] = False
    options['--max-bundle-frags'] = None
    assemble(options, command=command_log, name='assemble')


def denovo_command(options, work_dir, command_log):
    from .denovo import denovo
    if options['--pAplus']:
        options['--as'] = '%s/as' % work_dir
        options['--rpkm'] = True
    else:
        options['--as'] = ''
        options['--rpkm'] = False
    options['--as-type'] = None
    options['--no-fix'] = False
    denovo(options, command=command_log, name='denovo')


if __name__ == '__main__':
    main()
