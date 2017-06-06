#!/usr/bin/env python
# fileencoding=utf-8

from base_handler import BaseHandler


class TestHandler(BaseHandler):

    def get(self):
        self.render('tes.html')
