#!/usr/bin/python
# -*- coding: utf-8 -*-

from io import open
from md5sum import md5sum
from contextlib import closing
from collections import deque

import time
import modlogger
import time
import os

import shelve
import json
try:
    import cPickle as pickle
except:
    import pickle

class PersistenceDeque(object):
    @staticmethod
    def dumpqueue(queue):
        '''queuedict = dumpqueue(queue)'''
        if isinstance(queue, deque):
            check = queue.actlib
            if check == 0:
                queuedict = dict({'elem':list(queue)})
            elif check == 1:
                queuedict = dict({'elem':list(queue), 'hashlib':queue.show()})
            return queuedict
        else:
            return None
    @staticmethod    
    def loadqueue(queue, queuedict):
        '''queue = loadqueue(queue, queuedict)'''
        if isinstance(queue, deque) and isinstance(queuedict, dict):
            length = len(queuedict.keys())
            if hasattr(queue, "actlib"):
                actlib = getattr(queue, "actlib")
                keys = queuedict.keys()
            if length == 1 and actlib == 0:
                queue.extendleft(queuedict[keys[0]])
            elif length == 2 and actlib == 1:
                queue.extendleft(queuedict[keys[1]])
                for k, v in queuedict[keys[0]].iteritems():
                    queue.lib[k] = v
            return queue
        else:
            return None


class checkHASH(md5sum):
    pass

class PersistenceObject(checkHASH):
    '''
        formats = { ".pik":pickle, ".json":json, ".db":shelver}
        save = PersistenceObject('di2', '/path/', 'r', '.json')
        save.load('di2.json', 'di2.md5')
        save.dump(di)
        print save.newobjects

    '''
    t = time.localtime()
    __rg = '-d{0}{1}{2}'.format(t.tm_hour,t.tm_min,t.tm_yday)
    
    #self.formats[format]    #   pik=pickle, json=json, db=shelver, .md5=hashobject
    def __init__(self, namefile, tmp='.tmp', flag='w', format='.pik'):
        
        self.flag = flag.lower()        #   r=readonly, c=create
        self.tmp = tmp
        self.key = ''
        self.checkhash = False
        self.namefile = namefile
        self.newobject = None
        self.format = format
        self.formats = {'.md5':[],
            '.pik':['rb', 'wb', pickle, None, 2],
            '.json':['r', 'wb', json, None, 'indent=2'],
            '.db':['r', 'w', shelve, None, 'writeback=True']}
    
        if self.flag == 'w':
            self.filesave = ''
        elif self.flag == 'r':
            self.fileobj = ''
        else:
            print('flag invalid, r=readonly or c=create and w=write')
            
        self.packet = self.formats[self.format]
    
    def __hash(self, fileobj):
        if os.access(fileobj, os.R_OK):
            self.gen_md5(fileobj)

    def dump(self, objected):
        if self.flag == 'w':
            self.filesave = self.tmp+self.namefile+self.__rg+self.format
            self.info = type(objected)
            if self.format in ('.json', '.pik'):
                with open(self.filesave, mode=self.packet[1], encoding=self.packet[3]) as f:
                    self.packet[2].dump(objected, f, self.packet[4])
                self.__hash(self.filesave)
            elif self.format == '.db':
                with closing(shelve.open(self.filesave, flag='c')) as f:
                    f[self.key] = objected
                self.__hash(self.filesave)
            else:
                raise NotImplementedError('Unknown format: ' + repr(self.format)) #log
    
    def load(self, fileobj, filehash):
        if self.flag == 'r':
            self.fileobj = self.tmp+fileobj
            filehash = self.tmp+filehash
            if os.access(self.fileobj, os.R_OK) and os.access(filehash, os.R_OK):
                self.checkhash = self.check(filehash, self.fileobj)
                self.chknew = ''
                self.chksum = ''
            if self.checkhash == True:
                if self.format in ('.pik', '.json'):
                    with open(self.fileobj, mode=self.packet[0], encoding=self.packet[3]) as f:
                        self.newobject = self.packet[2].load(f)
                elif self.format == '.db':
                    with closing(shelve.open(self.fileobj, flag='r')) as f:
                        self.newobject = f
                else:
                    raise NotImplementedError('Unknown format: ' + repr(self.format)) #log
            else:
                return self.checkhash