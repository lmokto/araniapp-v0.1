# -*- coding: utf-8 -*-

import sys
import os
from lib import *

import redis

redis = redis.StrictRedis(host='localhost', port=6379, db=0)

PATHLOG = os.getcwd() + '/araniapp/lib/log/'
LOG = build_logger("main", "info", PATHLOG + "main.log")
LOG.add_handler("StreamHandler", "debug")
LOG.add_handler("FileHandler", "info")

externos = set([])
subdominios = set([])


def main(semilla):

    conn = Connection(semilla)
    conn.debuglevel = 0
    conn.req()
    extract(conn.source, semilla)

    while True:

        if redis.scard(semilla) != 0:
            
            time.sleep(1)
            LOG.info(conn.estados[conn.pos])

            if conn.pos == 0:
                time.sleep(120)
                continue

            path = redis.srandmember(semilla)
            redis.smove(semilla, 'indexados::{0}'.format(semilla), path)

            LOG.info(path)
            conn.req(path)

            if conn.source > 0:
                code = conn.source
                extract(code, semilla)
            else:
                continue
        else:
            break


if __name__ == '__main__':

    def extract(source, semilla=''):
        code = bs4.BeautifulSoup(source)
        for i in code.find_all('a', href=True):
            url = i['href']
            parsed = urlparse(url)
            netloc = parsed.netloc.replace("www.", '')
            if netloc == semilla.replace("www.", '') or netloc == '':
                if search("^/", parsed.path):
                    url = norm.replace(parsed.path + parsed.params)
                    p = urlparse(url)
                    path = p.path + p.params
                    if not redis.sismember('indexados::{0}'.format(semilla), path):
                        redis.sadd(semilla, path)


    semilla = sys.argv[1]
    norm = norm(semilla)
    LOG.info(40 * "=")
    LOG.info("SCANING {0}".format(semilla))
    main(semilla)
