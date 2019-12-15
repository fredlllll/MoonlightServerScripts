from pymongo import MongoClient
import logging

from Settings.Settings import MONGO_DB

logger = logging.getLogger(__name__)


class MongoUtil:
    instance = None

    @classmethod
    def get_client(cls):
        if cls.instance is None:
            cls.instance = MongoClient(MONGO_DB.host, MONGO_DB.port)
        return cls.instance

    @classmethod
    def get_database(cls, db=MONGO_DB.db_name):
        client = cls.get_client()
        return client[db]
