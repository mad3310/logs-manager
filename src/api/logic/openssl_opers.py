import os
import re
import logging

from tornado.options import options
from common.abstractOpers import AbstractOpers
from utils import get_file_data, set_file_data
from utils import http_get


class OpensslOpers(AbstractOpers):

    def new_config(self, args):
        ip = args.get('ip')
        content = get_file_data(options.openssl_conf)
        target = re.findall('\[ v3_ca \]([\s\S]*?)\[', content)[0]
        replaced = re.findall('(.*subjectAltName=.*)', target)[0]
        new_replaced = "subjectAltName=IP:%s\n" % ip
        new_target = target.replace(replaced, new_replaced)
        content = content.replace(target, new_target)
        set_file_data(options.openssl_conf, content)
        logging.info('config openssl success')

        os.system(options.openssl_cmd)
        logging.info('generate .key and .crt file')

        self.backup_key_and_ca()

    @staticmethod
    def backup_key_and_ca():
        if not os.path.exists(options.tmp_keys_file):
            os.mkdir(options.tmp_keys_file)

        key_cmd = 'cp %s %s' % (
            options.openssl_key_file, options.tmp_keys_file)
        crt_cmd = 'cp %s %s' % (
            options.openssl_crt_file, options.tmp_keys_file)
        logging.info('do copy: %s' % key_cmd)
        logging.info('do copy: %s' % crt_cmd)
        os.system(key_cmd)
        os.system(crt_cmd)

    def config(self, args):

        _ip = args.get('ip')
        content = get_file_data(options.openssl_conf)
        replaced = re.findall('.*IP:(.*)\n?', content)[0]
        content = content.replace(replaced, _ip)
        set_file_data(options.openssl_conf, content)

        logging.info('generate .key and .crt file')
        os.system(options.openssl_cmd)

        self.backup_key_and_ca()

        return {"message": "config openssl.cnf successfully"}

    def copyssl(self, args):
        _ip = args.get('ip')
        port = args.get('port')
        logging.info('ip :%s, port:%s' % (_ip, port))
        crt_filepath = os.path.join(
            options.tmp_keys_file, 'logstash-forwarder.crt')
        key_filepath = os.path.join(
            options.tmp_keys_file, 'logstash-forwarder.key')
        host = "%s:%s" % (_ip, port)
        crt_ret = self._get(crt_filepath, host)
        key_ret = self._get(key_filepath, host)
        set_file_data(options.openssl_crt_file, crt_ret)
        set_file_data(options.openssl_key_file, key_ret)
        return {"message": "copy .crt and .key file successfully"}

    def get_info(self, args):
        tp = args.get('type')
        if tp == 'crt':
            path = options.openssl_crt_file
        elif tp == 'key':
            path = options.openssl_key_file
        else:
            return "type error"
        with open(path, 'r') as f:
            return f.read(1024)

    def _get(self, filename, host):
        uri = '/inner/admin/file/%s' % filename
        curl = 'http://%s%s' % (host, uri)
        fetch_ret = http_get(curl)
        return fetch_ret
