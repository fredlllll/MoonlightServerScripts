using MoonlightDashboard.Apis.Steam;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Pages;
using System.Text.Json;

namespace MoonlightDashboard.Jobs
{
    public class LoginSteam : IJobExecutor
    {
        public async Task RunAsync(Job job, IServiceScope scope, CancellationToken stoppingToken)
        {
            if (job.Data == null)
            {
                throw new Exception("No data provided for the job.");
            }
            (string user, string pwd, string authcode) = JsonSerializer.Deserialize<(string, string, string)>(job.Data);

            var cmd = new SteamCmd();
            cmd.Username = user;
            cmd.Password = pwd;
            cmd.AuthCode = authcode;
            var result = await cmd.RunAsync(stoppingToken);
            job.Result = result.GetCompleteOutputAsMarkup();
            var db = scope.ServiceProvider.GetRequiredService<DatabaseContext>();
            db.SetSettingsValue(SettingsModel.SettingLastSteamUser, cmd.Username);
            db.SaveChanges();
        }
    }
}
