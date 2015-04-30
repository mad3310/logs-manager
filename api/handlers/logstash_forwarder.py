'''
Created on Mar 8, 2015

@author: root
'''
from base import APIHandler
from tornado_letv.tornado_basic_auth import require_basic_auth
from tornado.web import asynchronous
from componentNode.logstash_forwarder_opers import LogstashForwarderOpers


@require_basic_auth
class Logstash_forwarder_Start_Handler(APIHandler):
    
    logstash_forwarder_opers = LogstashForwarderOpers()
    
    @asynchronous
    def post(self):
        '''
        function: start node
        url example: curl --user root:root -d "" "http://localhost:8888/cluster/node/start"
        '''
        result = self.logstash_forwarder_opers.start()
        self.finish(result)


@require_basic_auth
class Logstash_forwarder_Stop_Handler(APIHandler):
    
    logstash_forwarder_opers = LogstashForwarderOpers()
    
    def post(self):
        '''
        function: stop node
        url example: curl --user root:root -d "" "http://localhost:8888/node/stop"
        '''
        result = self.logstash_forwarder_opers.stop()
        self.finish(result)


@require_basic_auth
class Logstash_forwarder_Restart_Handler(APIHandler):
    
    logstash_forwarder_opers = LogstashForwarderOpers()
    
    def post(self):
        '''
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888/node/reload"
        '''
        result = self.logstash_forwarder_opers.restart()
        self.finish(result)


@require_basic_auth
class Logstash_forwarder_Config_Handler(APIHandler):
    
    logstash_forwarder_opers = LogstashForwarderOpers()
    
    def post(self):
        '''
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888/node/reload"
        '''
        args = self.get_all_arguments()
        result = self.logstash_forwarder_opers.config(args)
        self.finish(result)
        