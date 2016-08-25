__author__ = 'xsank'

from tornado.options import options

from utils.zk_helper import ZkHelper
from utils import get_zk_address
from utils import getClusterUUID
from utils import get_cluster_name
from utils.configFileOpers import ConfigFileOpers
from utils.singleton import singleton


CONFIG_ES = 'es'

LOCK_CONFIG = 'config'


class ZkOpers(object):

    root_path = "/letv/elasticsearch/cluster"
    config_op = ConfigFileOpers()

    def __init__(self):
        self.zk_helper = None
        self.base_path = ''
        self.lock_path = ''
        self.config_path = ''
        self.datanode_path = ''
        self.monitor_path = ''
        self.status_path = ''
        self.init()
        self.init_path()

    def init(self):
        address, port = get_zk_address()
        self.zk_helper = ZkHelper(address, port)

    def init_path(self):
        self.base_path = self._get_base_path()
        self.lock_path = self.base_path + '/lock/'
        self.config_path = self.base_path + '/config/'
        self.datanode_path = self.base_path + '/datanode/'
        self.monitor_path = self.base_path + '/monitor/'
        self.status_path = self.base_path + '/status/'

    def _get_base_path(self):
        return self.root_path + '/' + get_cluster_name() + '/' + getClusterUUID()

    def watch_config(self):
        path = self.config_path + CONFIG_ES
        self.zk_helper.ensure_path(path)

        @self.zk_helper.zk.DataWatch(path)
        def watch_es_config(data, stat):
            data = self.read_es_config()
            if data:
                self_ip = self.config_op.get_value(
                    options.data_node_property, 'dataNodeIp')
                if self_ip in data['discovery.zen.ping.unicast.hosts']:
                    data['discovery.zen.ping.unicast.hosts'].remove(self_ip)
                self.config_op.set_value(options.es_config, data, ':')

    def get_self_ip(self):
        self_ip = self.config_op.get_value(
            options.data_node_property, 'dataNodeIp')
        return self_ip

    def cluster_exists(self, name):
        cluster_path = self.root_path + '/' + name
        return self.zk_helper.get_children_list(cluster_path)

    def get_config_lock(self):
        path = self.lock_path + LOCK_CONFIG
        return self.zk_helper.get_lock(path)

    def write(self, path, data):
        self.zk_helper.write(path, str(data))

    def read(self, path):
        data = self.zk_helper.read(path)
        return eval(data) if data else {}

    def write_cluster_info(self, data):
        self.write(self.base_path, data)

    def read_cluster_info(self):
        return self.read(self.base_path)

    def read_cluster_info(self, cluster_name, uuid):
        path = self.root_path + '/' + cluster_name + '/' + uuid
        return self.read(path)

    def read_cluster_info(self, cluster_name):
        cluster_path = self.root_path + '/' + cluster_name
        uuid = self.zk_helper.get_children_list(cluster_path)[0]
        path = cluster_path + '/' + uuid
        return self.read(path)

    def write_config(self, node, data):
        path = self.config_path + node
        self.write(path, data)

    def write_es_config(self, data):
        self.write_config(CONFIG_ES, data)

    def read_es_config(self):
        return self.read_config(CONFIG_ES)

    def read_config(self, node):
        path = self.config_path + node
        return self.read(path)

    def write_data_node(self, ip, data):
        path = self.datanode_path + ip
        self.write(path, data)

    def read_data_node(self, ip):
        path = self.datanode_path + ip
        return self.read(path)

    def write_monitor(self, data):
        node = self.get_self_ip()
        path = self.monitor_path + node
        self.write(path, data)

    def read_monitor(self, node):
        path = self.monitor_path + node
        return self.read(path)

    def write_status(self, data):
        self.write(self.status_path, data)

    def read_status(self):
        return self.read(self.status_path)


@singleton
class RequestZkOpers(ZkOpers):
    '''
    specially for request
    '''


@singleton
class ToolZkOpers(ZkOpers):
    '''
    specially for tool class
    '''

