using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Arma3;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Filters;
using MoonlightDashboard.Lib;
using MoonlightDashboard.Services;

namespace MoonlightDashboard.Pages.Servers
{
    [LoggedIn]
    public class IndexModel : PageModel
    {
        public List<Arma3Server> Servers = null!;
        public Dictionary<string, string> ActiveModsetNames = null!;
        public string? Error => this.GetError();
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

        public IActionResult OnPostCreate(string name, int port)
        {
            if (name.Length < 3)
            {
                this.SetError("Name too short");
                OnGet();
                return Page();
            }
            var server = new Arma3Server()
            {
                Id = Util.GetNewId<Arma3Server>(),
                Name = name,
                Port = port
            };
            db.Arma3Servers.Add(server);
            db.SaveChanges();
            var api = new Arma3ServerApi(server.Id);
            api.CreateServiceFile(server);
            //dont need to create config files here as the next page will create them when reading contents if they dont exist
            return LocalRedirect($"/Servers/Details/{server.Id}");
        }

        public IActionResult OnPostUpdateServer()
        {
            JobService.EnqueueUpdateServer(db, null);
            return LocalRedirect("/Jobs");
        }

        public IActionResult OnPostUpdateServerCreatorDlc()
        {
            JobService.EnqueueUpdateServer(db, "creatordlc");
            return LocalRedirect("/Jobs");
        }
    }
}
