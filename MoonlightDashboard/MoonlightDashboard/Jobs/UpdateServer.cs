using MoonlightDashboard.Apis.Steam;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Jobs
{
    public class UpdateServer : IJobExecutor
    {
        public async Task RunAsync(Job job, IServiceScope scope, CancellationToken stoppingToken)
        {
            var beta = job.Data;

            var cmd = new SteamCmd();
            cmd.Username = "TODO: get from login, remember";
            cmd.AddAppUpdate(Constants.ARMA3SERVERAPPID, true, beta);
            await cmd.RunAsync(stoppingToken);
        }
    }
}
