#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
fetch_ucsc.py
Fetch relevant annotation or sequence files from UCSC.
author: Xiao-Ou Zhang <zhangxiaoou@picb.ac.cn>
'''

import sys
import requests
import gzip
import tarfile
import pysam


def fetch_file(options):
    if len(options) != 4:
        sys.exit('fetch_ucsc.py hg19/hg38/mm9/mm10 ref/kg/ens/fa out')
    if options[1] in {'hg19', 'hg38', 'mm9', 'mm10'}:
        path = 'http://hgdownload.soe.ucsc.edu/goldenPath/%s/' % options[1]
    else:
        sys.exit('Only support human or mouse!')
    s = {32:95}
    if options[2] == 'ref':  # RefSeq gene annotations
        download_file(path + 'database/refFlat.txt.gz', 'refFlat.txt.gz')
        with open(options[3], 'wb') as outf:
            outf.write(gzip.open('refFlat.txt.gz', 'rb').read())
    elif options[2] == 'kg':  # KnownGenes gene annotations
        download_file(path + 'database/knownGene.txt.gz', 'knownGene.txt.gz')
        download_file(path + 'database/kgXref.txt.gz', 'kgXref.txt.gz')
        kg_iso = {}
        with gzip.open('kgXref.txt.gz', 'rb') as kg_id_f:
            for line in kg_id_f:
                iso = line.decode().split('\t')[0]
                gene = line.decode().split('\t')[4].translate(s)
                kg_iso[iso] = gene
        with gzip.open('knownGene.txt.gz', 'rb') as kg_f:
            with open(options[3], 'w') as outf:
                for line in kg_f:
                    entry = line.decode().split('\t')
                    iso = entry[0]
                    outf.write('\t'.join([kg_iso[iso]] + entry[:10]) + '\n')
    elif options[2] == 'ens':  # Ensembl gene annotations
        if options[1] == 'hg38' or options[1] == 'mm10':
            sys.exit('No Ensembl gene annotations for hg38 or mm10!')
        download_file(path + 'database/ensGene.txt.gz', 'ensGene.txt.gz')
        download_file(path + 'database/ensemblToGeneName.txt.gz',
                      'ensemblToGeneName.txt.gz')
        ens_iso = {}
        with gzip.open('ensemblToGeneName.txt.gz', 'rb') as ens_id_f:
            for line in ens_id_f:
                iso, gene = line.decode().split()
                ens_iso[iso] = gene
        with gzip.open('ensGene.txt.gz', 'rb') as ens_f:
            with open(options[3], 'w') as outf:
                for line in ens_f:
                    entry = line.decode().split()
                    iso = entry[1]
                    outf.write('\t'.join([ens_iso[iso]] + entry[1:11]) + '\n')
    elif options[2] == 'fa':  # Genome sequences
        if options[1] == 'hg38':
            fa_path = 'bigZips/hg38.chromFa.tar.gz'
        else:
            fa_path = 'bigZips/chromFa.tar.gz'
        download_file(path + fa_path, 'chromFa.tar.gz')
        with tarfile.open('chromFa.tar.gz', 'r:gz') as fa:
            with open(options[3], 'w') as outf:
                for f in fa:
                    if f.isfile():
                        content = fa.extractfile(f).read()
                        outf.write(content.decode())
        pysam.faidx(options[3])
    else:
        sys.exit('Only support ref/kg/ens/fa!')


def download_file(url, dest):
    r = requests.get(url, stream=True)
    with open(dest, 'wb') as f:
        for chunk in r.iter_content():
            f.write(chunk)


def main():
    fetch_file(sys.argv)


if __name__ == '__main__':
    main()
