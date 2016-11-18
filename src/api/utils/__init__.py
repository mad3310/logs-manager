import base64
import logging
import socket
import os
import re
import urllib
import json

from tornado.httpclient import HTTPError, HTTPRequest, HTTPClient
from tornado.options import options

from utils.configFileOpers import ConfigFileOpers
from utils.invokeCommand import InvokeCommand
from utils.exceptions import CommonException


confOpers = ConfigFileOpers()


def get_zk_address():
    ret_dict = confOpers.getValue(options.zk_property, ['zkAddress', 'zkPort'])
    zk_address = ret_dict['zkAddress']
    zk_port = ret_dict['zkPort']
    return zk_address, zk_port


def retrieve_userName_passwd():
    confDict = confOpers.getValue(options.cluster_property, [
                                  'adminUser', 'adminPassword'])
    adminUser = confDict['adminUser']
    adminPasswd = base64.decodestring(confDict['adminPassword'])
    return (adminUser, adminPasswd)


def get_dict_from_text(sourceText, keyList):
    totalDict = {}
    resultValue = {}

    lineList = sourceText.split('\n')
    for line in lineList:
        if not line:
            continue

        pos1 = line.find('=')
        key = line[:pos1]
        value = line[pos1 + 1:len(line)].strip('\n')
        totalDict.setdefault(key, value)

    if keyList == None:
        resultValue = totalDict
    else:
        for key in keyList:
            value = totalDict.get(key)
            resultValue.setdefault(key, value)

    return resultValue


def getNIC():
    cmd = "route -n|grep UG|awk '{print $NF}'"
    _nic = os.popen(cmd).read()
    return _nic.split('\n')[0]


def get_host_ip():
    NIC = getNIC()
    cmd = "ifconfig %s|grep 'inet addr'|awk '{print $2}'" % NIC
    out_ip = os.popen(cmd).read()
    ip = out_ip.split('\n')[0]
    ip = re.findall('.*:(.*)', ip)[0]
    return ip


def getClusterUUID():
    ret_dict = confOpers.getValue(options.cluster_property, ['clusterUUID'])
    clusterUUID = ret_dict['clusterUUID']
    return clusterUUID


def get_cluster_name():
    ret_dict = confOpers.getValue(options.cluster_property, ['clusterName'])
    return ret_dict['clusterName']


def set_file_data(filename, data, mode='w'):
    with open(filename, mode) as f:
        f.write(data)
        f.close()


def get_file_data(filename, mode='r'):
    with open(filename, mode) as f:
        data = f.read()
        f.close()
        return data


def _request_fetch(request):
    # access to the target ip machine to retrieve the dict,then modify the
    # config
    http_client = HTTPClient()

    response = None
    try:
        response = http_client.fetch(request)
    finally:
        http_client.close()

    return_result = False
    if response is None:
        raise CommonException('response is None!')

    if response.error:
        return_result = False
        message = "remote access,the key:%s,error message:%s" % (
            request, response.error)
        logging.error(message)
    else:
        return_result = response.body.strip()

    return return_result


def http_post(url, body={}, _connect_timeout=40.0, _request_timeout=40.0, auth_username=None, auth_password=None):
    request = HTTPRequest(url=url, method='POST', body=urllib.urlencode(body), connect_timeout=_connect_timeout,
                          request_timeout=_request_timeout, auth_username=auth_username, auth_password=auth_password)
    fetch_ret = _request_fetch(request)
    return_dict = json.loads(fetch_ret)
    logging.info('POST result :%s' % str(return_dict))
    return return_dict


def http_get(url, _connect_timeout=40.0, _request_timeout=40.0, auth_username=None, auth_password=None):
    request = HTTPRequest(url=url, method='GET', connect_timeout=_connect_timeout, request_timeout=_request_timeout,
                          auth_username=auth_username, auth_password=auth_password)
    fetch_ret = _request_fetch(request)
    #return_dict = json.loads(fetch_ret)
    logging.info('GET result :%s' % str(fetch_ret))
    return fetch_ret
