#!/usr/bin/env python
# encoding: utf-8

import logging
import re
import string
from controller.error import BLError


_UNICODE_SPACE_PATTERN = re.compile(
    ur'[\x00-\x20\x7F-\xA0\u1680\u180E\u2000-\u200B\u2028\u2029\u202F'
    ur'\u205F\u3000\uFEFF]')
_USERNAME_PATTERN = re.compile(ur'^[\w\d\-_\u0100-\uffff]+$')
_USERNAME_PATTERN_1 = re.compile(ur'\d+$')
_VALID_PASSWORD_CHARS = set(string.letters + string.digits +
                            string.punctuation + ' ')


def check_name(name):
    if not 2 <= len(name) <= 32:
        raise BLError(u'真实姓名长度必须在[2, 32]之间！')
    if _UNICODE_SPACE_PATTERN.search(name):
        raise BLError(u'真实姓名不能含有空白字符！')
    if not _USERNAME_PATTERN.match(name):
        raise BLError(u'真实姓名不能含有英文标点符号或特殊字符！')


def check_password(password):
    if not 6 <= len(password) <= 32:
        raise BLError(u'密码长度必须在[6, 32]之间！')
    for c in password:
        if c not in _VALID_PASSWORD_CHARS:
            raise BLError(u'密码只能包含英文大小写字母、数字、标点符号'
                          u'和空格！')


def check_username_exist(db, username):
    if db.user.find_one({'username': username}):
        raise BLError(u'该用户名已存在！')


def find_user(handler, username, password):
    user = handler.db.user.find_one({'username': username})
    if user is None:
        raise BLError('没有该用户：{}'.format(username))
    elif user['password'] != password:
        raise BLError('密码不正确！')
    else:
        return user


def create_user(handler, username, password):
    check_name(username)
    check_password(password)
    check_username_exist(handler.db, username)
    id_ = handler.db.user.insert({'username': username, 'password': password})
    logging.info("created new user {}".format(username))
    return id_
