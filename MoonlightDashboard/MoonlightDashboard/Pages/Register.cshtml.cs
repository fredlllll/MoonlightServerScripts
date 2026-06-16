using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;
using System.Xml.Linq;

namespace MoonlightDashboard.Pages
{
    public class RegisterModel : PageModel
    {
        public string? Error { get; set; } = null;

        public void OnGet()
        {
        }

        public void OnPostRegister(string user, string password, string password1)
        {

            if (password != password1)
            {
                Error = "Passwords do not match.";
                return;
            }

            if (string.IsNullOrEmpty(user) || string.IsNullOrEmpty(password))
            {
                Error = "Username and password cannot be empty.";
                return;
            }

            using var db = HttpContext.RequestServices.GetRequiredService<Database.DatabaseContext>();
            if (db.Users.Any(u => u.Name == user))
            {
                Error = "Username is already taken.";
                return;
            }
            bool auto_activate = !db.Users.Any();// automatically activate the first user who registers

            var salt = PassHash.GenerateSalt();
            var hash = PassHash.HashPassword(password, salt);
            var usr = new User()
            {
                Id = Util.GetNewId<User>(),
                Name = user,
                PasswordHash = hash,
                PasswordSalt = salt,
                ActivationTimestamp = null,
            };
            if (auto_activate)
            {
                usr.ActivationTimestamp = DateTime.UtcNow;
                db.GiveUserPermission(usr, "admin");
            }
            db.SaveChanges();
            Response.Redirect("/login");
        }
    }
}
