#!/usr/bin/env python
# encoding: utf-8

import os
import xlrd
import time
import traceback

from error import BLError

XLS_TYPE = [[u'student_name', u'score'],
            [u'student_name', u'class_name', u'score']]


def upload_excel(handler, data):
    xls_dict = XLS_TYPE[handler.excel_type]
    xls_name = str(time.time()) + '_temp_score.xls'
    try:
        students_xls = open(xls_name, 'w')
        students_xls.write(data)
        students_xls.close()
        xls = xlrd.open_workbook(xls_name)
        table = xls.sheets()[0]
        students = []
        for row in range(table.nrows):
            student = dict()
            for col in range(min(table.ncols, len(xls_dict))):
                value = table.cell(row, col).value
                if type(value) is float:
                    value = str(int(value))
                student[xls_dict[col]] = value
            students.append(student)
        if os.path.exists(xls_name):
            os.remove(xls_name)
        return students
    except:
        print traceback.print_exc()
        if os.path.exists(xls_name):
            os.remove(xls_name)
        raise BLError(u'excel 上传失败')
