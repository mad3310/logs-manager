import os
import logging

from tornado.options import options
from common.abstractOpers import AbstractOpers


class LogstashOpers(AbstractOpers):

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
