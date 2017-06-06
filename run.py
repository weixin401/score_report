#!/usr/bin/env python
# encoding: utf-8

import logging
import os

from tornado.httpserver import HTTPServer
from tornado.options import options, parse_command_line, parse_config_file
from tornado.ioloop import IOLoop
from tornado.web import Application

from jinja2 import ChoiceLoader
from jinja2 import FileSystemLoader
from template import JinjaLoader
from request_handlers import SmartStaticFileHandler, MultiFileFindler, install_tornado_shutdown_handler

from pymongo import MongoClient
import routes
import sys
import settings
reload(sys)
sys.setdefaultencoding('utf-8')
del sys.setdefaultencoding
del sys


class RunReport(Application):
    def __init__(self):
        settings.define_app_options()
        parse_command_line(final=False)
        self_dir = os.path.dirname(os.path.abspath(__file__))
        conf_file_path = os.path.join(self_dir, 'server.conf')
        if os.path.exists(conf_file_path):
            parse_config_file(conf_file_path, final=False)
        parse_command_line(final=True)

        loader = JinjaLoader(loader=ChoiceLoader([
            FileSystemLoader(os.path.join(self_dir, 'template')),
        ]), debug=options.debug)
        SmartStaticFileHandler.file_finder = MultiFileFindler(
            [],
            os.path.join(self_dir, 'static'))

        mongodb_client = self.setup_mongodb_client()
        app_settings = {
            'template_loader': loader,
            'mongodb_client': mongodb_client,
            'static_handler_class': SmartStaticFileHandler,
            'xsrf_cookies': False,
            'static_path': u'/static/',
            'debug': options.debug,
        }
        super(RunReport, self).__init__(routes.get(), **app_settings)

    @staticmethod
    def setup_mongodb_client():
        client = MongoClient(options.mongodb_host, options.mongodb_port)
        logging.info('Connected to subject db: %s:%d' %
                     (options.mongodb_host, options.mongodb_port))
        return client


def start(app):
    server = HTTPServer(app, xheaders=True)
    server.listen(options.port)
    install_tornado_shutdown_handler(IOLoop.instance(), server)
    logging.info("start service at port =  " + str(options.port) + "\n")

    IOLoop.instance().start()
    logging.info('Done. Bye.')


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                        datefmt='%y%m%d %H:%M:%S')
    app = RunReport()
    start(app)

if __name__ == "__main__":
    import sys
    sys.exit(main())

