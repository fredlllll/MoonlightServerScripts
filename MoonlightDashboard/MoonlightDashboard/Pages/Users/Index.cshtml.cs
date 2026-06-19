using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Pages.Users
{
    public class IndexModel : PageModel
    {
        private DatabaseContext db;
        public IEnumerable<User> Users { get; private set; }  = Enumerable.Empty<User>();
        public Dictionary<string, string> UserPermissions { get; } = new Dictionary<string, string>();
        public IndexModel(DatabaseContext db)
        {
            this.db = db;
        }

        public void OnGet()
        {
            Users = db.Users.ToList();
            foreach (var user in Users)
            {
                var permissions = Permissions.GetUserPermissions(db, user).ToList();
                UserPermissions[user.Id] = string.Join(", ", permissions);
            }
        }
    }
}
