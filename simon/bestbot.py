import sleekxmpp
import logging
import sys
import glob
import json
import yaml
from time import sleep
from multiprocessing import Queue
from xml.etree.ElementTree import Element as XMLElement, tostring, XML
from signal import *


import simon


class BestBot(sleekxmpp.ClientXMPP):

    def __init__(self, jid, password):
        super().__init__(jid, password)        
        self.logger = logging.getLogger()
        self.add_event_handler("session_start", self.session_start,
                               threaded=True)
        # signal(SIGCHLD, SIG_IGN)
        
    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        sleep(0)
        self.loop()

    def loop(self):
        scripts = self.load_scripts()
        self.logger.info('Loaded {} script file(s).'.format(len(scripts)))
        iq_queue = Queue()
        for script in scripts:
            p = simon.Interpreter(script, iq_queue)
            p.start()


        while not self.stop.is_set():
            try:
                iq = iq_queue.get()
                self.make_iq_set(*iq).send()
            except Exception:
                pass


    def load_scripts(self):
        """Load *n* script files to a dict"""

        scripts = []
        for file in glob.iglob('scripts/*.json'):
            with open(file) as f:
                scripts.append(json.load(f))
        for file in glob.iglob('scripts/*.yaml'):
            with open(file) as f:
                scripts.append(yaml.load(f))

        return scripts
