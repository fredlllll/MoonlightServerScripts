using Microsoft.AspNetCore.Components;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Arma3ServerDashboard.Handlers
{
    [Route("/")]
    public class Home
    {
        public static async Task Get(HttpContext context)
        {
            context.Response.Headers["Content-Type"] = "text/html";
            await context.Response.WriteAsync("<i> AAAAAa </i>");
        }
    }
}
