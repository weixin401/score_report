#!/usr/bin/env python
# encoding: utf-8

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def initialize(self):
        redis = self.application.redis
        self.session = self.application.SessionHandler(self, redis, session_lifetime=20)
        self.current_password = self.session.password

    def prepare(self):
        pass

    @property
    def db(self):
        return self.settings['mongodb_client']['report']

    @property
    def upload_dir(self):
        return self.settings['upload_dir']

    def get_current_user(self):
        return self.get_secure_cookie("username")

