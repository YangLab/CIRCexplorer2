"""
Usage: CIRCexplorer2 denovo [options] -r REF -g GENOME <circ_dir>

Options:
    -h --help                      Show help message.
    --version                      Show version.
    -r REF --ref=REF               Gene annotation.
    --as                           Detect alternative splicing.
    --as-type=AS_TYPE              Only check certain type (CE/RI/ASS) of AS \
events.
    -a PLUS_OUT --pAplus=PLUS_OUT  TopHat mapping directory for p(A)+ RNA-seq.
    -g GENOME --genome=GENOME      Genome FASTA file.
    --tophat-dir=TOPHAT_DIR        TopHat mapping directory for p(A)- RNA-seq.
    --no-fix                       No-fix mode (useful for species \
with poor gene annotations).
    --rpkm                         Calculate RPKM for cassette exons.
"""

import sys
import os.path
from collections import defaultdict, deque
from annotate import annotate_fusion, fix_fusion
from parser import parse_junc
from helper import logger, fetch_psi, fetch_read, Expression
from dir_func import check_dir, create_dir
import pysam
from scipy.stats import fisher_exact, binom
from genomic_interval import Interval

__author__ = 'Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn)'

__all__ = ['denovo']


@logger
def denovo(options):
    # check output directory
    out_dir = check_dir(options['<circ_dir>'])
    # check tophat results
    if options['--tophat-dir']:
        tophat_dir = check_dir(options['--tophat-dir'])
    else:
        tophat_dir = check_dir(out_dir + '/tophat')
    # prepare denovo directory
    denovo_dir = '%s/denovo' % out_dir
    create_dir(denovo_dir)
    # combine ref files
    cufflinks_ref_path = '%s/cufflinks/transcripts_ref.txt' % out_dir
    if os.path.isfile(cufflinks_ref_path):
        print('Combine %s with %s to create a new ref file!' %
              (options['--ref'], cufflinks_ref_path))
        ref_path = '%s/combined_ref.txt' % denovo_dir
        new_ref_f = open(ref_path, 'w')
        with open(cufflinks_ref_path, 'r') as cuff_ref:
            for line in cuff_ref:
                if line.startswith('CUFF'):  # only import novel isoforms
                    new_ref_f.write(line)
        new_ref_f.write(open(options['--ref'], 'r').read())
        new_ref_f.close()
    else:
        print('Warning: no cufflinks directory under %s!' % out_dir)
        print('Please run CIRCexplorer2 assembly before this step!')
        ref_path = options['--ref']
    # annotate fusion junctions
    annotate_fusion(ref_path, denovo_dir, denovo_flag=1)
    # fix fusion juncrions
    fix_fusion(ref_path, options['--genome'], denovo_dir,
               options['--no-fix'], denovo_flag=1)
    # extract novel circRNAs
    extract_novel_circ(denovo_dir, options['--ref'])
    if options['--as']:
        if options['--pAplus'] and os.path.isdir(options['--pAplus']):
            pAplus_dir = os.path.abspath(options['--pAplus'])
        else:
            sys.exit('You should offer --pAplus option in --as mode!')
        if not options['--as-type'] or options['--as-type'] == 'CE':
            # extract cassette exons
            extract_cassette_exon(denovo_dir, tophat_dir, pAplus_dir,
                                  options['--rpkm'])
        if not options['--as-type'] or options['--as-type'] == 'RI':
            # extract retained introns
            extract_retained_intron(denovo_dir, tophat_dir, pAplus_dir)
        if not options['--as-type'] or options['--as-type'] == 'ASS':
            # characterize A5SS and A3SS
            parse_splice_site(denovo_dir, tophat_dir, pAplus_dir)


