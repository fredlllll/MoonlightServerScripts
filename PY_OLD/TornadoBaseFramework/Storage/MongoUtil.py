from pymongo import MongoClient
import logging

from ..Settings import Settings

logger = logging.getLogger(__name__)


class MongoUtil:
    instance = None

    @classmethod
    def get_client(cls):
        if cls.instance is None:
            cls.instance = MongoClient(Settings.MONGO_DB_HOST, Settings.MONGO_DB_PORT)
        return cls.instance

    @classmethod
    def get_database(cls, db=Settings.MONGO_DB_DB_NAME):
        client = cls.get_client()
        return client[db]
