#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def prepare(self):
        pass

    @property
    def db(self):
        return self.settings['mongodb_client']['klx_xmath']

