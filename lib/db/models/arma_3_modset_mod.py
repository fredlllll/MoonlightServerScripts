from lib.db.models.model import Model


class Arma3ModsetMod(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'arma_3_modset_mods'

    def _get_fields(self):
        return [
            'modset_id',
            'mod_steam_id',
        ]
