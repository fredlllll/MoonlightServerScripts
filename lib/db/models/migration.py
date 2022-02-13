from lib.db.models.model import Model


class Migration(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'migrations'

    @classmethod
    def _get_fields(cls):
        return [
            'timestamp'
        ]
