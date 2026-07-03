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
            string[] expandedData = JsonSerializer.Deserialize<string[]>(job.Data) ?? throw new Exception("data is invalid");
            string user = expandedData[0];
            string pwd = expandedData[1];
            string authcode = expandedData[2];

            var cmd = new SteamCmd();
            cmd.Username = user;
            cmd.Password = pwd;
            cmd.AuthCode = authcode;
            try
            {
                await cmd.RunAsync(stoppingToken);
            }
            catch (OperationCanceledException) { }
            finally
            {
                job.Result = cmd.Result.GetCompleteOutputAsMarkup();
            }
            var db = scope.ServiceProvider.GetRequiredService<DatabaseContext>();
            db.SetSettingsValue(SettingsModel.SettingLastSteamUser, cmd.Username);
            db.SaveChanges();
        }
    }
}
