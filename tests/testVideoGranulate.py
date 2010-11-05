#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from xmlrpclib import Server
from os.path import dirname, abspath, join
from base64 import decodestring, b64encode
from subprocess import call, Popen
from multiprocessing import Process
from time import sleep

FOLDER_PATH = abspath(dirname(__file__))

class VideoGranulateTest(unittest.TestCase):

    def setUp(self):
        self.video_granulate_service = Server("http://test:test@localhost:8885/xmlrpc")
        self.sam = Server("http://test:test@localhost:8888/xmlrpc")
        self.uid_list = []

    def testGranulate(self):
        input_video = open(join(FOLDER_PATH,'input','rubik.flv')).read()
        b64_encoded_video = b64encode(input_video)
        uid = self.video_granulate_service.granulate(b64_encoded_video)
        self.uid_list.append(uid)
        self.assertTrue(isinstance(uid,str))

        sleep(60)

        grains_dict = eval(self.sam.get(uid))
        self.assertTrue(isinstance(grains_dict, dict))
        self.assertEquals(len(grains_dict), 4)

if __name__ == '__main__':
        videogranulate_ctl = join(FOLDER_PATH, '..', 'bin', 'videogranulate_ctl')
        slave = join(FOLDER_PATH, '..', 'etc', 'slave.py')
        slave_process = Popen("%s" % slave)
        add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
        del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
        try:
            call("%s start" % videogranulate_ctl, shell=True)
            call("%s test test" % add_user, shell=True)
            sleep(5)
            unittest.main()
        finally:
            slave_process.kill()
            call("%s stop" % videogranulate_ctl, shell=True)
            call("%s test" % del_user, shell=True)

