#!/usr/bin/python
# -*- coding: utf-8 -*-

from lxml import html, etree
from lxml import html as LH
from lxml import html, cssselect
from os.path import basename
from urlparse import urlsplit
import urllib2

def event(dochtml, tag='a', event='onclick'):
    '''busca en el tag a los eventos 'onclick, parametros modificables ejemplo tag="div", event="onload" '''
    onevent = []
    for link in dochtml.cssselect(tag):
        if link.attrib.has_key(event):
            onevent.append(link.get(event))
    return onevent

def img(dochtml, ext='all'):
    '''only return jpg, png, gif or tif'''
    onimg = []
    t = ['jpg', 'png', 'gif', 'tif']
    if ext == 'all':
        search = t
    else:
        search = [t[t.index(ext)]]
    for elem, attr, path, pos in dochtml.iterlinks():
        if path.rpartition(".")[2] in search:
            onimg.append(path)
    return onimg

def download_img(img):
    try:
        imgData = urllib2.urlopen(img).read()
        fileName = basename(urlsplit(img)[2])
        output = open(fileName,'wb')
        output.write(imgData)
        output.close()
    except:
        pass

def js(dochtml, href='src', ext='js'):
    '''Retorna los archivos javascript ubicados en src, href. La extension es modificable.'''
    onext = []
    for elem, attr, path, pos in dochtml.iterlinks():
        if attr == href and path.rpartition(".")[2] == ext:
            onext.append(path)
    return onext

def links(dochtml, tag='a', href='href'):
    onurl = []
    for elem in dochtml.cssselect(tag):
        onurl.append(elem.get(href))
    return onurl

def text(dochtml):
    pass

def textform():
    pass


def get_text(dochtml, tag='div', cls='class'):
    for div in dochtml.cssselect('{0}.{1}'.format(tag, cls)):
        text = div.text_content()
        if len(text) > 1:
            return text

def in_iter(ilist):
    if isinstance(ilist, list):
        ilist = iter(ilist)
    for number, element in enumerate(ilist):
        return number, element

    