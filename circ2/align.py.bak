'''
Usage: CIRCexplorer2 align [options] -G GTF (-g GENOME | -i INDEX1 -j INDEX2 \
| -i INDEX1 | -j INDEX1) <fastq>...

Options:
    -h --help                      Show help message.
    -v --version                   Show version.
    -G GTF --gtf=GTF               Annotation GTF file.
    -g GENOME --genome=GENOME      Genome fasta file.
    -i INDEX1 --bowtie1=INDEX1     Index files for Bowtie1 (used for \
TopHat-Fusion).
    -j INDEX2 --bowtie2=INDEX2     Index files for Bowtie2 (used for TopHat2).
    -p THREAD --thread=THREAD      Running threads. [default: 10]
    -o OUT --output=OUT            Output directory. [default: circ_out]
    --bw                           Create BigWig file.
    --scale                        Scale to HPB.
    --skip-tophat                  Skip TopHat mapping.
    --skip-tophat-fusion           Skip TopHat-Fusion mapping.
'''

import sys
import os
import os.path
import pysam
import pybedtools
from parse import tophat_fusion_parse
from helper import logger, which, link_index, build_index
from dir_func import create_dir

__author__ = 'Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn)'

__all__ = ['align']


@logger
def align(options):
    # check options
    if options['--skip-tophat'] and options['--skip-tophat-fusion']:
        sys.exit('Cannot set --skip-tophat and --skip-tophat-fusion together!')
    if not options['--genome']:
        if not options['--bowtie1'] and not options['--skip-tophat-fusion']:
            sys.exit('TopHat-Fusion require bowtie1 index files!')
        elif not options['--bowtie2'] and not options['--skip-tophat']:
            sys.exit('TopHat2 require bowtie2 index files!')
    skip_tophat = True if options['--skip-tophat'] else False
    skip_tophat_fusion = True if options['--skip-tophat-fusion'] else False
    # check output directory
    out_dir = check_outdir(options['--output'])
    # check tophat
    if which('tophat2') is None:
        sys.exit('TopHat2 is required for CIRCexplorer2 align!')
    # check index files
    if options['--genome']:  # build index
        index_flag = (True, skip_tophat, skip_tophat_fusion)
        prefix1, prefix2 = check_index(index_flag, out_dir,
                                       options['--genome'],
                                       options['--thread'])
    else:  # index exist
        index_flag = (False, skip_tophat, skip_tophat_fusion)
        prefix1, prefix2 = check_index(index_flag, out_dir,
                                       (options['--bowtie1'],
                                        options['--bowtie2']),
                                       options['--thread'])
    if not skip_tophat:
        # tophat2 mapping
        tophat_map(options['--gtf'], out_dir, prefix2, options['<fastq>'],
                   options['--thread'], bw=options['--bw'],
                   scale=options['--scale'])
    if not skip_tophat_fusion:
        # tophat fusion mapping
        if skip_tophat:  # skip tophat, so use fastq files directly
            tophat_fusion_map(out_dir, prefix1, options['--thread'],
                              fq=options['<fastq>'])
        else:
            tophat_fusion_map(out_dir, prefix1, options['--thread'])
        # parse tophat fusion results
        fusion_bam_f = '%s/tophat_fusion/accepted_hits.bam' % out_dir
        out = '%s/fusion_junction.bed' % out_dir
        tophat_fusion_parse(fusion_bam_f, out)


def check_outdir(out_dir):
    '''
    1. Clear output directory if not empty
    2. Create essential subdirectories
    '''
    print('Check output directory...')
    # clear output directory if not empty
    create_dir(out_dir)
    dir_path = os.path.abspath(out_dir)
    # create essential subdirectories
    os.mkdir(dir_path + '/bowtie1_index')
    os.mkdir(dir_path + '/bowtie2_index')
    os.mkdir(dir_path + '/tophat')
    os.mkdir(dir_path + '/tophat_fusion')
    return dir_path


def check_index(index_flag, out_dir, index_file, thread):
    '''
    1. Build index for Bowtie1 and Bowtie2 if not exist
    2. Links index files if exist
    '''
    print('Check index files....')
    genome_flag, skip_tophat, skip_tophat_fusion = index_flag
    if genome_flag:  # index files not exist
        prefix = os.path.split(index_file)[1]
        if not skip_tophat_fusion:  # not skip TopHat-Fusion
            # build index for bowtie1
            print('Build index for Bowtie1...')
            build_index(1, index_file, prefix, out_dir, thread)
        if not skip_tophat:  # not skip TopHat2
            # build index for bowtie2
            print('Build index for Bowtie2...')
            build_index(2, index_file, prefix, out_dir, thread)
        return (prefix, prefix)
    else:  # index files exist
        if not skip_tophat_fusion:  # not skip TopHat-Fusion
            # link index files for bowtie1
            print('Link index files for Bowtie1...')
            prefix1 = link_index(1, index_file[0], out_dir)
        else:
            prefix1 = ''
        if not skip_tophat:  # not skip TopHat2
            # link index files for bowtie2
            print('Link index files for Bowtie2...')
            prefix2 = link_index(2, index_file[1], out_dir)
        else:
            prefix2 = ''
        return (prefix1, prefix2)


