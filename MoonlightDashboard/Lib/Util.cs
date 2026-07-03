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
            processInfo.ArgumentList.Add(command);

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
