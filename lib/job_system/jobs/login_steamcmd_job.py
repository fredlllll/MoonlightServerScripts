from lib.job_system.job import Job
from lib.apis.steamcmd import SteamCmd


class LoginSteamCmdJob(Job):
    def __init__(self, user: str, password: str, auth_code: str):
        super().__init__('Logging in SteamCLI', '')
        self.user = user
        self.password = password
        self.auth_code = auth_code

    def _run(self):
        steamcmd = SteamCmd()
        steamcmd.login(self.user, self.password, self.auth_code)
        steamcmd.wait()
