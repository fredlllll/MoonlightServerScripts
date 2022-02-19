from lib.settings import Settings
from pymongo import MongoClient

instance: MongoClient = None


def get_client():
    global instance
    if instance is None:
        kwargs = {}
        if Settings.mongo_db_user and Settings.mongo_db_password and Settings.mongo_db_auth_db:
            kwargs['username'] = Settings.mongo_db_user
            kwargs['password'] = Settings.mongo_db_password
            kwargs['authSource'] = Settings.mongo_db_auth_db
        instance = MongoClient(Settings.mongo_db_host, Settings.mongo_db_port, **kwargs)
    return instance


def get_database(db=Settings.mongo_db_db_name):
    client = get_client()
    return client[db]


def get_collection(name, db=Settings.mongo_db_db_name):
    client = get_client()
    return client[db][name]
