# -*- coding: utf-8 -*-

import gzip
import zlib
from cStringIO import StringIO
import binascii
import httplib
import socket
import modlogger
import re
import time
from urlparse import urlparse
import dequeforce2
import os

PATHLOG = os.getcwd() + "/araniapp/lib/log/"
LOG = modlogger.build_logger("extract4", "info", PATHLOG + "extract4.log")
LOG.add_handler("FileHandler", "info")
LOG.add_handler('StreamHandler', 'debug')

methods = ["HEAD", "GET", "PATH", "CONNECT", "DELETE", "PUT", "POST"]

excepts = {
    'socket.gaierror': 'Name or service not known',
    'CannotSendRequest': 'CannotSendRequest()',
    'socket.timeout': 'timed out',
    'httplib.ResponseNotReady': 'Network is unreachable'
}


class State(httplib.HTTPConnection):
    ''''''
    pos = 0
    estados = ["Close", "Listening", "Established"]

    def reset(self):
        if self.pos == len(self.estados):
            self.pos = 0


class Connection(State):
    ''' 
        conn = Connection(semilla)
        conn.debuglevel = 1
        conn.req()
    '''

    sinindex = set([])
    notfound = set([])

    def __init__(self, host, port=80, timeout=300):

        if host != 'localhost':
            self.host = host
            try:
                self.name, self.aliaslist, self.address = socket.gethostbyname_ex(host)
                for ip in range(len(self.address)):
                    self.address[ip] = tuple(int(v) for v in address.split('.'))
                self.address = tuple(self.address)
            except Exception:
                self.address = [None, '']
                self.headers = {'status': 401}
            self.timeout = timeout
            self.port = port

        socket.setdefaulttimeout(timeout)
        httplib.HTTPConnection.__init__(self, self.host, port=self.port, source_address=None)
        httplib.HTTPConnection.debuglevel = 0

        self.source = ''
        self.pos = 1

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
            'DNT': 1  # DO NOT TRACK  : 1 (Do Not Track Enabled) or 0 (Do Not Track Disabled)
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
                self.headers = dict(self.res.getheaders() + [("status", self.res.status)])
            else:
                self.headers = {'status': 504}
        except Exception:
            self.pos = 0

    def req(self, path='/', method="HEAD", encoding=1, skip_host=0):

        # import ipdb; ipdb.set_trace()

        self.encoding = encoding
        self.skip_host = skip_host
        self.method = method
        self.path = path

        if self.method == "HEAD":
            self.callreq()
            if self.headers['status'] in (200, 201, 203):
                self.req(self.path, "GET")
            elif self.headers['status'] in (301, 302, 303, 307, 308):
                self.path = urlparse(self.headers['location']).path
                self.req(self.path, "GET")
            elif self.headers['status'] in (400, 401, 403, 404):
                self.notfound.add(self.path)
                self.source = ''
                self.close()
            elif self.headers['status'] in (502, 503, 504):
                self.sinindex.add(self.path)
                self.source = ''
                self.close()
            else:
                log.info({"url": self.host + self.path, "headers": self.headers})
        elif self.method == "GET":
            self.close()
            self.callreq()
            self.getencoding = self.headers.get('content-encoding')
            self.getcontent = self.headers.get('content-type')
            LOG.info('content-type {0} -- path {1}'.format(self.headers, self.path))
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
            elif re.search('multipart/form-data', self.getcontent):  # contenido ? imagenes? pdfs? swf?, etc
                LOG.info(self.path)
            elif re.search('application/x-www-form-urlencoded', self.getcontent):
                LOG.info(self.path)
            elif re.search('application/json', self.getcontent):
                LOG.info(self.path)
            elif re.search('image/jpg', self.getcontent):
                LOG.info(self.path)
            elif re.search('image/svg', self.getcontent):
                LOG.info(self.path)
            elif re.search('image/svg+xml', self.getcontent):
                LOG.info(self.path)
            else:
                self.source = ''
                self.close()
