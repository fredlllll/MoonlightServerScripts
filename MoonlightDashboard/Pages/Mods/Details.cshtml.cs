using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Filters;

namespace MoonlightDashboard.Pages.Mods
{
    [LoggedIn]
    public class DetailsModel : PageModel
    {
        public void OnGet()
        {
        }
    }
}
