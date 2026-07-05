using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Filters;
using System.Threading.Tasks;

namespace MoonlightDashboard.Pages
{
    [LoggedIn]
    public class JobsModel : PageModel
    {
        public IEnumerable<Job> Jobs = Enumerable.Empty<Job>();

        private DatabaseContext db;
        public JobsModel(DatabaseContext db)
        {
            this.db = db;
        }

        public async Task OnGet()
        {
            Jobs = db.Jobs;
            var modInfos = await Apis.Steam.Local.Mods.GetModInfos(db, Jobs.Select(x => x.Data ?? ""));
            foreach (var job in Jobs)
            {
                if (job.JobType == JobType.DownloadMod)
                {
                    job.Data = modInfos.Where(modInfos => modInfos.ModId == job.Data).Select(modInfo => modInfo.Name).FirstOrDefault() ?? job.Data;
                }
            }
        }

        public IActionResult OnPostClear()
        {
            var jobsToClear = db.Jobs.Where(j => j.IsComplete);
            db.Jobs.RemoveRange(jobsToClear);
            db.SaveChanges();
            return RedirectToPage();
        }

        public IActionResult OnPostRerun(string jobId)
        {
            var job = db.Jobs.FirstOrDefault(j => j.Id == jobId);
            if (job != null && job.IsComplete)
            {
                job.IsComplete = false;
                job.IsSuccessful = false;
                job.IsRunning = false;
                job.ErrorMessage = null;
                job.Result = null;
                job.Updated = DateTime.UtcNow;
                job.CancellationRequested = false;
                db.SaveChanges();
            }
            return RedirectToPage();
        }

        public IActionResult OnPostCancel(string jobId)
        {
            var job = db.Jobs.FirstOrDefault(j => j.Id == jobId);
            if (job != null && job.IsRunning && !job.CancellationRequested)
            {
                job.CancellationRequested = true;
                db.SaveChanges();
            }
            return RedirectToPage();
        }

        public IActionResult OnPostDelete(string jobId)
        {
            var job = db.Jobs.FirstOrDefault(j => j.Id == jobId);
            if (job != null)
            {
                db.Jobs.Remove(job);
                db.SaveChanges();
            }
            return RedirectToPage();
        }
    }
}
