__author__ = 'SolPie'
import hashlib
import os


def walkImages(db, path):
    for root, dirs, files in os.walk(path):
        for img_path in files:
            f = open(path + img_path, 'r')
            md5 = hashlib.md5()
            md5.update(f.read())
            md5num = md5.hexdigest()
            db[md5num] = img_path
            print md5num, img_path
            f.close()
    db.close()
    pass
