using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Db
{
    public static class DbUtil
    {
        public static string GetResourceId(string resourceType)
        {
            string alphabet = "abcdefghijklmnopqrstuvwxyz0123456789";
            char[] chars = new char[32];
            for (int i = 0; i < chars.Length; i++)
            {
                chars[i] = alphabet[Util.Random.Next(alphabet.Length)];
            }
            return $"{resourceType} {new string(chars)}";
        }
    }
}
