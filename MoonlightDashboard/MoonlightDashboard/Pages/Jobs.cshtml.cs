using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;

namespace MoonlightDashboard.Pages
{
    public class JobsModel : PageModel
    {
        public IEnumerable<Job> Jobs = Enumerable.Empty<Job>();

        private DatabaseContext db;
        public JobsModel(DatabaseContext db)
        {
            this.db = db;
        }

        public void OnGet()
        {
            Jobs = db.Jobs;
        }

        public void OnPostClear()
        {
            var jobsToClear = db.Jobs.Where(j => j.IsComplete);
            db.Jobs.RemoveRange(jobsToClear);
            db.SaveChanges();
            OnGet();
        }

        public void OnPostRerun(string jobId)
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
            OnGet();
        }

        public void OnPostCancel(string jobId)
        {
            var job = db.Jobs.FirstOrDefault(j => j.Id == jobId);
            if (job != null && job.IsRunning && !job.CancellationRequested)
            {
                job.CancellationRequested = true;
                db.SaveChanges();
            }
            OnGet();
        }

        public void OnPostDelete(string jobId)
        {
            var job = db.Jobs.FirstOrDefault(j => j.Id == jobId);
            if (job != null)
            {
                db.Jobs.Remove(job);
                db.SaveChanges();
            }
            OnGet();
        }
    }
}
