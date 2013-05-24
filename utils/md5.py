__author__ = 'SolPie'
import hashlib


def md5_path(path):
    f = open(path, 'r')
    md5num = md5_bytes(f.read())
    f.close()
    return md5num


def md5_bytes(b):
    md5 = hashlib.md5()
    md5.update(b)
    return md5.hexdigest()