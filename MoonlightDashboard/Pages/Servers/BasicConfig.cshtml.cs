using Microsoft.AspNetCore.Hosting.Server;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Arma3;
using MoonlightDashboard.Database;

namespace MoonlightDashboard.Pages.Servers
{
    public class BasicConfigModel : PageModel
    {
        public Arma3ServerApi ServerApi = null!;

        private DatabaseContext db;

        public BasicConfigModel(DatabaseContext db)
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
            ServerApi.SetBasicConfigFileContents(content);
            return RedirectToPage();
        }

        public IActionResult OnPostReset(string id)
        {
            db.Arma3Servers.First(s => s.Id == id); //check if server exists
            ServerApi = new Arma3ServerApi(id);
            ServerApi.ResetBasicConfigFileContents();
            return RedirectToPage();
        }
    }
}
