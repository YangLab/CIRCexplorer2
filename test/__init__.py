'''
Set up some stuff for unit testing
'''

import os


def setup_package():
    print('#test.__init__: Start testing')
    os.chdir('test')


def teardown_package():
    print('#test.__init__: End testing')
