from TornadoBaseFramework.Storage.Model import Model
from TornadoBaseFramework.Settings import Settings


class Session(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'sessions'

    def _get_fields(self):
        return [
            'user_model_id'
        ]

    @classmethod
    def find_by_user(cls, user_model_id):
        record = cls._load_one_record_by_query({'user_model_id': {"$eq": user_model_id}})
        if record is None:
            return None
        return cls(**record)

    def set_cookie(self, handler):
        handler.set_secure_cookie(Settings.SESSION_COOKIE_NAME, self.model_id.encode())

    def clear_cookie(self, handler):
        handler.clear_cookie(Settings.SESSION_COOKIE_NAME)

    @classmethod
    def get_from_cookie(cls, handler):
        session_id_bytes = handler.get_secure_cookie(Settings.SESSION_COOKIE_NAME)
        if session_id_bytes is not None:
            session_id = session_id_bytes.decode()
            session = Session.find(session_id)
            return session
        return None
