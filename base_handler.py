#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def initialize(self):
        pass

    def prepare(self):
        pass

    @property
    def db(self):
        return self.settings['mongodb_client']['klx_xmath']

    @property
    def upload_dir(self):
        return self.settings['upload_dir']

