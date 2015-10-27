#!/usr/bin/env python
#-*- coding: utf-8 -*-


from handlers.admin import AdminConf, AdminUser, DownloadFile
from handlers.logstash import *
from handlers.logstash_forwarder import *
from handlers.elasticsearch import *
from handlers.kibana import *
from handlers.openssl import *


handlers = [
    (r"/admin/conf", AdminConf),
    (r"/admin/user", AdminUser),
    (r"/inner/admin/file/(.*)", DownloadFile),

    # for logstash
    (r"/logstash/start", Logstash_Start_Handler),
    (r"/logstash/stop", Logstash_Stop_Handler),
    (r"/logstash/restart", Logstash_Restart_Handler),

    (r"/openssl/config", Openssl_Config_Handler),
    (r"/openssl/copy", Openssl_Copy_Handler),
    (r"/openssl/info", Openssl_Info_Handler),

    # for logstash-forwarder, depracated
    (r"/logstash_forwarder/start", Logstash_forwarder_Start_Handler),
    (r"/logstash_forwarder/stop", Logstash_forwarder_Stop_Handler),
    (r"/logstash_forwarder/restart", Logstash_forwarder_Restart_Handler),
    (r"/logstash_forwarder/config", Logstash_forwarder_Config_Handler),

    # for kibana
    (r"/kibana/config", Kibana_Config_Handler),
    (r"/kibana/start", Kibana_Start_Handler),
    (r"/kibana/stop", Kibana_Stop_Handler),
    (r"/kibana/restart", Kibana_Restart_Handler),

    # for elasticsearch
    (r"/elasticsearch/cluster/init", ElasticsearchClusterInitHandler),
    (r"/elasticsearch/cluster/sync", ElasticsearchNodeSyncHandler),
    (r"/elasticsearch/node/init", ElasticsearchNodeInitHandler),
    (r"/elasticsearch/config", ElasticsearchConfigHandler),
    (r"/elasticsearch/start", Elasticsearch_Start_Handler),
    (r"/elasticsearch/stop", Elasticsearch_Stop_Handler),
    (r"/elasticsearch/restart", Elasticsearch_Restart_Handler),
]
