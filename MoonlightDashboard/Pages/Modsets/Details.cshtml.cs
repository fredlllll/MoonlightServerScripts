using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Filters;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Pages.Modsets
{
    [LoggedIn]
    public class DetailsModel : PageModel
    {
        private DatabaseContext db;

        public Arma3Modset Modset = null!;
        public Dictionary<string, ModInfo> AllMods = null!;
        public Dictionary<string, Arma3ModsetMod> ActiveMods = null!;
        public List<Arma3ModsetMod> ActiveButDeletedMods = null!;
        public Dictionary<string, ModInfo> DeletedModInfos = null!;

        public DetailsModel(DatabaseContext db)
        {
            this.db = db;
        }

        public async Task OnGet(string id)
        {
            Modset = db.Arma3Modsets.First(m => m.Id == id);
            AllMods = (await Apis.Steam.Local.Mods.GetModInfos(db, Apis.Steam.Local.Mods.GetDownloadedModsIds())).ToDictionary(m => m.ModId);
            ActiveMods = db.Arma3ModsetMods.Where(ms => ms.ModsetId == Modset.Id).ToDictionary(m => m.ModSteamId);

            ActiveButDeletedMods = new();
            foreach (var kv in ActiveMods)
            {
                if (!AllMods.ContainsKey(kv.Key))
                {
                    ActiveButDeletedMods.Add(kv.Value);
                }
            }
            DeletedModInfos = (await Apis.Steam.Local.Mods.GetModInfos(db, ActiveButDeletedMods.Select(m => m.ModSteamId))).ToDictionary(x=>x.ModId);
        }

        public IActionResult OnPostDeleteModset(string id)
        {
            foreach (var server in db.Arma3Servers.Where(x => x.ActiveModsetId == id))
            {
                server.ActiveModsetId = null;
            }
            db.RemoveRange(db.Arma3ModsetMods.Where(ms => ms.ModsetId == id));
            db.Remove(db.Arma3Modsets.First(m => m.Id == id));
            db.SaveChanges();
            return LocalRedirect("/Modsets");
        }

        public IActionResult OnPostUpdate(string id)
        {
            ActiveMods = db.Arma3ModsetMods.Where(ms => ms.ModsetId == id).ToDictionary(m => m.ModSteamId);

            var selectedModIds = new HashSet<string>();
            string prefix = "mod_";
            foreach (string key in Request.Form.Keys)
            {
                if (key.StartsWith(prefix))
                {
                    string idPart = key.Substring(prefix.Length);
                    selectedModIds.Add(idPart);
                }
            }

            //remove mods that are in activeMods but not in selectedMods
            var toDelete = ActiveMods.Keys.Except(selectedModIds).ToList();
            // Add mods that are in selectedModIds but not in activeMods
            var toAdd = selectedModIds.Except(ActiveMods.Keys).ToList();

            foreach (var modId in toDelete)
            {
                db.Remove(db.Arma3ModsetMods.First(ms => ms.ModsetId == id && ms.ModSteamId == modId));
            }
            foreach (var modId in toAdd)
            {
                var mod = new Arma3ModsetMod()
                {
                    Id = Util.GetNewId<Arma3ModsetMod>(),
                    ModSteamId = modId,
                    ModsetId = id,
                };
                db.Add(mod);
            }

            db.SaveChanges();

            return RedirectToPage();
        }
    }
}
