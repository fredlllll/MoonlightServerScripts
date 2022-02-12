from handlers.MoonlightBaseHandler import MoonlightBaseHandler
from models.User import User
from models.Session import Session
from utils.UserUtils import hash_password
from .Index import IndexHandler
import logging
import time

logger = logging.getLogger(__name__)


class LoginSignupHandler(MoonlightBaseHandler):
    """
    renders the login page
    """
    url = '/login_signup'

    def _render(self,**kwargs):
        self.render("page_login_signup.html",**kwargs)

    def get(self, *args, **kwargs):
        if self.get_argument("logout", None) is not None:
            self.do_logout()
            return
        if self.current_user is not None:
            self.redirect(IndexHandler.url)
        else:
            self._render()

    def do_sign_up(self):
        user_name = self.get_argument("user")
        password = self.get_argument("password")
        password1 = self.get_argument("password1")
        if password != password1:
            self.redirect(self.url)  # dont create a user

        if len(User.all()) == 0: # automatically activate the first user who registers
            auto_activate = True
        else:
            auto_activate = False
        user = User(name=user_name, password=hash_password(password))
        if auto_activate:
            user.activation_timestamp = time.time()
        user.save()
        self.redirect(self.url)  # to login

    def do_login(self):
        user_name = self.get_argument("user")
        password = self.get_argument("password")
        user = User.authenticate_user(user_name, password)  # either false or user object
        if user:  # login worked
            session = Session(user_model_id=user.model_id)
            session.save()
            session.set_cookie(self)
        self.redirect('/')

    def do_logout(self):
        if self.current_user is not None:
            session = Session.get_from_cookie(self)
            session.clear_cookie(self)
            session.delete()

    def post(self, *args, **kwargs):
        logged_out = self.current_user is None
        if self.get_argument("login", None) is not None and logged_out:
            self.do_login()
        elif self.get_argument("signup", None) is not None and logged_out:
            self.do_sign_up()
        elif self.get_argument("logout", None) is not None:
            self.do_logout()
            self.redirect("/")
        else:
            self.redirect("/")
