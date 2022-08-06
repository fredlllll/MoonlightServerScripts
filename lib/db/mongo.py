from lib.settings import Settings
from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database
from typing import Optional

instance: Optional[MongoClient] = None


def get_client() -> MongoClient:
    global instance
    if instance is None:
        kwargs = {}
        if Settings.mongo_db_user and Settings.mongo_db_password and Settings.mongo_db_auth_db:
            kwargs['username'] = Settings.mongo_db_user
            kwargs['password'] = Settings.mongo_db_password
            kwargs['authSource'] = Settings.mongo_db_auth_db
        instance = MongoClient(Settings.mongo_db_host, Settings.mongo_db_port, **kwargs)
    return instance


def get_database(db=Settings.mongo_db_db_name) -> Database:
    client = get_client()
    return client[db]


def get_collection(name, db=Settings.mongo_db_db_name) -> Collection:
    client = get_client()
    return client[db][name]
