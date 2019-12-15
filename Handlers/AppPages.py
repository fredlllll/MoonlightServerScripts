from Handlers.API.AppAPIHandler import AppAPIHandler

from Handlers.Pages.Page_IndexHandler import Page_IndexHandler
from Handlers.Pages.Page_ModDownloaderHandler import Page_ModDownloaderHandler
from Handlers.Pages.Page_JobsHandler import Page_JobsHandler
from Handlers.Pages.Page_ModLinkerHandler import Page_ModLinkerHandler
from Handlers.Pages.Page_StartupScriptMakerHandler import Page_StartupScriptMakerHandler
from Handlers.Pages.Page_LoginSignupHandler import Page_LoginSignupHandler
from Handlers.Pages.Page_403Handler import Page_403
from Handlers.Pages.Page_404Handler import Page_404

pages = [
    AppAPIHandler,
    Page_IndexHandler,
    Page_ModDownloaderHandler,
    Page_JobsHandler,
    Page_ModLinkerHandler,
    Page_StartupScriptMakerHandler,
    Page_LoginSignupHandler,
    Page_403,
    Page_404
]
