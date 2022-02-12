from TornadoBaseFramework.Storage.Model import Model
from TornadoBaseFramework.Settings import Settings
from apis.Arma3ServerAPI import create_service, create_startup_script
import shutil
import os


class Arma3Server(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'arma_3_servers'

    def _get_fields(self):
        return [
            'name',
            'path',
            'additional_commandline',
        ]

    def create_files(self):
        create_service(self.model_id)
        create_startup_script(self.model_id, "", [])
        shutil.copy("ArmaServerDefaultFiles/basic.cfg", os.path.join(Settings.ARMA3SERVERDIR, self.model_id + "_basic.cfg"))
        shutil.copy("ArmaServerDefaultFiles/server.cfg", os.path.join(Settings.ARMA3SERVERDIR, self.model_id + "_server.cfg"))
