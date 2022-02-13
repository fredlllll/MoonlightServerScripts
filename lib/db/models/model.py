from abc import ABC, abstractmethod
from lib.db.mongo import get_collection
from lib.util import get_resource_id
import pymongo
import time

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
    def _get_type_id(cls):
        return cls._get_collection_name()[:-1]

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
        return 'id'

    @classmethod
    def _get_collection(cls):
        return get_collection(cls._get_collection_name())

    @classmethod
    async def _load_one_record_by_query(cls, query):
        coll = cls._get_collection()
        record = await coll.find_one(query)
        return record

    @classmethod
    def _load_many_records_by_query(cls, query, skip=None, limit=None, sort=None, sort_dir=pymongo.ASCENDING):
        coll = cls._get_collection()
        cursor = coll.find(query)
        if sort is not None:
            cursor = cursor.sort(sort, sort_dir)
        if skip is not None:
            cursor = cursor.skip(skip)
        if limit is not None:
            cursor = cursor.limit(limit)
        return cursor

    @classmethod
    async def _delete_one_by_query(cls, query):
        coll = cls._get_collection()
        await coll.delete_one(query)

    @classmethod
    async def _delete_many_by_query(cls, query):
        coll = cls._get_collection()
        await coll.delete_many(query)

    @classmethod
    async def delete_by_key(cls, key):
        if key is None:
            return
        return await cls._delete_one_by_query({cls._get_key(): {"$eq": key}})

    @classmethod
    async def find(cls, key):
        if key is None:
            return None
        record = await cls._load_one_record_by_query({cls._get_key(): {"$eq": key}})
        if record is None:
            return None
        return cls(**record)

    @classmethod
    async def all(cls):
        return await cls.where({})

    @classmethod
    async def where(cls, query, skip=None, limit=None, sort=None, sort_dir=pymongo.ASCENDING):
        models = []
        async for record in cls._load_many_records_by_query(query, skip, limit, sort, sort_dir):
            models.append(cls(**record))
        return models

    @classmethod
    async def delete_where(cls, query):
        await cls._delete_many_by_query(query)

    @classmethod
    async def modify_numeric_field(cls, key, field, change):
        coll = cls._get_collection()
        # cause mongodb is a bit stoopid i have to do some extra magic here
        await coll.update_one({cls._get_key(): {'$eq': key}}, [{'$set': {
            field: {
                "$add": [
                    {"$ifNull": ['$' + field, 0]},
                    change
                ]
            }
        }}])

    @classmethod
    async def create_index(cls, keys, unique=True, **kwargs):
        """
        create_index([("mike", pymongo.DESCENDING),...,("eliot", pymongo.ASCENDING)])
        :param keys:
        :param unique: if the index forces the value to be unique
        :return:
        """
        kwargs['unique'] = unique
        coll = cls._get_collection()
        coll.create_index(keys, **kwargs)

    def _load_from_record(self, record):
        for f in self._get_fields():
            self.__dict__[f] = record.get(f, None)
        for sf in self._get_special_fields():
            self.__dict__[sf] = record.get(sf, None)

    def update_from_record(self, record):
        if record is None:
            return
        for f in self._get_fields():
            if f in record:
                self.__dict__[f] = record.get(f)

    async def reload(self):
        record = await self._load_one_record_by_query({self._get_key(): {"$eq": self.__dict__[self._get_key()]}})
        self._load_from_record(record)

    async def save(self, only_if_not_exists=False, not_exists_fields=None):
        if self.__dict__[self._get_key()] is None:
            self.__dict__[self._get_key()] = get_resource_id(self._get_type_id())
        if self.__dict__[CREATED_TIMESTAMP_FIELD] is None:
            self.__dict__[CREATED_TIMESTAMP_FIELD] = time.time()
        self.__dict__[UPDATED_TIMESTAMP_FIELD] = time.time()  # set updated time

        record = self.to_record()
        _filter = {}

        coll = self._get_collection()
        if only_if_not_exists:
            if not_exists_fields is None:
                not_exists_fields = [self._get_key()]

            for f in not_exists_fields:
                _filter[f] = record[f]

            result = await coll.update_one(_filter, {"$setOnInsert": record}, upsert=True)
            return result.upserted_id is not None
        else:
            _filter[self._get_key()] = record[self._get_key()]
            await coll.update_one(_filter, {"$set": record}, upsert=True)
        return True

    def to_record(self, special_fields=True, normal_fields=True):
        record = {}
        if special_fields:
            for sf in self._get_special_fields():
                record[sf] = self.__dict__.get(sf, None)
        if normal_fields:
            for f in self._get_fields():
                record[f] = self.__dict__.get(f, None)
        return record

    async def delete(self):
        await self._delete_one_by_query({self._get_key(): {"$eq": self.__dict__[self._get_key()]}})