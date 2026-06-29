using AspNetCoreGeneratedDocument;
using Microsoft.AspNetCore.Hosting.Server;
using Microsoft.Extensions.Logging;
using MoonlightDashboard.Apis.A2Sharp;
using MoonlightDashboard.Apis.Steam.Local;
using MoonlightDashboard.Apis.SystemD;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;
using System.Diagnostics;
using System.Linq;
using System.Net;
using System.Text;

namespace MoonlightDashboard.Apis.Arma3
{
    public class Arma3ServerApi
    {
        public string Id { get; }
        public Arma3ServerApi(string id)
        {
            Id = id;
        }

        public static string GetDefaultBasicConfigFilePath()
        {
            return Path.GetFullPath(Path.Combine("ArmaServerDefaultFiles", "basic.cfg"));
        }

        public static string GetDefaultServerConfigFilePath()
        {
            return Path.GetFullPath(Path.Combine("ArmaServerDefaultFiles", "server.cfg"));
        }
        public static string GetDefaultServerProfileFilePath()
        {
            return Path.GetFullPath(Path.Combine("ArmaServerDefaultFiles", "server.arma3profile"));
        }

        public string GetServerModsFolder()
        {
            return Path.Combine(Steam.Local.Steam.GetArma3ServerFolder(), "mods", Id);
        }

        public string GetSystemDUnitFilePath()
        {
            return Path.Combine("etc", "systemd", "system", Id + ".service");
        }

        public string GetStartupScriptFilePath()
        {
            return Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".moonlightdashboard", "startupscripts", Id + ".sh");
        }

        public string GetBasicConfigFilePath()
        {
            return Path.Combine(Steam.Local.Steam.GetArma3ServerFolder(), Id, "basic.cfg");
        }
        public string GetServerConfigFilePath()
        {
            return Path.Combine(Steam.Local.Steam.GetArma3ServerFolder(), Id, "server.cfg");
        }