def extract_novel_circ(denovo_dir, ref_path):
    """
    Fetch circRNAs with novel back-spliced exons or splicing pattern
    """
    print('Start to fetch novel circular RNAs...')
    all_circ = {}
    # set path
    fusion_f = '%s/circ_fusion.txt' % denovo_dir
    with open(fusion_f, 'r') as f:
        for line in f:
            circ_type = line.split()[13]
            if circ_type == 'ciRNA':  # not fetch ciRNAs
                continue
            chrom, start, end, name, score, strand = line.split()[:6]
            circ_id = '\t'.join([chrom, start, end, name, score, strand])
            iso = line.split()[14]
            if circ_id in all_circ:
                if all_circ[circ_id].startswith('CUFF'):
                    all_circ[circ_id] = iso
            else:
                all_circ[circ_id] = iso
    ref_left = set()
    ref_right = set()
    with open(ref_path, 'r') as ref_f:
        for line in ref_f:
            chrom = line.split()[2]
            for x in line.split()[9].split(',')[:-1]:
                ref_left.add('\t'.join([chrom, x]))
            for x in line.split()[10].split(',')[:-1]:
                ref_right.add('\t'.join([chrom, x]))
    novel_out = '%s/novel_circ.txt' % denovo_dir
    annotated_out = '%s/annotated_circ.txt' % denovo_dir
    novel_circ_num = 0
    with open(novel_out, 'w') as novel, open(annotated_out, 'w') as annotated:
        for circ_id in all_circ:
            if all_circ[circ_id].startswith('CUFF'):
                novel_circ_num += 1
                chrom, start, end, name, score, strand = circ_id.split()
                left_id = '\t'.join([chrom, start])
                right_id = '\t'.join([chrom, end])
                if left_id in ref_left:
                    left_flag = 'Annotated'
                else:
                    left_flag = 'Novel'
                if right_id in ref_right:
                    right_flag = 'Annotated'
                else:
                    right_flag = 'Novel'
                novel.write('\t'.join([circ_id, left_flag, right_flag]) +
                            '\n')
            else:
                annotated.write('\t'.join([circ_id, all_circ[circ_id]]) +
                                '\n')
    print('Fetch %d circular RNAs!' % novel_circ_num)


def extract_cassette_exon(denovo_dir, tophat_dir, pAplus_dir, rpkm_flag):
    """
    1. Check each exon and fetch PSI
    2. Calculate RPKM if needed
    Modified from Han et al., Nature, 2013, 498:241-245.
    """
    print('Start to parse circular RNA exons...')
    exons = {}
    # set path
    fusion_f = '%s/circ_fusion.txt' % denovo_dir
    pAminus_junc_f = tophat_dir + '/junctions.bed'
    (pAminus_junc,
     pAminus_left_junc,
     pAminus_right_junc) = parse_junc(pAminus_junc_f, 1)
    pAplus_junc_f = '%s/junctions.bed' % pAplus_dir
    (pAplus_junc,
     pAplus_left_junc,
     pAplus_right_junc) = parse_junc(pAplus_junc_f, 1)
    if rpkm_flag:
        pAminus_bam = Expression('%s/accepted_hits.bam' % tophat_dir)
        pAplus_bam = Expression('%s/accepted_hits.bam' % pAplus_dir)
    with open(fusion_f, 'r') as f:
        for line in f:
            circ_type = line.split()[13]
            if circ_type == 'ciRNA':  # not check ciRNAs
                continue
            reads = line.split()[12]
            chrom = line.split()[0]
            start = int(line.split()[1])
            strand = line.split()[5]
            sizes = [int(x) for x in line.split()[10].split(',')]
            offsets = [int(x) for x in line.split()[11].split(',')]
            gene, iso = line.split()[14:16]
            exon_deque = deque(maxlen=3)  # set exon sliding window
            for s, o in zip(sizes, offsets):
                sta = start + o
                end = start + o + s
                exon_id = [sta, end]
                exon_deque.append(exon_id)
                gene_info = '\t'.join([strand, gene, iso])
                if len(exon_deque) == 3:  # only check middle exon
                    exon_info = '%s\t%d\t%d' % (chrom, exon_deque[1][0],
                                                exon_deque[1][1])
                    if exon_info in exons:
                        if exons[exon_info][0].find('CUFF'):
                            if not gene.startswith('CUFF'):  # annotated exon
                                exons[exon_info][0] = gene_info
                        if int(reads) > int(exons[exon_info][1]):  # more reads
                            exons[exon_info][1] = reads
                    else:
                        # fetch junctions for circular RNAs
                        (psi_circ,
                         inclusion_circ,
                         exclusion_circ,
                         max_left_circ,
                         max_right_circ) = fetch_psi(exon_info,
                                                     pAminus_junc,
                                                     pAminus_left_junc,
                                                     pAminus_right_junc)
                        if max_left_circ == 'None' or max_left_circ == 'None':
                            flag = []
                        else:
                            flag = [max_left_circ, max_right_circ]
                        # fetch junctions for linear RNAs
                        (psi_linear,
                         inclusion_linear,
                         exclusion_linear) = fetch_psi(exon_info,
                                                       pAplus_junc,
                                                       pAplus_left_junc,
                                                       pAplus_right_junc,
                                                       flag)
                        # fisher exact test (circular > linear)
                        odd1, p1 = fisher_exact([[inclusion_circ,
                                                  2 * exclusion_circ],
                                                 [inclusion_linear,
                                                  2 * exclusion_linear]],
                                                alternative='greater')
                        # fisher exact test (circular < linear)
                        odd2, p2 = fisher_exact([[inclusion_circ,
                                                  2 * exclusion_circ],
                                                [inclusion_linear,
                                                 2 * exclusion_linear]],
                                                alternative='less')
                        info = '\t'.join(str(round(x, 3))
                                         for x in (psi_circ, psi_linear, p1,
                                                   p2,
                                                   inclusion_circ,
                                                   exclusion_circ,
                                                   inclusion_linear,
                                                   exclusion_linear))
                        if rpkm_flag:
                            circ_exp = pAminus_bam.rpkm(chrom, *exon_deque[1])
                            linear_exp = pAplus_bam.rpkm(chrom, *exon_deque[1])
                            info += '\t%.3f\t%.3f' % (circ_exp, linear_exp)
                        exons[exon_info] = [gene_info, reads, info]
    output_f = '%s/all_exon_info.txt' % denovo_dir
    with open(output_f, 'w') as output:
        for exon in exons:
            chrom, start, end = exon.split()
            output.write('\t'.join([chrom, start, end, 'Exon', '0']))
            output.write('\t' + '\t'.join(exons[exon]))
            output.write('\n')
    print('Complete parsing circular RNA exons!')


