'''
Set up some stuff for unit testing
'''

import os
from utils import download_fa


def setup_package():
    print('#test.__init__: Start testing')
    os.chdir('test')
    download_fa('data')


def teardown_package():
    print('#test.__init__: End testing')
    os.remove('data/chromFa.tar.gz')
    os.remove('data/hg19.fa')
    os.remove('data/hg19.fa.fai')
