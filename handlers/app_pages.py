from handlers.api.AppAPIHandler import AppAPIHandler

from handlers.pages.Index import IndexHandler
from handlers.pages.ModDownloader import ModDownloaderHandler
from handlers.pages.Jobs import JobsHandler
from handlers.pages.ModLinker import ModLinkerHandler
from handlers.pages.StartupScriptMaker import StartupScriptMakerHandler
from handlers.pages.LoginSignup import LoginSignupHandler
from handlers.pages.Page403 import Page403
from handlers.pages.Page404 import Page404

pages = [
    AppAPIHandler,
    IndexHandler,
    ModDownloaderHandler,
    JobsHandler,
    ModLinkerHandler,
    StartupScriptMakerHandler,
    LoginSignupHandler,
    Page403,
    Page404
]
