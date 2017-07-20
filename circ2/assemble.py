'''
Usage: CIRCexplorer2 assemble [options] -r REF <circ_dir>

Options:
    -h --help                      Show help message.
    -v --version                   Show version.
    -r REF --ref=REF               Gene annotation file.
    -p THREAD --thread=THREAD      Running threads. [default: 10]
    --bb                           Convert assembly results to BigBed.
    --tophat-dir=TOPHAT_DIR        TopHat mapping directory.
    --chrom-size=CHROM_SIZE        Chrom size file for converting to BigBed.
    --remove-rRNA                  Ignore rRNA during assembling (only for \
human hg19).
    --max-bundle-frags=FRAGMENTS   Cufflinks --max-bundle-frags option.
'''

import sys
import os
import os.path
from parser import parse_junc
from helper import logger, which, genepred_to_bed
from dir_func import check_dir, create_dir
import pybedtools
import pysam

__author__ = 'Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn)'

__all__ = ['assemble']


@logger
def assemble(options):
    # check output directory
    out_dir = check_dir(options['<circ_dir>'])
    # check tophat results
    if options['--tophat-dir']:
        tophat_dir = check_dir(options['--tophat-dir'])
    else:
        tophat_dir = check_dir(out_dir + '/tophat')
    # check cufflinks
    if which('cufflinks') is None:
        sys.exit('Cufflinks is required for CIRCexplorer2 assemble!')
    # check genePredToGtf
    if which('genePredToGtf') is None:
        sys.exit('genePredToGtf is required for CIRCexplorer2 assemble!')
    # check gtfToGenePred
    if which('gtfToGenePred') is None:
        sys.exit('gtfToGenePred is required for CIRCexplorer2 assemble!')
    # prepare cufflinks directory
    cufflinks_dir = out_dir + '/cufflinks'
    create_dir(cufflinks_dir)
    # filter ref file
    ref_filter(options['--ref'], tophat_dir, out_dir)
    # assemble with cufflinks
    cufflinks_assemble(out_dir, tophat_dir, cufflinks_dir, options['--thread'],
                       options['--remove-rRNA'], options['--max-bundle-frags'])
    # convert assembly results
    convert_assembly_gtf(out_dir, cufflinks_dir, options['--ref'],
                         options['--bb'], options['--chrom-size'])


def ref_filter(ref, tophat_dir, out_dir):
    '''
    Extract isoform with at least two supported junction reads for each
    junction
    '''
    print('Read gene annotations...')
    # read junction information
    junction_f = tophat_dir + '/junctions.bed'
    junc = parse_junc(junction_f)
    print('Filter gene annotations with junction information...')
    # filter out gene annotations using junction reads
    filtered_junction_f = '%s/cufflinks/filtered_junction.txt' % out_dir
    with open(ref, 'r') as ref_f, open(filtered_junction_f, 'w') as out_f:
        for line in ref_f:
            chrom = line.split()[2]
            starts = line.split()[10].split(',')[:-2]
            ends = line.split()[9].split(',')[1:-1]
            for s, e in zip(starts, ends):
                junc_id = '%s\t%s\t%s' % (chrom, s, e)
                if junc[junc_id] < 2:
                    break
            else:  # all the junctions have enough reads
                out_f.write('\t'.join(line.split()[1:]) + '\n')
    filtered_junction_gtf = '%s/cufflinks/filtered_junction.gtf' % out_dir
    return_code = os.system('genePredToGtf file %s %s' %
                            (filtered_junction_f, filtered_junction_gtf)) >> 8
    if return_code:
        sys.exit('Error: cannot convert GenePred to GTF!')


def cufflinks_assemble(out_dir, tophat_dir, cufflinks_dir, thread, flag_rRNA,
                       fragments):
    '''
    Cufflinks RABT assembly
    '''
    # prepare cufflinks command
    gtf_path = '%s/cufflinks/filtered_junction.gtf' % out_dir
    bam_path = tophat_dir + '/accepted_hits.bam'
    if flag_rRNA:  # remove rRNA
        new_bam_path = '%s/tophat_no_rRNA.bam' % out_dir
        previous_bam = pysam.AlignmentFile(bam_path, 'rb')
        new_bam = pysam.AlignmentFile(new_bam_path, 'wb',
                                      template=previous_bam)
        for read in previous_bam:
            chr = previous_bam.getrname(read.reference_id)
            if chr != 'chrUn_gl000220':
                new_bam.write(read)
        previous_bam.close()
        new_bam.close()
        bam_path = new_bam_path
    cufflinks_cmd = 'cufflinks -u -F 0 -j 0 '
    cufflinks_cmd += '-p %s ' % thread
    if fragments:
        cufflinks_cmd += '--max-bundle-frags %s ' % fragments
    cufflinks_cmd += '-g %s -o %s %s ' % (gtf_path, cufflinks_dir, bam_path)
    cufflinks_cmd += '2> %s/cufflinks.log' % out_dir
    # run cufflinks
    print('Assemble with Cufflinks...')
    print('Cufflinks assemble command:')
    print(cufflinks_cmd)
    return_code = os.system(cufflinks_cmd) >> 8
    if return_code:
        sys.exit('Error: cannot assemble with Cufflinks!')


def convert_assembly_gtf(out_dir, cufflinks_dir, ref, bb, chrom_size):
    '''
    1. Convert Cufflinks GTF to GenePred
    2. Add gene symbols
    3. Convert to BigBed file if needed
    '''
    # convert cufflinks gtf to genepred
    print('Convert Cufflinks GTF to GenePred...')
    gtf_path = '%s/transcripts.gtf' % cufflinks_dir
    genePred_path = '%s/transcripts.txt' % cufflinks_dir
    return_code = os.system('gtfToGenePred %s %s' % (gtf_path,
                                                     genePred_path)) >> 8
    if return_code:
        sys.exit('Error: cannot convert gtf to GenePred!')
    # add gene symbol
    print('Add gene symbols...')
    with open(ref, 'r') as ref_f:
        gene_symbol = {line.split()[1]: line.split()[0] for line in ref_f}
    ref_path = '%s/transcripts_ref.txt' % cufflinks_dir
    with open(genePred_path, 'r') as genePred_f, open(ref_path, 'w') as ref_f:
        for line in genePred_f:
            iso = line.split()[0]
            symbol = gene_symbol[iso] if iso in gene_symbol else iso
            ref_f.write(symbol + '\t' + line)
    # convert to bigbed if needed
    if bb:
        if which('bedToBigBed') is not None:
            print('Convert to BigBed file...')
            if not chrom_size:  # no chrom size file, search it in tophat folder
                chrom_size = '%s/tophat/chrom.size' % out_dir
                if not os.path.isfile(chrom_size):
                    sys.exit('Please offer the path of chrom.size!')
            bed_path = '%s/transcripts_ref.bed' % cufflinks_dir
            genepred_to_bed(ref_path, bed_path)
            sorted_bed_path = '%s/transcripts_ref_sorted.bed' % cufflinks_dir
            bed = pybedtools.BedTool(bed_path)
            bed = bed.sort()
            bed.saveas(sorted_bed_path)
            bb_path = '%s/transcripts_ref_sorted.bb' % cufflinks_dir
            return_code = os.system('bedToBigBed -type=bed12 %s %s %s' %
                                    (sorted_bed_path, chrom_size, bb_path)) >> 8
            if return_code:
                sys.exit('Error: cannot convert bed to BigBed!')
        else:
            print('Could not find bedToBigBed, so skip this step!')
