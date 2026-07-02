using MoonlightDashboard.Apis.Steam;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;
using MoonlightDashboard.Pages;

namespace MoonlightDashboard.Jobs
{
    public class UpdateServer : IJobExecutor
    {
        public async Task RunAsync(Job job, IServiceScope scope, CancellationToken stoppingToken)
        {
            var beta = job.Data;

            var db = scope.ServiceProvider.GetRequiredService<DatabaseContext>();

            var cmd = new SteamCmd();
            cmd.Username = db.GetSettingsValue(SettingsModel.SettingLastSteamUser);
            cmd.AddAppUpdate(Constants.ARMA3SERVERAPPID, true, beta);
            var result = await cmd.RunAsync(stoppingToken);
            job.Result = result.GetCompleteOutputAsMarkup();
        }
    }
}
