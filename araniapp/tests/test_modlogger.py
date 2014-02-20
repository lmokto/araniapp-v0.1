#!/usr/bin/python
# -*- coding: utf-8 -*-

import unittest
from lib import build_logger
import os

PATHLOG = os.getcwd()+"/tests/log/"

def func(a, b):
    return a+b

global LOG
LOG = build_logger("FUNC2", "info", PATHLOG+"/test_modlogger.log")

class TestWriteLog(unittest.TestCase):
    
    def setup(self):
        r = func(2, 2)
        LOG.add_handler("FileHandler", "info")
        LOG.add_handler("StreamHandler", "debug")
        LOG.info("llamaron la funcion, %s con el resultaod, %s" % (__file__, r))
        LOG.info({'host': 'somehost.com', 'headers':{'head1':'content1','head2':'content2'}})
    
    def test(self):
        self.setup()
    
if __name__ == '__main__':
    unittest.main()