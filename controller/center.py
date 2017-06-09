#!/usr/bin/env python
# encoding: utf-8

import os
import json
import xlrd
import time
from util.base_handler import BaseHandler
from util.escape import safe_json_decode
import report
import excel


class FileUploadHandler(BaseHandler):

    def initialize(self, excel_type):
        self.excel_type = excel_type

    def get(self):
        template = 'upload' + str(self.excel_type) + '.html'
        self.render(template)

    def post(self):
        file_metas = self.request.files.get('file', None)
        students = excel.upload_excel(self, file_metas[0]['body'])
        self.write(json.dumps(students))


class ScoreReportHandler(BaseHandler):

    def initialize(self, report_type):
        self.report_type = report_type

    def get(self):
        pass

    def post(self):
        students_score = safe_json_decode(self.get_argument('students_score'))
        total_score = self.get_argument('total_score')
        total_score = int(total_score)
        school_name = self.get_argument('school_name', None)
        class_name = self.get_argument('class_name', None)
        result = report.generate_report(self, students_score, total_score, school_name, class_name)
        self.write(json.dumps(result))



