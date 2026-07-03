using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;
using MoonlightDashboard.Services;

namespace MoonlightDashboard.Pages.Mods
{
    public class IndexModel : PageModel
    {
        private readonly DatabaseContext db;
        public IEnumerable<ModInfo> ModInfos = null!;
        public string? Error => this.GetError();

        public IndexModel(DatabaseContext db)
        {
            this.db = db;
        }

        public async Task OnGet()
        {
            ModInfos = await Apis.Steam.Local.Mods.GetModInfos(db, Apis.Steam.Local.Mods.GetDownloadedModsIds());
        }

        public IActionResult OnPostDeleteMod(string modId)
        {
            Apis.Steam.Local.Mods.DeleteMod(modId);
            return RedirectToPage();
        }

        public IActionResult OnPostDeleteAllMods()
        {
            var ids = Apis.Steam.Local.Mods.GetDownloadedModsIds();
            foreach (var id in ids)
            {
                Apis.Steam.Local.Mods.DeleteMod(id);
            }
            return RedirectToPage();
        }

        public async Task<IActionResult> OnPostDownloadMods(string? collectionId, string? modIds)
        {
            IEnumerable<string> modIdsList;
            if (!string.IsNullOrWhiteSpace(collectionId))
            {
                modIdsList = await Apis.Steam.Local.Mods.GetCollectionModIds(collectionId);
            }
            else if (!string.IsNullOrWhiteSpace(modIds))
            {
                modIdsList = modIds.Split(',').Select(m => m.Trim());
            }
            else
            {
                this.SetError("no mod ids given");
                return RedirectToPage();
            }

            foreach (var modId in modIdsList)
            {
                JobService.EnqueueDownloadMod(db, modId);
            }

            return LocalRedirect("/Jobs");
        }
    }
}
