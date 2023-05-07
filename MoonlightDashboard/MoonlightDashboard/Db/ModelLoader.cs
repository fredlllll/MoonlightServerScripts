using Microsoft.AspNetCore.DataProtection.KeyManagement;
using MongoDB.Bson;
using MongoDB.Driver;
using MoonlightDashboard.Db.Models;
using MoonlightDashboard.Lib;
using System.ComponentModel;
using System.Reflection;

namespace MoonlightDashboard.Db
{
    public static class ModelLoader<T> where T : Model, new()
    {
        public const string KEY_FIELD = "id";
        public const string CREATED_TIMESTAMP_FIELD = "created_timestamp";
        public const string UPDATED_TIMESTAMP_FIELD = "updated_timestamp";

        /// <summary>
        /// Workaround because i cant do T.Method() in static method cause c# is retarded apparently. even autocomplete finds the method, why cant this be in c#???
        /// </summary>
        /// <typeparam name="U"></typeparam>
        /// <param name="name"></param>
        /// <param name="args"></param>
        /// <returns></returns>
        /// <exception cref="Exception"></exception>
        private static U CallStaticOnT<U>(string name, params object[] args)
        {
            var methodInfo = typeof(T).GetMethod(name, BindingFlags.Static | BindingFlags.NonPublic | BindingFlags.Public);
            if (methodInfo == null)
            {
                throw new Exception($"Method {name} doesnt exist");
            }
            return (U)methodInfo.Invoke(null, args);
        }

        public static IMongoCollection<BsonDocument> GetCollection()
        {
            return Mongo.GetCollection(CallStaticOnT<string>("GetCollectionName"));
        }

        public static BsonDocument? LoadOneRecordByQuery(FilterDefinition<BsonDocument> query)
        {
            var coll = GetCollection();
            return coll.Find(query).FirstOrDefault();
        }

        public static IEnumerable<BsonDocument> LoadManyRecordsByQuery(FilterDefinition<BsonDocument> query)
        {
            var coll = GetCollection();
            var result = coll.Find(query);
            return result.ToEnumerable();
        }

        public static DeleteResult DeleteOneByQuery(FilterDefinition<BsonDocument> query)
        {
            var coll = GetCollection();
            return coll.DeleteOne(query);
        }

        public static DeleteResult DeleteManyByQuery(FilterDefinition<BsonDocument> query)
        {
            var coll = GetCollection();
            return coll.DeleteMany(query);
        }

        public static DeleteResult? DeleteByKey(string? key)
        {
            if (key == null)
            {
                return null;
            }
            return DeleteOneByQuery(Builders<BsonDocument>.Filter.Eq(KEY_FIELD, key));
        }

        public static void LoadFromRecord(T instance, BsonDocument record, bool assignDefaults = true)
        {
            var properties = typeof(T).GetProperties(BindingFlags.Instance | BindingFlags.Public);
            foreach (var property in properties)
            {
                var recordFieldName = property.Name.PascalCaseToSnakeCase();
                var bsonValue = record[recordFieldName];
                if (bsonValue != null && bsonValue.BsonType != BsonType.Undefined)
                {
                    property.SetValue(instance, BsonTypeMapper.MapToDotNetValue(bsonValue));
                }
                else if (assignDefaults)
                {
                    property.SetValue(instance, ReflectionUtil.GetDefault(property.PropertyType));
                }
            }
        }

        public static BsonDocument ToRecord(T instance)
        {
            BsonDocument result = new BsonDocument();
            var properties = typeof(T).GetProperties(BindingFlags.Instance | BindingFlags.Public);
            foreach (var property in properties)
            {
                result[property.Name] = BsonTypeMapper.MapToBsonValue(property.GetValue(instance));
            }
            return result;
        }

        public static T? Find(string key)
        {
            if (key == null)
            {
                return null;
            }
            var record = LoadOneRecordByQuery(Builders<BsonDocument>.Filter.Eq(KEY_FIELD, key));
            if (record == null)
            {
                return null;
            }
            var result = new T();
            LoadFromRecord(result, record);
            return result;
        }

        public static void Reload(T instance)
        {
            var record = LoadOneRecordByQuery(Builders<BsonDocument>.Filter.Eq(KEY_FIELD, instance.Id));
            if (record == null)
            {
                throw new Exception("could not locate record to update from");
            }
            LoadFromRecord(instance, record);
        }

        public static void Save(T instance, bool OnlyIfNotExists = false, string[]? NotExistsFields = null)
        {
            instance.Id ??= DbUtil.GetResourceId(CallStaticOnT<string>("GetTypeId"));
            var now = new DateTimeOffset(DateTime.UtcNow).ToUnixTimeSeconds();
            instance.CreatedTimestamp ??= now;
            instance.UpdatedTimestamp = now;

            var record = ToRecord(instance);

            var coll = GetCollection();
            if (OnlyIfNotExists)
            {
                if (NotExistsFields == null)
                {
                    NotExistsFields = new string[] { KEY_FIELD };
                }

                foreach(var f in NotExistsFields)
                {

                }
            }
        }
    }
}
