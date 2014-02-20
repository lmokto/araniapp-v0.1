##!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urlparse
import urlnorm
from string import lower

__regexps__ = ["\.[a-z0-9]{2,4}$|/$", '', ''] # re.search("\.[a-z0-9]{2,4}$|/$", path) 
__filewebs__ = ['index.html', 'index.htm', 'index.xhtml', 'index.xhtm', "index.asp", "index.aspx", "default.asp", "default.aspx"]


class norm(object):
    
    '''
        documentar codigo
    '''
    http = "http://"
    https = "https://"
        
    def __init__(self, host):
        if host:
            newhost = self.clean(host)
            self.host = self.http+newhost
        
    def clean(self, url):
        return url.rpartition('//')[2].replace('www.', '')
    
    def replace(self, arg, charset='utf-8'):
        #n = arg.rpartition("/")[0].count("/")
        self.host = urlparse.urljoin(self.host, arg.replace("//", "/"))
        this = ''
        try:
            this = lower(self.host.replace("www.", ""))
            if isinstance(this, unicode):
                this = this.encode(charset, 'ignore')
        except UnicodeEncodeError:
            pass #log
        scheme, netloc, path_A, qs, anchor = urlparse.urlsplit(this)
        path_B = urlnorm.norm_path("http", path_A)
        path = urllib.quote(path_B.encode('utf-8'), '/%')
        qs = urllib.quote_plus(qs.encode('utf8'), ':&?/=')
        split = urlparse.urlunsplit((scheme, netloc, lower(path), qs, anchor))
        
        return split