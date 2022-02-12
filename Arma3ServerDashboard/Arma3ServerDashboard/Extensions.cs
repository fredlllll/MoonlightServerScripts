using Arma3ServerDashboard.Models;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Arma3ServerDashboard
{
    public static class Extensions
    {
        public static User GetUser(this HttpContext ctx)
        {
            if (ctx.Items.TryGetValue("user", out object val))
            {
                return val as User;
            }
            return null;
        }
    }
}
