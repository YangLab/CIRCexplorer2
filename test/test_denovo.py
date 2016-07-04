'''
test_denovo.py: Test denovo module
'''

import os.path
import shutil
from utils import check_file
from circ2.denovo import denovo


class TestDenovo(object):

    def setup(self):
        '''
        Run CIRCexplorer2 denovo
        '''
        print('$%s: Start testing denovo' % __name__)
        circ_path = 'data'
        ref_path = circ_path + '/ref.txt'
        fa_path = circ_path + '/chr21.fa'
        pAplus_tophat_path = circ_path + '/pAplus_tophat'
        options = {'--ref': ref_path, '--genome': fa_path,
                   '--as': True, '--as-type': 'CE',
                   '--pAplus': pAplus_tophat_path,
                   '--tophat-dir': None, '--no-fix': False,
                   '--rpkm': False, '<circ_dir>': circ_path}
        denovo(options, command='CIRCexplorer2 denovo', name='denovo')

    def testDenovo(self):
        '''
        Check files in denovo directory
        '''
        print('#%s: Test denovo' % __name__)
        result_path = 'data/denovo'
        assert os.path.isdir(result_path), 'No denovo directory'
        # check files in denovo directory
        file_list = ['annotated_fusion.txt', 'circ_fusion.txt',
                     'annotated_circ.txt', 'novel_circ.txt',
                     'all_exon_info.txt']
        for f in file_list:
            check_file(f, result_path, 'data/denovo_result')

    def teardown(self):
        '''
        Delete denovo directory
        '''
        print('#%s: End testing denovo' % __name__)
        shutil.rmtree('data/denovo')
