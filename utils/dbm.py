__author__ = 'SolPie'
import shelve

from utils import table, singleton


class DBM(object):
    def __init__(self, name=None):
        self.name = name
        pass

    def open(self, *arg):
        self.shelve = shelve.open(*arg)

    def get(self, key):
        return self.shelve[key]

    def set(self, key, value):
        self.shelve[key] = value

    def del_key(self, key):
        del self.shelve[key]

    def has_key(self, key):
        return self.shelve.has_key(key)

    def keys(self):
        return self.shelve.keys()

    def values(self):
        return self.shelve.values()

    def sync(self):
        if self.shelve:
            self.shelve.sync()

    def clear(self):
        self.shelve.clear()

    def del_value(self, value):
        for k in self.shelve.keys():
            if self.shelve.get(k) == value:
                self.del_key(k)

    def close(self):
        if self.shelve:
            self.shelve.close()


@singleton
class PhotoDBM(DBM):
    def __init__(self):
        pass


@table
class TrashDBM(DBM):
    name = 'trash'

    def __init__(self, name):
        self.name = name
        self.open('trash.dbm')