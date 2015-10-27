#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os.path
import routes
import logging.config
import tornado.ioloop
import tornado.options
import tornado.web

from tornado.options import options
from tornado.httpserver import HTTPServer
from appdefine import appDefine


class Application(tornado.web.Application):

    def __init__(self):
        template_path = os.path.join(options.base_dir, "templates"),
        settings = dict(debug=options.debug)
        tornado.web.Application.__init__(self, routes.handlers, **settings)


def main():
    config_path = os.path.join(options.base_dir, "config")
    logging.config.fileConfig(config_path + '/logging.conf')
    tornado.options.parse_command_line()
    http_server = HTTPServer(Application())
    http_server.listen(options.port)

    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
