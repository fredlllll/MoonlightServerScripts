from lib.job_system.job import Job
from lib.apis.steam import download_mods
from typing import List


class DownloadModsJob(Job):
    def __init__(self, mod_ids: List[str]):
        super().__init__('Download Mods', 'Mod Ids: ' + ', '.join(mod_ids))
        self.mod_ids: List[str] = mod_ids

    def _run(self):
        download_mods(self.mod_ids)
