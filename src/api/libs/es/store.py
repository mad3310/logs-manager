# -*- coding: utf-8 -*-

from tornado.options import options

from componentNode.elasticsearch_opers import ElasticsearchOpers


def _get_es():
    if not getattr(_get_es, '_es', None):
        from mimas.es.context import init_context
        from mimas.es import ElasticsearchEngine
        context = init_context('mcluster', options.es_hosts)
        es = ElasticsearchEngine.init_by_context(context)
        _get_es._es = es
    return _get_es._es

monitor_es = _get_es()


def _get_local_es():
    es_opers = ElasticsearchOpers()
    node_info = es_opers.config_op.getValue(options.data_node_property, ['dataNodeIp', 'dataNodeName'])
    node_ip = node_info.get('dataNodeIp')
    es_localhost = "{{node_ip}}:{{es_port}}".format(node_ip=node_ip,es_port=options.es_port)
    if not getattr(_get_local_es, '_es', None):
        from mimas.es.context import init_context
        from mimas.es import ElasticsearchEngine
        context = init_context('mcluster', es_localhost)
        es = ElasticsearchEngine.init_by_context(context)
        _get_local_es._es = es
    return _get_local_es._es

local_es = _get_local_es()