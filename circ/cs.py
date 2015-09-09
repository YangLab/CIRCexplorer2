'''
Usage: CIRCexplorer2 cs [options] -g GENOME <circ_out>

Options:
    -h --help                      Show help message.
    -v --version                   Show version.
    -g GENOME --genome=GENOME      Genome fasta file.
    -l LENGTH --length=LENGTH      Minimum element length. [default: 50]
    -p THREAD --thread=THREAD      Running threads. [default: 10]
    -o OUT --output=OUT            Output file. [default: circ_cs.txt]
    --tmp                          Keep temporary BLAST results.
'''

import time
import re
import pysam
import subprocess
import os
from multiprocessing import Pool
from collections import defaultdict
from file_parse import check_fasta
from dir_func import create_temp, delete_temp

__authors__ = ['Rui Dong (dongrui@picb.ac.cn)',
               'Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn)']

__all__ = ['cs']


def cs(options):
    local_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
    print('Start CIRCexplorer2 cs at %s' % local_time)
    # check fasta file
    fa_f = check_fasta(options['--genome'], pysam_flag=False)
    # check whether keep tmp files
    if options['--tmp']:
        tmp_flag = True
        os.mkdir('cs_tmp')
    else:
        tmp_flag = False
    with open(options['<circ_out>'], 'r') as circ:
        p = Pool(int(options['--thread']))
        results = []
        for line in circ:
            circ_type = line.split()[13]
            if circ_type == 'ciRNA':  # only check circRNAs
                continue
            left_intron, right_intron = line.split()[16].split('|')
            # not first/last exons
            if left_intron == 'None' or right_intron == 'None':
                continue
            circ_id = '\t'.join(line.split()[:3])
            length = int(options['--length'])
            results.append(p.apply_async(cal_cs, args=(fa_f, circ_id,
                                                       left_intron,
                                                       right_intron,
                                                       length, tmp_flag)))
        p.close()
        p.join()
    with open(options['--output'], 'w') as outf:
        for r in results:
            outf.write(r.get() + '\n')
    local_time = time.strftime('%H:%M:%S', time.localtime(time.time()))
    print('End CIRCexplorer2 cs at %s' % local_time)


def cal_cs(fa_f, circ_id, left_intron, right_intron, length, tmp_flag):
    '''
    1. Fetch intron sequences and run BLAST
    2. Filter BLAST results and create reflection between elements
    3. Calculate complementary score
    '''
    fa = pysam.FastaFile(fa_f)
    chrom, start, end = circ_id.split()
    start = int(start)
    end = int(end)
    # create temporary files
    if tmp_flag:
        folder = '%s_%d_%d' % (chrom, start, end)
        os.mkdir('cs_tmp/%s' % folder)
        left_f = 'cs_tmp/%s/left_intron.fa' % folder
        right_f = 'cs_tmp/%s/right_intron.fa' % folder
        across_f = 'cs_tmp/%s/across_blast.txt' % folder
    else:
        temp_dir, left_f, right_f = create_temp()
    # fetch intron sequences
    left_start, left_end = fetch_fa(fa, left_f, left_intron)
    right_start, right_end = fetch_fa(fa, right_f, right_intron)
    # blast alignments
    across_blast = run_blast(left_f, right_f)
    left_blast = run_blast(left_f, left_f)
    right_blast = run_blast(right_f, right_f)
    if tmp_flag:
        with open(across_f, 'w') as f:
            f.write(across_blast)
    # filter blast results
    across_blast_info = filter_blast(across_blast, left_start, right_start,
                                     length)
    left_blast_info = filter_blast(left_blast, left_start, left_start,
                                   length, within_flag=True)
    right_blast_info = filter_blast(right_blast, right_start, right_start,
                                    length, within_flag=True)
    # create reflection between elements for within pairings
    left_score, left_reflection = reflect(left_blast_info, length)
    right_score, right_reflection = reflect(right_blast_info, length)
    # calculate complementary score
    max_score, score1, score2, score3 = 0.0, 0.0, 0.0, 0.0
    left_region, right_region = 'NULL', 'NULL'
    for info in across_blast_info:
        (region1_start, region1_end,
         region2_start, region2_end,
         pair_score) = info
        symmetry_score = cal_symmetry_score(region1_end, start, end,
                                            region2_start)
        left_compete_score = cal_compete_score(region1_start, region1_end,
                                               left_score, left_reflection,
                                               left_blast_info)
        right_compete_score = cal_compete_score(region2_start, region2_end,
                                                right_score, right_reflection,
                                                right_blast_info)
        across_score = pair_score
        pairing_potential = across_score / (across_score + left_compete_score +
                                            right_compete_score)
        complementary_score = symmetry_score * pairing_potential * across_score
        if complementary_score > max_score:
            max_score = complementary_score
            score1 = symmetry_score
            score2 = pairing_potential
            score3 = across_score
            left_region = '%s:%d-%d' % (chrom, region1_start, region1_end)
            right_region = '%s:%d-%d' % (chrom, region2_start, region2_end)
    if not tmp_flag:
        delete_temp(temp_dir)
    return '\t'.join([circ_id, str(max_score), str(score1), str(score2),
                      str(score3), left_region, right_region])


