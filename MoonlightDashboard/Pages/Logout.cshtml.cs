using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Filters;
using MoonlightDashboard.Lib;
using MoonlightDashboard.Middleware;

namespace MoonlightDashboard.Pages
{
    [LoggedIn]
    public class LogoutModel : PageModel
    {
        public void OnGet()
        {
            var session = HttpContext.GetCurrentSession();
            if (session != null)
            {
                var db = HttpContext.RequestServices.GetRequiredService<Database.DatabaseContext>();
                db.Sessions.Remove(session);
                db.SaveChanges();
                Response.Cookies.Delete(UserSession.cookieName);
            }
            Response.Redirect("/Login");
        }
    }
}
