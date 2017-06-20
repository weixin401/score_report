#!/usr/bin/env python
# encoding: utf-8

import os
import xlrd
import time
import traceback

from util.error import BLError

XLS_TYPE = [[u'student_name', u'score'],
            [u'student_name', u'class_name', u'score']]


def checkout_item_sum_score(students):
    wrong_score = list()
    wrong_item_score = list()
    for student in students:
        score_sum = 0
        for index, score in enumerate(student['items_score']):
            score_sum += score
            if score > students[0]['items_score'][index]:
                wrong_item_score.append(student['student_name'])
        if score_sum != student['score']:
            wrong_score.append(student['student_name'])
    if len(wrong_score) != 0 or len(wrong_item_score) != 0:
        message = ''
        if len(wrong_score) != 0:
            message += u'{} 小题得分总和与得分不符'.format(','.join(wrong_score))
        if len(wrong_item_score) != 0:
            message += u'{} 小题得分超过试卷预设分数'.format(','.join(wrong_item_score))
        return {'message': message,
                'status': False}
    else:
        return {'status': True}


def upload_excel(handler, data):
    xls_name = str(time.time()) + '_temp_score.xls'
    try:
        students_xls = open(xls_name, 'w')
        students_xls.write(data)
        students_xls.close()
        xls = xlrd.open_workbook(xls_name)
        table = xls.sheets()[0]
    except:
        if os.path.exists(xls_name):
            os.remove(xls_name)
        return {'message': u'excel 文件不合法', 'status': False}
    students = []
    if handler.excel_type <= 1:
        xls_dict = XLS_TYPE[handler.excel_type]
        try:
            for row in range(table.nrows):
                student = dict()
                for col in range(min(table.ncols, len(xls_dict))):
                    value = table.cell(row, col).value
                    if type(value) is float:
                        value = int(value)
                    student[xls_dict[col]] = value
                students.append(student)
            if os.path.exists(xls_name):
                os.remove(xls_name)
        except:
            print traceback.print_exc()
            if os.path.exists(xls_name):
                os.remove(xls_name)
            return {'message': u'excel 解析失败', 'status': False}
    elif handler.excel_type <= 3:
        try:
            students.append({
                'student_name': u'预设分数',
                'class_name': u'预设分数',
                'score': int(table.cell(0, 1).value) if handler.excel_type == 2 else int(table.cell(0, 2).value),
                'items_score': [int(table.cell(0, col).value)
                                for col in range(2 if handler.excel_type == 2 else 3, table.ncols)]
            })
            for row in range(1, table.nrows):
                student = dict()
                student['student_name'] = table.cell(row, 0).value
                if handler.excel_type == 2:
                    student['score'] = int(table.cell(row, 1).value)
                else:
                    student['class_name'] = table.cell(row, 1).value
                    student['score'] = int(table.cell(row, 2).value)
                student['items_score'] = list()
                for col in range(2 if handler.excel_type == 2 else 3, table.ncols):
                    value = int(table.cell(row, col).value)
                    student['items_score'].append(value)
                students.append(student)
            if os.path.exists(xls_name):
                os.remove(xls_name)
            status = checkout_item_sum_score(students)
            if status['status'] is False:
                return status
        except:
            print traceback.print_exc()
            if os.path.exists(xls_name):
                os.remove(xls_name)
            return {'message': u'excel 解析失败', 'status': False}

    return {'status': True, 'students': students}
