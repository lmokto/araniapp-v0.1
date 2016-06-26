# -*- coding: utf-8 -*-

import sys
import os
from lib import *
import redis
import json
from configobj import ConfigObj

__DIRNAME__ = os.path.dirname(__file__)

config = ConfigObj(__DIRNAME__ + '/config.cfg')
redis_cfg = config['redis']
extract_cfg = config['extract']
#loggger_cfg = config['logger_main']

redis = redis.StrictRedis(host=redis_cfg['host'], port=redis_cfg[
                          'port'], db=redis_cfg['db'])

logging = build_logger('main', 'info', __DIRNAME__ + '/main.log')
logging.add_handler('StreamHandler', 'debug')
logging.add_handler('FileHandler', 'info')


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
        logging.info(conn.estados[conn.pos])

        if conn.pos == 0:
            time.sleep(120)

        path = redis.srandmember(semilla)
        redis.smove(semilla, 'indexados::{0}'.format(semilla), path)

        logging.info(path)
        conn.req(path)

        if conn.source > 0:
            code = conn.source
            extract(code, semilla)


if __name__ == '__main__':

    semilla = sys.argv[1]
    norm = norm(semilla)
    logging.info(40 * '=')
    logging.info('SCANING {0}'.format(semilla))
    main(semilla)
