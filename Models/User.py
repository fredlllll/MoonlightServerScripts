from Framework.Model import Model
from Utils.UserUtils import verify_password


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
    def user_has_permission(cls, user_model_id, permission):
        user = super(cls).find(user_model_id)
        if user is None:
            return False
        return user.has_permission(permission)

    @classmethod
    def is_user_name_taken(cls, name):
        record = cls._load_one_record_by_query({'name': {"$eq": name}})
        return record is not None

    @classmethod
    def get_user_by_name(cls, name):
        record = cls._load_one_record_by_query({'name': {"$eq": name}})
        if record is None:
            return None
        return cls(**record)

    @classmethod
    def get_user_by_email(cls, email):
        record = cls._load_one_record_by_query({'email': {"$eq": email}})
        if record is None:
            return None
        return cls(**record)

    @classmethod
    def authenticate_user(cls, name, password, force=False):
        """
        authenticate a user and delete all old sessions
        :param name: username
        :param password: password
        :param force: forced authentication, even if deactivated
        :return: false on failure and a session on success
        """
        record = cls._load_one_record_by_query({'name': {"$eq": name}})
        if record is None:
            return False
        user = cls(**record)
        if user.activation_timestamp is not None or force:
            if verify_password(password, user.password):
                return user
        return False
