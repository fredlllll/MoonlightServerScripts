from abc import ABC

from lib.db.models.model import Model


class MongoModelDeletionLogic(Model, ABC):
    @classmethod
    async def _delete_from_record(cls, record):
        pass

    @classmethod
    async def _delete_one_by_query(cls, query):
        coll = cls._get_collection()

        record = await coll.find_one(query)
        if record is None:
            return None

        await cls._delete_from_record(record)

        return await coll.delete_one({'_id': record['_id']})

    @classmethod
    async def _delete_many_by_query(cls, query):
        coll = cls._get_collection()

        records = coll.find(query)

        ids = []
        async for r in records:
            ids.append(r['_id'])

            await cls._delete_from_record(r)

        await coll.delete_many({'_id': {'$in': ids}})
