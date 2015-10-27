'''
Created on Mar 13, 2015

@author: root
'''
import os
import uuid
import logging

from tornado.options import options
from common.abstractOpers import AbstractOpers
from utils.configFileOpers import ConfigFileOpers
from logic.zk_opers import ToolZkOpers


class ElasticsearchOpers(AbstractOpers):
    '''
    classdocs
    '''

    def __init__(self):
        self.config_op = ConfigFileOpers()
        self._zk_op = None

    @property
    def zk_op(self):
        return self._zk_op if self._zk_op else ToolZkOpers()

    def init_cluster(self, param):
        cluster_uuid = str(uuid.uuid1())
        param['clusterUUID'] = cluster_uuid

        self.config_op.set_value(options.cluster_property, param)
        self.zk_op.write_cluster_info(
            self.config_op.getValue(options.cluster_property))

    def sync_node(self, cluster_name):
        data = self.zk_op.read_cluster_info(cluster_name)
        self.config_op.set_value(options.cluster_property, data)
        self.zk_op.init_path()
        self.zk_op.watch_config()

    def init_node(self, param):
        self._add_ip(param['dataNodeIp'])
        self.config_op.set_value(options.data_node_property, param)
        self.zk_op.write_data_node(param['dataNodeIp'], param)

    def action(self, cmd):
        ret_val = os.system(cmd)

        result = {}
        if ret_val != 0:
            message = "do %s failed" % cmd
            logging.info(message)
            result.setdefault("message", message)
        else:
            message = "do %s successfully" % cmd
            logging.error(message)
            result.setdefault("message", message)

        return result

    def config(self):
        node_info = self.config_op.getValue(options.data_node_property, [
                                            'dataNodeIp', 'dataNodeName'])
        cluster_info = self.config_op.getValue(
            options.cluster_property, ['clusterUUID', 'clusterName'])

        total_dic = {}
        total_dic['cluster.name'] = cluster_info['clusterName']
        total_dic['node.name'] = node_info['dataNodeName']
        total_dic['index.number_of_shards'] = 2
        total_dic['path.data'] = '/var/log/esdata'
        total_dic['path.work'] = '/var/log/eswork'
        total_dic['bootstrap.mlockall'] = 'true'
        total_dic['network.host'] = node_info['dataNodeIp']
        total_dic['discovery.zen.minimum_master_nodes'] = 3
        total_dic['discovery.zen.ping.timeout'] = '5s'
        total_dic['discovery.zen.ping.multicast.enabled'] = 'false'
        # this should be set from zookeeper listener
        # total_dic['discovery.zen.ping.unicast.hosts']=''#get from zookeeper

        self.config_op.set_value(options.es_config, total_dic, separator=':')

    def _add_ip(self, ip):
        lock = self.zk_op.get_config_lock()
        with lock:
            zk_ip = self.zk_op.read_es_config()
            if zk_ip:
                ips = zk_ip['discovery.zen.ping.unicast.hosts']
                if ip not in ips:
                    ips.append(ip)
            else:
                zk_ip['discovery.zen.ping.unicast.hosts'] = [ip]
            self.zk_op.write_es_config(zk_ip)

    def _remove_ip(self, ip):
        lock = self.zk_op.get_config_lock()
        with lock:
            zk_ip = self.zk_op.read_es_config()
            if zk_ip:
                ips = zk_ip['discovery.zen.ping.unicast.hosts']
                if ip in ips:
                    ips.remove(ip)
            self.zk_op.write_es_config(zk_ip)

    def start(self):
        return self.action(options.start_elasticsearch)

    def stop(self):
        return self.action(options.stop_elasticsearch)

    def restart(self):
        return self.action(options.restart_elasticsearch)
