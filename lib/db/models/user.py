from lib.db.models.model import Model
from lib.util import verify_password


class User(Model):
    @classmethod
    def _get_collection_name(cls):
        return 'users'

    def _get_fields(self):
        return [
            'name',
            'password',
            'activation_timestamp',
            'permissions'
        ]

    def has_permission(self, permission):
        if self.permissions is None:
            return False
        return permission in self.permissions

    @classmethod
    async def user_has_permission(cls, user_id, permission):
        user = await cls.find(user_id)
        if user is None:
            return False
        return user.has_permission(permission)

    @classmethod
    async def is_user_name_taken(cls, name):
        record = await cls._load_one_record_by_query({'name': name})
        return record is not None

    @classmethod
    async def get_user_by_name(cls, name):
        record = await cls._load_one_record_by_query({'name': name})
        if record is None:
            return None
        return cls(**record)

    @classmethod
    async def authenticate_user(cls, name, password, force=False):
        """
        authenticate a user and delete all old sessions
        :param name: username
        :param password: password
        :param force: forced authentication, even if deactivated
        :return: false on failure and a session on success
        """
        user = await cls.get_user_by_name(name)
        if user is None:
            return False
        if user.activation_timestamp is not None or force:
            if verify_password(password, user.password):
                return user
        return False
