import logging
import socket
import time

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
        if not total_dic['cluster.name'] or not total_dic['node.name']:
            return
        # title = "{cluster}-{node}-PORT(9200)ERROR".format(cluster=total_dic['cluster.name'], node=total_dic['node.name'])
        subject = "service down"
        body = "%s, %s, PORT(9200) ERROR" % (total_dic['cluster.name'], total_dic['node.name'])
        try:
            ip = "127.0.0.1"
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            s.shutdown(2)
        except:
            MailEgine.send_exception_email(options.smtp_from_address, options.admins, subject, body)