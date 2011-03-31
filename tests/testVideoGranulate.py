#!/usr/bin/env python
#-*- coding:utf-8 -*-

import unittest
from os.path import dirname, abspath, join
from base64 import decodestring, b64encode
from subprocess import call, Popen
from multiprocessing import Process
from time import sleep
from json import loads
from restfulie import Restfulie

FOLDER_PATH = abspath(dirname(__file__))

class VideoGranulateTest(unittest.TestCase):

    def setUp(self):
        self.video_granulate_service = Restfulie.at("http://localhost:8885/").auth('test', 'test').as_('application/json')
        self.sam = Restfulie.at("http://localhost:8888/").auth('test', 'test').as_('application/json')
        self.uid_list = []

    def testGranulate(self):
        input_video = open(join(FOLDER_PATH,'input','rubik.flv')).read()
        b64_encoded_video = b64encode(input_video)
        response = self.video_granulate_service.post({'video':b64_encoded_video, 'format':'ogm'}).resource()
        self.uid_list.append(response.grains_key)
        self.uid_list.append(response.video_key)

        sleep(60)

        grains_response = self.sam.get({'key':response.grains_key})
        grains_dict = loads(grains_response.body)

        self.assertTrue(isinstance(grains_dict, dict))
        self.assertEquals(len(grains_dict), 4)
        self.assertEquals(len(grains_dict['data']['grains']), 2)

if __name__ == '__main__':
        videogranulate_ctl = join(FOLDER_PATH, '..', 'bin', 'videogranulate_ctl')
        worker = join(FOLDER_PATH, '..', 'bin', 'start_worker -name test_worker')
        stop_worker = join(FOLDER_PATH, '..', 'bin', 'stop_worker test_worker')
        add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
        del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
        try:
            call("%s start" % videogranulate_ctl, shell=True)
            call("%s test test" % add_user, shell=True)
            call("%s" % worker, shell=True)
            unittest.main()
        finally:
            call("%s" % stop_worker, shell=True)
            call("%s stop" % videogranulate_ctl, shell=True)
            call("%s test" % del_user, shell=True)

