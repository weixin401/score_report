#!/usr/bin/env python
# encoding: utf-8
from base_handler import BaseHandler


class HomePageHandler(BaseHandler):

    def get(self):
        print self.db.user.find_one()
        self.render('HomePage.html')
