#!/usr/bin/env python

import sys
import re


def main():
    with open(sys.argv[1], 'r') as fusion:
        for circ_read in parse_fusion(fusion):
            if circ_read:
                print(circ_read)


def parse_fusion(fusion):
    for line in fusion:
        (chr1, site1, strand1,
         chr2, site2, strand2,
         flag, info) = line.split('\t', 7)
        flag = int(flag)  # not encompassing junction
        if flag < 0:
            yield None
            continue
        if chr1 != chr2 or strand1 != strand2:  # different chrom or strand
            yield None
            continue
        if strand1 == '+':
            start = int(site2)
            end = int(site1) - 1
        else:
            start = int(site1)
            end = int(site2) - 1
        if start > end:
            yield None
            continue
        _, _, _, pos1, cigar1, pos2, cigar2 = info.rstrip().split()
        # no internal junction
        if cigar1.find('N') == -1 and cigar2.find('N') == -1:
            yield '%s\t%d\t%d\tNone' % (chr1, start, end)
            continue
        junc = []
        if cigar2.find('N') != -1:
            junc.extend(parse_junc(pos2, cigar2))
        if cigar1.find('N') != -1:
            junc.extend(parse_junc(pos1, cigar1))
        yield '%s\t%d\t%d\t%s' % (chr1, start, end, '|'.join(junc))


def parse_junc(pos, cigar):
    pos = int(pos) - 1
    junc = []
    for segment in re.finditer(r'[\d|-]+\w', cigar):
        count = int(segment.group()[:-1])
        tag = segment.group()[-1]
        if tag in ['M', 'D', 'p']:
            pos += count
        elif tag == 'N':
            junc_start = pos
            pos += count
            junc_end = pos
            junc.append('%d:%d' % (junc_start, junc_end))
    return junc


if __name__ == '__main__':
    main()
