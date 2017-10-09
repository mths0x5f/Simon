import json
from time import sleep
import itertools
import logging
from xml.etree.ElementTree import Element as XMLElement

from multiprocessing import Process

logger = logging.getLogger()


class Interpreter(Process):

    def __init__(self, script, queue):
        super().__init__()
        self.script = script
        self.queue = queue

    def run(self):
        version = self.script['version'].split(':')

        if version == ['smp', '1']: 
            self.smp_v1_interpreter(self.script)
        else:
            print('Not implemented.')

    def smp_v1_interpreter(self, script):
        
        for carrier in script['setup']['operators']: 
            for probe in script['probes']:

                logger.info(str(self.pid) + '::: ' + probe + carrier)
                
                iqs = self.create_iqs(script['process']['queue'],
                                      probe, 'xmpp.algartelecom.com.br',
                                      'Probe1.0')

                # launch a process for each probe
                Process(target=self.put_iqs_in_queue,
                        args=(iqs,)).start()
            
            # time to wait until put things in queue again
            sleep(script['process']['interval'])

    def create_iqs(self, script, user, domain, resource):
        iqs = []
        for i in script:
            xml = XMLElement(i['name'], i.get('params', {}), xmlns=i['ns'])
            jid = '{}@{}/{}'.format(user, domain, resource)
            iqs.append((xml, jid))
        return iqs

    def put_iqs_in_queue(self, iqs):
        for iq in iqs:
            self.queue.put(iq)
