#!/usr/bin/env python
# encoding: utf-8


def get():

    routes = [
        (r'/?', 'controller.homepage.HomePageHandler'),
        (r'/tes', 'controller.statistic.TestHandler'),

    ]

    return routes
