using MoonlightDashboard.Lib;
using System.Diagnostics;
using System.Linq;

namespace MoonlightDashboard.Apis.SystemD
{
    public class SystemDUnit
    {
        private string name;
        public SystemDUnit(string name)
        {
            this.name = name;
        }

        public void Enable()
        {
            SystemDUtil.SystemCtl("enable", name).WaitForExit();
        }

        public void Disable()
        {
            SystemDUtil.SystemCtl("disable", name).WaitForExit();
        }

        public void Start()
        {
            SystemDUtil.SystemCtl("start", name).WaitForExit();
        }

        public void Stop()
        {
            SystemDUtil.SystemCtl("stop", name).WaitForExit();
        }

        public SystemDUnitInfo GetInfo()
        {
            using var p = SystemDUtil.SystemCtl(true, "show", name, "--no-page");
            Dictionary<string, string> data = new Dictionary<string, string>();
            while (!p.HasExited)
            {
                var line = p.StandardOutput.ReadLine();
                if (line == null)
                {
                    break;
                }
                var parts = line.Split('=', 2);
                data[parts[0]] = parts[1];
            }
            return PropertyMapper.MapFromDictionary<SystemDUnitInfo>(data);
        }

        public string GetLog(int lines)
        {
            return SystemDUtil.JournalCtl("-u", name, "-n", lines.ToString(), "--no-pager").StandardOutput.ReadToEnd();
        }
    }
}
