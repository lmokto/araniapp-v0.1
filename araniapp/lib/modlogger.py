# -*- coding: utf-8 -*-

import os
import logging
import errno

FLAGS = os.O_CREAT | os.O_EXCL | os.O_WRONLY

LEVEL = {"notset": logging.NOTSET,
         "debug": logging.DEBUG,
         "info": logging.INFO,
         "warning": logging.WARNING,
         "error": logging.ERROR,
         "critical": logging.CRITICAL}

FORMATS = ['%(filename)s', '%(levelname)s', '%(funcName)s', '%(lineno)s', '%(message)s']
HANDLER = {"FileHandler": logging.FileHandler,
           "StreamHandler": logging.StreamHandler}


class build_logger(object):
    '''
        logging = build_logger('main', 'info', '.' + '/logger.log')
        logging.add_handler('StreamHandler', 'debug')
        logging.add_handler('FileHandler', 'info')
    '''

    def __init__(self, name, lvl, savefile=None):
        
        self.savefile = savefile
        
        try:
            file_handle = os.open(self.savefile, FLAGS)
        except OSError as e:
            if e.errno == errno.EEXIST:
                pass
            else:
                raise

        self.logger = logging.getLogger(name)
        self.logger.setLevel(LEVEL.get(lvl))
        self.formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def add_handler(self, handler, lvl):
        self.handler = HANDLER.get(handler)
        if handler == "FileHandler":
            h = self.handler(self.savefile)
        else:
            h = self.handler()
        h.setLevel(LEVEL.get(lvl))
        h.setFormatter(self.formatter)
        self.logger.addHandler(h)

    def debug(self, d):
        self.logger.debug('%s', d)

    def info(self, i):
        self.logger.info('%s', i)

    def warning(self, w):
        self.logger.warning('%s', w)

    def error(self, e):
        self.logger.error('%s', e)

    def critical(self, c):
        self.logger.error('%s', c)
