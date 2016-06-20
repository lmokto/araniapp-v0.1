# -*- coding: utf-8 -*-

import gzip
import zlib
from cStringIO import StringIO
import binascii
import httplib
import socket
import re
import os
import time
import redis

import modlogger
from urlparse import urlparse
from status_codes import (
    __SUCCESS__, __INFO__, __REDIRECTION__, __CLIENT_ERROR__, __SERVER_ERROR__
)


PATHLOG = os.getcwd() + "/araniapp/lib/log/"
LOG = modlogger.build_logger("extract4", "info", PATHLOG + "extract4.log")
LOG.add_handler("FileHandler", "info")
LOG.add_handler('StreamHandler', 'debug')


class State(httplib.HTTPConnection):

    ''''''

    pos = 0
    estados = ["Close", "Listening", "Established"]
    exception = {
        'socket.gaierror': 'Name or service not known',
        'CannotSendRequest': 'CannotSendRequest()',
        'socket.timeout': 'timed out',
        'httplib.ResponseNotReady': 'Network is unreachable'
    }

    SUCCESS = __SUCCESS__
    INFO = __INFO__
    REDIRECTION = __REDIRECTION__
    CLIENT_ERROR = __CLIENT_ERROR__
    SERVER_ERROR = __SERVER_ERROR__

    def reset(self):
        if self.pos == len(self.estados):
            self.pos = 0


class Connection(State):
    ''' 
        conn = Connection(semilla)
        conn.debuglevel = 1
        conn.req()
    '''

    def __init__(self, host, redis, config={}, port=80, timeout=300):

        self.hiredis = redis
        self.config = config
        self.find_types = self.config['contents_types']['enabled']
        self.contents_types = self.config['contents_types']['types']

        if host != 'localhost':
            self.host = host
            try:
                self.name, self.aliaslist, self.address = socket.gethostbyname_ex(
                    host)
                for ip in range(len(self.address)):
                    self.address[ip] = tuple(int(v)
                                             for v in address.split('.'))
                self.address = tuple(self.address)
            except Exception:
                self.address = [None, '']
                self.headers = {'status': 401}
            self.timeout = timeout
            self.port = port

        socket.setdefaulttimeout(timeout)
        httplib.HTTPConnection.__init__(
            self, self.host, port=self.port, source_address=None)
        httplib.HTTPConnection.debuglevel = self.config['debuglevel']

        self.methods = ["HEAD", "GET", "PATH",
                        "CONNECT", "DELETE", "PUT", "POST"]
        self.source = ''
        self.pos = 1

    def __sadd(self, key, member=[], code=False, mimetype=False):
        _key = '{0}::{1}'.format(key, self.host)
        if code:
            self.hiredis.sadd('{0}::codes'.format(self.host), key)
        elif mimetype:
            self.hiredis.sadd('{0}::mimetype'.format(self.host), key)
        self.hiredis.sadd(_key, member)

    def add_headers(self, addhead={}):
        self.pos = 2
        listhead = {
            'accept-charset': 'utf-8,*',
            'cache-control': 'no-cache',
            'accept-encoding': 'gzip,deflate,sdch',
            'accept': 'text/html',
            # 'cookie': ''
            'accept-language': 'es,en-US;q=0.8,en;q=0.6',
            'user-agent': '[Mozilla/5.0 (X11; Linux x86_64)',
            'connection': 'keep-alive',
            # DO NOT TRACK  : 1 (Do Not Track Enabled) or 0 (Do Not Track
            # Disabled)
            'DNT': 1
        }
        if len(addhead) != 0:
            listhead.update(addhead)
        for head, value in listhead.iteritems():
            self.putheader(head, value)
        self.endheaders()

    def callreq(self):
        try:
            self.putrequest(self.method, self.path,
                            skip_accept_encoding=self.encoding)
            self.add_headers()
            if self.getresponse:
                self.res = self.getresponse()
                self.headers = dict(self.res.getheaders() +
                                    [("status", self.res.status)])
            else:
                self.headers = {'status': 504}
        except Exception:
            self.pos = 0

    def set_content_type(self, content_type, path):
        if self.find_types:
            if content_type in self.contents_types:
                self.__sadd(content_type, path)
        else:
            self.__sadd(content_type, path)

    def req(self, path='/', method="HEAD", encoding=1, skip_host=0):

        #import ipdb
        #ipdb.set_trace()

        self.encoding = encoding
        self.skip_host = skip_host
        self.method = method
        self.path = path

        if self.method == "HEAD":
            self.callreq()
            status = self.headers['status']
            if status in self.INFO.keys():
                self.__sadd(status, self.path, code=True)
            elif status in self.SUCCESS.keys():
                content_type = self.headers.get('content-type')
                self.__sadd(status, self.path, code=True)
                self.__sadd(content_type, self.path, mimetype=True)
                self.set_content_type(content_type, self.path)
                self.req(self.path, "GET")
            elif status in self.REDIRECTION.keys():
                self.__sadd(status, self.path, code=True)
                self.path = urlparse(self.headers['location']).path
                self.req(self.path, "GET")
            elif status in self.CLIENT_ERROR.keys():
                self.__sadd(status, self.path, code=True)
                self.source = ''
                self.close()
            elif status in self.SERVER_ERROR.keys():
                self.__sadd(status, self.path, code=True)
                self.source = ''
                self.close()
            else:
                self.__sadd(status, self.path, code=True)
                log.info({"url": self.host + self.path,
                          "headers": self.headers})
        elif self.method == "GET":
            self.close()
            self.callreq()
            self.getencoding = self.headers.get('content-encoding')
            self.getcontent = self.headers.get('content-type')
            LOG.info(
                'content-type {0} -- path {1}'.format(self.headers, self.path))
            if re.search('text/html', self.getcontent):
                try:
                    stream = StringIO(self.res.read())
                    if self.getencoding in ('gzip', 'x-zip'):
                        with gzip.GzipFile(mode="rb", fileobj=stream) as f:
                            self.source = f.read()
                    elif self.getencoding == "deflate":
                        self.source = gzip.GzipFile('', 'rb', 9, stream)
                    else:
                        self.source = stream.read()
                except Exception as err:
                    self.pos = 0
            else:
                self.source = ''
                self.close()
