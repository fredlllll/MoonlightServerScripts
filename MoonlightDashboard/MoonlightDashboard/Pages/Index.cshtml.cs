using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Filters;

namespace MoonlightDashboard.Pages
{
    [LoggedIn]
    public class IndexModel : PageModel
    {
        public void OnGet()
        {
        }
    }
}