def tophat_map(gtf, out_dir, prefix, fastq, thread, bw=False, scale=False,
               gtf_flag=1):
    '''
    1. Map reads with TopHat2
    2. Extract unmapped reads
    3. Create BigWig file if needed
    '''
    # tophat2 mapping
    print('Map reads with TopHat2...')
    tophat_cmd = 'tophat2 -g 1 --microexon-search -m 2 '
    if gtf_flag:
        tophat_cmd += '-G %s ' % gtf
    tophat_cmd += '-p %s -o %s ' % (thread, out_dir + '/tophat')
    tophat_cmd += '%s/bowtie2_index/%s ' % (out_dir, prefix) + ','.join(fastq)
    tophat_cmd += ' 2> %s/tophat.log' % out_dir
    print('TopHat2 mapping command:')
    print(tophat_cmd)
    return_code = os.system(tophat_cmd) >> 8
    if return_code:
        sys.exit('Error: cannot map reads with TopHat2!')
    # extract unmapped reads
    print('Extract unmapped reads...')
    unmapped_bam = pybedtools.BedTool('%s/tophat/unmapped.bam' % out_dir)
    unmapped_bam.bam_to_fastq(fq='%s/tophat/unmapped.fastq' % out_dir)
    # create Bigwig file if needed
    if bw and which('bedGraphToBigWig') is not None:
        print('Create BigWig file...')
        map_bam_fname = '%s/tophat/accepted_hits.bam' % out_dir
        # index bam if not exist
        if not os.path.isfile(map_bam_fname + '.bai'):
            pysam.index(map_bam_fname)
        map_bam = pysam.AlignmentFile(map_bam_fname, 'rb')
        # extract chrom size file
        chrom_size_fname = '%s/tophat/chrom.size' % out_dir
        with open(chrom_size_fname, 'w') as chrom_size_f:
            for seq in map_bam.header['SQ']:
                chrom_size_f.write('%s\t%s\n' % (seq['SN'], seq['LN']))
        if scale:  # scale to HPB
            mapped_reads = map_bam.mapped
            for read in map_bam:
                read_length = read.query_length
                break
            s = 1000000000.0 / mapped_reads / read_length
        else:
            s = 1
        map_bam = pybedtools.BedTool(map_bam_fname)
        bedgraph_fname = '%s/tophat/accepted_hits.bg' % out_dir
        with open(bedgraph_fname, 'w') as bedgraph_f:
            for line in map_bam.genome_coverage(bg=True, g=chrom_size_fname,
                                                scale=s, split=True):
                value = str(int(float(line[3]) + 0.5))
                bedgraph_f.write('\t'.join(line[:3]) + '\t%s\n' % value)
        bigwig_fname = '%s/tophat/accepted_hits.bw' % out_dir
        return_code = os.system('bedGraphToBigWig %s %s %s' %
                                (bedgraph_fname, chrom_size_fname,
                                 bigwig_fname)) >> 8
        if return_code:
            sys.exit('Error: cannot convert bedGraph to BigWig!')
    else:
        print('Could not find bedGraphToBigWig, so skip this step!')


def tophat_fusion_map(out_dir, prefix, thread, fq=None):
    '''
    1. Map reads with TopHat-Fusion
    2. Extract fusion junction reads
    '''
    # tophat_fusion mapping
    print('Map unmapped reads with TopHat-Fusion...')
    if fq:
        fastq = ','.join(fq)
    else:
        fastq = '%s/tophat/unmapped.fastq' % out_dir
    tophat_fusion_cmd = 'tophat2 --fusion-search --keep-fasta-order --bowtie1 '
    tophat_fusion_cmd += '--no-coverage-search '
    tophat_fusion_cmd += '-p %s -o %s ' % (thread, out_dir + '/tophat_fusion')
    tophat_fusion_cmd += '%s/bowtie1_index/%s ' % (out_dir, prefix)
    tophat_fusion_cmd += fastq
    tophat_fusion_cmd += ' 2> %s/tophat_fusion.log' % out_dir
    print('TopHat-Fusion mapping command:')
    print(tophat_fusion_cmd)
    return_code = os.system(tophat_fusion_cmd) >> 8
    if return_code:
        sys.exit('Error: cannot map unmapped reads with TopHat-Fusion!')
