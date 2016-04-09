"""
Usage: CIRCexplorer2 annotate [options] -r REF -g GENOME <circ_dir>

Options:
    -h --help                      Show help message.
    --version                      Show version.
    -r REF --ref=REF               Gene annotation.
    -g GENOME --genome=GENOME      Genome FASTA file.
    --no-fix                       No-fix mode (useful for species \
with poor gene annotations).
"""

from genomic_interval import Interval
from parser import parse_ref, parse_bed, check_fasta
from helper import logger, map_fusion_to_iso, fix_bed, generate_bed
from dir_func import check_dir, create_dir

__author__ = 'Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn)'

__all__ = ['annotate']


@logger
def annotate(options):
    # check output directory
    out_dir = check_dir(options['<circ_dir>'])
    # prepare annotate directory
    annotate_dir = '%s/annotate' % out_dir
    create_dir(annotate_dir)
    # annotate fusion junctions
    annotate_fusion(options['--ref'], annotate_dir)
    # fix fusion juncrions
    fix_fusion(options['--ref'], options['--genome'], annotate_dir,
               options['--no-fix'])


def annotate_fusion(ref_f, out_dir, denovo_flag=0):
    """
    Align fusion juncrions to gene annotations
    """
    print('Start to annotate fusion junctions...')
    # gene annotations
    genes, novel_genes, gene_info, chrom_info = parse_ref(ref_f, 1)
    fusion_bed = '%s/../fusion_junction.bed' % out_dir
    fusions, fusion_index = parse_bed(fusion_bed)  # fusion junctions
    total = set()
    annotated_fusion_f = '%s/annotated_fusion.txt' % out_dir
    with open(annotated_fusion_f, 'w') as outf:
        for chrom in chrom_info:
            # overlap gene annotations with fusion juncrions
            result = []
            # overlap genes
            if chrom in genes:
                result += Interval.overlapwith(genes[chrom].interval,
                                               fusions[chrom])
            # overlap novel genes in denovo mode
            if denovo_flag and chrom in novel_genes:
                result += Interval.overlapwith(novel_genes[chrom].interval,
                                               fusions[chrom])
            for itl in result:
                # extract gene annotations
                iso = list(filter(lambda x: x.startswith('iso'), itl[2:]))
                # for each overlapped fusion junction
                for fus in itl[(2 + len(iso)):]:
                    reads = fus.split()[1]
                    fus_start, fus_end = fusion_index[fus]
                    edge_annotations = []  # first or last exon flag
                    for iso_id in iso:
                        g, i, c, s = iso_id.split()[1:]
                        start = gene_info[iso_id][0][0]
                        end = gene_info[iso_id][-1][-1]
                        # fusion junction excesses boundaries of gene
                        # annotation
                        if fus_start < start - 10 or fus_end > end + 10:
                            continue
                        (fusion_info,
                         index,
                         edge) = map_fusion_to_iso(fus_start,
                                                   fus_end, s,
                                                   gene_info[iso_id])
                        if fusion_info:
                            fus_start_str = str(fus_start)
                            fus_end_str = str(fus_end)
                            bed_info = '\t'.join([chrom, fus_start_str,
                                                  fus_end_str,
                                                  'FUSIONJUNC/%s' % reads,
                                                  '0', s, fus_start_str,
                                                  fus_start_str, '0,0,0'])
                            bed = '\t'.join([bed_info, fusion_info, g, i,
                                             index])
                            if not edge:  # not first or last exon
                                outf.write(bed + '\n')
                                total.add(fus)
                            else:  # first or last exon
                                edge_annotations.append(bed)
                    if edge_annotations:
                        for bed in edge_annotations:
                            outf.write(bed + '\n')
                        total.add(fus)
    print('Annotated %d fusion junctions!' % len(total))


def fix_fusion(ref_f, genome_fa, out_dir, no_fix, denovo_flag=0):
    """
    Realign fusion juncrions
    """
    print('Start to fix fusion junctions...')
    fa = check_fasta(genome_fa)
    ref = parse_ref(ref_f, 2)
    annotated_fusion_f = '%s/annotated_fusion.txt' % out_dir
    fusions, fusion_names, fixed_flag = fix_bed(annotated_fusion_f, ref, fa,
                                                no_fix, denovo_flag)
    total = 0
    annotations = set()
    fixed_fusion_f = '%s/circ_fusion.txt' % out_dir
    with open(fixed_fusion_f, 'w') as outf:
        for fus in fusion_names:
            reads = str(fusions[fus])
            fixed = fixed_flag[fus]
            if fixed > 0:
                total += 1
            fixed = str(fixed)
            name = 'circular_RNA/' + reads
            gene, iso, chrom, strand, index = fus.split()
            starts, ends = ref['\t'.join([gene, iso, chrom, strand])]
            exon_num = len(starts)
            intron_num = exon_num - 1
            if ',' in index:  # back spliced exons
                s, e = [int(x) for x in index.split(',')]
                if strand == '+':
                    index_info = ','.join(str(x + 1) for x in xrange(s, e + 1))
                else:
                    index_info = ','.join(str(exon_num - x)
                                          for x in xrange(s, e + 1))
                start = str(starts[s])
                end = str(ends[e])
                length = str(e - s + 1)
                sizes, offsets = generate_bed(int(start), starts[s:(e + 1)],
                                              ends[s:(e + 1)])
                annotation_info = '\t'.join([chrom, start, end, sizes,
                                             offsets])
                # remove circular RNA info duplications in denovo mode
                if denovo_flag and annotation_info in annotations:
                    continue
                if s == 0:
                    left_intron = 'None'
                else:
                    left_intron = '%s:%d-%d' % (chrom, ends[s - 1], starts[s])
                if e == len(ends) - 1:
                    right_intron = 'None'
                else:
                    right_intron = '%s:%d-%d' % (chrom, ends[e], starts[e + 1])
                intron = '|'.join([left_intron, right_intron])
                bed = '\t'.join([chrom, start, end, name, fixed, strand, start,
                                 start, '0,0,0', length, sizes, offsets,
                                 reads, 'circRNA', gene, iso, index_info,
                                 intron])
            else:  # ciRNAs
                index, start, end = index.split('|')
                size = str(int(end) - int(start))
                annotation_info = '\t'.join([chrom, start, end, size, '0'])
                # remove circular RNA info duplications in denovo mode
                if denovo_flag and annotation_info in annotations:
                    continue
                index = int(index)
                if strand == '+':
                    index_info = str(index + 1)
                else:
                    index_info = str(intron_num - index)
                intron = '%s:%d-%d' % (chrom, ends[index], starts[index + 1])
                bed = '\t'.join([chrom, start, end, name, fixed, strand, start,
                                 start, '0,0,0', '1', size, '0',
                                 reads, 'ciRNA', gene, iso, index_info,
                                 intron])
            if denovo_flag:  # in denovo mode
                annotations.add(annotation_info)
            outf.write(bed + '\n')
    print('Fixed %d fusion junctions!' % total)
