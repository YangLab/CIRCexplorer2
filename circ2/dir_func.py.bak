import sys
import os.path
import shutil
import tempfile


def check_dir(dir):
    '''
    Check directory
    '''
    if os.path.isdir(dir):
        dir_path = os.path.abspath(dir)
    else:
        sys.exit('Error: your directory %s is wrong!' % dir)
    return dir_path


def create_dir(dir):
    '''
    Check and create directory
    '''
    if os.path.isdir(dir):
        if os.listdir(dir):
            print('Warning: the directory %s is not empty!' % dir)
        shutil.rmtree(dir)
    os.mkdir(dir)


def create_temp():
    temp_dir = tempfile.mkdtemp()
    temp1 = temp_dir + '/tmp1'
    temp2 = temp_dir + '/tmp2'
    return (temp_dir, temp1, temp2)


def delete_temp(temp_dir):
    shutil.rmtree(temp_dir)
