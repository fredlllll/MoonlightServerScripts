from lib.db.models.model_deletion_logic import MongoModelDeletionLogic
from lib.db.models.arma_3_server import Arma3Server


class Arma3Modset(MongoModelDeletionLogic):
    @classmethod
    def _get_collection_name(cls):
        return 'arma_3_modsets'

    def _get_fields(self):
        return [
            'name',
        ]

    @classmethod
    def _delete_from_record(cls, record):
        servers = Arma3Server.where({'modset_id': record['id']})
        for server in servers:
            server.modset_id = None
            server.save()
