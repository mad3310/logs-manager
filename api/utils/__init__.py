import base64
import logging
import socket
import os
import re

from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPError
from tornado.options import options

from utils.configFileOpers import ConfigFileOpers
from utils.invokeCommand import InvokeCommand


confOpers = ConfigFileOpers()

def get_zk_address():
        ret_dict = confOpers.getValue(options.logs_manager_property, ['zkAddress','zkPort'])
        zk_address = ret_dict['zkAddress']
        zk_port = ret_dict['zkPort']
        return zk_address, zk_port

def retrieve_userName_passwd():
    confDict = confOpers.getValue(options.cluster_property, ['adminUser','adminPassword'])
    adminUser = confDict['adminUser']
    adminPasswd = base64.decodestring(confDict['adminPassword'])
    return (adminUser,adminPasswd)

def get_dict_from_text(sourceText, keyList):
    totalDict = {}
    resultValue = {}
    
    lineList = sourceText.split('\n')
    for line in lineList:
        if not line:
            continue
        
        pos1 = line.find('=')
        key = line[:pos1]
        value = line[pos1+1:len(line)].strip('\n')
        totalDict.setdefault(key,value)
        
    if keyList == None:
        resultValue = totalDict
    else:
        for key in keyList:
            value = totalDict.get(key)
            resultValue.setdefault(key,value)
            
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

def set_file_data(filename, data, mode='w'):
    with open(filename, mode) as f:
        f.write(data)
        f.close()

def get_file_data(filename, mode='r'):
    with open(filename, mode) as f:
        data = f.read()
        f.close()
        return data