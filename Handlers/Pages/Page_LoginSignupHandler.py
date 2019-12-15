from Util import urlencode
from Handlers.BaseHandler import BaseHandler
from Models.User import User
from Models.Session import Session
from Utils.UserUtils import hash_password
from Handlers.Pages.Page_IndexHandler import Page_IndexHandler
import logging

logger = logging.getLogger(__name__)


class Page_LoginSignupHandler(BaseHandler):
    """
    renders the login page
    """
    url_pattern = r'/login_signup'
    url = '/login_signup'

    def get(self, *args, **kwargs):
        if self.get_argument("logout", None) is not None:
            self._post_logout()
            return
        if self.current_user is not None:
            self.redirect(Page_IndexHandler.url)
        else:
            self.render("page_login_signup.html")

    def _post_sign_up(self):
        user_name = self.get_argument("user")
        password = self.get_argument("password")
        password1 = self.get_argument("password1")
        if password != password1:
            self.redirect(self.url)  # dont create a user

        user = User(name=user_name, password=hash_password(password))
        user.save()
        self.redirect(self.url)  # to login

    def _post_login(self):

        user_name = self.get_argument("user")
        password = self.get_argument("password")
        user = User.authenticate_user(user_name, password)  # either false or user object
        if user:  # login worked
            session = Session(user_model_id=user.model_id)
            session.save()
            session.set_cookie(self)
        self.redirect('/')

    def _post_logout(self):
        if self.current_user is not None:
            session = Session.get_from_cookie(self)
            session.clear_cookie(self)
            session.delete()
        self.redirect("/")

    def post(self, *args, **kwargs):
        logged_out = self.current_user is None
        if self.get_argument("login", None) is not None and logged_out:
            self._post_login()
        elif self.get_argument("signup", None) is not None and logged_out:
            self._post_sign_up()
        elif self.get_argument("logout", None) is not None:
            self._post_logout()
        else:
            self.redirect("/")
