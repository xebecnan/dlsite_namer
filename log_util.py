# coding: utf-8

import os
import time

log_file = None

def logf_open(log_dir):
    global log_file
    assert log_file == None
    log_file = open(os.path.join(log_dir, time.strftime('%Y-%m-%d.log')), 'ab')

def logf_close():
    global log_file
    assert log_file != None
    log_file.close()

def logf_env(log_dir):
    class LogFEnv(object):
        def __enter__(self):
            logf_open(log_dir)

        def __exit__(self, exc_type, exc_value, traceback):
            logf_close()
    return LogFEnv()

def logf(v):
    try:
        print v.decode('utf8', 'ignore')
    except Exception, e:
        print e
    log_file.write('[')
    log_file.write(time.strftime('%Y-%m-%d %H:%M:%S'))
    log_file.write(']  ')
    log_file.write(v)
    log_file.write('\n')

