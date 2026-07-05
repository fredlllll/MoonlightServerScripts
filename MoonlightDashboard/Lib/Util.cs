using System.Diagnostics;
using System.Text.RegularExpressions;
using UUIDNext;

namespace MoonlightDashboard.Lib
{
    public static class Util
    {
        public static string GetNewId<T>()
        {
            var t = typeof(T);
            var typeId = t.Name.ToLower();
            var id = Uuid.NewDatabaseFriendly(UUIDNext.Database.SQLite);
            return $"{typeId}_{id}";
        }

        public static (string output, string error) BashExecute(string command, Dictionary<string, string?>? envVars = null)
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
            processInfo.ArgumentList.Add(command);
            if (envVars != null)
            {
                foreach (var kvp in envVars)
                {
                    if (kvp.Value != null)
                    {
                        processInfo.Environment[kvp.Key] = kvp.Value;
                    }
                }
            }

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

        public static void DebconfSetSelections(params string[] commands)
        {
            var processInfo = new ProcessStartInfo
            {
                FileName = "debconf-set-selections",
                UseShellExecute = false,
                RedirectStandardInput = true,
                CreateNoWindow = true
            };
            processInfo.ArgumentList.Add("-v");
            var process = Process.Start(processInfo);
            if (process == null)
            {
                throw new Exception("Failed to start debconf-set-selections process.");
            }
            using (process)
            {
                //using will close stream
                using (var writer = process.StandardInput)
                {
                    foreach (var command in commands)
                    {
                        writer.Write(command + "\n");
                    }
                }
                process.WaitForExit();
            }
        }

        public static void DebconfCommunicate(string owner, params string[] commands)
        {
            var processInfo = new ProcessStartInfo
            {
                FileName = "debconf-communicate",
                UseShellExecute = false,
                RedirectStandardInput = true,
                CreateNoWindow = true
            };
            processInfo.ArgumentList.Add(owner);

            var process = Process.Start(processInfo);
            if (process == null)
            {
                throw new Exception("Failed to start debconf-communicate process.");
            }
            using (process)
            {
                //using will close stream
                using (var writer = process.StandardInput)
                {
                    foreach (var command in commands)
                    {
                        writer.Write(command + "\n");
                    }
                    writer.Write("quit\n");
                }
                process.WaitForExit();
            }
        }
    }
}
