# coding: utf-8

import os
from io_util import prepare_dir_for

class Cache(object):
    def __init__(self, cache_dir):
        self.dir = cache_dir
        self.d = {}

    def get(self, key):
        assert len(key) == 32
        if key in self.d:
            return self.d[key]

        head, tail = key[:2], key[2:]
        path = os.path.join(self.dir, head, tail)
        prepare_dir_for(path)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                return f.read()
        return None

    def set(self, key, value):
        assert len(key) == 32
        if self.get(key) == value:
            return
        self.d[key] = value
        head, tail = key[:2], key[2:]
        path = os.path.join(self.dir, head, tail)
        prepare_dir_for(path)
        with open(path, 'wb') as f:
            f.write(value)


