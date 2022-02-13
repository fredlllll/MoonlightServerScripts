from lib.db.models.model import Model
from lib.settings import Settings


class Session(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'sessions'

    def _get_fields(self):
        return [
            'user_id',
        ]

    @classmethod
    def find_by_user(cls, user_id):
        record = cls._load_one_record_by_query({'user_id': user_id})
        if record is None:
            return None
        return cls(**record)

    def set_cookie(self, response):
        response.cookies[Settings.session_cookie_name] = self.id
        response.cookies[Settings.session_cookie_name]['max-age'] = 3600 * 24 * 365  # one year

    @classmethod
    def clear_cookie(cls, response):
        response.cookies[Settings.session_cookie_name] = 'invalid'
