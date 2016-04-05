"""
Usage: CIRCexplorer2 parse [options] -t ALIGNER <fusion>

Options:
    -h --help                      Show help message.
    --version                      Show version.
    -t ALIGNER                     Aligner (STAR, MapSplice, segemehl).
    -o OUT --output=OUT            Output directory. [default: circ_out]
"""

import sys
import os.path
from collections import defaultdict
from dir_func import create_dir
from helper import logger

__author__ = 'Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn)'

__all__ = ['parse']


@logger
def parse(options):
    aliger = set(['STAR', 'MapSplice', 'segemehl'])
    if options['-t'] not in aliger:
        sys.exit('Error: CIRCexplorer2 parse does not support %s!' %
                 options['-t'])
    # check output directory
    create_dir(options['--output'])
    out_dir = os.path.abspath(options['--output'])
    out = out_dir + '/fusion_junction.bed'
    # parse fusion junctions from other aligers
    if options['-t'] == 'STAR':
        star_parse(options['<fusion>'], out)
    elif options['-t'] == 'MapSplice':
        mapsplice_parse(options['<fusion>'], out)
    elif options['-t'] == 'segemehl':
        segemehl_parse(options['<fusion>'], out)


def star_parse(fusion, out):
    '''
    Parse fusion junctions from STAR aligner
    '''
    print('Start parsing fusion junctions from STAR...')
    junc = defaultdict(int)
    with open(fusion, 'r') as junc_f:
        for line in junc_f:
            flag = int(line.split()[6])
            if flag < 0:
                continue
            chr1, site1, strand1, chr2, site2, strand2 = line.split()[:6]
            if chr1 != chr2 or strand1 != strand2:
                continue
            if strand1 == '+':
                start = int(site2)
                end = int(site1) - 1
            else:
                start = int(site1)
                end = int(site2) - 1
            if start > end:
                continue
            junc_id = '%s\t%d\t%d' % (chr1, start, end)
            junc[junc_id] += 1
    with open(out, 'w') as outf:
        for i, j in enumerate(junc):
            outf.write('%s\tFUSIONJUNC_%d/%d\t0\t+\n' % (j, i, junc[j]))


def mapsplice_parse(fusion, out):
    '''
    Parse fusion junctions from MapSplice aligner
    '''
    print('Start parsing fusion junctions from MapSplice...')
    with open(fusion, 'r') as junc_f, open(out, 'w') as outf:
        for i, line in enumerate(junc_f):
            chrom, site1, site2, name, reads, strand = line.split()[:6]
            chr1, chr2 = chrom.split('~')
            if chr1 != chr2:
                continue
            site1 = int(site1)
            site2 = int(site2)
            if strand == '++' and site1 > site2:
                start = site2 - 1
                end = site1
            elif strand == '--' and site1 < site2:
                start = site1 - 1
                end = site2
            else:
                continue
            outf.write('%s\t%d\t%d\tFUSIONJUNC_%d/%s\t0\t+\n' % (chr1, start,
                                                                 end, i,
                                                                 reads))


def segemehl_parse(fusion, out):
    '''
    Parse fusion junctions from segemehl aligner
    '''
    print('Start parsing fusion junctions from segemehl...')
    with open(fusion, 'r') as junc_f, open(out, 'w') as outf:
        for i, line in enumerate(junc_f):
            chrom, start, end, info = line.split()[:4]
            if not info.endswith('C:P'):
                continue
            reads = info.split(':')[1]
            start = str(int(start) - 1)
            outf.write('\t'.join([chrom, start, end,
                                  'FUSIONJUNC_%d/%s\t+\n' % (i, reads)]))
