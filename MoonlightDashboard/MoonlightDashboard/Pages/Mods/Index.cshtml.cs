using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Services;

namespace MoonlightDashboard.Pages.Mods
{
    public class IndexModel : PageModel
    {
        private readonly DatabaseContext db;
        public IEnumerable<ModInfo> ModInfos = null!;
        public string? Error = null;

        public IndexModel(DatabaseContext db)
        {
            this.db = db;
        }

        public async Task OnGet()
        {
            ModInfos = await Apis.Steam.Local.Mods.GetModInfos(db, Apis.Steam.Local.Mods.GetDownloadedModsIds());
        }

        public async Task OnPostDeleteMod(string modId)
        {
            Apis.Steam.Local.Mods.DeleteMod(modId);
            await OnGet();
        }

        public async Task OnPostDeleteAllMods()
        {
            var ids = Apis.Steam.Local.Mods.GetDownloadedModsIds();
            foreach (var id in ids)
            {
                Apis.Steam.Local.Mods.DeleteMod(id);
            }
            await OnGet();
        }

        public async Task OnPostDownloadMods(string collectionId, string modIds)
        {
            IEnumerable<string> modIdsList = null;
            if (collectionId.Length > 0)
            {
                modIdsList = await Apis.Steam.Local.Mods.GetCollectionModIds(collectionId);
            }
            else if (modIds.Length > 0)
            {
                modIdsList = modIds.Split(',').Select(m=>m.Trim());
            }
            else
            {
                Error = "no mod ids given";
                await OnGet();
                return;
            }

            foreach (var modId in modIdsList)
            {
                JobService.EnqueueDownloadMod(db, modId);
            }

            Redirect("/Jobs");
        }
    }
}
