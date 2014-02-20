#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib
import modlogger
from io import open
import os
import time

class md5sum(object):

    t = time.localtime()
    __rg = '-d{0}{1}{2}'.format(t.tm_hour,t.tm_min,t.tm_yday)
    chksum = ''
    chknew = ''
    path = os.getcwd()+'/lib/tmp/'
    
    def md5_save(self, md5):
        hashsave = md5
        path = os.path.dirname(self.filename)
        name = self.filename.replace(path+"/", '').split('.')[0]
        self.savehash = self.path+"/"+name+'.md5'
        with open(self.savehash, mode='wb') as f:
            f.write(hashsave)

    def gen_md5(self, filename, block_size=65536):
        self.filename = filename
        with open(self.filename, mode='rb') as f:
            md5 = hashlib.md5()
            while True:
                data = f.read(block_size)
                if not data:
                    break
                md5.update(data)
        self.chksum = md5.hexdigest()
        if self.chknew == '':
            self.md5_save(self.chksum)

    def open_md5(self, filemd5):
        with open(filemd5, mode='r', encoding='utf-8') as f:
            self.chknew = f.read()

    def check(self, filemd5, filename):
        self.open_md5(filemd5)
        self.gen_md5(filename)
        if self.chksum == self.chknew:
            return True
        else:
            return False
