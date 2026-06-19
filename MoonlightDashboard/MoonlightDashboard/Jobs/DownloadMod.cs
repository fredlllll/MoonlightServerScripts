
using MoonlightDashboard.Apis.Steam;
using MoonlightDashboard.Database.Models;

namespace MoonlightDashboard.Jobs
{
    public class DownloadMod : IJobExecutor
    {
        public async Task RunAsync(Job job, IServiceScope scope, CancellationToken stoppingToken)
        {
            var modId = job.Data;
            if (modId == null)
            {
                throw new Exception("No Mod Id given");
            }

            var cmd = new SteamCmd();
            cmd.Username = "TODO: get from login, remember";
            cmd.AddModDownload(Lib.Constants.ARMA3APPID, modId);
            await cmd.RunAsync(stoppingToken);
        }
    }
}
