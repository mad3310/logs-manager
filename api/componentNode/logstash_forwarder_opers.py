'''
Created on Mar 13, 2015

@author: root
'''
import os
import logging
import re

from tornado.options import options
from common.abstractOpers import AbstractOpers
from utils import get_file_data, set_file_data


class LogstashForwarderOpers(AbstractOpers):
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''

    def action(self, cmd):
        ret_val = os.system(cmd)
        
        result = {}
        if ret_val != 0:
            message = "do %s failed" % cmd
            logging.info(message)
            result.setdefault("message", message)
        else:
            message = "do %s successfully" % cmd
            logging.error(message)
            result.setdefault("message", message)
        
        return result        

    def start(self):
        return self.action(options.start_logstash)

    def stop(self):
        return self.action(options.stop_logstash)

    def restart(self):
        return self.action(options.restart_logstash)
    
    def config(self, args):
        
        _ip = args.get('ip')
        content = get_file_data(options.logstash_forwarder_conf)
        replaced = re.findall('.*(\d{3}.*):5043', content)[0]
        content = content.replace(replaced, _ip)
        set_file_data(options.logstash_forwarder_conf, content)
        
        return {"message": "config /etc/logstash-forwarder.conf successfully"}
