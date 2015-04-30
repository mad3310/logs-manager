#!/usr/bin/env python
#-*- coding: utf-8 -*-


from handlers.admin import AdminConf, AdminUser
from handlers.logstash import *
from handlers.logstash_forwarder import *

handlers = [
            (r"/admin/conf", AdminConf),
            (r"/admin/user", AdminUser),
            
            (r"/logstash/start", Logstash_Start_Handler),
            (r"/logstash/stop", Logstash_Stop_Handler),
            (r"/logstash/restart", Logstash_Restart_Handler),
            
            (r"/openssl/config", Openssl_Config_Handler),
            (r"/openssl/copy", Openssl_Copy_Handler),
            
            (r"/logstash_forwarder/start", Logstash_forwarder_Start_Handler),
            (r"/logstash_forwarder/stop", Logstash_forwarder_Stop_Handler),
            (r"/logstash_forwarder/restart", Logstash_forwarder_Restart_Handler),
            (r"/logstash_forwarder/config", Logstash_forwarder_Config_Handler),
]