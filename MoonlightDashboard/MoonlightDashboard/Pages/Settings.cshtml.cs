using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Steam;
using MoonlightDashboard.Database;

namespace MoonlightDashboard.Pages
{
    public class SettingsModel : PageModel
    {
        public const string SettingLastSteamUser = "lastSteamUser";

        private DatabaseContext db;

        public SettingsModel(DatabaseContext db)
        {
            this.db = db;
        }

        public void OnGet()
        {
        }

        public async Task OnPostSteamLogin(string user, string password, string authCode)
        {
            var cmd = new SteamCmd();
            cmd.Username = user;
            cmd.Password = password;
            cmd.AuthCode = authCode;
            db.SetSettingsValue(SettingLastSteamUser, user);
            db.SaveChanges();
            await cmd.RunAsync(CancellationToken.None);
        }
    }
}