def extract_retained_intron(denovo_dir, tophat_dir, pAplus_dir):
    """
    Check each intron and fetch PIR
    Modified from Braunschweig et al., Genome Research, 2014, gr-177790.
    """
    print('Start to parse circular RNA introns...')
    # set path
    fusion_f = '%s/circ_fusion.txt' % denovo_dir
    pAminus_junc_f = tophat_dir + '/junctions.bed'
    pAminus_junc = parse_junc(pAminus_junc_f)
    pAminus_bam_f = tophat_dir + '/accepted_hits.bam'
    pAminus_bam = pysam.AlignmentFile(pAminus_bam_f, 'rb')
    pAplus_junc_f = '%s/junctions.bed' % pAplus_dir
    pAplus_junc = parse_junc(pAplus_junc_f)
    pAplus_bam_f = '%s/accepted_hits.bam' % pAplus_dir
    pAplus_bam = pysam.AlignmentFile(pAplus_bam_f, 'rb')
    excluded_region = defaultdict(list)
    novel_region = defaultdict(list)
    intron = defaultdict(list)
    intron_list = set()
    intron_info_list = {}
    with open(fusion_f, 'r') as f:
        for line in f:
            chrom, start, end = line.split()[:3]
            start = int(start)
            end = int(end)
            strand = line.split()[5]
            circ_type = line.split()[13]
            if circ_type == 'ciRNA':  # not check ciRNAs
                excluded_region[chrom].append([start, end])
                continue
            sizes = [int(x) for x in line.split()[10].split(',')]
            offsets = [int(x) for x in line.split()[11].split(',')]
            reads = line.split()[12]
            gene, iso = line.split()[14:16]
            for s, o in zip(sizes, offsets):
                if gene.startswith('CUFF'):
                    novel_region[chrom].append([start + o, start + o + s])
                else:
                    excluded_region[chrom].append([start + o, start + o + s])
            if gene.startswith('CUFF'):  # only check annotated introns
                continue
            num = int(line.split()[9])
            for i in range(num - 1):
                sta = start + offsets[i] + sizes[i]
                end = start + offsets[i + 1]
                if end - sta == 0:
                    continue
                intron_info = '%s\t%d\t%d\t%s' % (chrom, sta, end, strand)
                if intron_info in intron_list:
                    if int(reads) > int(intron_info_list[intron_info][2]):
                        intron_info_list[intron_info] = [gene, iso, reads]
                    continue
                intron[chrom].append([sta, end, intron_info])
                intron_list.add(intron_info)
                intron_info_list[intron_info] = [gene, iso, reads]
    intron_set = set()
    for chrom in excluded_region:
        intron_region = []
        # retain introns covered by novel assembled transcripts
        combined_region = Interval(novel_region[chrom]).interval
        for region in Interval.overlapwith(combined_region, intron[chrom]):
            if len(region) >= 3:
                for intron_info in region[2:]:
                    chrom, start, end = intron_info.split()[:3]
                    intron_region.append([int(start), int(end), intron_info])
                    intron_set.add(intron_info)
        # remove introns overlapped with annotated exons
        combined_region = Interval(excluded_region[chrom]).interval
        for region in Interval.overlapwith(combined_region, intron_region):
            if len(region) >= 3:
                for intron_info in region[2:]:
                    intron_set.discard(intron_info)
    output_f = '%s/all_intron_info.txt' % denovo_dir
    with open(output_f, 'w') as output:
        for intron in intron_set:
            chrom, sta, end, strand = intron.split()
            intron_info = '\t'.join([chrom, sta, end])
            sta = int(sta)
            end = int(end)
            # fetch junctions for circular RNAs
            circ_junc_read = pAminus_junc[intron_info]
            circ_left_read = fetch_read(pAminus_bam, chrom, sta - 8, sta + 8)
            circ_right_read = fetch_read(pAminus_bam, chrom, end - 8, end + 8)
            circ_ri_read = circ_left_read + circ_right_read
            circ_intron_read = fetch_read(pAminus_bam, chrom, sta, end, flag=0)
            # calculate PIR for circular RNAs
            if circ_ri_read == 0 and circ_junc_read == 0:
                pir_circ = 0
            else:
                pir_circ = 100.0 * circ_ri_read / (circ_ri_read +
                                                   2 * circ_junc_read)
            # exact binomial test for circular RNAs
            m = min(circ_left_read, circ_right_read, circ_intron_read)
            n = m + max(circ_left_read, circ_right_read, circ_intron_read)
            p = 1 / 3.5
            p1 = binom.cdf(m, n, p)  # one-side binomial test
            # fetch junctions for linear RNAs
            linear_junc_read = pAplus_junc[intron_info]
            linear_left_read = fetch_read(pAplus_bam, chrom, sta - 8, sta + 8)
            linear_right_read = fetch_read(pAplus_bam, chrom, end - 8, end + 8)
            linear_ri_read = linear_left_read + linear_right_read
            linear_intron_read = fetch_read(pAplus_bam, chrom, sta, end,
                                            flag=0)
            # calculate PIR for linear RNAs
            if linear_ri_read == 0 and linear_junc_read == 0:
                pir_linear = 0
            else:
                pir_linear = 100.0 * linear_ri_read / (linear_ri_read +
                                                       linear_junc_read * 2)
            # exact binomial test for linear RNAs
            m = min(linear_left_read, linear_right_read,
                    linear_intron_read)
            n = m + max(linear_left_read, linear_right_read,
                        linear_intron_read)
            p = 1 / 3.5
            p2 = binom.cdf(m, n, p)  # one-side binomial test
            info = '\t'.join(str(round(x, 3))
                             for x in (pir_circ, pir_linear, p1, p2,
                                       circ_ri_read,
                                       circ_junc_read,
                                       circ_intron_read,
                                       linear_ri_read,
                                       linear_junc_read,
                                       linear_intron_read))
            other_info = '\t'.join(intron_info_list[intron])
            output.write('\t'.join([chrom, str(sta), str(end), 'Intron', '0',
                                    strand, other_info, info]))
            output.write('\n')
    print('Complete parsing circular RNA introns!')


