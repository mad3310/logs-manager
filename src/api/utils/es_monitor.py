# -*- coding: utf-8 -*-
import socket

from tornado.options import options

from libs.es.store import es
from utils.mail import MailEgine
from componentNode.elasticsearch_opers import ElasticsearchOpers



class ESMonitor():


    @staticmethod
    def portuse(port=options.es_port):
        total_dic = {}
        es_opers = ElasticsearchOpers()
        node_info = es_opers.config_op.getValue(options.data_node_property, ['dataNodeIp', 'dataNodeName'])
        cluster_info = es_opers.config_op.getValue(options.cluster_property, ['clusterUUID', 'clusterName'])
        total_dic['cluster.name'] = cluster_info.get('clusterName')
        total_dic['node.name'] = node_info.get('dataNodeName')
        total_dic['node.ip'] = node_info.get('dataNodeIp')
        if not total_dic['cluster.name'] or not total_dic['node.name'] or not total_dic['node.ip']:
            return
        subject = "%s %s %s" % (total_dic['cluster.name'], total_dic['node.name'], "PORT(9200) ERROR")
        body = "%s %s %s" % (total_dic['cluster.name'], total_dic['node.name'], "PORT(9200) ERROR")
        try:
            ip = total_dic.get('node.ip')
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            s.shutdown(2)
        except:
            MailEgine.send_exception_email(options.smtp_from_address, options.admins, subject, body)

    @staticmethod
    def state():
        pass


    @staticmethod
    def main():
        pass




