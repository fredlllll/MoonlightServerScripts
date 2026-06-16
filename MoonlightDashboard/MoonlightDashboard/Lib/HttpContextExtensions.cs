using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;

namespace MoonlightDashboard.Lib
{
    public static class HttpContextExtensions
    {
        public static bool HasPermission(this HttpContext context, string permission)
        {
            using var db = context.RequestServices.GetRequiredService<DatabaseContext>();

            var user = context.GetCurrentUser();
            if (user == null)
            {
                return false;
            }

            var userPermissions = db.UserPermissions
                            .Where(up => up.UserId == user.Id)
                            .Join(db.Permissions, up => up.PermissionId, p => p.Id, (up, p) => p.Name).ToList();
            return userPermissions.Contains(permission, StringComparer.OrdinalIgnoreCase);
        }

        public static User? GetCurrentUser(this HttpContext context)
        {
            return context.Items["User"] as User;
        }

        public static void SetCurrentUser(this HttpContext context, User? user)
        {
            context.Items["User"] = user;
        }

        public static Session? GetCurrentSession(this HttpContext context)
        {
            return context.Items["Session"] as Session;
        }

        public static void SetCurrentSession(this HttpContext context, Session? session)
        {
            context.Items["Session"] = session;
        }

        public static bool IsLoggedIn(this HttpContext context)
        {
            return context.GetCurrentUser() != null && context.GetCurrentSession() != null;
        }
    }
}
