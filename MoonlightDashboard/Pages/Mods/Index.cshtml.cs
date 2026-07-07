using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Filters;
using MoonlightDashboard.Lib;
using MoonlightDashboard.Services;
using System.Text.RegularExpressions;

namespace MoonlightDashboard.Pages.Mods
{
    [LoggedIn]
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

        public async Task<IActionResult> OnPostDownloadMods(string? collectionId, string? modIds, IFormFile? modsetHtml)
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
            else if (modsetHtml != null && modsetHtml.Length > 0)
            {
                using var reader = new StreamReader(modsetHtml.OpenReadStream());
                var content = await reader.ReadToEndAsync();

                var regex = new Regex(@"filedetails/\?id=(\d+)");
                var matches = regex.Matches(content);
                modIdsList = matches.Select(m => m.Groups[1].Value).Distinct();
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
