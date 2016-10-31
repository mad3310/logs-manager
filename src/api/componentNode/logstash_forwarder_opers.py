import os
import logging
import re

from tornado.options import options
from common.abstractOpers import AbstractOpers
from utils import get_file_data, set_file_data


class LogstashForwarderOpers(AbstractOpers):

    def __init__(self):
        pass

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
        return self.action(options.start_logstash_forwarder)

    def stop(self):
        return self.action(options.stop_logstash_forwarder)

    def restart(self):
        return self.action(options.restart_logstash_forwarder)

    def config(self, args):

        logging.info('config args:%s' % str(args))
        _ip = args.get('ip')
        _path = args.get('paths')
        content = get_file_data(options.logstash_forwarder_conf)
        ip_replaced = re.findall('.*servers": \[ "(.*):5043', content)[0]
        path_replaced = re.findall('"paths": \[ "(.*)" ].*', content)[0]
        logging.info('str_ip :%s, str_path :%s' % (ip_replaced, path_replaced))
        content = content.replace(ip_replaced, _ip)
        logging.info('content:%s' % content)
        content = content.replace(path_replaced, _path)
        logging.info('content:%s' % content)
        set_file_data(options.logstash_forwarder_conf, content)

        return {"message": "config /etc/logstash-forwarder.conf successfully"}
