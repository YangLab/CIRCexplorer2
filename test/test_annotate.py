'''
test_annotate.py: Test annotate module
'''

import os.path
from .utils import check_file
from circ2.annotate import annotate


class TestAnnotate(object):

    def setup(self):
        '''
        Run CIRCexplorer2 annotate
        '''
        print('#%s: Start testing annotate' % __name__)
        circ_path = 'data'
        ref_path = circ_path + '/ref.txt'
        fa_path = circ_path + '/chr21.fa'
        options = {'--ref': ref_path, '--genome': fa_path,
                   '--no-fix': False,
                   '--bed': circ_path + '/fusion_junction.bed',
                   '--low-confidence': True,
                   '--output': 'circularRNA_known.txt'}
        annotate(options, command='CIRCexplorer2 annotate', name='annotate')

    def testAnnotate(self):
        '''
        Check files in annotate directory
        '''
        print('#%s: Test annotate' % __name__)
        # check circ_fusion.txt file
        check_file('circularRNA_known.txt',
                   'data/annotate_result/circ_fusion.txt')
        # check low_circ_fusion.txt file
        check_file('low_conf_circularRNA_known.txt',
                   'data/annotate_result/low_circ_fusion.txt')

    def teardown(self):
        '''
        Delete annotate directory
        '''
        print('#%s: End testing annotate' % __name__)
        os.remove('circularRNA_known.txt')
        os.remove('low_conf_circularRNA_known.txt')
