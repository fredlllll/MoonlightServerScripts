using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Pages.Users
{
    public class DetailsModel : PageModel
    {
        private DatabaseContext db;
        public new User User { get; set; } = null!;
        public string? Error { get; set; } = null;
        public DetailsModel(DatabaseContext db)
        {
            this.db = db;
        }

        private void LoadUser(string id)
        {
            User = db.Users.FirstOrDefault(u => u.Id == id) ?? throw new Exception("User not found");
        }

        public void OnGet(string id)
        {
            LoadUser(id);
        }

        public void OnPostSetPermissions(string id, string permissions)
        {
            LoadUser(id);
            var perms = permissions.Split(',').Select(p => p.Trim()).Where(p => !string.IsNullOrEmpty(p)).ToList();
            Permissions.SetUserPermissions(db, User, perms);
            db.SaveChanges();
        }

        public void OnPostActivate(string id)
        {
            LoadUser(id);
            User.ActivationTimestamp = DateTime.UtcNow;
            db.SaveChanges();
        }

        public void OnPostDelete(string id)
        {
            LoadUser(id);
            db.Users.Remove(User);
            db.SaveChanges();
            Response.Redirect("/Users");
        }
    }
}
