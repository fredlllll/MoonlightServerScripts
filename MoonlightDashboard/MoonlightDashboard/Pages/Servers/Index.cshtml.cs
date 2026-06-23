using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;
using MoonlightDashboard.Services;

namespace MoonlightDashboard.Pages.Servers
{
    public class IndexModel : PageModel
    {
        public List<Arma3Server> Servers = null!;
        public Dictionary<string, string> ActiveModsetNames = null!;
        private DatabaseContext db;

        public IndexModel(DatabaseContext db)
        {
            this.db = db;
        }

        public void OnGet()
        {
            Servers = db.Arma3Servers.ToList();
            ActiveModsetNames = new();

            foreach (var server in Servers)
            {
                if (server.ActiveModsetId != null)
                {
                    var modset = db.Arma3Modsets.FirstOrDefault(m => m.Id == server.ActiveModsetId);
                    if (modset != null)
                    {
                        ActiveModsetNames[server.Id] = modset.Name;
                    }
                    else
                    {
                        ActiveModsetNames[server.Id] = "Not Found";
                    }
                }
            }
        }

        public void OnPostCreate(string name, int port)
        {
            var server = new Arma3Server()
            {
                Id = Util.GetNewId<Arma3Server>(),
                Name = name,
                Port = port
            };
            db.Arma3Servers.Add(server);
            db.SaveChanges();
            Redirect($"/Servers/{server.Id}");
        }

        public void OnPostUpdateServer()
        {
            JobService.EnqueueUpdateServer(db, null);
            Redirect("/Jobs");
        }

        public void OnPostUpdateServerCreatorDlc()
        {
            JobService.EnqueueUpdateServer(db, "creatordlc");
            Redirect("/Jobs");
        }
    }
}
