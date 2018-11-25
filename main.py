# coding: utf-8

import os
import re
import eel
import time
import base64
import random
import traceback
import webbrowser

from io_util import prepare_dir
from http_util import HttpGet
from log_util import logf_env, logf

LOG_DIR = 'log'
CACHE_DIR = 'http_cache'

prepare_dir(LOG_DIR)
prepare_dir(CACHE_DIR)

j = os.path.join
http_get = HttpGet(CACHE_DIR)

def main():
    eel.init('web')

    @eel.expose
    def convert(x):
        m = re.search(r'(rj\d+)', x.lower())
        if not m:
            return ''
        rj = m.group(1).upper()
        url = 'http://www.dlsite.com/maniax/work/=/product_id/{}.html'.format(rj)
        c = http_get(url)

        with open('tmp.html', 'wb') as f:
            f.write(c)

        m = re.search(r'<span\b[^>]*class="maker_name"><a\b.*?>(.*?)<', c)
        maker = m and m.group(1) or '?'

        m = re.search(r'<th>販売日</th>\s*<td><a.*?/year/(\d+)/mon/(\d+)/day/(\d+)/', c, re.S)
        if m:
            pub_year = int(m.group(1))
            pub_mon  = int(m.group(2))
            pub_day  = int(m.group(3))
            pub_time = '%04d-%02d-%02d' % (pub_year, pub_mon, pub_day)
        else:
            pub_time = '?'

        m = re.search(r'<h1\b[^>]*\bid="work_name">\s*<a\b.*?>(.*?)<', c, re.S)
        title = m and m.group(1) or '?'

        return {
            'fullname': '[{}][{}][{}] {}'.format(maker, pub_time, rj, title),
            'maker': maker,
            'rj': rj,
            'title': title,
            'url': url,
        }

    @eel.expose
    def open_url(url):
        webbrowser.open(url)

    eel.start('index.html?s=' + str(time.time()) + str(random.random()), size=(1400, 600))

if __name__ == '__main__':
    with logf_env(LOG_DIR):
        try:
            main()
        except Exception:
            logf(traceback.format_exc())
