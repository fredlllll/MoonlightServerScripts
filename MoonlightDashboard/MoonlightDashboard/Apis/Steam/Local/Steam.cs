using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Apis.Steam.Local
{
    public static class Steam
    {
        public static string GetSteamFolderPath()
        {
            return "/home/steam/Steam";
        }

        public static string GetArma3ServerFolder()
        {
            return Path.Combine(GetSteamFolderPath(), "steamapps", "common", "Arma 3 Server");
        }

        public static string GetArmaWorkshopAcfPath()
        {
            return Path.Combine(GetSteamFolderPath(), "steamapps", "workshop", $"appworkshop_{Constants.ARMA3APPID}.acf");
        }
    }
}
