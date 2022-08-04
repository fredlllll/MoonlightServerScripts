from lib.db.models.model import Model


class Arma3Modset(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'arma_3_modsets'

    def _get_fields(self):
        return [
            'name',
        ]
