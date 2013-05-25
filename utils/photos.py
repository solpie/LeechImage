__author__ = 'SolPie'
import hashlib
import os


class Photo(object):
    md5num = None
    title = None
    slug = None
    path = None
    filename = None

    def __init__(self):
        pass

    def __str__(self):
        return '<Photo filename:%s md5:%s title:%s>' % (self.filename, self.md5num, self.title)


def walkImages(db, dir):
    for root, dirs, files in os.walk(dir):
        for filename in files:
            p = Photo()
            p.path = dir + filename
            p.filename = filename
            f = open(dir + filename, 'r')
            md5 = hashlib.md5()
            md5.update(f.read())
            p.md5num = md5.hexdigest()
            db.set(p.md5num, p)
            # print md5num, img_path, short_url.encode_url(md5num)
            f.close()
    db.sync()
    return db


def walkTrash(db, path):
    l = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            l.append(filename)
    db.set('trash', l)
    return l