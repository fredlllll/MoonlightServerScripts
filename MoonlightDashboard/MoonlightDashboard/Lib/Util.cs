using UUIDNext;

namespace MoonlightDashboard.Lib
{
    public static class Util
    {
        public static string ApplicationFolder { get; private set; }

        public static string GetApplicationFilePath(string subPath)
        {
            return Path.Join(ApplicationFolder, subPath);
        }

        static Util()
        {
            ApplicationFolder = Path.Join(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "YoutubeSubVideoManager");
            Directory.CreateDirectory(ApplicationFolder);
        }

        public static string GetNewId<T>()
        {
            var t = typeof(T);
            var typeId = t.Name.ToLower();
            var id = Uuid.NewDatabaseFriendly(UUIDNext.Database.PostgreSql);
            return $"{typeId}_{id}";
        }
    }
}
