# coding: utf8

import os
import hashlib

def get_file_md5(path):
    m = hashlib.md5()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            m.update(chunk)
    return m.hexdigest()

def get_hash(v):
    m = hashlib.md5()
    m.update(v)
    return m.hexdigest()

class HashStore(object):
    def __init__(self, store_dir):
        self.store_dir = store_dir

    def check_hash(self, h):
        head, tail = h[:2], h[2:]
        path = os.path.join(self.store_dir, head)
        if os.path.exists(path):
            with open(path, 'rb') as f:
                for line in f:
                    if line.startswith(tail):
                        return True
        return False

    def write_hash(self, h):
        if self.check_hash(h):
            return
        head, tail = h[:2], h[2:]
        path = os.path.join(self.store_dir, head)
        with open(path, 'ab') as f:
            f.write(tail)
            f.write('\n')

    def check_data(self, data):
        return self.check_hash(get_hash(data))

    def write_data(self, data):
        return self.write_hash(get_hash(data))

