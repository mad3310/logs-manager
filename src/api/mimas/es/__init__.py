# -*- coding: utf-8 -*-

from elasticsearch import Elasticsearch

SNIFFER_TIMEOUT = 300
SNIFF_TIMEOUT = 20


class ElasticsearchEngine(object):

    def __init__(self, context):
        self.hosts = context.config.get('ELASTICSEARCH_SERVERS')
        self.engine = None

    def __repr__(self):
        return '<Elasticsearch servers=%s>' % self.hosts

    def connect(self):
        if self.engine is None:
            try:
                engine = Elasticsearch(
                    self.hosts,
                    sniff_on_start=False,
                    sniff_on_connection_fail=True,
                    sniffer_timeout=SNIFFER_TIMEOUT,
                    sniff_timeout=SNIFF_TIMEOUT,
                )
            except:
                raise
        self.engine = engine
        return engine

    def add(self, index, doc_type, body, doc_id=None):
        if not self.engine:
            self.connect()
        return self.engine.index(index=index, doc_type=doc_type, id=doc_id, body=body)

    def delete(self, index, doc_type, doc_id):
        if not self.engine:
            self.connect()
        self.engine.delete(index=index, doc_type=doc_type, id=doc_id)

    @classmethod
    def init_by_context(cls, context):
        return ElasticsearchEngine(context)

    def get_stats(self):
        if not self.engine:
            self.connect()
        return self.engine.cluster.stats()

    def get_health(self):
        if not self.engine:
            self.connect()
        return self.engine.cluster.health()



