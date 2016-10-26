# -*- coding: utf-8 -*-
import os

from tornado.options import define

join = os.path.join
dirname = os.path.dirname

base_dir = os.path.abspath(dirname(dirname(__file__)))

define('port', default=9999, type=int, help='app listen port')
define('debug', default=False, type=bool, help='is debuging?')
define('sitename', default="logs manager", help='site name')
define('domain', default="letv.com", help='domain name')

define('send_email_switch', default=True, type=bool,
       help='the flag of if send error email')
define('admins', default=("zhoubingzheng <zhoubingzheng@letv.com>",
                          "wangyiyang <wangyiyang@le.com>",
                          "liujinliu <liujinliu@le.com>"), help='admin email address')
define('smtp_host', default="mail.letv.com", help='smtp host')
define('smtp_port', default=587, help='smtp port')
define('smtp_user', default="mcluster", help='smtp user')
define('smtp_password', default="Mcl_20140903!", help='smtp password')
define('smtp_from_address', default='mcluster@letv.com', help='smtp from address')
define('smtp_duration', default=10000, type=int, help='smtp duration')
define('smtp_tls', default=False, type=bool, help='smtp tls')

define("zk_property", default=join(base_dir, "config",
                                   "zookeeper.property"), help="logs manager config file")
define("data_node_property", default=join(base_dir, "config",
                                          "dataNode.property"), help="data componentNode config file")
define("cluster_property", default=join(base_dir, "config",
                                        "cluster.property"), help="cluster config file")
define("es_config", default="/etc/elasticsearch/elasticsearch.yml",
       help="es cnf file name")
define("sys_es_config", default="/etc/sysconfig/elasticsearch",
       help="sysconfig es cnf file name")
define("base_dir", default=base_dir, help="project base dir")

define("alarm_serious", default="tel:sms:email", help="alarm level is serious")
define("alarm_general", default="sms:email", help="alarm level is general")
define("alarm_nothing", default="nothing", help="no alarm")

define("tmp_keys_file", default="/tmp/keys/",
       help="store two keys file temporary")
define("openssl_crt_file", default="/etc/pki/tls/certs/logstash-forwarder.crt",
       help="opensll config file crt path")
define("openssl_key_file", default="/etc/pki/tls/private/logstash-forwarder.key",
       help="opensll config file key path")
define("openssl_conf", default="/etc/pki/tls/openssl.cnf",
       help="opensll config file path")
define("openssl_cmd", default="openssl req -x509 -batch -nodes -days 3650 -newkey rsa:2048 -keyout /etc/pki/tls/private/logstash-forwarder.key -out /etc/pki/tls/certs/logstash-forwarder.crt", help="get openssl rsa keys file")

define("start_logstash", default="service logstash start", help="start logstash")
define("stop_logstash", default="service logstash stop", help="stop logstash")
define("restart_logstash", default="service logstash restart", help="stop logstash")

define("logstash_forwarder_conf", default="/etc/logstash-forwarder.conf",
       help="logstash-forwarder config file")
define("start_logstash_forwarder", default="service logstash-forwarder start",
       help="start  logstash-forwarder")
define("stop_logstash_forwarder", default="service logstash-forwarder stop",
       help="stop  logstash-forwarder")
define("restart_logstash_forwarder",
       default="service logstash-forwarder restart", help="stop  logstash-forwarder")

define("start_elasticsearch", default="/etc/init.d/elasticsearch start",
       help="start  elasticsearch")
define("stop_elasticsearch", default="/etc/init.d/elasticsearch stop",
       help="stop  elasticsearch")
define("restart_elasticsearch",
       default="/etc/init.d/elasticsearch restart", help="stop  elasticsearch")

define("start_kibana", default="service kibana start", help="start kibana")
define("stop_kibana", default="service kibana stop", help="stop kibana")
define("restart_kibana", default="service kibana restart", help="restart kibana")
define("kibana_conf", default="/opt/kibana-4.0.2-linux-x64/config/kibana.yml",
       help="kibana config file path")

define("es_port", default=9200, type=int, help='es port')
define("es_heap_size", default=1073741824, type=int, help='es_heap_size')
