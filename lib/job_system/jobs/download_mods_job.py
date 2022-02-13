from lib.job_system.job import Job
from lib.apis.steam import download_mods


class DownloadModsJob(Job):
    def __init__(self, mod_ids, user, password, auth_code):
        super().__init__('Download Mods', 'Mod Ids: ' + ', '.join(mod_ids))
        self.user = user
        self.password = password
        self.auth_code = auth_code
        self.mod_ids = mod_ids

    def _run(self):
        download_mods(self.mod_ids, self.user, self.password, self.auth_code)
