using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Steam.Local;
using MoonlightDashboard.Filters;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Pages
{
    [LoggedIn]
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
            //accept steams license agreement before installing steamcmd, otherwise it will silently fail
            Util.DebconfSetSelections(
                "steam steam/license note ",
                "steam steam/question select I AGREE");
            Util.BashExecute("apt install -y steamcmd", new Dictionary<string, string?> { { "DEBIAN_FRONTEND", "noninteractive" } });
            this.SetInfo("Steam CMD installed successfully.");
            return RedirectToPage();
        }
    }
}
