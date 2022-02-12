using Microsoft.AspNetCore.Routing;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Arma3ServerDashboard.Framework;
using Arma3ServerDashboard.Handlers;

namespace Arma3ServerDashboard
{
    public static class Routes
    {
        public static void AddEndpoints(IEndpointRouteBuilder endpoints)
        {
            endpoints.MapHandler(typeof(Home));
        }
    }
}
