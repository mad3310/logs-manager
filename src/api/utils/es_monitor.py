# -*- coding: utf-8 -*-

import logging

from elasticsearch import TransportError
from tornado.options import options

from utils.mail import MailEgine
from componentNode.elasticsearch_opers import ElasticsearchOpers
from common.appconfig import ES_MONTIOR_TRTRY
from libs.es.store import LOCAL_ES


class ESMonitor:
    def __init__(self):
        self.retry = 0
        self.node_info = self.get_node_info()

    def get_node_info(self):
        total_dic = {}
        es_opers = ElasticsearchOpers()
        node_info = es_opers.config_op.getValue(options.data_node_property, ['dataNodeIp', 'dataNodeName'])
        cluster_info = es_opers.config_op.getValue(options.cluster_property, ['clusterUUID', 'clusterName'])
        total_dic['cluster.name'] = cluster_info.get('clusterName')
        total_dic['node.name'] = node_info.get('dataNodeName')
        total_dic['node.ip'] = node_info.get('dataNodeIp')
        return total_dic

    def get_stats(self):
        return LOCAL_ES.get_stats()


    def send_mail(self, message):
        subject = "%s %s %s" % (self.node_info['cluster.name'], self.node_info['node.name'], message)
        body = "%s %s %s" % (self.node_info['cluster.name'], self.node_info['node.name'], message)
        MailEgine.send_exception_email(options.smtp_from_address, options.admins, subject, body)



es_monitor = ESMonitor()

def main():
    stats = None
    while True:
        try:
            stats = es_monitor.get_stats()
        except TransportError as e:
            logging.info(e)
            stats = None

        if stats is None:
            es_monitor.retry += 1
        else:
            es_monitor.retry = 0
            break
        if es_monitor.retry == ES_MONTIOR_TRTRY:
            es_monitor.send_mail("are not available")
            break




