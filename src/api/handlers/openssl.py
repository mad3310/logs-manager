from tornado_letv.tornado_basic_auth import require_basic_auth

from base import APIHandler
from logic.openssl_opers import OpensslOpers


@require_basic_auth
class Openssl_Config_Handler(APIHandler):

    openssl_opers = OpensslOpers()

    def post(self):
        '''
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888/openssl/config"
        '''

        args = self.get_all_arguments()
        self.openssl_opers.new_config(args)
        self.finish({"message": "config openssl success"})


@require_basic_auth
class Openssl_Copy_Handler(APIHandler):

    openssl_opers = OpensslOpers()

    def post(self):
        '''
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888//openssl/copy"
        '''
        args = self.get_all_arguments()
        self.openssl_opers.copyssl(args)
        self.finish({"message": "copy ok"})


@require_basic_auth
class Openssl_Info_Handler(APIHandler):

    openssl_opers = OpensslOpers()

    def post(self):
        '''
        function: reload node
        url example: curl --user root:root -d "" "http://localhost:8888//openssl/info"
        '''
        args = self.get_all_arguments()
        result = self.openssl_opers.get_info(args)
        self.finish({"message": result})