def fetch_fa(fa, f_path, intron):
    chrom, start, end = re.split(':|-', intron)
    start = int(start)
    end = int(end)
    fasta = fa.fetch(chrom, start, end)
    with open(f_path, 'w') as f:
        f.write('>' + intron + '\n')
        f.write(fasta + '\n')
    return (start, end)


def run_blast(file1, file2):
    p = subprocess.Popen('blastn -query %s -subject %s ' % (file1, file2) +
                         '-word_size 11 -gapopen 5 -gapextend 2 -penalty -3 ' +
                         '-reward 2 -strand minus -outfmt 6',
                         shell=True, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE, close_fds=True)
    out, err = p.communicate()
    return out.decode('utf-8')


def filter_blast(blast_result, offset1, offset2, length, within_flag=False):
    blast_info = []
    for line in blast_result.split('\n')[:-1]:
        loc1, loc2, loc4, loc3 = [int(x) for x in line.split()[6:10]]
        e, blast_score = [float(x) for x in line.split()[10:]]
        if within_flag and loc3 < loc1:
            continue
        if loc2 - loc1 < length or loc4 - loc3 < length:
            continue
        if e > 1e-5:
            continue
        region1_start = offset1 + loc1
        region1_end = offset1 + loc2
        region2_start = offset2 + loc3
        region2_end = offset2 + loc4
        pair_score = cal_pair_score(region1_end, region2_start, blast_score)
        blast_info.append([region1_start, region1_end, region2_start,
                           region2_end, pair_score])
    return blast_info


def reflect(blast_info, length):
    reflection = {}
    score = defaultdict(float)
    if not blast_info:
        return (score, reflection)
    boundary = []
    score_info = defaultdict(float)
    for info in blast_info:
        (region1_start, region1_end,
         region2_start, region2_end,
         pair_score) = info
        region1 = '%d\t%d' % (region1_start, region1_end)
        region2 = '%d\t%d' % (region2_start, region2_end)
        if region1 not in score_info:
            boundary.append([region1_start, region1_end])
        score_info[region1] += pair_score
        if region2 not in score_info:
            boundary.append([region2_start, region2_end])
        score_info[region2] += pair_score
    boundary.sort()
    b1 = boundary[0]
    b1_info = '\t'.join(str(x) for x in b1)
    reflection[b1_info] = b1_info
    score[b1_info] = score_info[b1_info]
    for b2 in boundary[1:]:
        b2_info = '\t'.join(str(x) for x in b2)
        if b1[1] - b2[0] >= length:  # has overlap
            reflection[b2_info] = b1_info
            score[b1_info] += score_info[b2_info]
        else:  # no overlap
            reflection[b2_info] = b2_info
            score[b2_info] = score_info[b2_info]
            # refresh element
            b1 = b2
            b1_info = b2_info
    return (score, reflection)


def cal_pair_score(left, right, score):
    distance = ((right - left) * 1.0 / 1000) ** 2
    return score / distance


def cal_symmetry_score(left1, left2, right1, right2):
    left_length = left2 - left1
    right_length = right2 - right1
    if left_length <= right_length:
        return left_length * 1.0 / right_length
    else:
        return right_length * 1.0 / left_length


def cal_compete_score(start, end, score_info, reflection, blast_info):
    compete_score = 0
    for info in blast_info:
        (region1_start, region1_end,
         region2_start, region2_end,
         pair_score) = info
        overlap1 = overlap(start, end, region1_start, region1_end)
        overlap2 = overlap(start, end, region2_start, region2_end)
        within_score = pair_score
        if overlap1 >= (end - start) * 1.0 / 2:
            region1 = '%d\t%d' % (region1_start, region1_end)
            compete_potential = within_score / score_info[reflection[region1]]
            compete_score += within_score * compete_potential
        if overlap2 >= (end - start) * 1.0 / 2:
            region2 = '%d\t%d' % (region2_start, region2_end)
            compete_potential = within_score / score_info[reflection[region2]]
            compete_score += within_score * compete_potential
    return compete_score


def overlap(start1, end1, start2, end2):
    region = [[start1, end1], [start2, end2]]
    region.sort()
    if region[1][0] < region[0][1]:
        return region[0][1] - region[1][0]
    else:
        return 0
