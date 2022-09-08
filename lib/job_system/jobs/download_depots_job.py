from lib.job_system.job import Job
from lib.apis.steam import download_depots
from typing import List, Tuple


class DownloadDepotsJob(Job):
    def __init__(self, depot_manifest_pairs: List[Tuple[str, str]], user: str, password: str, auth_code: str):
        super().__init__('Download Depots', 'Depot Manifest Pairs: ' + ', '.join([str(i) for i in depot_manifest_pairs]))
        self.user: str = user
        self.password: str = password
        self.auth_code: str = auth_code
        self.depot_manifest_pairs: List[Tuple[str, str]] = depot_manifest_pairs

    def _run(self):
        download_depots(self.depot_manifest_pairs, self.user, self.password, self.auth_code)
