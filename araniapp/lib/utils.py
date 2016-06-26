# -*- coding: utf-8 -*-

import os
import errno
import tld

flags = os.O_CREAT | os.O_EXCL | os.O_WRONLY


def touch_file(filename):
    try:
        file_handle = os.open(filename, flags)
    except OSError as e:
        if e.errno == errno.EEXIST:  # Failed as the file already exists.
            pass
        else:  # Something unexpected went wrong so reraise the exception.
            raise


def gethref(href):

    if not hasattr(href, 'href'):
        return href
    return href['href']


def getDomain(url):
    try:
        url_object = tld.get_tld(url)
        return url_object.encode('utf-8')
    except:
        pass


def getSubdomain(url):
    url_object = tld.get_tld(url, as_object=True)
    return url_object.subdomain.encode('utf-8')


def getTLD(url):
    url_object = tld.get_tld(url, as_object=True)
    return {
        'domain': url_object.domain.encode('utf-8'),
        'extension': url_object.extension.encode('utf-8'),
        'subdomain': url_object.subdomain.encode('utf-8'),
        'suffix': url_object.suffix.encode('utf-8'),
        'tld': url_object.tld.encode('utf-8')
    }
