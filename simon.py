#!/usr/bin/env python3

# Entraince point for Simon bot.

import sleekxmpp
import argparse
import logging
import colorlog
import configparser
import sys

import interpreter


class BestBot(sleekxmpp.ClientXMPP):
    def __init__(self, jid, password):
        super().__init__(jid, password)        
        self.add_event_handler("session_start", self.session_start,
                               threaded=True)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        self.loop()

    def loop(self):
        qq = interpreter.Interpreter(self)
        while not self.stop.is_set():
            qq.load()
            print('++++++')


if __name__ == '__main__':

    # arguments definitions
    parser = argparse.ArgumentParser(description='Just another bot.')
    parser.add_argument('--conf', help='configuration file',
                        default='simon.conf', metavar='FILE')
    parser.add_argument('-v', help='changes console log level',
                        default='info', choices=['debug', 'info', 'warn'])
    args = parser.parse_args()
    
    # logging
    logging.getLogger().setLevel(args.v.upper())

    console = logging.StreamHandler()
    color_fmt = colorlog.ColoredFormatter('%(asctime)s %(log_color)s'
                                          '%(levelname)s\t%(message)s')
    console.setFormatter(color_fmt)
    logging.getLogger().addHandler(console) 

    # configuration loading
    conf = configparser.ConfigParser()
    try:
        conf.read_file(open(args.conf))
    except FileNotFoundError:
        logging.critical('Configuration file \'{}\' not found. '
                         'Must exit.'.format(args.conf))
        sys.exit(1)
    
    jid = '{}@{}/Simon'.format(conf['default'].get('user'),
                               conf['default'].get('host'))
    password = '{}'.format(conf['default'].get('password'))

    xmpp = BestBot(jid, password)
    xmpp.connect()
    xmpp.process(block=True)
