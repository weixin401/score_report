#!/usr/bin/env python
# encoding: utf-8

import os
import xlrd
import time
import traceback
import copy
from error import BLError


def generate_report(handler, students_score, total_score, school_name, class_name):
    report_type_fuc = [generate_report_v0, generate_report_v1]
    report_type_fuc[handler.report_type](handler, students_score, total_score, school_name, class_name)


def generate_report_v0(handler, students_score, total_score, school_name, class_name):
    students_score.sort(key=lambda x: x['score'], reverse=True)
    rank_students(students_score, 'class_rank', total_score)
    class_total_score = 0
    perfect_count = 0
    good_count = 0
    pass_count = 0
    fail_count = 0
    score_segment = dict()
    max_segment = total_score / 10
    if total_score % 10 == 0:
        max_segment -= 1
    for segment in range(max_segment):
        score_segment[segment] = 0
    for student in students_score:
        score = student['score']
        class_total_score += score
        segment = score / 10
        if score % 10 == 0 and score == total_score:
            segment -= 1
        score_segment[segment] += 1
        if score == total_score:
            perfect_count += 1
            good_count += 1
            pass_count += 1
        elif score >= total_score * 0.85:
            good_count += 1
            pass_count += 1
        elif score >= total_score * 0.6:
            pass_count += 1
        else:
            fail_count += 1

    class_size = len(students_score)
    report = {
        'total_score': total_score,
        'average': round(class_total_score / class_size * 1.0, 1),
        'perfect': perfect_count,
        'perfect_rate': round(perfect_count / class_size * 1.0, 3),
        'good': good_count,
        'good_rate': round(good_count / class_size * 1.0, 3),
        'pass': pass_count,
        'pass_rate': round(pass_count / class_size * 1.0, 3),
        'fail': fail_count,
        'fail_rate': round(fail_count / class_size * 1.0, 3),
        'score_segment': score_segment,
        'school_name': school_name,
        'class_name': class_name,
        'students': students_score
    }
    return report


def rank_students(students_score, rank_type, total_score):
    last_score = total_score
    last_rank = 1
    for index, student in enumerate(students_score, 1):
        if student['score'] < last_score:
            last_rank = index
            last_score = student['score']
        student[rank_type] = last_rank


def generate_report_v1(handler,  students_score, total_score):
    students_score.sort(key=lambda x: x['score'])
    rank_students(students_score, 'grand_rank', total_score)
    class_report = dict()
    score_segment = dict()
    max_segment = total_score / 10
    if total_score % 10 == 0:
        max_segment -= 1
    for segment in range(max_segment):
        score_segment[segment] = 0

    for student in students_score:
        class_name = student['class_name']
        if class_name not in class_report:
            class_report[class_name] = {
                'perfect': 0, 'good': 0, 'pass': 0, 'fail': 0, 'size': 0,
                'score_segment': copy.deepcopy(score_segment), 'total_score': 0,
                'students': list()
            }
        class_report[class_name]['students'].append(student)
        report = class_report[class_name]
        report['size'] += 1
        score = student['score']
        report['total_score'] += score
        segment = score / 10
        if score % 10 == 0 and score == total_score:
            segment -= 1
        report['score_segment'][segment] += 1
        if score == total_score:
            report['perfect'] += 1
            report['good'] += 1
            report['pass'] += 1
        elif score >= total_score * 0.85:
            report['good'] += 1
            report['pass'] += 1
        elif score >= total_score * 0.6:
            report['pass'] += 1
        else:
            report['fail'] += 1

    for _, report in class_report.items():
        rank_students(report['students'], 'class_rank', total_score)
        report['perfect_rate'] = round(report['perfect'] / report['size'] * 1.0, 3)
        report['good_rate'] = round(report['good'] / report['size'] * 1.0, 3)
        report['pass_rate'] = round(report['pass'] / report['size'] * 1.0, 3)
        report['fail_rate'] = round(report['fail'] / report['size'] * 1.0, 3)
        report['average'] = round(report['total_score'] / report['size'], 1)

    return class_report
