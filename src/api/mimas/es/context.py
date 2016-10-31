# -*- coding: utf-8 -*-


class ElasticsearchContext(object):

    def __init__(self, **config):
        assert config.get('APP')
        assert config.get('ELASTICSEARCH_SERVERS')
        self.config = config

# 注释原因：目前线上部署还不支持.env环境变量自动导入
# def get_by_env_prefix(app_name):
#     mod = __import__('envcfg.json.%s' % app_name,
#                      fromlist=[app_name])
#     config = vars(mod)
#     return config


def init_context(app_name, servers=None):
    develop_mode = True

    # 注释原因：目前线上部署还不支持.env环境变量自动导入
    # config = get_by_env_prefix(app_name)
    # if config:
    #     hosts_str = config.get('ELASTICSEARCH_SERVERS')
    #     hosts = map(lambda x: dict(host=x.split(':')[0], port=x.split(':')[1]),
    #                 hosts_str.split(','),)

    if servers:
        hosts = map(lambda x: dict(host=x.split(':')[0], port=x.split(':')[1]),
                    servers.split(','),)

    if not hosts:
        raise Exception('ELASTICSEARCH_SERVER should not be empty.')

    return ElasticsearchContext(APP=app_name,
                                DEVELOP_MODE=develop_mode,
                                ELASTICSEARCH_SERVERS=hosts)
