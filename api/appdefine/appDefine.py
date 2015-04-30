#-*- coding: utf-8 -*-
import os

from tornado.options import define

join = os.path.join
dirname = os.path.dirname

base_dir = os.path.abspath(dirname(dirname(__file__)))

define('port', default = 8888, type = int, help = 'app listen port')
define('debug', default = False, type = bool, help = 'is debuging?')
define('sitename', default = "logs manager", help = 'site name')
define('domain', default = "letv.com", help = 'domain name')

define('send_email_switch', default = True, type = bool, help = 'the flag of if send error email')
define('admins', default = ("zhoubingzheng <zhoubingzheng@letv.com>", "zhangzeng <zhangzeng@letv.com>",), help = 'admin email address')
define('smtp_host', default = "mail.letv.com", help = 'smtp host')
define('smtp_port', default = 587, help = 'smtp port')
define('smtp_user', default = "mcluster", help = 'smtp user')
define('smtp_password', default = "Mcl_20140903!", help = 'smtp password')
define('smtp_from_address', default='mcluster@letv.com', help = 'smtp from address')
define('smtp_duration', default = 10000, type = int, help = 'smtp duration')
define('smtp_tls', default = False, type = bool, help = 'smtp tls')

define("logs_manager_property",default=join(base_dir, "config","logs_manager.property"), help="logs manager config file")
define("data_node_property",default=join(base_dir,"config","dataNode.property"), help="data componentNode config file")
define("cluster_property",default=join(base_dir,"config","cluster.property"), help="cluster config file")
define("cluster_property",default=join(base_dir,"config","cluster.property"), help="cluster config file")
define("base_dir", default=base_dir, help="project base dir")

define("alarm_serious", default="tel:sms:email", help="alarm level is serious")
define("alarm_general", default="sms:email", help="alarm level is general")
define("alarm_nothing", default="nothing", help="no alarm")

define("tmp_keys_file",default="/tmp/keys/", help="store two keys file temporary")
define("openssl_crt_file",default="/etc/ssl/certs/logstash-forwarder.crt", help="opensll config file crt path")
define("openssl_key_file",default="/etc/ssl/private/logstash-forwarder.key", help="opensll config file key path")
define("openssl_conf",default="/etc/pki/tls/openssl.cnf", help="opensll config file path")
define("openssl_cmd",default="openssl req -x509 -batch -nodes -newkey rsa:2048 -keyout /etc/ssl/private/logstash-forwarder.key -out /etc/ssl/certs/logstash-forwarder.crt -days 365", help="get openssl rsa keys file")

define("start_logstash",default="service logstash start", help="start logstash")
define("stop_logstash",default="service logstash stop", help="stop logstash")
define("restart_logstash",default="service logstash restart", help="stop logstash")

define("logstash_forwarder_conf",default="/etc/logstash-forwarder.conf", help="logstash-forwarder config file")
define("start_logstash-forwarder",default="service logstash-forwarder start", help="start  logstash-forwarder")
define("stop_logstash-forwarder",default="service logstash-forwarder stop", help="stop  logstash-forwarder")
define("reload_logstash-forwarder",default="service logstash-forwarder restart", help="stop  logstash-forwarder")