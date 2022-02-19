from abc import ABC

from lib.db.models.model import Model


class MongoModelDeletionLogic(Model, ABC):
    @classmethod
    def _delete_from_record(cls, record):
        pass

    @classmethod
    def _delete_one_by_query(cls, query):
        coll = cls._get_collection()

        record = coll.find_one(query)
        if record is None:
            return None

        cls._delete_from_record(record)

        return coll.delete_one({'_id': record['_id']})

    @classmethod
    def _delete_many_by_query(cls, query):
        coll = cls._get_collection()

        records = coll.find(query)

        ids = []
        for r in records:
            ids.append(r['_id'])

            cls._delete_from_record(r)

        coll.delete_many({'_id': {'$in': ids}})
