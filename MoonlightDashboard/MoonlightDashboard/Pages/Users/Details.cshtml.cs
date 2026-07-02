using AspNetCoreGeneratedDocument;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Internal;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Pages.Users
{
    public class DetailsModel : PageModel
    {
        private DatabaseContext db;
        public new User User { get; set; } = null!;
        public string Permissions = "";
        public string? Error => this.GetError();
        public DetailsModel(DatabaseContext db)
        {
            this.db = db;
        }

        private void LoadUser(string id)
        {
            User = db.Users.First(u => u.Id == id);
        }

        public void OnGet(string id)
        {
            LoadUser(id);
            Permissions = string.Join(", ", db.UserPermissions.Where(x => x.UserId == id).Join(db.Permissions, up => up.PermissionId, p => p.Id, (up, p) => p.Name));
        }

        public IActionResult OnPostSetPermissions(string id, string permissions)
        {
            try
            {
                LoadUser(id);
                var perms = permissions.Split(',').Select(p => p.Trim()).Where(p => !string.IsNullOrEmpty(p)).ToList();
                Lib.Permissions.SetUserPermissions(db, User, perms);
                db.SaveChanges();
            }
            catch(Exception ex)
            {
                this.SetError(ex.Message);
            }
            return RedirectToPage();
        }

        public IActionResult OnPostActivate(string id)
        {
            LoadUser(id);
            User.ActivationTimestamp = DateTime.UtcNow;
            db.SaveChanges();
            return RedirectToPage();
        }

        public IActionResult OnPostDelete(string id)
        {
            LoadUser(id);
            db.UserPermissions.RemoveRange(db.UserPermissions.Where(x => x.UserId == id));
            db.Users.Remove(User);
            db.SaveChanges();
            return LocalRedirect("/Users");
        }
    }
}
