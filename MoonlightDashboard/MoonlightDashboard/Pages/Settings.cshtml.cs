using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Steam;
using MoonlightDashboard.Database;
using MoonlightDashboard.Services;

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

        public IActionResult OnPostSteamLogin(string user, string password, string authCode)
        {
            JobService.EnqueueLoginSteam(db, user, password, authCode);
            return LocalRedirect("/jobs");
        }
    }
}
