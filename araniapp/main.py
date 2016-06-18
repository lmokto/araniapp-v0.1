# -*- coding: utf-8 -*-

import sys
import os
from lib import *

import redis

redis = redis.StrictRedis(host='localhost', port=6379, db=0)

PATHTMP = os.getcwd() + '/araniapp/lib/tmp/'
PATHLOG = os.getcwd() + '/araniapp/lib/log/'

FILEOBJ = ''
FILEHASH = ''

LOG = build_logger("main", "info", PATHLOG + "main.log")
LOG.add_handler("FileHandler", "info")

internos = li()
externos = set([])
subdominios = set([])


def main(semilla):
    NAME = semilla.rsplit('.')[1]
    BACKUP = PersistenceObject(NAME, PATHTMP, 'r', '.pik')

    conn = Connection(semilla)
    conn.debuglevel = 1
    conn.req()
    extract(conn.source, semilla)

    while True:
        if redis.scard(semilla) != 0:
            time.sleep(1)
            print conn.estados[conn.pos]
            if conn.pos == 0:
                BACKUP.flag = 'w'
                BACKUP.dump(list(redis.smembers(semilla)))
                break
            path = redis.spop(semilla)
            print path
            conn.req(path)
            if conn.source > 0:
                code = conn.source
                extract(code)
            else:
                continue
        else:
            break


if __name__ == '__main__':

    def extract(source, semilla):
        code = bs4.BeautifulSoup(source)
        for i in code.find_all('a', href=True):
            url = i['href']
            parsed = urlparse(url)
            netloc = parsed.netloc.replace("www.", '')
            if netloc == semilla.replace("www.", '') or netloc == '':
                if search("^/", parsed.path):
                    url = norm.replace(parsed.path + parsed.params)
                    p = urlparse(url)
                    redis.sadd(semilla, p.path + p.params)


    semilla = sys.argv[1]
    norm = norm(semilla)
    print 40 * "="
    print "SCANING ", semilla
    main(semilla)
