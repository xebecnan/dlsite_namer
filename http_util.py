# coding: utf-8

import requests
from hash_util import get_hash
from cache import Cache
from log_util import logf

TIMEOUT = 30

def proxy_get(*args, **kwds):
    proxies = {
        'http': 'http://127.0.0.1:8123',
        'https': 'http://127.0.0.1:8123',
    }
    kwds['proxies'] = proxies
    return strong_requests_get(*args, **kwds)

def strong_requests_get(*args, **kwds):
    kwds['timeout'] = kwds.get('timeout', TIMEOUT)
    for i in xrange(3):
        try:
            return requests.get(*args, **kwds)
        except Exception, e:
            logf('[http-get] error: {}'.format(str(e)))
            logf('[http-get] retry: {}'.format(i+1))

class HttpGet(object):
    def __init__(self, cache_dir):
        self.cache = Cache(cache_dir)

    def __call__(self, url):
        cache = self.cache
        # url_hash -> data_hash -> data
        url_hash = get_hash(url)
        logf('[url] {} {}'.format(url_hash, url))
        data_hash = cache.get(url_hash)
        if data_hash:
            data = cache.get(data_hash)
            if data:
                return data

        data = proxy_get(url).content
        data_hash = get_hash(data)
        if not cache.get(data_hash):
            cache.set(data_hash, data)
        cache.set(url_hash, data_hash)

        return data
