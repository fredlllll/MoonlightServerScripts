using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Filters;
using MoonlightDashboard.Lib;
using MoonlightDashboard.Middleware;

namespace MoonlightDashboard.Pages
{
    [LoggedOut]
    public class LoginModel : PageModel
    {
        public string? Error=> this.GetError();

        public void OnGet()
        {
        }

        public IActionResult OnPostLogin(string user, string password)
        {
            var db = HttpContext.RequestServices.GetRequiredService<Database.DatabaseContext>();

            var userEntity = db.Users.FirstOrDefault(u => u.Name == user);
            if (userEntity == null ||
            userEntity.ActivationTimestamp == null ||
            !PassHash.VerifyPassword(password, userEntity.Password)
            )
            {
                this.SetError("Invalid username or password.");
                return RedirectToPage();
            }

            var session = new Session
            {
                Id = Util.GetNewId<Session>(),
                UserId = userEntity.Id
            };
            db.Sessions.Add(session);
            db.SaveChanges();

            Response.Cookies.Append(UserSession.cookieName, session.Id);
            return LocalRedirect("/");
        }
    }
}
