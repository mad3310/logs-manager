
from base import APIHandler
from tornado_letv.tornado_basic_auth import require_basic_auth
from componentNode.openssl_opers import OpensslOpers


@require_basic_auth
class Openssl_Config_Handler(APIHandler):
    
    openssl_opers = OpensslOpers()
    
    def post(self):
        '''
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888/node/reload"
        '''
        
        args = self.get_all_arguments()
        result = self.openssl_opers.config(args)
        self.finish(result)


@require_basic_auth
class Openssl_Copy_Handler(APIHandler):
    
    openssl_opers = OpensslOpers()
    
    def post(self):
        '''
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888//openssl/copy"
        '''
        args = self.get_all_arguments()
        result = self.openssl_opers.copyssl(args)
        self.finish(result)