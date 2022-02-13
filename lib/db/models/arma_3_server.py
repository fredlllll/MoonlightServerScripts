from lib.db.models.model import Model
from lib.settings import Settings
from lib.apis.arma_3_server import create_service, create_startup_script
import shutil
import os


class Arma3Server(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'arma_3_servers'

    def _get_fields(self):
        return [
            'name',
            'port',
            'additional_commandline',
        ]

    def create_files(self):
        create_service(self.id)
        create_startup_script(self)
        shutil.copy("ArmaServerDefaultFiles/basic.cfg", os.path.join(Settings.arma_3_server_dir, self.id + "_basic.cfg"))
        shutil.copy("ArmaServerDefaultFiles/server.cfg", os.path.join(Settings.arma_3_server_dir, self.id + "_server.cfg"))
