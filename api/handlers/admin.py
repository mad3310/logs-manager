#-*- coding: utf-8 -*-
import base64
import logging

from utils.configFileOpers import ConfigFileOpers
from base import APIHandler
from tornado.options import options
from utils.exceptions import HTTPAPIError
from tornado_letv.tornado_basic_auth import require_basic_auth


class AdminConf(APIHandler):
    
    confOpers = ConfigFileOpers()
    
    def post(self):
        '''
        function: admin conf
        url example: curl -d "zkAddress=10.204.8.211&zkPort=2181" "http://localhost:8888/admin/conf"
        '''
        requestParam = self.get_all_arguments()
        if requestParam != {}:
            self.confOpers.setValue(options.logs_manager_property, requestParam)
            
        result = {}
        result.setdefault("message", "admin conf successful!")
        self.finish(result)


class AdminUser(APIHandler):
    
    confOpers = ConfigFileOpers()
    
    def post(self):
        '''
        function: create admin user
        url example: curl -d "adminUser=root&adminPassword=root" "http://localhost:8888/admin/user"
        '''
        requestParam = {}
        args = self.request.arguments
        logging.info("args :"+ str(args))
        for key in args:
            value = args[key][0]
            if key == 'adminPassword':
                value = base64.encodestring(value).strip('\n')
            requestParam.setdefault(key,value)
        if requestParam['adminUser'] == '' or requestParam['adminPassword'] == '':
            raise HTTPAPIError(status_code=401, error_detail="username or password is empty",\
                               notification = "direct", \
                               log_message= "username or password is empty", \
                               response = "username or password is empty")
        if requestParam != {}:
            self.confOpers.setValue(options.cluster_property, requestParam)
        
        result = {}
        result.setdefault("message", "creating admin user successful!")
        self.finish(result)


@require_basic_auth
class DownloadFile(APIHandler):
    
    def get(self, filename):
        '''
        function: create admin user
        url example: curl -d "adminUser=root&adminPassword=root" "http://localhost:8888/admin/user"
        '''
        
        ifile  = open(filename, "r")
        self.set_header('Content-Type', 'text/cnf')
        self.set_header('Content-Disposition', 'attachment; filename='+filename+'')
        self.write(ifile.read())