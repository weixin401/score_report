#!/usr/bin/env python
# fileencoding=utf-8
from tornado.web import RequestHandler
from base_handler import BaseHandler
import logging
import os


class TestHandler(BaseHandler):

    def get(self):
        template = self.template + '/tes.html'
        self.render(template)
