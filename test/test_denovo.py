'''
test_denovo.py: Test denovo module
'''

import os.path
import shutil
from .utils import check_file
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
                   '--as': circ_path+'/as', '--as-type': 'CE',
                   '--abs': '',
                   '--bed': circ_path + '/fusion_junction.bed',
                   '--tophat': circ_path + '/tophat',
                   '--pAplus': pAplus_tophat_path,
                   '--cuff': circ_path + '/cufflinks',
                   '--no-fix': False,
                   '--rpkm': False, '--output': circ_path+'/denovo'}
        denovo(options, command='CIRCexplorer2 denovo', name='denovo')

    def testDenovo(self):
        '''
        Check files in denovo directory
        '''
        print('#%s: Test denovo' % __name__)
        denovo_path = 'data/denovo'
        as_path = 'data/as'
        assert os.path.isdir(denovo_path), 'No denovo directory'
        assert os.path.isdir(as_path), 'No as directory'
        # check files in denovo directory
        check_file(denovo_path + '/circularRNA_full.txt',
                   'data/denovo_result/circularRNA_full.txt')
        check_file(denovo_path + '/annotated_circ.txt',
                   'data/denovo_result/annotated_circ.txt')
        check_file(denovo_path + '/novel_circ.txt',
                   'data/denovo_result/novel_circ.txt')
        check_file(as_path + '/all_exon_info.txt',
                   'data/denovo_result/all_exon_info.txt')

    def teardown(self):
        '''
        Delete denovo directory
        '''
        print('#%s: End testing denovo' % __name__)
        shutil.rmtree('data/denovo')
        shutil.rmtree('data/as')
