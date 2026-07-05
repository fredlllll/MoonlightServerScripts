using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Filters;
using MoonlightDashboard.Lib;
using System.Xml.Linq;

namespace MoonlightDashboard.Pages
{
    [LoggedOut]
    public class RegisterModel : PageModel
    {
        public string? Error => this.GetError();

        public void OnGet()
        {
        }

        public IActionResult OnPostRegister(string user, string password, string password1)
        {

            if (password != password1)
            {
                this.SetError("Passwords do not match.");
                return RedirectToPage();
            }

            if (string.IsNullOrEmpty(user) || string.IsNullOrEmpty(password))
            {
                this.SetError("Username and password cannot be empty.");
                return RedirectToPage();
            }

            var db = HttpContext.RequestServices.GetRequiredService<Database.DatabaseContext>();
            if (db.Users.Any(u => u.Name == user))
            {
                this.SetError("Username is already taken.");
                return RedirectToPage();
            }
            bool auto_activate = !db.Users.Any();// automatically activate the first user who registers

            var hash = PassHash.HashPassword(password);
            var usr = new User()
            {
                Id = Util.GetNewId<User>(),
                Name = user,
                Password = hash,
                ActivationTimestamp = null,
            };
            db.Users.Add(usr);
            if (auto_activate)
            {
                usr.ActivationTimestamp = DateTime.UtcNow;
                db.GiveUserPermission(usr, "admin");
            }
            db.SaveChanges();
            return LocalRedirect("/login");
        }
    }
}
