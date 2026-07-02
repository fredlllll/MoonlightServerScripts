using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Arma3;
using MoonlightDashboard.Apis.SystemD;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;
using System.Linq;


namespace MoonlightDashboard.Pages.Servers
{
    public class DetailsModel : PageModel
    {
        public Arma3Server Server = null!;
        public Arma3ServerApi ServerApi = null!;
        public List<Arma3Modset> Modsets = null!;
        public List<Arma3CreatorDlc> CreatorDlcs = null!;
        public HashSet<string> ActiveCreatorDlcs = null!;
        public SystemDUnit ServerUnit = null!;
        public SystemDUnitInfo ServerUnitInfo = null!;
        public string LastLog = "";
        private DatabaseContext db;

        public DetailsModel(DatabaseContext db)
        {
            this.db = db;
        }

        public void OnGet(string id)
        {
            Server ??= db.Arma3Servers.First(s => s.Id == id);
            ServerApi ??= new Arma3ServerApi(id);
            Modsets = db.Arma3Modsets.ToList();
            CreatorDlcs = db.Arma3CreatorDlcs.ToList();
            ActiveCreatorDlcs = new HashSet<string>(db.Arma3ServerCreatorDlcs.Where(cdlc => cdlc.Arma3ServerId == Server.Id).Select(x => x.Arma3CreatorDlcId));
            ServerUnit ??= new SystemDUnit(id);
            ServerUnitInfo = ServerUnit.GetInfo();
            LastLog = ServerUnit.GetLog(1000);
        }

        public IActionResult OnPostSetModset(string id, string? modsetId)
        {
            if (string.IsNullOrWhiteSpace(modsetId))
            {
                modsetId = null;
            }
            Server = db.Arma3Servers.First(s => s.Id == id);
            Server.ActiveModsetId = modsetId;
            db.SaveChanges();
            return RedirectToPage();
        }

        public IActionResult OnPostSetPort(string id, int port)
        {
            Server = db.Arma3Servers.First(s => s.Id == id);
            Server.Port = port;
            db.SaveChanges();
            return RedirectToPage();
        }

        public IActionResult OnPostSetCreatorDlcs(string id)
        {
            Server = db.Arma3Servers.First(s => s.Id == id);
            var activeDlcIds = db.Arma3ServerCreatorDlcs.Where(x => x.Arma3ServerId == id).Select(x => x.Arma3CreatorDlcId);

            var selectedDlcIds = new HashSet<string>();
            string prefix = "cdlc_";
            foreach (string key in Request.Form.Keys)
            {
                if (key.StartsWith(prefix))
                {
                    string idPart = key.Substring(prefix.Length);
                    selectedDlcIds.Add(idPart);
                }
            }

            //remove dlcs that are in activeDlcs but not in selectedDlcs
            var toDelete = activeDlcIds.Except(selectedDlcIds).ToList();
            // Add mods that are in selectedModIds but not in activeMods
            var toAdd = selectedDlcIds.Except(activeDlcIds).ToList();

            foreach (var dlcId in toDelete)
            {
                db.RemoveRange(db.Arma3ServerCreatorDlcs.Where(x => x.Arma3ServerId == id && x.Arma3CreatorDlcId == dlcId));
            }
            foreach (var dlcId in toAdd)
            {
                var dlc = new Arma3ServerCreatorDlc()
                {
                    Id = Util.GetNewId<Arma3ServerCreatorDlc>(),
                    Arma3ServerId = id,
                    Arma3CreatorDlcId = dlcId,
                };
                db.Arma3ServerCreatorDlcs.Add(dlc);
            }
            db.SaveChanges();

            return RedirectToPage();
        }

        public IActionResult OnPostUpdateBasicConfig(string id, string content)
        {
            ServerApi = new Arma3ServerApi(id);
            ServerApi.SetBasicConfigFileContents(content);
            return RedirectToPage();
        }

        public IActionResult OnPostResetBasicConfig(string id)
        {
            ServerApi = new Arma3ServerApi(id);
            ServerApi.ResetBasicConfigFileContents();
            return RedirectToPage();
        }

        public IActionResult OnPostUpdateServerConfig(string id, string content)
        {
            ServerApi = new Arma3ServerApi(id);
            ServerApi.SetServerConfigFileContents(content);
            return RedirectToPage();
        }
        public IActionResult OnPostResetServerConfig(string id)
        {
            ServerApi = new Arma3ServerApi(id);
            ServerApi.ResetServerConfigFileContents();
            return RedirectToPage();
        }

        public IActionResult OnPostUpdateServerProfile(string id, string content)
        {
            ServerApi = new Arma3ServerApi(id);
            ServerApi.SetServerProfileFileContents(content);
            return RedirectToPage();
        }

        public IActionResult OnPostResetServerProfile(string id)
        {
            ServerApi = new Arma3ServerApi(id);
            ServerApi.ResetServerProfileFileContents();
            return RedirectToPage();
        }
    }
}
