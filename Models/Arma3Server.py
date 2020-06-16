from TornadoBaseFramework.Storage.Model import Model


class Arma3Server(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'arma_3_servers'

    def _get_fields(self):
        return [
            'name',
            'path',
        ]
