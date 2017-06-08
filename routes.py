#!/usr/bin/env python
# encoding: utf-8


def get():

    routes = [
        (r'/?', 'controller.homepage.HomePageHandler'),
        (r'/tes', 'controller.statistic.TestHandler'),
        (r'/login', 'controller.login.AuthLoginHandler'),
        (r'/signup', 'controller.login.AuthSignupHandler'),
        (r'/upload0', 'controller.center.FileUploadHandler', {'excel_type': 0}),
        (r'/upload1', 'controller.center.FileUploadHandler', {'excel_type': 1}),
        (r'/score_report_v0', 'controller.center.ScoreReportHandler', {'report_type': 0}),
        (r'/score_report_v1', 'controller.center.ScoreReportHandler', {'report_type': 1})
    ]

    return routes
