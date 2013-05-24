__author__ = 'SolPie'
import hashlib
import os
import utils.short_url as short_url


def walkImages(db, path):
    for root, dirs, files in os.walk(path):
        for img_path in files:
            f = open(path + img_path, 'r')
            md5 = hashlib.md5()
            md5.update(f.read())
            md5num = md5.hexdigest()
            db.set(md5num, img_path)
            # print md5num, img_path, short_url.encode_url(md5num)
            f.close()
    db.sync()
    pass
