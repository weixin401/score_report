#!/usr/bin/env python
# encoding: utf-8

import logging
from tornado.options import define


def define_app_options():
    define('debug', default=True)
    define('log_level', default=logging.INFO)
    define('cookie_secret', default='')
    define('port', default=8001)

    define('mongodb_host', default='127.0.0.1')
    define('mongodb_port', default=27017)
    define('mongodb_name', default="test")
    define('db_name')
    define('types', default=[])
