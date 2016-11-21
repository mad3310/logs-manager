# -*- coding: utf-8 -*-

import urllib2
import json

# MCLUSTER_VIP = 'localhost'
MCLUSTER_VIP = "10.154.255.131"
CPU_FIRE_LINE = 99
MEM_FIRE_LINE = 99
SDISK_FIRE_LINE = 99


def check_monitor_main(serious_dict, general_dict, nothing_dict):
    url = "http://%s:9998/elasticsearch/monitor" % (MCLUSTER_VIP)
    f = urllib2.urlopen(url)
    encodedjson = f.read()
    monitor_return_json_value = json.loads(encodedjson)

    reponse_code = monitor_return_json_value['meta']['code']
    if reponse_code != 200:
        serious_dict.setdefault(
            url, "due to response code error, please check email to find the reason!")
        return

    node_available = 0
    node_health = 0
    node_total = len(monitor_return_json_value['response']["nodes_info"])
    for node_info in monitor_return_json_value['response']["nodes_info"]:
        print node_info.keys()[0]
        if node_info[node_info.keys()[0]]["availability"]:
            node_available += 1
        if node_info[node_info.keys()[0]]['mem_rate'] < MEM_FIRE_LINE or \
                        node_info[node_info.keys()[0]][
                            'sdisk_rate'] < SDISK_FIRE_LINE or \
                        node_info[node_info.keys()[0]]['cpu_rate'] < CPU_FIRE_LINE:
            node_health += 1

    logic_return_message = "node_total={node_total},node_available={node_available},node_health={node_health}".format(
        node_total=node_total, node_available=node_available, node_health=node_health)
    if node_total > node_available:
        serious_dict.setdefault(
            "message", logic_return_message)
    elif node_total > node_health:
        general_dict.setdefault(
            "message", logic_return_message)
    else:
        nothing_dict.setdefault(
            "message", logic_return_message)


def main():
    serious_dict = {}

    general_dict = {}

    nothing_dict = {}

    check_monitor_main(serious_dict, general_dict, nothing_dict)

    print "main_serious:%s" % serious_dict
    print "main_general:%s" % general_dict
    print "main_nothing:%s" % nothing_dict


if __name__ == "__main__":
    main()
