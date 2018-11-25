# coding: utf-8

import os
import sys

enc = sys.stdout.encoding
if enc:
    def pe(s):
        print s.decode('utf-8').encode(enc)
else:
    def pe(s):
        print s

def prepare_dir(dirname):
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

def prepare_dir_for(filename):
    dirname = os.path.dirname(filename)
    prepare_dir(dirname)