        public string GetServerProfileFilePath()
        {
            // TODO: https://community.bistudio.com/wiki/Arma_3:_Dedicated_Server
            // TODO: The first time you run the server it will auto-create a profile file at
            // ~/.local/share/Arma 3 - Other Profiles/server/server.Arma3Profile. Edit this file to customise difficulty settings.
            // TODO: The -profiles= parameter is broken on Linux - you must place your profiles in this directory.
            // TODO: test if my changes are actually correct
            return Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".local", "share", "Arma 3 - Other Profiles", Id, "server.Arma3");
        }

        //TODO: make steam owner of files after copy from default

        public string GetBasicConfigFileContents()
        {
            var path = GetBasicConfigFilePath();
            if (!File.Exists(path))
            {
                File.Copy(GetDefaultBasicConfigFilePath(), path);
                Util.Chown(path, "steam", "steam");
            }
            return File.ReadAllText(path);
        }

        public string GetServerConfigFileContents()
        {
            var path = GetServerConfigFilePath();
            if (!File.Exists(path))
            {
                File.Copy(GetDefaultServerConfigFilePath(), path);
                Util.Chown(path, "steam", "steam");
            }
            return File.ReadAllText(path);
        }

        public string GetServerProfileFileContents()
        {
            var path = GetServerProfileFilePath();
            if (!File.Exists(path))
            {
                File.Copy(GetDefaultServerProfileFilePath(), path);
                Util.Chown(path, "steam", "steam");
            }
            return File.ReadAllText(path);
        }

        public void SetBasicConfigFileContents(string content)
        {
            var path = GetBasicConfigFilePath();
            File.WriteAllText(path, content);
        }

        public void SetServerConfigFileContents(string content)
        {
            var path = GetServerConfigFilePath();
            File.WriteAllText(path, content);
        }

        public void SetServerProfileFileContents(string content)
        {
            var path = GetServerProfileFilePath();
            File.WriteAllText(path, content);
        }

        public void ResetBasicConfigFileContents()
        {
            var path = GetBasicConfigFilePath();
            File.Copy(GetDefaultBasicConfigFilePath(), path, true);
            Util.Chown(path, "steam", "steam");
        }

        public void ResetServerConfigFileContents()
        {
            var path = GetServerConfigFilePath();
            File.Copy(GetDefaultServerConfigFilePath(), path, true);
            Util.Chown(path, "steam", "steam");
        }

        public void ResetServerProfileFileContents()
        {
            var path = GetServerProfileFilePath();
            File.Copy(GetDefaultServerProfileFilePath(), path, true);
            Util.Chown(path, "steam", "steam");
        }

        public async Task LinkMods(Arma3Server server, DatabaseContext db)
        {
            List<string> modIds = new List<string>();
            if (!string.IsNullOrWhiteSpace(server.ActiveModsetId))
            {
                modIds = db.Arma3ModsetMods.Where(x => x.ModsetId == server.ActiveModsetId).Select(x => x.ModSteamId).ToList();
            }

            var workshopModsFolder = Steam.Local.Mods.GetWorkshopModsFolder();
            var serverModsFolder = GetServerModsFolder();

            Directory.Delete(serverModsFolder, true);
            Directory.CreateDirectory(serverModsFolder);

            var modInfos = await Mods.GetModInfos(db, modIds);

            foreach (var mod in modInfos)
            {
                var modFolder = Steam.Local.Mods.GetModFolder(mod.ModId);
                var modName = mod.Name;
                var targetFolder = Path.Combine(serverModsFolder, $"@{Util.SanitizeFolderName(modName)}");
                Directory.CreateDirectory(targetFolder);
                var allFiles = Directory.EnumerateFiles(modFolder, "*", SearchOption.AllDirectories);
                foreach (var absFilePath in allFiles)
                {
                    // Get the path relative to the root mod folder
                    string relFilePath = Path.GetRelativePath(modFolder, absFilePath);
                    // Force the relative path to lowercase
                    string relFilePathLower = relFilePath.ToLowerInvariant();
                    // Combine with target folder to get the destination path
                    string absTargetFilePath = Path.Combine(targetFolder, relFilePathLower);
                    // Ensure the parent directory structure exists (automatically handles sub-dirs)
                    string? targetDir = Path.GetDirectoryName(absTargetFilePath);
                    if (targetDir != null)
                    {
                        Directory.CreateDirectory(targetDir);
                    }
                    // Create the file symlink
                    if (!File.Exists(absTargetFilePath))
                    {
                        File.CreateSymbolicLink(absTargetFilePath, absFilePath);
                    }
                }
            }
            Util.Chown(serverModsFolder, "steam", "steam", true);
        }

        public async Task CreateStartupScript(Arma3Server server, DatabaseContext db)
        {
            string fileName = GetStartupScriptFilePath();
            string arma3ServerDir = Steam.Local.Steam.GetArma3ServerFolder();
            string serverModsFolder = GetServerModsFolder();

            var sb = new StringBuilder();

            // Start building the bash script content
            sb.AppendLine("#!/bin/bash");
            sb.AppendLine($"cd \"{arma3ServerDir}\"");
            sb.Append($"./arma3server_x64 -cfg=basic.cfg -config=server.cfg -port={server.Port} -name={server.Id}");

            if (!string.IsNullOrEmpty(server.AdditionalCommandlineArgs))
            {
                sb.Append($" {server.AdditionalCommandlineArgs}");
            }

            sb.AppendLine(" -mod=\"\\");

            // Handle Modsets if they exist
            if (!string.IsNullOrEmpty(server.ActiveModsetId))
            {
                var modIds = db.Arma3ModsetMods.Where(x => x.ModsetId == server.ActiveModsetId).Select(x => x.ModSteamId).ToList();
                var modInfos = await Mods.GetModInfos(db, modIds);

                foreach (var modInfo in modInfos)
                {
                    var modName = modInfo.Name;
                    var absPath = Path.Combine(serverModsFolder, $"@{Util.SanitizeFolderName(modName)}");

                    // Get path relative to the executable directory
                    string relPath = Path.GetRelativePath(arma3ServerDir, absPath);
                    sb.AppendLine($"{relPath};\\");
                }
            }

            var serverCreatorDlcIds = db.Arma3ServerCreatorDlcs.Where(x => x.Arma3ServerId == Id).Select(x => x.Arma3CreatorDlcId);
            var creatorDlcs = db.Arma3CreatorDlcs.Where(x => serverCreatorDlcIds.Contains(x.Id));
            foreach (var dlc in creatorDlcs)
            {
                sb.AppendLine($"{dlc.ShortName};\\");
            }

            sb.Append('\"');

            // Write content to file
            File.WriteAllText(fileName, sb.ToString());

            Util.Chown(fileName, "steam", "steam");
        }

        public void CreateServiceFile(Arma3Server server)
        {
            string fileName = GetSystemDUnitFilePath();

            // Use a C# raw string literal ($"""...""") for clean, multi-line formatting
            string content = $"""
            [Unit]
            Description=Arma 3 Server

            [Service]
            User=steam
            Group=steam
            WorkingDirectory=/home/steam
            ExecStart=/bin/bash "{GetStartupScriptFilePath()}"
            Restart=always

            [Install]
            WantedBy=multi-user.target
            """;

            // Write the string to the file
            File.WriteAllText(fileName, content);

            SystemDUtil.SystemCtl("daemon-reload").WaitForExit();
        }

        public Arma3ServerRuntimeInfo GetRuntimeInfo(Arma3Server server)
        {
            var info = new Arma3ServerRuntimeInfo();

            var address = IPAddress.Loopback;
            var port = server.Port + 1;
            var a2sInfo = A2Sharp.A2Sharp.GetInfo(address, port, 300);
            var a2sPlayers = A2Sharp.A2Sharp.GetPlayers(address, port, 300);

            info.Name = a2sInfo.Name;
            info.Map = a2sInfo.Map;
            info.Players = a2sPlayers.Select(x => x.Name).ToList();
            info.Mission = a2sInfo.Game;
            info.MaxPlayers = a2sInfo.MaxPlayers;

            return info;
        }
    }
}
