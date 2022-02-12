using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Arma3ServerDashboard.Middlewares
{
    public static class MiddlewareExtensions
    {
        public static IApplicationBuilder UseMyAuth(this IApplicationBuilder builder)
        {
            return builder.UseMiddleware<MyAuthentication>();
        }

        public static bool IsLoggedIn(this HttpContext context)
        {
            return false; //TODO
        }
    }
}
