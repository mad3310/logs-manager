# -*- coding: utf-8 -*-

import base64
import logging

from utils.configFileOpers import ConfigFileOpers
from base import APIHandler
from tornado.options import options
from utils.exceptions import HTTPAPIError
from tornado.web import RequestHandler


class AdminConf(APIHandler):

    confOpers = ConfigFileOpers()

    def post(self):
        """
        function: admin conf
        url example: curl -d "zkAddress=10.204.8.211&zkPort=2181" "http://localhost:8888/admin/conf"
        """
        requestParam = self.get_all_arguments()
        if requestParam != {}:
            self.confOpers.set_value(options.zk_property, requestParam, '=')

        result = {}
        result.setdefault("message", "admin conf successful!")
        self.finish(result)


class AdminUser(APIHandler):

    confOpers = ConfigFileOpers()

    def post(self):
        """
        function: create admin user
        url example: curl -d "adminUser=root&adminPassword=root" "http://localhost:8888/admin/user"
        """
        requestParam = self.get_all_arguments()
        if 'adminPassword' in requestParam:
            new_value = base64.encodestring(
                requestParam['adminPassword']).strip('\n')
            requestParam['adminPassword'] = new_value
        logging.info("args :" + str(requestParam))

        if requestParam != {}:
            self.confOpers.set_value(
                options.cluster_property, requestParam, '=')

        result = {}
        result.setdefault("message", "creating admin user successful!")
        self.finish(result)


class DownloadFile(RequestHandler):

    def get(self, filename):
        """
        function: create admin user
        url example: curl -d "adminUser=root&adminPassword=root" "http://localhost:8888/admin/user"
        """

        ifile = open(filename, "r")
        self.set_header('Content-Type', 'text/cnf')
        self.set_header('Content-Disposition',
                        'attachment; filename=' + filename + '')
        self.write(ifile.read())
