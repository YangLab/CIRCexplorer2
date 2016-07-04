import sys
import os
import os.path
import math
import time
from collections import defaultdict
from string import maketrans
from functools import wraps
import pysam


def which(program):
    '''
    Check the path of external programs, and source codes are modified from
    https://github.com/infphilo/tophat/blob/master/src/tophat.py.
    '''
    def is_executable(fpath):
        return os.path.isfile(fpath) and os.access(fpath, os.X_OK)
    for path in os.environ["PATH"].split(os.pathsep):
        progpath = os.path.join(path, program)
        if is_executable(progpath):
            return progpath
    return None


def logger(fn):
    '''
    Record parameters and runming time
    '''
    @wraps(fn)
    def wrapper(*args, **kwargs):
        print(kwargs['command'])
        local_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        print('Start CIRCexplorer2 %s at %s' % (kwargs['name'], local_time))
        fn(*args)
        local_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
        print('End CIRCexplorer2 %s at %s' % (kwargs['name'], local_time))
    return wrapper


class Expression(object):
    def __init__(self, bam_f):
        if not os.path.isfile(bam_f + '.bai'):  # index bam if not exist
            pysam.index(bam_f)
        self.bam = pysam.AlignmentFile(bam_f, 'rb')
        self.total_reads = self.bam.mapped
        for read in self.bam:
            read_length = read.query_length
            break
        self.total_bases = self.total_reads * read_length

    def rpkm(self, chrom, start, end):
        bases = 0
        region_length = end - start
        for read in self.bam.fetch(chrom, start, end):
            bases += read.get_overlap(start, end)
        return (bases * math.pow(10, 9)) * 1.0 / (self.total_bases *
                                                  region_length)


def map_fusion_to_iso(start, end, strand, iso_info):
    starts = iso_info[0]
    ends = iso_info[1]
    # check sequnence within +/-10bp
    start_points = list(range(start - 10, start + 11))
    end_points = list(range(end - 10, end + 11))
    start_index, end_index = None, None
    start_intron_flag, end_intron_flag = False, False
    # check starts
    for i, s in enumerate(starts):
        if s in start_points:
            start_index = i
            break
    else:
        for j, e in enumerate(ends):
            if e in start_points:
                if j != len(ends) - 1:
                    start_index = j
                    start_intron_flag = True
                    break
    # check ends
    for j, e in enumerate(ends):
        if e in end_points:
            end_index = j
            break
    else:
        for i, s in enumerate(starts):
            if s in end_points:
                if i != 0:
                    end_index = i - 1
                    end_intron_flag = True
                    break
    # ciRNAs
    if start_intron_flag and strand == '+' and end < starts[start_index + 1]:
        return ('\t'.join(['1', str(end - start), '0', 'ciRNA']),
                str(start_index), False)
    elif end_intron_flag and strand == '-' and start > ends[end_index]:
        return ('\t'.join(['1', str(end - start), '0', 'ciRNA']),
                str(end_index), False)
    # back spliced exons
    elif (start_index is not None and end_index is not None and
          not start_intron_flag and not end_intron_flag):
        if start_index != 0 and end_index != len(ends) - 1:
            edge_flag = False
        else:
            edge_flag = True
        return convert_to_bed(start, end,
                              starts[start_index:(end_index + 1)],
                              ends[start_index:(end_index + 1)],
                              str(start_index), str(end_index), edge_flag)
    else:
        return(None, None, False)


def convert_to_bed(start, end, starts, ends, start_index, end_index, edge):
    new_starts = [start] + starts[1:]
    new_ends = ends[:-1] + [end]
    block_starts, block_sizes = [], []
    for s, e in zip(new_starts, new_ends):
        block_starts.append(str(s - start))
        block_sizes.append(str(e - s))
    length = len(block_sizes)
    block_starts = ','.join(block_starts)
    block_sizes = ','.join(block_sizes)
    index = ','.join([start_index, end_index])
    return ('\t'.join([str(length), block_sizes, block_starts, 'circRNA']),
            index, edge)


