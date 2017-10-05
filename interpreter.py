import json
from time import sleep
import itertools
from xml.etree.ElementTree import Element as XMLElement, tostring, XML

class Interpreter():
    def __init__(self, main_thread):
        self.main_thread = main_thread
        # self.load()

    def load(self):
        with open('probe.json') as script:
            self.data = json.load(script)

        version = self.data['version'].split(':')
        if version == ['smp', '1']: 
            self._smp_v1_interpreter(self.data)

    def _smp_v1_interpreter(self, data):

        for x in data['setup']['operators']:        
            for probe in data['probes']:
                print(probe, x)
                # launch a process for each probe
                self.__process_queue(data['process']['queue'], probe)
                
            sleep(data['process']['interval'])
            print('===') # time to wait until send another tests.

    def __process_queue(self, tests, probe):
        for test in tests:
            xml = XMLElement(test['name'], test.get('params', {}),
                             xmlns=test['ns'], tid='')
            print(tostring(xml), probe)
            try:
                jid = probe+'@'+'xmpp.algartelecom.com.br'+'/Probe1.0'
                self.main_thread.make_iq_set(xml, jid).send()
            except Exception as e:
                pass
            # send iq set stanza