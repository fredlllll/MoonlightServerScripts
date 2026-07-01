using System.Diagnostics;
using System.Text.RegularExpressions;
using UUIDNext;

namespace MoonlightDashboard.Lib
{
    public static class Util
    {
        public static string ApplicationFolder { get; private set; }

        public static string GetApplicationFilePath(string subPath)
        {
            return Path.Join(ApplicationFolder, subPath);
        }

        static Util()
        {
            ApplicationFolder = Path.Join(Environment.GetFolderPath(Environment.SpecialFolder.LocalApplicationData), "YoutubeSubVideoManager");
            Directory.CreateDirectory(ApplicationFolder);
        }

        public static string GetNewId<T>()
        {
            var t = typeof(T);
            var typeId = t.Name.ToLower();
            var id = Uuid.NewDatabaseFriendly(UUIDNext.Database.SQLite);
            return $"{typeId}_{id}";
        }

        public static void Chown(string path, string user, string? group = null, bool recursive = false)
        {
            var psi = new ProcessStartInfo
            {
                FileName = "chown",
                UseShellExecute = false,
                CreateNoWindow = true
            };

            if (recursive)
            {
                psi.ArgumentList.Add("-R");
            }
            psi.ArgumentList.Add("--no-dereference");
            if (group != null)
            {
                psi.ArgumentList.Add($"{user}:{group}");
            }
            else
            {
                psi.ArgumentList.Add(user);
            }
            psi.ArgumentList.Add(path);


            using (var process = Process.Start(psi))
            {
                if (process == null)
                {
                    throw new Exception("could not start chown");
                }
                process.WaitForExit();
                if (process.ExitCode != 0)
                {
                    throw new UnauthorizedAccessException("Failed to change ownership. Ensure you have sudo/root privileges.");
                }
            }
        }

        static Regex invalidFolderCharsRegex = new Regex($"[{Regex.Escape(new string(Path.GetInvalidFileNameChars()) + new string(Path.GetInvalidPathChars()))}]");

        public static string SanitizeFolderName(string name)
        {
            return invalidFolderCharsRegex.Replace(name, "-");
        }

        public static (string output, string error) BashExecute(string command)
        {
            var processInfo = new ProcessStartInfo
            {
                FileName = "/bin/bash",
                RedirectStandardOutput = true,
                RedirectStandardError = true,
                UseShellExecute = false,
                CreateNoWindow = true
            };
            processInfo.ArgumentList.Add("-c");
            processInfo.Arguments = command;

            var process = Process.Start(processInfo);
            if (process == null)
            {
                throw new Exception("Failed to start bash process.");
            }
            using (process)
            {
                process.WaitForExit();

                string output = process.StandardOutput.ReadToEnd();
                string error = process.StandardError.ReadToEnd();
                return (output, error);
            }
        }
    }
}
