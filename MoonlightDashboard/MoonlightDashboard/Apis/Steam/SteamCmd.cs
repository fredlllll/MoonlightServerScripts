using Microsoft.EntityFrameworkCore;
using MoonlightDashboard.Lib;
using System.ComponentModel.DataAnnotations;
using System.Diagnostics;

namespace MoonlightDashboard.Apis.Steam
{
    public class SteamCmd
    {
        private readonly List<string> parameters = new List<string>();
        public string? Username { get; set; }
        public string? Password { get; set; }
        public string? AuthCode { get; set; }

        public async Task<ProcessResult> RunAsync(CancellationToken stoppingToken)
        {
            var argList = new List<string>();
            if (!string.IsNullOrWhiteSpace(Username))
            {
                argList.Add("+login");
                argList.Add(Username);
                if (!string.IsNullOrWhiteSpace(Password))
                {
                    argList.Add(Password);
                }
                if (!string.IsNullOrWhiteSpace(AuthCode))
                {
                    argList.Add(AuthCode);
                }
            }

            var psi = new ProcessStartInfo()
            {
                FileName = "steamcmd",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                UserName = "steam"
            };

            psi.Environment["HOME"] = "/home/steam";

            foreach (var arg in argList)
            {
                psi.ArgumentList.Add(arg);
            }
            foreach (var param in parameters)
            {
                psi.ArgumentList.Add(param);
            }
            psi.ArgumentList.Add("+quit");

            using var process = Process.Start(psi) ?? throw new Exception("could not create process");
            process.StandardInput.Close(); // makes it hopefully not wait for input and instead error out. needed if login token is not present
            try
            {
                await process.WaitForExitAsync(stoppingToken);
            }
            catch (OperationCanceledException)
            {
                try
                {
                    process.Kill();
                }
                catch (InvalidOperationException)
                {
                    // Race condition: Process exited just as we tried to kill it.
                    // Safe to ignore.
                }
                throw;
            }
            finally
            {
                process.WaitForExit();
            }
            return new ProcessResult
            {
                Output = await process.StandardOutput.ReadToEndAsync(),
                Error = await process.StandardError.ReadToEndAsync(),
                ExitCode = process.ExitCode
            };
        }

        public void AddModDownload(string appId, string modId)
        {
            parameters.Add("+workshop_download_item");
            parameters.Add(appId);
            parameters.Add(modId);
        }

        public void AddAppUpdate(string appId, bool validate = true, string? beta = null)
        {
            parameters.Add("+app_update");
            parameters.Add(appId);
            if (!string.IsNullOrWhiteSpace(beta))
            {
                parameters.Add("-beta");
                parameters.Add(beta);
                parameters.Add("''"); // no idea if it works without the '' in there
            }
            if (validate)
            {
                parameters.Add("validate");
            }
        }
    }
}
