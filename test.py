# -*- coding: utf-8 -*-

from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from session import SessionHandler
from redis import client
from tornado import escape

import tornado.web


class BaseHandler(RequestHandler):
    def initialize(self):
        redis = self.application.redis
        self.session = self.application.SessionHandler(self, redis, session_lifetime=20)
        self.current_password = self.session.password

    def get_current_user(self):
        return self.get_secure_cookie("username")


class MainHandler(BaseHandler):
    def get(self):
        if not self.current_user or not self.current_password:
            self.redirect("/login")
            return
        name = escape.xhtml_escape(self.current_user)
        self.write("Home Page | Logined | %s" % name)


class LoginHandler(BaseHandler):
    def get(self):
        if self.current_user and not self.current_password:
            html = """\
                <html>
                    <body>
                        <p>
                        session超时了,要重新输入密码!
                        </p>
                        <form action="/login" method="post">
                            Password:<input type="password" name="password">
                            <input type="submit" value="sign in">
                        </form>
                    </body>
                </html>
                """
        else:
            html = """\
                <html>
                    <body>
                        <p>
                        未登录,或者cookie超时了,要重新输入用户名和密码!
                        </p>
                        <form action="/login" method="post">
                            Username:<input type="text" name="username">
                            Password:<input type="password" name="password">
                            <input type="submit" value="sign in">
                        </form>
                    </body>
                </html>
                """
        self.write(html)

    def post(self):
        username = self.get_secure_cookie("username") or self.get_argument("username")
        password = self.get_argument("password")
        if not self.current_password:
            if username == "abc" and password == "123":
                self.set_secure_cookie("username", username)
                self.session.password = password
                self.redirect("/")
            else:
                raise tornado.web.HTTPError(403, "user or password error")
        else:
            self.redirect("/")


urls = [
    (r"/", MainHandler),
    (r"/login", LoginHandler),

]

settings = {
    "cookie_secret": "61oETzKXQAGaYdkL5gEmGeJJFuYh7EQnp2XdTP1o/Vo=",  # 带签名的cookie
    "login_url": "/login",
    # "xsrf_cookies":"Ture", # 跨站伪造请求(Cross-site request forgery) 防范策略 xsrf_cookies

}

app = Application(urls, **settings)
app.listen(8000)
app.redis = client.Redis()
app.SessionHandler = SessionHandler

IOLoop.instance().start()