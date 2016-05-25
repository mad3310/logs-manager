import urllib
import httplib
import base64
from autotest import AutoTest
from multiprocessing.pool import ThreadPool

class Cluster(AutoTest):

    def __init__(self):
        '''init data'''
        self.container_ips = ["10.154.238.221", "10.154.238.222", "10.154.238.223"]
        #self.zk_ips = ["10.140.62.49", "10.140.62.48", "10.140.62.47"]
        self.zk_ips=["10.154.156.150","10.154.156.151","10.154.156.152"]
        self.main_host = self.container_ips[0]
        self.cluster_name = "es_mysql"
        self.user = 'root'
        self.pwd = 'root'

    def test(self):
        '''before all test processes'''

    def test_1(self):
        '''set zookeeper'''
        urls = [(self.container_ips[i], 9999, (), 'POST', '/admin/conf',
                 {"zkAddress": self.zk_ips[i], "zkPort":2181}) for i in range(len(self.container_ips))]
        code, data = multi_request(urls)
        return code != 200

    def test_2(self):
        '''set user'''
        urls = [(self.container_ips[i], 9999, (), 'POST', '/admin/user',
                 {"adminUser": self.user, "adminPassword": self.pwd}) for i in range(len(self.container_ips))]
        code, data = multi_request(urls)
        return code != 200

    def test_3(self):
        '''init cluster'''
        code, data = http_request(self.main_host, 9999, (self.user, self.pwd),
                                  'POST', "/elasticsearch/cluster/init", {"clusterName": self.cluster_name})
        return code != 200

    def test_4(self):
        '''sync data'''
        urls = [(self.container_ips[i], 9999, (self.user, self.pwd), 'POST', '/elasticsearch/cluster/sync',
                 {"clusterName": self.cluster_name}) for i in range(len(self.container_ips))]
        code, data = multi_request(urls)
        return code != 200

    def test_5(self):
        '''init node'''
        urls = [(self.container_ips[i], 9999, (self.user, self.pwd), 'POST', '/elasticsearch/node/init', {"dataNodeIp": self.container_ips[
                 i], "dataNodeName":"d-logs-%s-n-%d" % (self.cluster_name, i+1)}) for i in range(len(self.container_ips))]
        code, data = multi_request(urls)
        return code != 200

    def test_6(self):
        '''config es'''
        urls = [(self.container_ips[i], 9999, (self.user, self.pwd), 'POST',
                 '/elasticsearch/config', {}) for i in range(len(self.container_ips))]
        code, data = multi_request(urls)
        return code != 200

    def test_7(self):
        '''start es'''
        urls = [(self.container_ips[i], 9999, (self.user, self.pwd), 'POST',
                 '/elasticsearch/start', {}) for i in range(len(self.container_ips))]
        code, data = multi_request(urls)
        return code != 200


def http_request(host='127.0.0.1', port=80, user=(),
                 method='GET', path='/', data={}):
    params = urllib.urlencode(data)

    headers = {
        "Content-type": "application/x-www-form-urlencoded",
        "Accept": "text/plain",
    }
    if user:
        encode_user = base64.encodestring("%s:%s" % (user[0], user[1]))[:-1]
        auth = "Basic %s" % encode_user
        headers.update({"Authorization": auth})

    con = httplib.HTTPConnection(host, port)
    con.request(method, path, params, headers)
    response = con.getresponse()
    data = response.read()
    con.close()
    return response.status, data

def multi_request(requests):
    assert requests
    pool = ThreadPool(processes=4)
    code, req = 200, ''
    for item in requests:
        future = pool.apply_async(http_request, item)
        code, req = future.get()
        if code != 200:
            break
    return code, req


if __name__ == "__main__":
    test = Cluster()
    test.run()
