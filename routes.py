#!/usr/bin/env python
# encoding: utf-8


def get():

    routes = [
        (r'/?', 'controller.homepage.HomePageHandler'),
        (r'/login', 'login.AuthLoginHandler'),
        (r'/logout', 'login.AuthLogoutHandler'),
        (r'/signup', 'login.AuthSignupHandler'),
        (r'/tool', 'controller.homepage.ToolHandler'),
        (r'/upload0', 'controller.center.FileUploadHandler', {'excel_type': 0}),
        (r'/upload1', 'controller.center.FileUploadHandler', {'excel_type': 1}),
        (r'/upload2', 'controller.center.FileUploadHandler', {'excel_type': 2}),
        (r'/upload3', 'controller.center.FileUploadHandler', {'excel_type': 3}),
        (r'/upload4', 'controller.center.FileUploadHandler', {'excel_type': 4}),
        (r'/score_report_v0', 'controller.center.ScoreReportHandler', {'report_type': 0}),
        (r'/score_report_v1', 'controller.center.ScoreReportHandler', {'report_type': 1}),
        (r'/score_report_v2', 'controller.center.ScoreReportHandler', {'report_type': 2}),
        (r'/score_report_v3', 'controller.center.ScoreReportHandler', {'report_type': 3}),
        (r'/score_report_v4', 'controller.center.ScoreReportHandler', {'report_type': 4})
    ]

    return routes