def fix_bed(fusion_file, ref, fa, no_fix, denovo_flag):
    fusions = defaultdict(int)
    # make sure order of fusion names according to fusion_file
    fusion_names = []
    fusion_set = set()
    fixed_flag = defaultdict(int)  # flag to indicate realignment
    junctions = set()
    with open(fusion_file, 'r') as f:
        for line in f:
            chrom = line.split()[0]
            strand = line.split()[5]
            start, end = [int(x) for x in line.split()[1:3]]
            junction_info = '%s\t%d\t%d' % (chrom, start, end)
            if not denovo_flag and junction_info in junctions:
                continue
            reads = int(line.split()[3].split('/')[1])
            flag, gene, iso, index = line.split()[-4:]
            flag = True if flag == 'ciRNA' else False
            name = '\t'.join([gene, iso, chrom, strand, index])
            iso_starts, iso_ends = ref['\t'.join([gene, iso, chrom, strand])]
            if not flag:  # back spliced exons
                s, e = [int(x) for x in index.split(',')]
                # not realign
                if start == iso_starts[s] and end == iso_ends[e]:
                    fusions[name] += reads
                    if name not in fusion_set:
                        fusion_set.add(name)
                        fusion_names.append(name)
                    junctions.add(junction_info)
                # no fix mode
                elif no_fix:
                    fusions[name] += reads
                    if name not in fusion_set:
                        fusion_set.add(name)
                        fusion_names.append(name)
                    fixed_flag[name] += 1
                    junctions.add(junction_info)
                # realign
                elif check_seq(chrom, [start, iso_starts[s], end, iso_ends[e]],
                               fa):
                    fusions[name] += reads
                    if name not in fusion_set:
                        fusion_set.add(name)
                        fusion_names.append(name)
                    fixed_flag[name] += 1
                    junctions.add(junction_info)
            else:  # ciRNAs
                index = int(index)
                if strand == '+':
                    # not realign
                    if start == iso_ends[index]:
                        name += '|'.join(['', str(start), str(end)])
                        fusions[name] += reads
                        if name not in fusion_set:
                            fusion_set.add(name)
                            fusion_names.append(name)
                        junctions.add(junction_info)
                    # realign
                    elif check_seq(chrom, [start, iso_ends[index], end], fa,
                                   intron_flag=True):
                        fixed_start = iso_ends[index]
                        fixed_end = end + fixed_start - start
                        name += '|'.join(['', str(fixed_start),
                                          str(fixed_end)])
                        fusions[name] += reads
                        if name not in fusion_set:
                            fusion_set.add(name)
                            fusion_names.append(name)
                        fixed_flag[name] += 1
                        junctions.add(junction_info)
                else:
                    if end == iso_starts[index + 1]:
                        # not realign
                        name += '|'.join(['', str(start), str(end)])
                        fusions[name] += reads
                        if name not in fusion_set:
                            fusion_set.add(name)
                            fusion_names.append(name)
                        junctions.add(junction_info)
                        # realign
                    elif check_seq(chrom, [end, iso_starts[index + 1], start],
                                   fa, intron_flag=True):
                        fixed_end = iso_starts[index + 1]
                        fixed_start = start + fixed_end - end
                        name += '|'.join(['', str(fixed_start),
                                          str(fixed_end)])
                        fusions[name] += reads
                        if name not in fusion_set:
                            fusion_set.add(name)
                            fusion_names.append(name)
                        fixed_flag[name] += 1
                        junctions.add(junction_info)
    return (fusions, fusion_names, fixed_flag)


def check_seq(chrom, pos, fa, intron_flag=False):
    if not intron_flag:  # back spliced exons
        if pos[0] - pos[1] != pos[2] - pos[3]:
            return False
        if pos[0] < pos[1]:
            seq1 = fa.fetch(chrom, pos[0], pos[1])
            seq2 = fa.fetch(chrom, pos[2], pos[3])
        else:
            seq1 = fa.fetch(chrom, pos[1], pos[0])
            seq2 = fa.fetch(chrom, pos[3], pos[2])
    else:  # ciRNAs
        if abs(pos[0] - pos[1]) <= 5:  # permit mismatches within 5bp
            return True
        elif pos[0] < pos[1]:
            seq1 = fa.fetch(chrom, pos[0], pos[1])
            seq2 = fa.fetch(chrom, pos[2], pos[2] + pos[1] - pos[0])
        else:
            seq1 = fa.fetch(chrom, pos[1], pos[0])
            seq2 = fa.fetch(chrom, pos[2] - pos[0] + pos[1], pos[2])
    if seq1 == seq2:
        return True
    else:
        return False


def generate_bed(start, starts, ends):
    sizes, offsets = [], []
    for s, e in zip(starts, ends):
        sizes.append(str(e - s))
        offsets.append(str(s - start))
    sizes = ','.join(sizes)
    offsets = ','.join(offsets)
    return (sizes, offsets)


def genepred_to_bed(genepred, bed):
    with open(genepred, 'r') as genepred_f, open(bed, 'w') as bed_f:
        for line in genepred_f:
            (gene, iso,
             chrom, strand,
             start, end,
             cds_s, cds_e, n) = line.split()[:9]
            iso_id = '%s/%s' % (gene, iso)
            starts = [int(x) for x in line.split()[9].split(',')[:-1]]
            ends = [int(x) for x in line.split()[10].split(',')[:-1]]
            sizes, offsets = [], []
            for s, e in zip(starts, ends):
                sizes.append(str(e - s))
                offsets.append(str(s - int(start)))
            size = ','.join(sizes)
            offset = ','.join(offsets)
            bed_f.write('\t'.join([chrom, start, end, iso_id, '0', strand,
                                   cds_s, cds_e, '0,0,0', n, size, offset]))
            bed_f.write('\n')


