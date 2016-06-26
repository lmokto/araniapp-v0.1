# -*- coding: utf-8 -*-

# http://www.useragentstring.com/pages/api.php
# http://www.useragentstring.com/?uas=Opera/9.70%20(Linux%20i686%20;%20U;%20en-us)%20Presto/2.2.0&getJSON=all


def make_custom():
    pass


__USERAGENTS__ = {
    "Chrome": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Firefox": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1",
    "IE": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; AS; rv:11.0) like Gecko",
    "Safari": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A",
    "AppEngine-Google": "AppEngine-Google; (+http://code.google.com/appengine; appid: webetrex)",
    "Android": "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30",
}

__DEFAUT__ = {
    'accept-charset': 'utf-8,*',
    'cache-control': 'no-cache',
    'accept-encoding': 'gzip,deflate,sdch',
    'accept': 'text/html',
    #'cookie': '',
    'accept-language': 'es,en-US;q=0.8,en;q=0.6',
    'user-agent': '[Mozilla/5.0 (X11; Linux x86_64)',
    'connection': 'keep-alive',
    'DNT': 1
}

__RANDOM__ = {}
