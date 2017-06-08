#!/usr/bin/env python
# encoding: utf-8

import logging
from tornado.escape import json_encode
from base_handler import BaseHandler
from error import BLError
from model.user import find_user, create_user


class AuthLoginHandler(BaseHandler):

    def get(self):
        next_url = self.get_argument('next_url', '')
        if self.current_user and self.current_user.is_login() and next_url:
            self.redirect(next_url)
        else:
            self.render('login.html',
                        next_url=next_url)

    def post(self):
        email = self.get_argument('email')
        password = self.get_argument('password')
        remember = self.get_argument('remember', False)
        next_url = self.get_argument('next_url', u'')

        error = u''
        url = '/'
        try:
            self.do_password_login(email, password, remember)
            if next_url:
                url = next_url
        except BLError as er:
            error = er.message

        self.write({
            'success': not error,
            'url': url,
            'error': error,
        })

    def do_password_login(self, email, password, remember=False):
        db_user = find_user(self, email, password)
        logging.info("%s is logined with password", db_user['username'])
        self.post_login(db_user, remember)

    def post_login(self, db_user, remember):
        self.current_user = db_user
        self.set_secure_cookie('user',
                               json_encode(self.current_user.as_cookie_stub()),
                               expires_days=30 if remember else None,
                               httponly=True)


class AuthSignupHandler(BaseHandler):

    def get(self):
        self.render('signup.html')

    def post(self):
        username = self.get_argument('username')
        password = self.get_argument('password')
        user_id = create_user(self, username, password)
        if user_id:
            self.write({'success': True, 'error': u''})




