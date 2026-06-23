using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;


namespace MoonlightDashboard.Pages.Servers
{
    public class DetailsModel : PageModel
    {
        public Arma3Server Server = null!;
        public List<Arma3Modset> Modsets = null!;
        private DatabaseContext db;

        public DetailsModel(DatabaseContext db)
        {
            this.db = db;
        }

        public void OnGet(string id)
        {
            Server = db.Arma3Servers.First(s => s.Id == id);
            Modsets = db.Arma3Modsets.ToList();
        }

        public void OnPostSetModset(string id, string? modsetId)
        {
            if (string.IsNullOrWhiteSpace(modsetId))
            {
                modsetId = null;
            }
            Server = db.Arma3Servers.First(s => s.Id == id);
            Server.ActiveModsetId = modsetId;
            db.SaveChanges();
            OnGet(id);
        }

        public void OnPostSetPort(string id, int port)
        {
            Server = db.Arma3Servers.First(s => s.Id == id);
            Server.Port = port;
            db.SaveChanges();
            OnGet(id);
        }

        public void OnPostStart(string id)
        {

        }
    }
}
