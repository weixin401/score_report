#!/usr/bin/env python
# encoding: utf-8

import tornado.ioloop
import logging
import os
from tornado.web import Application
import time
import argparse
import config
import routes
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
del sys.setdefaultencoding
del sys


class RunReport(Application):
    def __init__(self, args):
        self_dir = os.path.dirname(os.path.abspath(__file__))
        appsettings = {
            'xsrf_cookies': False,
            'debug': args.debug,
            'template': self_dir + '/template'
        }
        super(RunReport, self).__init__(routes.get(), **appsettings)


def start(app):
    app.listen(config.get('port'))
    logging.info("start service at port =  " + config.get('port') + "\n")
    tornado.ioloop.IOLoop.instance().start()


def main():
    argp = argparse.ArgumentParser()
    argp.add_argument('--debug', default=1, type=int)
    argp.add_argument('--port', required=True, type=int)
    args = argp.parse_args()
    if args.debug == 0:
        args.debug = False
    else:
        args.debug = True

    logging.basicConfig(level=logging.DEBUG,
                        format='[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
                        datefmt='%y%m%d %H:%M:%S')

    config.load_config('./server.conf')
    config.update('port', args.port)

    app = RunReport(args)
    start(app)

if __name__ == "__main__":
    import sys
    sys.exit(main())