def fetch_psi(exon, junc, left_junc, right_junc, max_flag=None):
    chrom, start, end = exon.split()
    if max_flag:  # predefine max_left and max_right
        max_left = '\t'.join([chrom, max_flag[0]])
        max_right = '\t'.join([chrom, max_flag[1]])
        max_left_right_read = junc['\t'.join([chrom] + max_flag)]
    else:
        max_left, max_right = '', ''
        max_read, max_left_right_read = 0, 0
    # #######------#############-------########
    #     left   right_id   left_id   right
    right_id = '%s\t%s' % (chrom, start)
    left_id = '%s\t%s' % (chrom, end)
    tmp_set = set()
    # inclusion read
    inclusion_read = 0
    for left_info in right_junc[right_id]:
        left, left_read = left_info
        inclusion_read += left_read
        for right_info in left_junc[left_id]:
            right, right_read = right_info
            if right not in tmp_set:  # make sure only counting once
                inclusion_read += right_read
                tmp_set.add(right)
            if not max_flag:
                left_right_read = junc['\t'.join([chrom, left, right])]
                total_read = left_read + right_read + left_right_read
                if total_read >= max_read:
                    max_read = total_read
                    max_left_right_read = left_right_read
                    max_left = '\t'.join([chrom, left])
                    max_right = '\t'.join([chrom, right])
    # exclusion read
    exclusion_read = 0
    for info in left_junc[max_left]:
        right, right_read = info
        if int(right) > int(end):  # include cassette exon
            exclusion_read += right_read
    for info in right_junc[max_right]:
        left, left_read = info
        if int(left) < int(start):  # include cassette exon
            exclusion_read += left_read
    exclusion_read -= max_left_right_read
    if inclusion_read == 0 and exclusion_read == 0:
        psi = 0
    else:
        psi = 100.0 * inclusion_read / (inclusion_read + 2 * exclusion_read)
    if max_flag is None:
        if max_left:
            max_left = max_left.split()[1]
        else:
            max_left = 'None'
        if max_right:
            max_right = max_right.split()[1]
        else:
            max_right = 'None'
        return (psi, inclusion_read, exclusion_read, max_left, max_right)
    else:
        return (psi, inclusion_read, exclusion_read)


def fetch_anchor(fa, chrom, start, end, strand):
    seq = fa.fetch(chrom, start, end)
    if strand == '+':
        seq = seq.upper()
    else:
        table = maketrans('ATCG', 'TAGC')
        seq = seq.upper().translate(table)[::-1]
    return seq


def fetch_read(bam, chrom, start, end, flag=1):
    region_length = end - start
    reads = 0
    for read in bam.fetch(chrom, start, end):
        base = read.get_overlap(start, end)
        if flag and base >= region_length:
            reads += 1
        elif not flag:
            reads += base
    if not flag:
        reads /= region_length
    return reads


def link_index(i, index_file, out_dir):
    if i == 1:  # bowtie1 index
        suffix = ['.1.ebwt', '.2.ebwt', '.3.ebwt', '.4.ebwt', '.rev.1.ebwt',
                  '.rev.2.ebwt']
    else:  # bowtie2 index
        suffix = ['.1.bt2', '.2.bt2', '.3.bt2', '.4.bt2', '.rev.1.bt2',
                  '.rev.2.bt2']
    prefix = os.path.split(index_file)[1]
    for s in suffix:
        f_abs = os.path.abspath(index_file + s)
        f_name = prefix + s
        if os.path.isfile(f_abs):
            os.symlink(f_abs, '%s/bowtie%d_index/%s' % (out_dir, i, f_name))
        else:
            sys.exit('Error: lack index file %s!' % f_name)
    return prefix


def build_index(i, genome_file, prefix, out_dir):
    if i == 1:
        v = ''
    else:
        v = '2'
    prog = 'bowtie%s-build' % v
    if which(prog) is None:
        sys.exit('%s is required to build index!' % prog)
    index_file = '%s/bowtie%d_index/%s' % (out_dir, i, prefix)
    return_code = os.system('%s %s %s > %s/bowtie%d_index.log' %
                            (prog, genome_file, index_file, out_dir, i)) >> 8
    if return_code:
        sys.exit('Error: cannot build index for bowtie%d!' % i)
