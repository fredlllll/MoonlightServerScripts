using Microsoft.AspNetCore.Hosting.Server;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Arma3;
using MoonlightDashboard.Database;

namespace MoonlightDashboard.Pages.Servers
{
    public class ServerProfileModel : PageModel
    {
        public Arma3ServerApi ServerApi = null!;

        private DatabaseContext db;

        public ServerProfileModel(DatabaseContext db)
        {
            this.db = db;
        }

        public void OnGet(string id)
        {
            db.Arma3Servers.First(s => s.Id == id); //check if server exists
            ServerApi ??= new Arma3ServerApi(id);
        }

        public IActionResult OnPostUpdate(string id, string content)
        {
            db.Arma3Servers.First(s => s.Id == id); //check if server exists
            ServerApi = new Arma3ServerApi(id);
            ServerApi.SetServerProfileFileContents(content);
            return RedirectToPage();
        }

        public IActionResult OnPostReset(string id)
        {
            db.Arma3Servers.First(s => s.Id == id); //check if server exists
            ServerApi = new Arma3ServerApi(id);
            ServerApi.ResetServerProfileFileContents();
            return RedirectToPage();
        }
    }
}
