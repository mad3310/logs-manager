import logging
import threading

from kazoo.client import KazooClient, KazooState
from kazoo.retry import KazooRetry


class ZkHelper(object):

    def __init__(self, address='', port=''):
        assert address and port
        self.zk_address = address
        self.zk_port = port
        self.retry = KazooRetry(max_delay=10000, max_tries=None)
        self.zk = KazooClient(hosts='%s:%s' % (
            self.zk_address, self.zk_port), connection_retry=self.retry, timeout=20)
        self.zk.add_listener(self._listener)
        self.zk.start()
        logging.info("instance zk client start (%s:%s)" %
                     (self.zk_address, self.zk_port))

    @staticmethod
    def _listener(state):
        if state == KazooState.LOST:
            logging.info(
                "zk connect lost, stop this connection and then start new one!")
        elif state == KazooState.SUSPENDED:
            logging.info(
                "zk connect suspended, stop this connection and then start new one!")

    def write(self, path, data):
        self.zk.ensure_path(path)
        self.retry(self.zk.set, path, data)
        logging.info("write data:%s to path:%s" % (data, path))

    def ensure_path(self, path):
        self.zk.ensure_path(path)

    def get_lock(self, path):
        return self.zk.Lock(path, threading.currentThread())

    def read(self, path):
        if self.zk.exists(path):
            data = self.retry(self.zk.get, path)
            logging.info("read data:%s from path:%s" % (data, path))
            return data[0]
        logging.info("path:%s not exist" % path)

    def get_children_list(self, path):
        if self.zk.exists(path):
            data = self.retry(self.zk.get_children, path)
            logging.info("get children:%s from path:%s" % (data, path))
            return data
        logging.info("path:%s not exist" % path)

    def exists(self, path):
        return self.zk.exists(path)

    def get_lock(self, path):
        lock = self.retry(self.zk.Lock, path, threading.current_thread())
        return lock

    def close(self):
        self.zk.close()
