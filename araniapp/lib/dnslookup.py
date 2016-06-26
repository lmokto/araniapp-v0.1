# -*- coding: utf-8 -*-

import socket


def getIP(d):
    """
    This method returns the first IP address string
    that responds as the given domain name
    """
    try:
        data = socket.gethostbyname(d)
        ip = repr(data)
        return ip
    except Exception:
        # fail gracefully!
        return False


#
def getIPx(d):
    """
    This method returns an array containing
    one or more IP address strings that respond
    as the given domain name
    """
    try:
        data = socket.gethostbyname_ex(d)
        ipx = repr(data[2])
        return ipx
    except Exception:
        # fail gracefully!
        return False


#
def getHost(ip):
    """
    This method returns the 'True Host' name for a
    given IP address
    """
    try:
        data = socket.gethostbyaddr(ip)
        host = repr(data[0])
        return host
    except Exception:
        # fail gracefully
        return False


#
def getAlias(d):
    """
    This method returns an array containing
    a list of aliases for the given domain
    """
    try:
        data = socket.gethostbyname_ex(d)
        alias = repr(data[1])
        # print repr(data)
        return alias
    except Exception:
        # fail gracefully
        return False



['https://twitter.com/#!/TelpinCorreo',
 'https://ap.telpin.com.ar/',
 'http://www.pinamarturismo.com.ar/',
 'http://telpineduca.telpin.com.ar/Proyectos/index.htm',
 '#',
 'http://www.telpinteve.com.ar',
 'http://www.usaeltelefono.com.ar/',
 'http://ovt.telpin.com.ar/',
 'http://eltiempo.telpin.com.ar/',
 'http://www.slidedeck.com',
 'http://www.telpinteve.com.ar/',
 'http://usaeltelefono.telpin.com.ar/',
 'http://webmail.telpin.com.ar/',
 'http://www.facebook.com/profile.php?id=100003304675342',
 'https://servicios1.afip.gov.ar/clavefiscal/qr/response.aspx?qr=IbecsVVr-r4e3APTEZvizA,,',
 'http://www.youtube.com/user/TelpinVideos',
 'http://telpineduca.telpin.com.ar/EGRESADOS/index.htm',
 'http://ovt.telpin.com.ar/guia/guia.asp',
 'http://telpineduca.telpin.com.ar/LP/Susini/index.htm',
 'http://www.adobe.com/go/getflashplayer',
 'http://ovt.telpin.com.ar/gestionar.asp']
 
#
'''
# test it
    
    x = raw_input("Domain name or IP address? > ")
    
    
    a = getIP(x)
    b = getIPx(x)
    c = getHost(x)
    d = getAlias(x)
    
    print " IP ", a
    print " IPx ", b
    print " Host ", c
    print " Alias ", d
'''
