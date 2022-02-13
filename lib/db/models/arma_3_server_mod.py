from lib.db.models.model import Model


class Arma3ServerMod(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'arma_3_server_mods'

    def _get_fields(self):
        return [
            'server_id',
            'mod_id',
        ]
