from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def prepare(self):
        self.template = self.settings['template']

