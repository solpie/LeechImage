__author__ = 'SolPie'
import hashlib


def md5_path(path):
    f = open(path, 'r')
    return md5_bytes(f.read())


def md5_bytes(b):
    md5 = hashlib.md5()
    md5.update(b)
    return md5.hexdigest()