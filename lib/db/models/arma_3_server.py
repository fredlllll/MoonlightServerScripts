from lib.db.models.model_deletion_logic import MongoModelDeletionLogic
from lib.settings import Settings
import os
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
