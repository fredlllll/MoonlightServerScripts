using Arma3ServerDashboard.Data;
using Arma3ServerDashboard.Models;
using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Arma3ServerDashboard.Middlewares
{
    public class MyAuthentication
    {
        
        private readonly RequestDelegate _next;
        private readonly DashboardDbContext dbContext;

        public MyAuthentication(RequestDelegate next, DashboardDbContext dbContext)
        {
            _next = next;
            this.dbContext = dbContext;
        }

        public async Task InvokeAsync(HttpContext context)
        {
            int? userId = context.Session.GetInt32("userId");
            if (userId.HasValue)
            {
                context.Items["user"] = dbContext.Users.Find(userId);
            }

            // Call the next delegate/middleware in the pipeline
            await _next(context);
        }
    }
}
