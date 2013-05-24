__author__ = 'SolPie'
from . import singleton
import shelve

@singleton
class DBM():
    def __init__(self):
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

    def sync(self):
        if self.shelve:
            self.shelve.sync()

    def close(self):
        if self.shelve:
            self.shelve.close()