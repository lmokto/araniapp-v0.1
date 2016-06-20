# -*- coding: utf-8 -*-

import sys
import os
from lib import *
import redis
import json


with open(os.path.dirname(__file__) + '/config.json') as json_data_file:
    config = json.load(json_data_file)
    redis_cfg = config['redis']
    extract_cfg = config['extract']
    loggger_cfg = config['logger']

redis = redis.StrictRedis(host=redis_cfg['host'], port=redis_cfg[
                          'port'], db=redis_cfg['db'])

PATHLOG = os.getcwd() + '/araniapp/lib/log/'
LOG = build_logger('main', 'info', PATHLOG + 'main.log')
LOG.add_handler('StreamHandler', 'debug')
LOG.add_handler('FileHandler', 'info')

externos = set([])
subdominios = set([])


def extract(source, semilla=''):

    # import ipdb; ipdb.set_trace()

    code = bs4.BeautifulSoup(source)

    for i in code.find_all('a', href=True):

        url = i['href']
        parsed = urlparse(url)
        netloc = parsed.netloc.replace('www.', '')

        if netloc == semilla.replace('www.', '') or netloc == '' and search('^/', parsed.path):
            url = norm.replace(parsed.path + parsed.params)
            p = urlparse(url)
            path = p.path + p.params
            if not redis.sismember('indexados::{0}'.format(semilla), path):
                redis.sadd(semilla, path)
        else:
            redis.sadd('externos{0}::'.format(semilla), url)


def main(semilla):

    conn = Connection(semilla, redis, config=extract_cfg)
    conn.debuglevel = 1
    conn.req()
    extract(conn.source, semilla)

    while True:

        if not redis.scard(semilla):
            break

        time.sleep(1)
        LOG.info(conn.estados[conn.pos])

        if conn.pos == 0:
            time.sleep(120)

        path = redis.srandmember(semilla)
        redis.smove(semilla, 'indexados::{0}'.format(semilla), path)

        LOG.info(path)
        conn.req(path)

        if conn.source > 0:
            code = conn.source
            extract(code, semilla)


if __name__ == '__main__':

    semilla = sys.argv[1]
    norm = norm(semilla)
    LOG.info(40 * '=')
    LOG.info('SCANING {0}'.format(semilla))
    main(semilla)
