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

        public ProcessResult Result { get; private set; } = new ProcessResult();

        public async Task RunAsync(CancellationToken stoppingToken)
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
                FileName = Local.Steam.GetSteamCmdPath(),
                RedirectStandardOutput = true,
                RedirectStandardInput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true,
                UserName = Constants.STEAMUSER
            };

            psi.WorkingDirectory = psi.Environment["HOME"] = "/home/" + Constants.STEAMUSER;
            psi.Environment["USER"] = Constants.STEAMUSER;

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
            process.StandardInput.Close(); // makes it not wait for input and instead error out. needed if login token is not present

            Result = new ProcessResult();
            process.OutputDataReceived += (sender, e) =>
            {
                if (e.Data != null)
                {
                    Result.OutputItems.Add(new ProcessOutputItem
                    {
                        IsError = false,
                        Text = e.Data
                    });
                }
            };
            process.ErrorDataReceived += (sender, e) =>
            {
                if (e.Data != null)
                {
                    Result.OutputItems.Add(new ProcessOutputItem
                    {
                        IsError = true,
                        Text = e.Data
                    });
                }
            };
            process.BeginOutputReadLine();
            process.BeginErrorReadLine();

            CancellationTokenRegistration? reg=null;
            try
            {
                reg = stoppingToken.Register(() =>
                {
                    try
                    {
                        process.Kill();
                    }
                    catch (InvalidOperationException e) {
                    }
                });
                await process.WaitForExitAsync(stoppingToken);
                stoppingToken.ThrowIfCancellationRequested();
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
                reg?.Unregister();
                process.WaitForExit();
                Result.ExitCode = process.ExitCode;
            }
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
