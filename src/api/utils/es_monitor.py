import logging
import socket
import time

from logic.zk_opers import ZkOpers


class ESMonitor():
    @staticmethod
    def _portuse(port=9200):
        try:
            zkoper = ZkOpers()
            ip = zkoper.get_self_ip()
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((ip, int(port)))
            s.shutdown(2)
            return True
        except:
            return False

    @staticmethod
    def save():
        try:
            zkoper = ZkOpers()
            ctime = time.strftime('%Y-%m-%d %H:%M:%S')
            data = {"availability": ESMonitor._portuse(), "ctime":ctime}
            zkoper.write_monitor(data=data)
        except Exception as e:
            logging.info("zk not inited  (%s)" % (e))