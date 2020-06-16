from Handlers.API.AppAPIHandler import AppAPIHandler

from Handlers.Pages.Index import IndexHandler
from Handlers.Pages.ModDownloader import ModDownloaderHandler
from Handlers.Pages.Jobs import JobsHandler
from Handlers.Pages.ModLinker import ModLinkerHandler
from Handlers.Pages.StartupScriptMaker import StartupScriptMakerHandler
from Handlers.Pages.LoginSignup import LoginSignupHandler
from Handlers.Pages.Page403 import Page403
from Handlers.Pages.Page404 import Page404

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
