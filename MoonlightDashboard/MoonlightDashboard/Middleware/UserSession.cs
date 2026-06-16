using MoonlightDashboard.Lib;

namespace MoonlightDashboard.Middleware
{

    public class UserSession
    {
        public const string cookieName = "sessionid";

        private readonly RequestDelegate _next;

        public UserSession(RequestDelegate next)
        {
            _next = next;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            context.SetCurrentSession(null);
            context.SetCurrentUser(null);

            using var db = context.RequestServices.GetRequiredService<Database.DatabaseContext>();
            var sentSessionId = context.Request.Cookies[cookieName];
            if(!string.IsNullOrEmpty(sentSessionId))
            {
                var session = db.Sessions.FirstOrDefault(s => s.Id == sentSessionId);
                if(session != null)
                {
                    var user = db.Users.FirstOrDefault(u => u.Id == session.UserId);
                    if (user != null)
                    {
                        context.SetCurrentSession(session);
                        context.SetCurrentUser(user);
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
