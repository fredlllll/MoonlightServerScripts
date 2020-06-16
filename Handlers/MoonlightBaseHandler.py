import tornado.escape
from tornado.web import RequestHandler
from TornadoBaseFramework.Util import generate_random_string,urlencode
from Models.Session import Session
from Models.User import User
from TornadoBaseFramework.Settings import Settings
import logging

logger = logging.getLogger(__name__)


class MoonlightBaseHandler(RequestHandler):
    def __init__(self, application, request, **kwargs):
        super().__init__(application, request, **kwargs)
        self.user = None

    def _link_to_css(self, link):
        return '<link href="/static/css/' + tornado.escape.xhtml_escape(link) + '" type="text/css" rel="stylesheet"/>'

    def _link_to_js(self, link):
        return '<script src="/static/js/' + tornado.escape.xhtml_escape(link) + '"></script>'

    def _get_lang(self):
        code = self.locale.code
        i = code.index('_')
        code = code[:i]
        return code

    def _has_permission(self, permission):
        return self.current_user is not None and self.current_user.has_permission(permission)

    def redirect_403(self):
        self.redirect("/403")

    def redirect_404(self):
        self.redirect("/404")

    def get_current_user(self):
        if self.user is None:
            session = Session.get_from_cookie(self)
            if session is not None:
                session.save()
                self.user = User.find(session.user_model_id)
        return self.user

    def render(self, template_name, **kwargs):
        kwargs["link_to_css"] = self._link_to_css
        kwargs["link_to_js"] = self._link_to_js
        kwargs["get_lang"] = self._get_lang
        is_authenticated = self.current_user is not None
        kwargs["is_authenticated"] = is_authenticated
        kwargs["generate_random_string"] = generate_random_string
        kwargs["application_name"] = Settings.APPLICATION_NAME

        if is_authenticated:
            kwargs["user"] = self.current_user
            kwargs["has_permission"] = self._has_permission

        super().render(template_name, **kwargs)
