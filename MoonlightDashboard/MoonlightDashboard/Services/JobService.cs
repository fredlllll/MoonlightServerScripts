
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Jobs;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Services
{
    public class JobService : BackgroundService
    {
        private static Dictionary<JobType, Type> ExecutorTypes = new Dictionary<JobType, Type>()
        {
            { JobType.DownloadMod, typeof(Jobs.DownloadMod) },
            { JobType.UpdateServer, typeof(Jobs.UpdateServer) }
        };

        private readonly IServiceScopeFactory _scopeFactory;
        public JobService(IServiceScopeFactory scopeFactory)
        {
            _scopeFactory = scopeFactory;
        }

        private void EndJob(string jobId, bool success, string? errorMessage = null)
        {
            using var scope = _scopeFactory.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<Database.DatabaseContext>();
            var dbJob = db.Jobs.Where(j => j.Id == jobId).FirstOrDefault();
            if (dbJob == null)
            {
                Console.WriteLine($"Failed to find job {jobId} to end it");
                return;
            }
            dbJob.IsRunning = false;
            dbJob.IsComplete = true;
            dbJob.IsSuccessful = success;
            dbJob.ErrorMessage = errorMessage;
            db.SaveChanges();
        }

        private void BeginJob(string jobId)
        {
            using var scope = _scopeFactory.CreateScope();
            var db = scope.ServiceProvider.GetRequiredService<Database.DatabaseContext>();
            var dbJob = db.Jobs.Where(j => j.Id == jobId).FirstOrDefault();
            if (dbJob == null)
            {
                Console.WriteLine($"Failed to find job {jobId} to begin it");
                return;
            }
            dbJob.IsRunning = true;
            dbJob.IsComplete = false;
            db.SaveChanges();
        }

        protected override async Task ExecuteAsync(CancellationToken stoppingToken)
        {
            while (!stoppingToken.IsCancellationRequested)
            {
                Job? job = null;
                {
                    using var scope = _scopeFactory.CreateScope();
                    var db = scope.ServiceProvider.GetRequiredService<Database.DatabaseContext>();
                    job = db.Jobs.Where(j => !j.IsComplete && !j.IsRunning).FirstOrDefault();
                }
                if (job == null)
                {
                    await Task.Delay(2000, stoppingToken);
                    continue;
                }
                IJobExecutor? executor;
                ExecutorTypes.TryGetValue(job.JobType, out Type? executorType);
                if (executorType == null)
                {
                    EndJob(job.Id, false, $"No executor found for job type {job.JobType}");
                    continue;
                }
                try
                {
                    executor = (IJobExecutor?)Activator.CreateInstance(executorType);
                    if (executor == null)
                    {
                        throw new Exception("CreateInstance returned null");
                    }
                }
                catch (Exception ex)
                {
                    EndJob(job.Id, false, $"Failed to create executor for job {job.Id} of type {job.JobType}: {ex.Message}");
                    continue;
                }
                try
                {
                    using var scope = _scopeFactory.CreateScope();
                    using var monitor = new JobCancellationMonitor(stoppingToken, scope, job.Id);
                    BeginJob(job.Id);
                    await executor.RunAsync(job, scope, monitor.Token);
                    EndJob(job.Id, true);
                }
                catch (Exception ex)
                {
                    EndJob(job.Id, false, ex.Message);
                    continue;
                }
            }
        }

        public static void EnqueueDownloadMod(DatabaseContext db, string modId)
        {
            var job = new Job()
            {
                Id = Util.GetNewId<Job>(),
                JobType = JobType.DownloadMod,
                Data = modId
            };
            db.Jobs.Add(job);
            db.SaveChanges();
        }

        public static void EnqueueUpdateServer(DatabaseContext db, string? beta)
        {
            var job = new Job()
            {
                Id = Util.GetNewId<Job>(),
                JobType = JobType.UpdateServer,
                Data = beta
            };
            db.Jobs.Add(job);
            db.SaveChanges();
        }
    }
}
