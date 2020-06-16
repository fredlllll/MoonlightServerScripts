from tornado.web import RequestHandler


class HttpsRedirectHandler(RequestHandler):
    def prepare(self):
        self.redirect("https://" + self.request.host + self.request.uri)
