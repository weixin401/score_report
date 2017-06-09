#!/usr/bin/env python
# encoding: utf-8
from util.base_handler import BaseHandler


class HomePageHandler(BaseHandler):

    def get(self):
        self.render('HomePage.html',
                    user=self.current_user)
