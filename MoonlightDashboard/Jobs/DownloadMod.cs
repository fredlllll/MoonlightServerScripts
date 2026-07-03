
using MoonlightDashboard.Apis.Steam;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Pages;

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
            var db = scope.ServiceProvider.GetRequiredService<DatabaseContext>();

            var cmd = new SteamCmd();
            cmd.Username = db.GetSettingsValue(SettingsModel.SettingLastSteamUser);
            cmd.AddModDownload(Lib.Constants.ARMA3APPID, modId);
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
