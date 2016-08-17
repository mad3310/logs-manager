import socket
import psutil
import time

from logic.zk_opers import ZkOpers




class ESMonitor():
    zkoper = ZkOpers()
    MONITOR_IP = zkoper.get_self_ip()

    @staticmethod
    def _portuse(ip=MONITOR_IP, port=9200):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
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
    def save(ip=MONITOR_IP,zkoper=zkoper):
        ctime = time.strftime('%Y-%m-%d %H:%M:%S')
        data = {"availability": ESMonitor._portuse(ip=ip), "cpu_rate": ESMonitor._getcpuInfo(),
                "mem_rate": ESMonitor._get_mem_rate(), "sdisk_rate": ESMonitor._get_sdisk_rate(),"ctime":ctime}
        zkoper.write_monitor(data=data)