#!/usr/bin/env python
# encoding: utf-8


def get():

    routes = [
        (r'/?', 'controller.homepage.HomePageHandler'),
        (r'/tes', 'controller.statistic.TestHandler'),
        (r'/upload', 'controller.center.FileUploadHandler', {'excel_type': 0}),
        (r'/score_report_v1', 'controller.center.ScoreReportHandler', {'report_type': 0})
    ]

    return routes
