__author__ = 'SolPie'
import hashlib
import os


class Photo():
    md5num = None
    title = None
    slug = None
    path = None
    filename = None

    def __init__(self):
        pass

    def __str__(self):
        return '<Photo filename:%s md5:%s title:%s>' % (self.filename, self.md5num, self.title)


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


def walkTrash(db, path):
    l = []
    for root, dirs, files in os.walk(path):
        for filename in files:
            l.append(filename)
    db.set('trash', l)
    return l