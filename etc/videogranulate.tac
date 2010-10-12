#!/usr/bin/env python
# coding: utf-8

import cyclone.web
from twisted.application import service, internet
from nsivideogranulate.xmlrpc import XmlrpcHandler
from nsivideogranulate.auth import Authentication
from ConfigParser import RawConfigParser

CONF = '/home/douglas/develop/videogranulate_buildout/buildout.cfg'
DB_FILE = '/home/douglas/develop/videogranulate_buildout/etc/storage.sqlite'

def get_authenticator(conf):
    return Authentication(DB_FILE)

class VideoGranulate(cyclone.web.Application):

    def __init__(self):
        handlers = [
            (r"/xmlrpc", XmlrpcHandler),
        ]

        settings = {
            "auth": get_authenticator(CONF),
        }

        cyclone.web.Application.__init__(self, handlers, **settings)


application = service.Application("VideoGranulate Service")
srv = internet.TCPServer(8887, VideoGranulate(), interface='0.0.0.0')
srv.setServiceParent(application)

