import tornado.escape
from tornado.web import RequestHandler
from ..Util import generate_random_string, urlencode
from ..Settings import Settings
import logging

logger = logging.getLogger(__name__)


def get_template_403():
    retval = "403.html"
    try:
        retval = Settings.TEMPLATE_NAME_403
    except:
        pass
    return retval


def get_template_404():
    retval = "404.html"
    try:
        retval = Settings.TEMPLATE_NAME_404
    except:
        pass
    return retval


class BaseHandler(RequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

    def do_403(self, message=None):
        self.render(get_template_403(), message=message)

    def do_404(self, message=None):
        self.render(get_template_404(), message=message)

    def get_current_user(self):
        return None

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
