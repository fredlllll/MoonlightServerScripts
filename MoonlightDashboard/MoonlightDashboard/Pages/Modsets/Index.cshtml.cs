using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Pages.Modsets
{
    public class IndexModel : PageModel
    {
        public List<Arma3Modset> Modsets { get; set; } = null!;
        public Dictionary<string, List<ModInfo>> ModsetModInfos { get; set; } = null!;

        public async Task OnGet()
        {
            var db = HttpContext.RequestServices.GetRequiredService<DatabaseContext>();
            Modsets = db.Arma3Modsets.ToList();

            ModsetModInfos = new();
            foreach (var modset in Modsets)
            {
                var mods = db.Arma3ModsetMods.Where(m => m.ModsetId == modset.Id);
                var modInfos = await Apis.Steam.Local.Mods.GetModInfos(db, mods.Select(ms => ms.ModSteamId));
                ModsetModInfos[modset.Id] = modInfos.ToList();
            }
        }

        public IActionResult OnPostCreate(string name)
        {
            var modset = new Arma3Modset()
            {
                Id = Util.GetNewId<Arma3Modset>(),
                Name = name,
            };

            var db = HttpContext.RequestServices.GetRequiredService<DatabaseContext>();
            db.Arma3Modsets.Add(modset);
            db.SaveChanges();

            return LocalRedirect($"/Modsets/{modset.Id}");
        }
    }
}
