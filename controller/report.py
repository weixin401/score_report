#!/usr/bin/env python
# encoding: utf-8

import os
import xlrd
import time
import traceback
import copy
import numpy as np
import pandas as pd
from util.error import BLError


def generate_report(handler, students_score):
    report_type_fuc = [generate_report_v0, generate_report_v1, generate_report_v2, generate_report_v3]
    return report_type_fuc[handler.report_type](handler, students_score)


def class_base_report(handler, students_score, total_score):
    students_score.sort(key=lambda x: x['score'], reverse=True)
    rank_students(students_score, 'class_rank', total_score)
    class_total_score = 0
    perfect_count = 0
    good_count = 0
    pass_count = 0
    fail_count = 0
    score_segment = dict()
    perfect_students = list()
    max_segment = total_score / 10
    if total_score % 10 == 0:
        max_segment -= 1
    for segment in range(max_segment + 1):
        score_segment[segment] = 0
    for student in students_score:
        score = int(student['score'])
        class_total_score += score
        segment = score / 10
        if score % 10 == 0 and score == total_score:
            segment -= 1
        score_segment[segment] += 1
        if score == total_score:
            perfect_count += 1
            perfect_students.append(student['student_name'])
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
        'average': round(float(class_total_score) / class_size, 1),
        'perfect': perfect_count,
        'perfect_student': perfect_students,
        'perfect_rate': round(float(perfect_count) / class_size, 3),
        'good': good_count,
        'good_rate': round(float(good_count) / class_size, 3),
        'pass': pass_count,
        'pass_rate': round(float(pass_count) / class_size, 3),
        'fail': fail_count,
        'fail_rate': round(float(fail_count) / class_size, 3),
        'score_segment': score_segment,
    }
    return report


def grade_base_report(handler, students_score, total_score):
    students_score.sort(key=lambda x: x['score'], reverse=True)
    rank_students(students_score, 'grand_rank', total_score)
    class_report = dict()
    score_segment = dict()
    max_segment = total_score / 10
    if total_score % 10 == 0:
        max_segment -= 1
    for segment in range(max_segment + 1):
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
        score = int(student['score'])
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
        report['perfect_rate'] = round(float(report['perfect']) / report['size'], 3)
        report['good_rate'] = round(float(report['good']) / report['size'], 3)
        report['pass_rate'] = round(float(report['pass']) / report['size'], 3)
        report['fail_rate'] = round(float(report['fail']) / report['size'], 3)
        report['average'] = round(float(report['total_score']) / report['size'], 1)

    return class_report


def base_items_analysis(students_score, items_score):
    items_analysis = [{'score': item_score,
                       'perfect': 0,
                       'max_score': 0,
                       'class_sum_score': 0} for item_score in items_score]
    class_size = len(students_score)
    for index_student, student in enumerate(students_score):
        for index, item_score in enumerate(student['items_score']):
            analysis = items_analysis[index]
            analysis['class_sum_score'] += item_score
            if item_score == analysis['score']:
                analysis['perfect'] += 1
            analysis['max_score'] = max(analysis['max_score'], item_score)

    for index, analysis in enumerate(items_analysis):
        analysis['average'] = round(float(analysis['class_sum_score']) / class_size, 1)
    return items_analysis


def rank_students(students_score, rank_type, total_score):
    last_score = total_score
    last_rank = 1
    for index, student in enumerate(students_score, 1):
        if int(student['score']) < last_score:
            last_rank = index
            last_score = int(student['score'])
        student[rank_type] = last_rank


def generate_report_v0(handler, students_score):
    total_score = students_score[0]['score']
    report = class_base_report(handler, students_score[1:], total_score)
    return report


def generate_report_v1(handler,  students_score):
    total_score = students_score[0]['score']
    report = grade_base_report(handler, students_score[1:], total_score)
    return report


def generate_report_v2(handler, students_score):
    total_score = students_score[0]['score']
    report = class_base_report(handler, students_score[1:], total_score)
    items_analysis = base_items_analysis(students_score[1:], students_score[:1]['items_score'])
    report['items_analysis'] = items_analysis
    return report


def generate_report_v3(handler, students_score):
    total_score = students_score[0]['score']
    items_score = students_score[0]['items_score']
    all_report = grade_base_report(handler, students_score[1:], total_score)
    class_students_score = {class_name: list() for class_name, _ in all_report.items()}
    for student_score in students_score[1:]:
        class_students_score[student_score['class_name']].append(student_score)
    for class_name, class_scores in class_students_score.items():
        all_report[class_name]['items_analysis'] = base_items_analysis(class_scores, items_score)
    all_report['grade'] = dict()
    grade_items_analysis = base_items_analysis(students_score[1:], items_score)
    all_report['grade']['items_analysis'] = grade_items_analysis
    return all_report
