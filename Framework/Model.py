from abc import ABC, abstractmethod
from MongoUtil import MongoUtil
from Util import generate_random_string
import time
import pymongo

CREATED_TIMESTAMP_FIELD = 'created_timestamp'
UPDATED_TIMESTAMP_FIELD = 'updated_timestamp'


class Model(ABC):
    def __init__(self, **kwargs):
        self._load_from_record(kwargs)

    @classmethod
    @abstractmethod
    def _get_fields(cls):
        pass

    @classmethod
    @abstractmethod
    def _get_collection_name(cls):
        pass

    @classmethod
    def _get_special_fields(cls):
        # fields that will be present on every model
        return [
            cls._get_key(),
            CREATED_TIMESTAMP_FIELD,
            UPDATED_TIMESTAMP_FIELD
        ]

    @classmethod
    def _get_key(cls):
        # key to be used as id key
        return 'model_id'

    @classmethod
    def _get_collection(cls):
        db = MongoUtil.get_database()
        return db[cls._get_collection_name()]

    @classmethod
    def _load_one_record_by_query(cls, query):
        coll = cls._get_collection()
        record = coll.find_one(query)
        return record

    @classmethod
    def _load_many_records_by_query(cls, query, skip=None, limit=None, sort=None, sort_dir=pymongo.ASCENDING):
        coll = cls._get_collection()
        records = coll.find(query)
        if skip is not None:
            records = records.skip(skip)
        if limit is not None:
            records = records.limit(limit)
        if sort is not None:
            records = records.sort(sort, sort_dir)
        return records

    @classmethod
    def _delete_one_by_query(cls, query):
        coll = cls._get_collection()
        coll.delete_one(query)

    @classmethod
    def find(cls, key):
        record = cls._load_one_record_by_query({cls._get_key(): {"$eq": key}})
        if record is None:
            return None
        return cls(**record)

    @classmethod
    def all(cls):
        records = cls._load_many_records_by_query({})
        models = []
        for record in records:
            models.append(cls(**record))
        return models

    @classmethod
    def modify_numeric_field(cls, key, field, change):
        coll = cls._get_collection()
        coll.update({cls._get_key(): {'$eq': key}}, {"$inc": {field: change}}, upsert=True)

    def _load_from_record(self, record):
        for f in self._get_fields():
            self.__dict__[f] = record.get(f, None)
        for sf in self._get_special_fields():
            self.__dict__[sf] = record.get(sf, None)

    def reload(self):
        record = self._load_one_record_by_query({self._get_key(): {"$eq": self.__dict__[self._get_key()]}})
        self._load_from_record(record)

    def save(self):
        if self.__dict__[self._get_key()] is None:
            self.__dict__[self._get_key()] = generate_random_string(32)
        if self.__dict__[CREATED_TIMESTAMP_FIELD] is None:
            self.__dict__[CREATED_TIMESTAMP_FIELD] = time.time()
        self.__dict__[UPDATED_TIMESTAMP_FIELD] = time.time()  # set updated time

        record = {}
        for sf in self._get_special_fields():
            record[sf] = self.__dict__.get(sf, None)
        for f in self._get_fields():
            record[f] = self.__dict__.get(f, None)
        _filter = {
            self._get_key(): record[self._get_key()]
        }
        coll = self._get_collection()
        coll.update_one(_filter, {"$set": record}, upsert=True)

    def delete(self):
        self._delete_one_by_query({self._get_key(): {"$eq": self.__dict__[self._get_key()]}})
