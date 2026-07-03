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
            try
            {
                await cmd.RunAsync(stoppingToken);
            }
            catch (OperationCanceledException)
            {
                throw;
            }
            finally
            {
                job.Result = cmd.Result.GetCompleteOutputAsMarkup();
            }
        }
    }
}
