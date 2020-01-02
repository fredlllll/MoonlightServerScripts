from JobSystem.Job import Job
from APIs.SteamAPI import delete_mods


class DeleteModsJob(Job):
    def __init__(self, mod_ids):
        super().__init__('Delete Mods', 'Mod Ids: ' + ', '.join(mod_ids))
        self.mod_ids = mod_ids

    def _run(self):
        delete_mods(self.mod_ids)
