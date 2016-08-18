import logging
import socket
import psutil
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
    def _getcpuInfo():
        return int(100-psutil.cpu_times_percent().idle)

    @staticmethod
    def _get_mem_rate():
        mem_rate = psutil.virtual_memory().percent
        return int(mem_rate)

    @staticmethod
    def _get_sdisk_rate():
        return int(psutil.disk_usage('/').percent)

    @staticmethod
    def save():
        try:
            zkoper = ZkOpers()
            ctime = time.strftime('%Y-%m-%d %H:%M:%S')
            data = {"availability": ESMonitor._portuse(), "cpu_rate": ESMonitor._getcpuInfo(),
                    "mem_rate": ESMonitor._get_mem_rate(), "sdisk_rate": ESMonitor._get_sdisk_rate(),"ctime":ctime}
            zkoper.write_monitor(data=data)
        except Exception as e:
            logging.info("zk not inited  (%s)" % (e))