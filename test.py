#!/usr/bin/env python
# encoding: utf-8

import tornado.web
import tornado.ioloop


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_secure_cookie('username', 'ansheng')
        self.set_secure_cookie('password', 'hello')
        self.render('test.html')

    def post(self, *args, **kwargs):
        username = self.get_argument('username', None)
        password = self.get_argument('password', None)
        cooike_user = self.get_secure_cookie('username')
        cooike_pass = self.get_secure_cookie('password')
        if username == cooike_user and password == cooike_pass:
            self.write('Hello ' + cooike_user)
        else:
            self.write(u'用户名或密码错误')


settings = {
    'template_path': 'template',
}

application = tornado.web.Application([
    (r'/', IndexHandler),
],  cookie_secret="508CE6152CB93994628D3E99934B83CC")

if __name__ == '__main__':
    print('http://127.0.0.1:8000')
    application.listen(8000)
    tornado.ioloop.IOLoop.instance().start()