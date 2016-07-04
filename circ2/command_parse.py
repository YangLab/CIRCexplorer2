#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Usage: CIRCexplorer2 (<command> | --help | --version)
'''

from docopt import docopt
import sys
from version import __version__

__author__ = 'Xiao-Ou Zhang (zhangxiaoou@picb.ac.cn)'

help_doc = '''
   ______________  ______                __
  / ____/  _/ __ \/ ____/__  _  ______  / /___  ________  _____
 / /    / // /_/ / /   / _ \| |/_/ __ \/ / __ \/ ___/ _ \/ ___/
/ /____/ // _, _/ /___/  __/>  </ /_/ / / /_/ / /  /  __/ /
\____/___/_/ |_|\____/\___/_/|_/ .___/_/\____/_/   \___/_/
                              /_/

Usage: CIRCexplorer2 <command> [options]

Command:
    align            Map circular RNA junction reads with TopHat2/TopHat-Fusion
    parse            Parse fusion junction information from other aligners
    annotate         Annotate circular RNA junction reads with gene annotations
    assemble         Assemble transcriptome for circular RNAs
    denovo           Fetch de novo circular RNA isoforms
'''


def main():
    # parse command
    command_log = 'CIRCexplorer parameters: ' + ' '.join(sys.argv)
    if len(sys.argv) == 1:
        sys.exit(help_doc)
    elif sys.argv[1] == '--version' or sys.argv[1] == '-v':
        sys.exit(__version__)
    elif sys.argv[1] == 'align':
        import align
        align.align(docopt(align.__doc__, version=__version__),
                    command=command_log, name='align')
    elif sys.argv[1] == 'parse':
        import parse
        parse.parse(docopt(parse.__doc__, version=__version__),
                    command=command_log, name='parse')
    elif sys.argv[1] == 'annotate':
        import annotate
        annotate.annotate(docopt(annotate.__doc__, version=__version__),
                          command=command_log, name='annotate')
    elif sys.argv[1] == 'assemble':
        import assemble
        assemble.assemble(docopt(assemble.__doc__, version=__version__),
                          command=command_log, name='assemble')
    elif sys.argv[1] == 'denovo':
        import denovo
        denovo.denovo(docopt(denovo.__doc__, version=__version__),
                      command=command_log, name='denovo')
    else:
        sys.exit(help_doc)


if __name__ == '__main__':
    main()
