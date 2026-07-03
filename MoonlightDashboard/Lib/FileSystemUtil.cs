using System.Diagnostics;
using System.Text.RegularExpressions;

namespace MoonlightDashboard.Lib
{
    public static class FileSystemUtil
    {
        /// <summary>
        /// Creates a directory path (including all subdirectories) and sets the ownership of the newly created folders.
        /// </summary>
        public static void CreateDirectoryWithOwner(string path, string user, string? group = null)
        {
            if (string.IsNullOrWhiteSpace(path))
            {
                throw new ArgumentException("Path cannot be null or empty.", nameof(path));
            }

            // Find the highest-level directory in the path that DOES NOT exist yet.
            // This ensures we only chown the folders we actually created.
            string? firstNewDirectory = FindFirstNonExistentParent(path);

            // Create the directory tree using standard .NET methods
            Directory.CreateDirectory(path);

            // If we actually created new directories, apply the ownership recursively
            if (firstNewDirectory != null)
            {
                // recursively change ownership of created folders
                Chown(firstNewDirectory, user, group, true);
            }
        }

        private static string? FindFirstNonExistentParent(string path)
        {
            var directoryInfo = new DirectoryInfo(path);
            string? highestNewDir = null;

            // Walk up the tree until we find a directory that already exists
            while (directoryInfo != null && !directoryInfo.Exists)
            {
                highestNewDir = directoryInfo.FullName;
                directoryInfo = directoryInfo.Parent;
            }

            return highestNewDir;
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
    }
}
