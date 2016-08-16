from base import APIHandler
from logic.zk_opers import ZkOpers


class ElasticSearchClusterMonitorSync(APIHandler):

    def get(self):
        result = {}
        nodes_info = []
        zk_op = ZkOpers()
        children_list = zk_op.zk_helper.get_children_list(zk_op.monitor_path)
        for children in children_list:
            nodes_info.append({children: zk_op.read_monitor(children)})
        result.setdefault("nodes_info", nodes_info)
        self.finish(result)
