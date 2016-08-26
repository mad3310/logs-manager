import logging
import socket
import time

from logic.zk_opers import ZkOpers
from tornado.options import options

from src.api.utils.mail import MailEgine

from src.api.componentNode.elasticsearch_opers import ElasticsearchOpers


class ESMonitor():

    @staticmethod
    def portuse(port=9200):
        es_opers = ElasticsearchOpers()
        node_info = es_opers.config_op.getValue(options.data_node_property, ['dataNodeIp', 'dataNodeName'])
        cluster_info = es_opers.config_op.getValue(options.cluster_property, ['clusterUUID', 'clusterName'])
        total_dic['cluster.name'] = cluster_info['clusterName']
        total_dic['node.name'] = node_info['dataNodeName']
        subject = ""
        body = ""
        try:
            zkoper = ZkOpers()
            ip = zkoper.get_self_ip()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except:
            MailEgine.send_normal_email(options.smtp_from_address, options.admins, subject, body)
            return False


# node_info = self.config_op.getValue(options.data_node_property, ['dataNodeIp', 'dataNodeName'])
# cluster_info = self.config_op.getValue(options.cluster_property, ['clusterUUID', 'clusterName'])
