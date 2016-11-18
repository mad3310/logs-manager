import os
import re
import logging

from tornado.options import options
from common.abstractOpers import AbstractOpers
from utils.configFileOpers import ConfigFileOpers


class KibanaOpers(AbstractOpers):

    def __init__(self):
        self.config_op = ConfigFileOpers()

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

    def config(self, args):
        ip = args.get('ip')
        url = self.config_op.get_value(
            options.kibana_conf, 'elasticsearch_url', ':')
        old_ip = re.findall('http://(.*):9200', url)[0]
        url = url.replace(old_ip, ip)
        self.config_op.set_value(options.kibana_conf, {
                                 "elasticsearch_url": url}, ':')

    def start(self):
        return self.action(options.start_kibana)

    def stop(self):
        return self.action(options.stop_kibana)

    def restart(self):
        return self.action(options.restart_kibana)
