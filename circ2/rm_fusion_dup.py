#!/usr/bin/env python

import sys
import pysam

if len(sys.argv) != 3:
    sys.exit('rm_dup.py in.bam out.bam')

bam_file = pysam.AlignmentFile(sys.argv[1], 'rb')
out_bam = pysam.AlignmentFile(sys.argv[2], 'wb', template=bam_file)

# to avoid the mate2 order is different from the mate1 order
removed = set()

bams = bam_file.fetch()
guard = (0, 0, 0)
for read in bams:
    if read.query_name in removed:
        continue
    elif read.has_tag('XF'):
        xf_tag = read.get_tag('XF').split()
        xf_tag = tuple(xf_tag[1:4])
        
        if xf_tag == guard:
            removed.add(read.query_name)
            continue

        guard = xf_tag
        out_bam.write(read)
    else:
        out_bam.write(read)

out_bam.close()
bam_file.close()
