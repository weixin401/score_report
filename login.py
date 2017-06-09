#!/usr/bin/env python
# encoding: utf-8

import logging
from tornado.escape import json_encode
from util.base_handler import BaseHandler
from util.error import BLError
from model.user import find_user, create_user


class AuthLoginHandler(BaseHandler):

    def get(self):
        self.render('login.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        remember = self.get_argument('remember', True)

        self.do_password_login(username, password, remember)

    def do_password_login(self, username, password, remember=False):
        find_user(self, username, password)
        logging.info("%s is logined with password", username)
        self.post_login(username, password, remember)

    def post_login(self, username, password, remember):
        self.set_secure_cookie('username', username,
                               expires_days=30 if remember else None,
                               httponly=True)
        self.session.password = password
        self.redirect('/')


class AuthSignupHandler(BaseHandler):

    def get(self):
        self.render('signup.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        repassword = self.get_argument('repassword')
        user_id = create_user(self, username, password, repassword)
        if user_id:
            self.write({'success': True, 'error': u''})


class AuthLogoutHandler(BaseHandler):

    def get(self):
        self.do_logout()
    post = get

    def do_logout(self):
        self.clear_cookie('username')
        self.redirect('/')



