using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;

namespace MoonlightDashboard.Pages
{
    public class JobsModel : PageModel
    {
        public IEnumerable<Job> Jobs;

        private DatabaseContext db;
        public JobsModel(DatabaseContext db)
        {
            this.db = db;
        }

        public void OnGet()
        {
            Jobs = db.Jobs;
        }
    }
}
