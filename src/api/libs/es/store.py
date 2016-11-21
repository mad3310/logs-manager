# -*- coding: utf-8 -*-

from tornado.options import options

from componentNode.elasticsearch_opers import ElasticsearchOpers
from common.appconfig import ES_PORT, ES_MONITOR_HOSTS


def _get_es():
    if not getattr(_get_es, '_es', None):
        from mimas.es.context import init_context
        from mimas.es import ElasticsearchEngine
        context = init_context('mcluster', ES_MONITOR_HOSTS)
        es = ElasticsearchEngine.init_by_context(context)
        _get_es._es = es
    return _get_es._es

MONITOR_ES = _get_es()


def _get_local_es():
    es_opers = ElasticsearchOpers()
    node_info = es_opers.config_op.getValue(options.data_node_property, ['dataNodeIp', 'dataNodeName'])
    node_ip = node_info.get('dataNodeIp')
    es_localhost = "{node_ip}:{es_port}".format(node_ip=node_ip, es_port=ES_PORT)
    if not getattr(_get_local_es, '_es', None):
        from mimas.es.context import init_context
        from mimas.es import ElasticsearchEngine
        context = init_context('logs', es_localhost)
        es = ElasticsearchEngine.init_by_context(context)
        _get_local_es._es = es
    return _get_local_es._es

LOCAL_ES = _get_local_es()