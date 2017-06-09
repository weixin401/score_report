#!/usr/bin/env python
# fileencoding=utf-8
'''
所有预期内的Python StandardError都要转成合适的QPBaseError
否则会作为未处理的异常处理返回 HTTP 500 。
'''


class BaseError(Exception):
    '''
    基类，不要直接raise
    '''
    def __init__(self, msg_fmt_str, *args, **kwargs):
        self.message = msg_fmt_str % args
        self.fmt_str = msg_fmt_str
        self.args = args

        # error_id 用以分类错误，以在处理时提供简单依据
        self.error_id = kwargs.get('error_id', self.__class__.__name__)
        # 期望的http状态码, web server 使用
        self.http_status_code = kwargs.get('http_status_code', None)

    def __str__(self):
        return '{}: {}'.format(self.error_id, self.message)

    def __unicode(self):
        return u'{}: {}'.format(self.error_id, self.message)


class BLError(BaseError):
    '''
    由用户不合理的请求触发的异常
    '''
    def __init__(self, *args, **kwargs):
        super(BLError, self).__init__(*args, **kwargs)

        self.http_status_code = self.http_status_code or 200