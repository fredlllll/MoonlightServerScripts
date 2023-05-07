using MongoDB.Bson;
using MongoDB.Driver;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Db
{
    public class Mongo
    {
        static MongoClient? mongoClient = null;
        public static MongoClient MongoClient
        {
            get
            {
                if (mongoClient == null)
                {
                    MongoClientSettings mongoSettings = new ();
                    mongoSettings.Server = new MongoServerAddress(Settings.GetValue<string>("mongo_db_host"), Settings.GetValue<int>("mongo_db_port"));
                    var mongoDbUser = Settings.GetValue<string>("mongo_db_user");
                    var mongoDbPassword = Settings.GetValue<string>("mongo_db_user");
                    var mongoDbAuthSource = Settings.GetValue<string>("mongo_db_user");
                    if (mongoDbUser != null && mongoDbPassword != null && mongoDbAuthSource != null)
                    {
                        mongoSettings.Credential = MongoCredential.CreateCredential(mongoDbAuthSource, mongoDbUser, mongoDbPassword);
                    }
                    mongoClient = new MongoClient(mongoSettings);
                }
                return mongoClient;
            }
        }

        public static IMongoDatabase GetDatabase(string? name = null)
        {
            name ??= Settings.GetValue<string>("mongo_db_db_name");
            return MongoClient.GetDatabase(name);
        }

        public static IMongoCollection<BsonDocument> GetCollection(string name, string? databaseName = null)
        {
            var db = GetDatabase(databaseName);
            return db.GetCollection<BsonDocument>(name);
        }
    }
}
