# -*- coding: utf-8 -*-
from base import APIHandler

from tornado_letv.tornado_basic_auth import require_basic_auth
from componentNode.elasticsearch_opers import ElasticsearchOpers
from utils.exceptions import HTTPAPIError
from common.appconfig import ES_HEAP_SIZE

from libs.es.store import LOCAL_ES


class ElasticSearchBaseHandler(APIHandler):

    elastic_op = ElasticsearchOpers()

    def check_cluster(self, name):
        zk_op = self.get_zkoper()
        if zk_op.cluster_exists(name) or not name:
            raise HTTPAPIError(status_code=417, error_detail="server has belong to a cluster,\
                                    should be not create new cluster!",
                               notification="direct",
                               log_message="server has belong to a cluster,should be not \
                                    create new cluster!",
                               response="the server has belonged to a cluster,should be \
                                    not create new cluster!")


@require_basic_auth
class ElasticsearchClusterInitHandler(ElasticSearchBaseHandler):

    def post(self):
        param = self.pretty_param()
        cluster_name = param['clusterName']
        self.check_cluster(cluster_name)

        self.elastic_op.init_cluster(param)
        self.finish({"message": "creating cluster successful!"})


@require_basic_auth
class ElasticsearchNodeInitHandler(ElasticSearchBaseHandler):

    def post(self):
        param = self.pretty_param()
        self.elastic_op.init_node(param)
        self.finish({"message": "creating cluster successful!"})


@require_basic_auth
class ElasticsearchNodeSyncHandler(ElasticSearchBaseHandler):

    def post(self):
        param = self.pretty_param()
        zk_op = self.get_zkoper()
        if zk_op.cluster_exists(param['clusterName']):
            self.elastic_op.sync_node(param['clusterName'])
        self.finish({"message": "sync cluster info successful!"})


@require_basic_auth
class ElasticsearchConfigHandler(ElasticSearchBaseHandler):
    """
    function: start node
    url example: curl --user root:root -d "" "http://localhost:9999/elasticsearch/config"
    """

    def post(self):
        param = self.pretty_param()
        es_heap_size = int(param.get('es_heap_size', ES_HEAP_SIZE))
        if es_heap_size < ES_HEAP_SIZE:
            self.set_status(500)
            self.finish({"message": "para not valid!"})
            return
        self.elastic_op.config()
        self.elastic_op.sys_config(
            es_heap_size='%dg' % (es_heap_size / ES_HEAP_SIZE))
        self.finish({"message": "config cluster successful!"})


@require_basic_auth
class Elasticsearch_Start_Handler(ElasticSearchBaseHandler):

    def post(self):
        """
        function: start node
        url example: curl --user root:root -d "" "http://localhost:8888/elasticsearch/start"
        """
        self.elastic_op.pull_config()
        result = self.elastic_op.start()
        self.finish(result)


@require_basic_auth
class Elasticsearch_Stop_Handler(ElasticSearchBaseHandler):

    def post(self):
        """
        function: stop node
        url example: curl --user root:root -d "" "http://localhost:8888/elasticsearch/stop"
        """
        result = self.elastic_op.stop()
        self.finish(result)


@require_basic_auth
class Elasticsearch_Restart_Handler(ElasticSearchBaseHandler):

    def post(self):
        """
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888/elasticsearch/restart"
        """
        result = self.elastic_op.restart()
        self.finish(result)


@require_basic_auth
class Elasticsearch_Nodes_Handler(ElasticSearchBaseHandler):

    def post(self):
        """
        function:add node
        url example: curl --user root:root -X POST
                     -d "ips=["10.154.255.248"]" "http://localhost:9999/elasticsearch/nodes"
        """
        requestParam = self.get_all_arguments()
        ips = eval(requestParam.get("ips", []))
        result = self.elastic_op.add_ip(ips)
        self.finish(result)

    def delete(self):
        """
        function:remove node
        url example: curl -g --user root:root -X DELETE "http://localhost:9999/elasticsearch/nodes?ips=['10.154.255.243']"
        """
        requestParam = self.get_all_arguments()
        ips = eval(requestParam.get("ips", []))
        result = self.elastic_op.remove_ip(ips)
        self.finish(result)


@require_basic_auth
class Elasticsearch_Health_Handler(ElasticSearchBaseHandler):
    """
    function:get health
    url example: curl --user root:root  "http://localhost:9999/elasticsearch/health"
    """

    def get(self):
        result = LOCAL_ES.get_health()
        self.finish(result)
