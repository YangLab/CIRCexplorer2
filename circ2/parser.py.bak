import os
import pysam
from collections import defaultdict
from itertools import groupby
from genomic_interval import Interval


class Segment(object):
    '''
    Modified from https://github.com/brentp/cigar
    '''
    def __init__(self, pos, cigar):
        self.ref_start = int(pos) - 1
        self.ref_end = self.ref_start
        read_consuming_ops = ("M", "I")
        ref_consuming_ops = ("M", "D")
        cig_iter = groupby(cigar, lambda c: c.isdigit())
        self.read_start, self.read_end = 0, 0
        for i, (g, n) in enumerate(cig_iter):
            counts, tag = int("".join(n)), "".join(next(cig_iter)[1])
            if i == 0 and tag == 'S':
                self.read_start += counts
                self.read_end += counts
            if tag in read_consuming_ops:
                self.read_end += counts
            if tag in ref_consuming_ops:
                self.ref_end += counts


def parse_fusion_bam(bam_f, pair_flag):
    fusions = {}
    bam = pysam.AlignmentFile(bam_f, 'rb')
    for read in bam:
        if read.is_secondary:  # not the primary alignment
            continue
        if not read.has_tag('XF'):  # not fusion junctions
            continue
        if pair_flag is True and not read.has_tag('XP'):
            continue

        chr1, chr2 = read.get_tag('XF').split()[1].split('-')
        if chr1 != chr2:  # not on the same chromosome
            continue
        strand = '+' if not read.is_reverse else '-'

        if pair_flag is True:
            xp_info = read.get_tag('XP')
        else:
            xp_info = ''

        if read.query_name not in fusions:  # first fragment
            fusions[read.query_name] = [chr1, strand, read.reference_start,
                                        read.reference_end, xp_info]
        else:  # second fragment
            if chr1 == fusions[read.query_name][0] \
               and strand == fusions[read.query_name][1]:
                yield [chr1, strand, read.reference_start, read.reference_end,
                       xp_info]
                yield fusions[read.query_name]
    bam.close()


def parse_ref(ref_file, flag):
    if flag == 1:
        genes = defaultdict(list)
        novel_genes = defaultdict(list)
        gene_info = {}
        chrom_info = set()
    else:
        genes = {}
    with open(ref_file, 'r') as f:
        for line in f:
            gene_id, iso_id, chrom, strand = line.split()[:4]
            total_id = '\t'.join(['iso', gene_id, iso_id, chrom, strand])
            starts = [int(x) for x in line.split()[9].split(',')[:-1]]
            ends = [int(x) for x in line.split()[10].split(',')[:-1]]
            start = starts[0]
            end = ends[-1]
            if flag == 1:
                if iso_id.startswith('CUFF'):
                    novel_genes[chrom].append([start, end, total_id])
                else:
                    genes[chrom].append([start, end, total_id])
                gene_info[total_id] = [starts, ends]
            else:
                genes['\t'.join([gene_id, iso_id, chrom, strand])] = [starts,
                                                                      ends]
    if flag == 1:
        for chrom in genes:
            genes[chrom] = Interval(genes[chrom])
            chrom_info.add(chrom)
        for chrom in novel_genes:
            novel_genes[chrom] = Interval(novel_genes[chrom])
            chrom_info.add(chrom)
        return (genes, novel_genes, gene_info, chrom_info)
    else:
        return genes


def parse_bed(fus):
    fusions = defaultdict(list)
    fusion_index = {}
    with open(fus, 'r') as f:
        for line in f:
            chrom, start, end, name = line.split()[:4]
            start = int(start)
            end = int(end)
            reads = name.split('/')[1]
            fusion_id = '%s\t%s' % (name, reads)
            fusions[chrom].append([start, end, fusion_id])
            fusion_index[fusion_id] = [start, end]
    return (fusions, fusion_index)


def parse_junc(junc_f, flag=0):
    junc = defaultdict(int)
    if flag == 1:
        left_junc = defaultdict(list)
        right_junc = defaultdict(list)
    elif flag == 2:
        left_junc = defaultdict(int)
        right_junc = defaultdict(int)
    with open(junc_f, 'r') as f:
        f.readline()  # skip header
        for line in f:
            chrom = line.split()[0]
            start = int(line.split()[1])
            reads = int(line.split()[4])
            size = int(line.split()[10].split(',')[0])
            offset = int(line.split()[11].split(',')[1])
            left = str(start + size)
            right = str(start + offset)
            junc_id = '\t'.join([chrom, left, right])
            junc[junc_id] += reads
            if flag == 1:
                left_junc_id = '\t'.join([chrom, left])
                right_junc_id = '\t'.join([chrom, right])
                left_junc[left_junc_id].append([right, reads])
                right_junc[right_junc_id].append([left, reads])
            if flag == 2:
                left_junc_id = '\t'.join([chrom, left])
                right_junc_id = '\t'.join([chrom, right])
                left_junc[left_junc_id] += reads
                right_junc[right_junc_id] += reads
    if flag:
        return (junc, left_junc, right_junc)
    else:
        return junc


def check_fasta(fa_f, pysam_flag=True):
    if not os.path.isfile(fa_f + '.fai'):
        pysam.faidx(fa_f)
    if pysam_flag:  # return pysam FastaFile object
        fa = pysam.FastaFile(fa_f)
        return fa
    else:  # return fasta file path
        return fa_f
