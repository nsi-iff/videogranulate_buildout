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
from should_dsl import *

FOLDER_PATH = abspath(dirname(__file__))

class VideoGranulateTest(unittest.TestCase):

    def setUp(self):
        self.video_granulate_service = Restfulie.at("http://localhost:8885/").auth('test', 'test').as_('application/json')
        self.sam = Restfulie.at("http://localhost:8888/").auth('test', 'test').as_('application/json')
        self.uid_list = []

        input_video = open(join(FOLDER_PATH,'input','working_google.flv')).read()
        self.b64_encoded_video = b64encode(input_video)

    def testGranulate(self):
        response = self.video_granulate_service.post(video=self.b64_encoded_video, filename='video1.flv', callback='http://localhost:8887/').resource()
        self.uid_list.append(response.video_key)

        self.video_granulate_service.get(key=response.video_key).resource() |should_not| be_done
        sleep(240)
        self.video_granulate_service.get(key=response.video_key).resource() |should| be_done

        grains_dict = loads(self.video_granulate_service.get(video_key=response.video_key).body)

        grains_dict.keys() |should| have(2).grains_types
        grains_dict['images'] |should| have(80).grains
        grains_dict['videos'] |should| have(80).grains

        [self.uid_list.append(key) for key in grains_dict['images']]
        [self.uid_list.append(key) for key in grains_dict['videos']]

    def testUidToGranulate(self):
        video_uid = self.sam.put(value={'video':self.b64_encoded_video}).resource().key
        response = self.video_granulate_service.post(video_uid=video_uid, filename='video2.flv', callback='http://localhost:8887/').resource()
        self.uid_list.append(video_uid)

        self.video_granulate_service.get(key=response.video_key).resource() |should_not| be_done
        sleep(160)
        self.video_granulate_service.get(key=response.video_key).resource() |should| be_done

        grains_dict = loads(self.video_granulate_service.get(video_key=video_uid).body)

        grains_dict.keys() |should| have(2).grains_types
        grains_dict['images'] |should| have(80).grains
        grains_dict['videos'] |should| have(80).grains

        [self.uid_list.append(key) for key in grains_dict['images']]
        [self.uid_list.append(key) for key in grains_dict['videos']]

    def testLinkToGranulate(self):
        uid_download = self.video_granulate_service.post(filename='video3.flv', video_link='http://localhost:8887/working_google.flv', callback='http://localhost:8887').resource()
        self.uid_list.append(uid_download.video_key)

        self.video_granulate_service.get(key=uid_download.video_key).resource() |should_not| be_done
        sleep(160)
        self.video_granulate_service.get(key=uid_download.video_key).resource() |should| be_done

        grains_dict = loads(self.video_granulate_service.get(video_key=uid_download.video_key).body)

        grains_dict.keys() |should| have(2).grains_types
        grains_dict['images'] |should| have(80).grains
        grains_dict['videos'] |should| have(80).grains

        [self.uid_list.append(key) for key in grains_dict['images']]
        [self.uid_list.append(key) for key in grains_dict['videos']]

    def tearDown(self):
        for uid in self.uid_list:
            self.sam.delete(key=uid)

if __name__ == '__main__':
        print "Necessario que o SAM esteja rodando na porta padrao com o usuario\n" + \
          "'test' e senha 'test' criados."
        videogranulate_ctl = join(FOLDER_PATH, '..', 'bin', 'videogranulate_ctl')
        worker = join(FOLDER_PATH, '..', 'bin', 'start_worker -name test_worker')
        stop_worker = join(FOLDER_PATH, '..', 'bin', 'stop_worker test_worker')
        add_user = join(FOLDER_PATH, '..', 'bin', 'add-user.py')
        del_user = join(FOLDER_PATH, '..', 'bin', 'del-user.py')
        callback_server = join(FOLDER_PATH, "callback_server.py")
        try:
            call("twistd -y %s" % callback_server, shell=True)
            call("%s start" % videogranulate_ctl, shell=True)
            call("%s test test" % add_user, shell=True)
            call("%s" % worker, shell=True)
            unittest.main()
        finally:
            call("kill -9 `cat twistd.pid`", shell=True)
            call("%s" % stop_worker, shell=True)
            call("%s stop" % videogranulate_ctl, shell=True)
            call("%s test" % del_user, shell=True)

