using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Filters;
using MoonlightDashboard.Lib;
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
            Jobs = db.Jobs.ToArray();
            var modInfos = await Apis.Steam.Local.Mods.GetModInfos(db, Jobs.Select(x => x.Data ?? ""));
            foreach (var job in Jobs)
            {
                if (job.JobType == JobType.DownloadMod)
                {
                    var modName = modInfos.FirstOrDefault(modInfo => modInfo.ModId == job.Data)?.Name;
                    if (modName != null)
                    {
                        job.Data = modName + " (" + job.Data + ")";
                    }
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
            var job = db.Jobs.First(j => j.Id == jobId);
            if (job.IsPending())
            {
                job.IsComplete = true;
                job.IsSuccessful = false;
                job.ErrorMessage = "Job was cancelled before it ran";
                this.SetInfo("Cancelled job in pending " + job.Id);
                db.SaveChanges();
            }
            else if (job.IsRunning && !job.CancellationRequested)
            {
                job.CancellationRequested = true;
                this.SetInfo("Cancelled job in running " + job.Id);
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
