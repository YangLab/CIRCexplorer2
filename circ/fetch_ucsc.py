#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
fetch_ucsc.py
Fetch relevant annotation or sequence files from UCSC.
author: Xiao-Ou Zhang <zhangxiaoou@picb.ac.cn>
'''

import sys
import urllib
import gzip
import string
import tarfile
import pysam


def main():
    if len(sys.argv) != 4:
        sys.exit('fetch_ucsc.py hg19/hg38/mm10 ref/kg/ens/fa out')
    if sys.argv[1] in {'hg19', 'hg38', 'mm10'}:
        path = 'http://hgdownload.soe.ucsc.edu/goldenPath/%s/' % sys.argv[1]
    else:
        sys.exit('Only support human or mouse!')
    s = string.maketrans(' ', '_')
    if sys.argv[2] == 'ref':  # RefSeq gene annotations
        urllib.urlretrieve(path + 'database/refFlat.txt.gz', 'refFlat.txt.gz')
        with open(sys.argv[3], 'w') as outf:
            outf.write(gzip.open('refFlat.txt.gz', 'rb').read())
    elif sys.argv[2] == 'kg':  # KnownGenes gene annotations
        urllib.urlretrieve(path + 'database/knownGene.txt.gz',
                           'knownGene.txt.gz')
        urllib.urlretrieve(path + 'database/kgXref.txt.gz', 'kgXref.txt.gz')
        kg_iso = {}
        with gzip.open('kgXref.txt.gz', 'rb') as kg_id_f:
            for line in kg_id_f:
                iso = line.split('\t')[0]
                gene = line.split('\t')[4].translate(s)
                kg_iso[iso] = gene
        with gzip.open('knownGene.txt.gz', 'rb') as kg_f:
            with open(sys.argv[3], 'w') as outf:
                for line in kg_f:
                    entry = line.split('\t')
                    iso = entry[0]
                    outf.write('\t'.join([kg_iso[iso]] + entry[:10]) + '\n')
    elif sys.argv[2] == 'ens':  # Ensembl gene annotations
        if sys.argv[1] == 'hg38':
            sys.exit('No Ensembl gene annotations for hg38!')
        urllib.urlretrieve(path + 'database/ensGene.txt.gz', 'ensGene.txt.gz')
        urllib.urlretrieve(path + 'database/ensemblToGeneName.txt.gz',
                           'ensemblToGeneName.txt.gz')
        ens_iso = {}
        with gzip.open('ensemblToGeneName.txt.gz', 'rb') as ens_id_f:
            for line in ens_id_f:
                iso, gene = line.split()
                ens_iso[iso] = gene
        with gzip.open('ensGene.txt.gz', 'rb') as ens_f:
            with open(sys.argv[3], 'w') as outf:
                for line in ens_f:
                    entry = line.split()
                    iso = entry[1]
                    outf.write('\t'.join([ens_iso[iso]] + entry[1:11]) + '\n')
    elif sys.argv[2] == 'fa':  # Genome sequences
        if sys.argv[1] == 'hg38':
            fa_path = 'bigZips/hg38.chromFa.tar.gz'
        else:
            fa_path = 'bigZips/chromFa.tar.gz'
        urllib.urlretrieve(path + fa_path, 'chromFa.tar.gz')
        with tarfile.open('chromFa.tar.gz', 'r:gz') as seq:
            with open(sys.argv[3], 'w') as outf:
                for f in seq:
                    outf.write(seq.extractfile(f).read())
        pysam.faidx(sys.argv[3])
    else:
        sys.exit('Only support ref/kg/ens/fa!')


if __name__ == '__main__':
    main()
