using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Pages
{
    public class MaintenanceModel : PageModel
    {
        public void OnGet()
        {
        }

        public void OnPostDeleteModsAcfFile()
        {

        }

        private void LogBoth((string,string) a)
        {
            Console.WriteLine(a.Item1);
            Console.WriteLine(a.Item2);
        }

        public void OnPostInstallSteamCmd()
        {
            LogBoth(Util.BashExecute("useradd -m -s /bin/bash steam"));
            LogBoth(Util.BashExecute("add-apt-repository -y multiverse"));
            LogBoth(Util.BashExecute("dpkg --add-architecture i386"));
            LogBoth(Util.BashExecute("apt update"));
            LogBoth(Util.BashExecute("apt install -y steamcmd"));
            LogBoth(Util.BashExecute("apt upgrade -y steamcmd"));
        }
    }
}
