'''
Created on Mar 8, 2015

@author: root
'''

from base import APIHandler
from tornado_letv.tornado_basic_auth import require_basic_auth
from componentNode.elasticsearch_opers import ElasticsearchOpers


@require_basic_auth
class Elasticsearch_Start_Handler(APIHandler):
    
    elasticsearch_opers = ElasticsearchOpers()
    
    def post(self):
        '''
        function: start node
        url example: curl --user root:root -d "" "http://localhost:8888/elasticsearch/start"
        '''
        result = self.elasticsearch_opers.start()
        self.finish(result)


@require_basic_auth
class Elasticsearch_Stop_Handler(APIHandler):
    
    elasticsearch_opers = ElasticsearchOpers()
    
    def post(self):
        '''
        function: stop node
        url example: curl --user root:root -d "" "http://localhost:8888/elasticsearch/stop"
        '''
        result = self.elasticsearch_opers.stop()
        self.finish(result)


@require_basic_auth
class Elasticsearch_Restart_Handler(APIHandler):
    
    elasticsearch_opers = ElasticsearchOpers()
    
    def post(self):
        '''
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888/elasticsearch/restart"
        '''
        result = self.elasticsearch_opers.restart()
        self.finish(result)
