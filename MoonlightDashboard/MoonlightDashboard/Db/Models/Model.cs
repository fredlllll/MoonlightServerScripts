using MongoDB.Bson;
using MongoDB.Driver;

namespace MoonlightDashboard.Db.Models
{
    public abstract class Model
    {
        public static string GetCollectionName()
        {
            throw new NotImplementedException(nameof(GetCollectionName) + " not implemented in child class");
        }

        public static string GetTypeId()
        {
            var name = GetCollectionName();
            return name.Substring(0, name.Length - 1);
        }

        public string? Id { get; set; }
        public long? CreatedTimestamp { get; set; }
        public long? UpdatedTimestamp { get; set; }
    }
}
