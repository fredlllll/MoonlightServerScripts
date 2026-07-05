using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Steam.Local;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Pages
{
    public class MaintenanceModel : PageModel
    {
        public void OnGet()
        {
        }

        public IActionResult OnPostDeleteModsAcfFile()
        {
            System.IO.File.Delete(Steam.GetArmaWorkshopAcfPath());
            this.SetInfo("Mods ACF file deleted successfully.");
            return RedirectToPage();
        }

        public IActionResult OnPostInstallSteamCmd()
        {
            Util.BashExecute("useradd -m -s /bin/bash steam");
            Util.BashExecute("add-apt-repository -y multiverse");
            Util.BashExecute("dpkg --add-architecture i386");
            Util.BashExecute("apt update");
            Util.BashExecute("apt install -y steamcmd");
            this.SetInfo("Steam CMD installed successfully.");
            return RedirectToPage();
        }
    }
}
