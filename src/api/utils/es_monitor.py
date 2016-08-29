import logging
import socket
import time

from logic.zk_opers import ZkOpers
from tornado.options import options

from utils.mail import MailEgine

from componentNode.elasticsearch_opers import ElasticsearchOpers


class ESMonitor():

    @staticmethod
    def portuse(port=9200):
        total_dic = {}
        es_opers = ElasticsearchOpers()
        node_info = es_opers.config_op.getValue(options.data_node_property, ['dataNodeIp', 'dataNodeName'])
        cluster_info = es_opers.config_op.getValue(options.cluster_property, ['clusterUUID', 'clusterName'])
        total_dic['cluster.name'] = cluster_info['clusterName']
        total_dic['node.name'] = node_info['dataNodeName']
        subject = "test subject"
        body = "test body"
        try:
            ip = "127.0.0.1"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            print "Y" * 30
            s.shutdown(2)
            print 1
        except:
            print "Z" * 30

            print options.smtp_from_address, ['wangyiyang <wangyiyang@le.com>'], subject, body
            MailEgine.send_exception_email(options.smtp_from_address, ['wangyiyang <wangyiyang@le.com>'], subject, body)
            print "W" * 30