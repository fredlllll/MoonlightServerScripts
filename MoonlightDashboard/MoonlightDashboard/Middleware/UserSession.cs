using System.Globalization;

namespace MoonlightDashboard.Middleware
{

    public class UserSession
    {
        private readonly RequestDelegate _next;

        public UserSession(RequestDelegate next)
        {
            _next = next;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            context.Items["User"] = null;
            context.Items["Session"] = null;
            context.Items["HasPermission"] = (string _) => { return false; };

            using var db = context.RequestServices.GetRequiredService<Database.DatabaseContext>();
            var sentSessionId = context.Request.Cookies["sessionid"];
            if(!string.IsNullOrEmpty(sentSessionId))
            {
                var session = db.Sessions.FirstOrDefault(s => s.Id == sentSessionId);
                if(session != null)
                {
                    var user = db.Users.FirstOrDefault(u => u.Id == session.UserId);
                    if (user != null)
                    {
                        context.Items["Session"] = session;
                        context.Items["User"] = user;
                        context.Items["HasPermission"] = (string permission) =>
                        {
                            var userPermissions = db.UserPermissions
                            .Where(up => up.UserId == user.Id)
                            .Join(db.Permissions, up => up.PermissionId, p => p.Id, (up, p) => p.Name).ToList();
                            return userPermissions.Contains(permission, StringComparer.OrdinalIgnoreCase);
                        };
                    }
                }
            }
            
            await _next(context);
        }
    }

    public static class UserSessionExtensions
    {
        public static IApplicationBuilder UseUserSessions(
            this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<UserSession>();
        }
    }

}
