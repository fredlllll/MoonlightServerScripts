using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;

namespace MoonlightDashboard.Lib
{
    public static class Permissions
    {
        public static IEnumerable<string> GetUserPermissions(DatabaseContext db, User user)
        {
            return db.UserPermissions
             .Where(up => up.UserId == user.Id)
             .Join(db.Permissions, up => up.PermissionId, p => p.Id, (up, p) => p.Name);
        }

        public static void SetUserPermissions(DatabaseContext db, User user, IEnumerable<string> permissions)
        {
            var perms = db.Permissions.Where(p => permissions.Contains(p.Name)).ToList();
            var existingPerms = db.UserPermissions.Where(up => up.UserId == user.Id).ToList();
            // Remove permissions that are not in the new list
            foreach (var up in existingPerms)
            {
                if (!perms.Any(p => p.Id == up.PermissionId))
                {
                    db.UserPermissions.Remove(up);
                }
            }
            // Add new permissions
            foreach (var perm in perms)
            {
                if (!existingPerms.Any(up => up.PermissionId == perm.Id))
                {
                    db.UserPermissions.Add(new UserPermission
                    {
                        Id = Util.GetNewId<UserPermission>(),
                        UserId = user.Id,
                        PermissionId = perm.Id
                    });
                }
            }
        }
    }
}
