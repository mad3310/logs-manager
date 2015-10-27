'''
Created on Mar 8, 2015

@author: root
'''

from base import APIHandler
from tornado_letv.tornado_basic_auth import require_basic_auth
from componentNode.logstash_opers import LogstashOpers


@require_basic_auth
class Logstash_Start_Handler(APIHandler):

    logstash_opers = LogstashOpers()

    def post(self):
        '''
        function: start node
        url example: curl --user root:root -d "" "http://localhost:8888/cluster/node/start"
        '''
        result = self.logstash_opers.start()
        self.finish(result)


@require_basic_auth
class Logstash_Stop_Handler(APIHandler):

    logstash_opers = LogstashOpers()

    def post(self):
        '''
        function: stop node
        url example: curl --user root:root -d "" "http://localhost:8888/node/stop"
        '''
        result = self.logstash_opers.stop()
        self.finish(result)


@require_basic_auth
class Logstash_Restart_Handler(APIHandler):

    logstash_opers = LogstashOpers()

    def post(self):
        '''
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888/node/reload"
        '''
        result = self.logstash_opers.restart()
        self.finish(result)
