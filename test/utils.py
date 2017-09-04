import os


def compare_file(fn1, fn2):
    '''
    Test if two files are same
    '''
    with open(fn1, 'r') as f1, open(fn2, 'r') as f2:
        content1 = set(f1.readlines())
        content2 = set(f2.readlines())
        return content1 == content2


def check_file(f1, f2):
    '''
    Check if files are existed and same
    '''
    test_f = f1
    result_f = f2
    print('Check %s file...' % test_f)
    assert os.path.isfile(test_f), 'No %s file' % test_f
    assert compare_file(test_f, result_f), 'Difference in %s' % test_f


def check_fusion(f1, f2):
    '''
    Check if fusion files are same
    '''
    test_f = f1
    result_f = f2
    print('Check %s file...' % test_f)
    assert os.path.isfile(test_f), 'No %s file' % test_f
    with open(test_f, 'r') as f:
        test_fusion = {'\t'.join(line.split()[:3]):
                       line.split()[3].split('/')[1]
                       for line in f}
    with open(result_f, 'r') as f:
        result_fusion = {'\t'.join(line.split()[:3]):
                         line.split()[3].split('/')[1]
                         for line in f}
    for i in test_fusion:
        assert i in result_fusion, 'Difference in %s' % test_f
        assert test_fusion[i] == result_fusion[i], 'Difference in %s' % test_f
