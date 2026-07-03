using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;

namespace MoonlightDashboard.Jobs
{
    public interface IJobExecutor
    {
        Task RunAsync(Job job, IServiceScope scope, CancellationToken stoppingToken);
    }
}