def parse_splice_site(denovo_dir, tophat_dir, pAplus_dir):
    """
    Characterize all the alternative splice site selections.
    """
    print('Start to parse alternative splice sites...')
    splice_site_5 = set()
    splice_site_3 = set()
    # set path
    fusion_f = '%s/circ_fusion.txt' % denovo_dir
    pAminus_junc_f = tophat_dir + '/junctions.bed'
    (pAminus_junc,
     pAminus_left_junc,
     pAminus_right_junc) = parse_junc(pAminus_junc_f, 2)
    pAplus_junc_f = '%s/junctions.bed' % pAplus_dir
    (pAplus_junc,
     pAplus_left_junc,
     pAplus_right_junc) = parse_junc(pAplus_junc_f, 2)
    with open(fusion_f, 'r') as f:
        for line in f:
            circ_type = line.split()[13]
            if circ_type == 'ciRNA':  # not check ciRNAs
                continue
            chrom = line.split()[0]
            start = int(line.split()[1])
            strand = line.split()[5]
            sizes = [int(x) for x in line.split()[10].split(',')]
            offsets = [int(x) for x in line.split()[11].split(',')]
            starts, ends = [], []
            for s, o in zip(sizes, offsets):
                starts.append(start + o)
                ends.append(start + o + s)
            starts = starts[1:]
            ends = ends[:-1]
            for s, e in zip(ends, starts):
                loc = '%s\t%d\t%d' % (chrom, s, e)
                left_id = '%s\t%d' % (chrom, s)
                right_id = '%s\t%d' % (chrom, e)
                if loc in pAminus_junc:
                    pAminus_reads = pAminus_junc[loc]
                else:  # circ_pcu=0
                    continue
                if loc in pAplus_junc:
                    pAplus_reads = pAplus_junc[loc]
                else:
                    pAplus_reads = 0
                if pAminus_left_junc[left_id] != 0:
                    pAminus_left_total = pAminus_left_junc[left_id]
                    pAminus_left_psu = (pAminus_reads * 100.0 /
                                        pAminus_left_total)
                    pAplus_left_total = pAplus_left_junc[left_id]
                    if pAplus_left_total != 0:
                        pAplus_left_psu = (pAplus_reads * 100.0 /
                                           pAplus_left_total)
                    else:
                        pAplus_left_psu = 0.0
                else:  # circ_left_total_reads=0
                    continue
                if pAminus_right_junc[right_id] != 0:
                    pAminus_right_total = pAminus_right_junc[right_id]
                    pAminus_right_psu = (pAminus_reads * 100.0 /
                                         pAminus_right_total)
                    pAplus_right_total = pAplus_right_junc[right_id]
                    if pAplus_right_total != 0:
                        pAplus_right_psu = (pAplus_reads * 100.0 /
                                            pAplus_right_total)
                    else:
                        pAplus_right_psu = 0.0
                else:  # circ_right_total_reads=0
                    continue
                f = '%s\t%s\t%d\t%d\t%f\t%d\t%d\t%f\n'
                left_info = f % (loc, strand, pAminus_reads,
                                 pAminus_left_total, pAminus_left_psu,
                                 pAplus_reads, pAplus_left_total,
                                 pAplus_left_psu)
                right_info = f % (loc, strand, pAminus_reads,
                                  pAminus_right_total, pAminus_right_psu,
                                  pAplus_reads, pAplus_right_total,
                                  pAplus_right_psu)
                if strand == '+':
                    if pAminus_left_psu != 100:
                        splice_site_3.add(left_info)
                    if pAminus_right_psu != 100:
                        splice_site_5.add(right_info)
                else:
                    if pAminus_left_psu != 100:
                        splice_site_5.add(left_info)
                    if pAminus_right_psu != 100:
                        splice_site_3.add(right_info)
    output_f = '%s/all_A5SS_info.txt' % denovo_dir
    with open(output_f, 'w') as output:
        output.write(''.join(splice_site_5))
    output_f = '%s/all_A3SS_info.txt' % denovo_dir
    with open(output_f, 'w') as output:
        output.write(''.join(splice_site_3))
    print('Complete parsing alternative splice sites!')
