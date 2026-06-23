using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;

namespace MoonlightDashboard.Pages.Mods
{
    public class IndexModel : PageModel
    {
        private readonly DatabaseContext db;
        private IEnumerable<ModInfo> modInfos;

        public IndexModel(DatabaseContext db)
        {
            this.db = db;
        }

        public async void OnGet()
        {
            modInfos = await Apis.Steam.Local.Mods.GetModInfos(db, Apis.Steam.Local.Mods.GetDownloadedModsIds());
            var modIds = Apis.Steam.Local.Mods.GetDownloadedModsIds();
            foreach (var modId in modIds)
            {

            }
        }
    }
}
