'''
test_parse.py: Test parse module
'''

import os
import os.path
from nose.tools import with_setup
from .utils import check_fusion
from circ2.parse import parse


def setup_function():
    '''
    Enter data directory
    '''
    print('#%s: Moving to data directory' % __name__)
    os.chdir('data')


def teardown_function():
    '''
    Delete circ_out directory and leave data directory
    '''
    print('#%s: Remove test files' % __name__)
    os.remove('back_spliced_junction.bed')
    os.chdir('..')


@with_setup(setup_function, teardown_function)
def test_tophat_fusion_parse():
    '''
    Test TopHat-Fusion parser
    '''
    print('#%s: Test parse TopHat-Fusion' % __name__)
    options = {'-t': 'TopHat-Fusion', '--bed': 'back_spliced_junction.bed',
               '<fusion>': 'tophat_fusion.bam', '--pe': False, '-f': False}
    parse(options, command='CIRCexplorer2 parse (TopHat-Fusion)', name='parse')
    check_fusion('back_spliced_junction.bed',
                 'parse_TopHat_Fusion/fusion_junction.bed')


@with_setup(setup_function, teardown_function)
def test_tophat_fusion_pe_parse():
    '''
    Test TopHat-Fusion PE parser
    '''
    print('#%s: Test parse TopHat-Fusion' % __name__)
    options = {'-t': 'TopHat-Fusion', '--bed': 'back_spliced_junction.bed',
               '<fusion>': 'tophat_fusion_PE.bam', '--pe': True, '-f': True}
    parse(options, command='CIRCexplorer2 parse (TopHat-Fusion PE)',
          name='parse')
    check_fusion('back_spliced_junction.bed',
                 'parse_TopHat_Fusion_PE/fusion_junction.bed')


@with_setup(setup_function, teardown_function)
def test_star_parse():
    '''
    Test STAR parser
    '''
    print('#%s: Test parse STAR' % __name__)
    options = {'-t': 'STAR', '--bed': 'back_spliced_junction.bed',
               '<fusion>': 'Chimeric.out.junction', '--pe': False}
    parse(options, command='CIRCexplorer2 parse (STAR)', name='parse')
    check_fusion('back_spliced_junction.bed', 'parse_STAR/fusion_junction.bed')


@with_setup(setup_function, teardown_function)
def test_mapsplice_parse():
    '''
    Test MapSplice parser
    '''
    print('#%s: Test parse MapSplice' % __name__)
    options = {'-t': 'MapSplice', '--bed': 'back_spliced_junction.bed',
               '<fusion>': 'fusions_raw.txt', '--pe': False}
    parse(options, command='CIRCexplorer2 parse (Mapsplice)', name='parse')
    check_fusion('back_spliced_junction.bed',
                 'parse_MapSplice/fusion_junction.bed')


@with_setup(setup_function, teardown_function)
def test_bwa_parse():
    '''
    Test BWA parser
    '''
    print('#%s: Test parse BWA' % __name__)
    options = {'-t': 'BWA', '--bed': 'back_spliced_junction.bed',
               '<fusion>': 'RNA_seq_bwa.sam', '--pe': False}
    parse(options, command='CIRCexplorer2 parse (BWA)', name='parse')
    check_fusion('back_spliced_junction.bed', 'parse_BWA/fusion_junction.bed')


@with_setup(setup_function, teardown_function)
def test_segemehl_parse():
    '''
    Test segemehl parser
    '''
    print('#%s: Test parse segemehl' % __name__)
    options = {'-t': 'segemehl', '--bed': 'back_spliced_junction.bed',
               '<fusion>': 'splicesites.bed', '--pe': False}
    parse(options, command='CIRCexplorer2 parse (segemehl)', name='parse')
    check_fusion('back_spliced_junction.bed',
                 'parse_segemehl/fusion_junction.bed')
