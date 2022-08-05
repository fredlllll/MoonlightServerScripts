from lib.db.models.model_deletion_logic import MongoModelDeletionLogic
from lib.arma_3_server_util import get_server_config_file_name, get_basic_config_file_name, get_service_file_name, get_startup_script_file_name, get_server_profile_file_name
from lib.settings import Settings
import os
import subprocess
import logging

logger = logging.getLogger(__name__)


class Arma3Server(MongoModelDeletionLogic):
    @classmethod
    def _get_collection_name(cls):
        return 'arma_3_servers'

    def _get_fields(self):
        return [
            'name',
            'port',
            'modset_id',
            'additional_commandline',
        ]

    @classmethod
    def _delete_from_record(cls, record):
        server_id = record['id']

        if Settings.debug_windows:
            logger.info("windows delete server dummy")
            return

        # remove service
        service_file_name = get_service_file_name(server_id)
        subprocess.check_call(f"sudo systemctl stop {os.path.basename(service_file_name)}")
        subprocess.check_call(f"sudo systemctl disable {os.path.basename(service_file_name)}")
        os.unlink(service_file_name)
        subprocess.check_call("sudo systemctl daemon-reload")

        # delete files
        os.unlink(get_startup_script_file_name(server_id))
        os.unlink(get_basic_config_file_name(server_id))
        os.unlink(get_server_config_file_name(server_id))
        os.unlink(get_server_profile_file_name(server_id))
