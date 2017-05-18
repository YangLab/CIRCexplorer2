'''
test_annotate.py: Test annotate module
'''

import os.path
import shutil
from utils import check_file
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
                   '--no-fix': False, '<circ_dir>': circ_path,
                   '--low-confidence': True}
        annotate(options, command='CIRCexplorer2 annotate', name='annotate')

    def testAnnotate(self):
        '''
        Check files in annotate directory
        '''
        print('#%s: Test annotate' % __name__)
        result_path = 'data/annotate'
        assert os.path.isdir(result_path), 'No annotate directory'
        # check annotated_fusion.txt file
        check_file('annotated_fusion.txt', result_path, 'data/annotate_result')
        # check circ_fusion.txt file
        check_file('circ_fusion.txt', result_path, 'data/annotate_result')
        # check low_circ_fusion.txt file
        check_file('low_circ_fusion.txt', result_path, 'data/annotate_result')

    def teardown(self):
        '''
        Delete annotate directory
        '''
        print('#%s: End testing annotate' % __name__)
        shutil.rmtree('data/annotate')
