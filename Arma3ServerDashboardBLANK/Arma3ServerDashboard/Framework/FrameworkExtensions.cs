using Microsoft.AspNetCore.Routing;
using Microsoft.AspNetCore.Builder;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Reflection;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Components;

namespace Arma3ServerDashboard.Framework
{
    public static class FrameworkExtensions
    {
        static string[] HTTPMethods = new string[]
        {
            "Get",
            //"Head",
            "Post",
            "Put",
            "Delete",
            //"Connect",
            //"Options",
            //"Trace",
            //"Patch"
        };

        public static void MapHandler(this IEndpointRouteBuilder me, Type handlerType)
        {
            Type[] args = new Type[] { typeof(HttpContext) };

            RouteAttribute route = handlerType.GetCustomAttribute(typeof(RouteAttribute)) as RouteAttribute;
            if (route == null)
            {
                throw new Exception("No Route attribute ( Microsoft.AspNetCore.Components ) found");
            }

            foreach (var m in HTTPMethods)
            {
                //(string name, BindingFlags bindingAttr, Binder? binder, Type[] types, ParameterModifier[]? modifiers);
                var method = handlerType.GetMethod(m, BindingFlags.Public | BindingFlags.Static, null, args, null);
                if (method != null)
                {
                    RequestDelegate del = (RequestDelegate)Delegate.CreateDelegate(typeof(RequestDelegate), method);
                    switch (m)
                    {
                        case "Get":
                            me.MapGet(route.Template, del);
                            break;
                        case "Post":
                            me.MapPost(route.Template, del);
                            break;
                        case "Put":
                            me.MapPut(route.Template, del);
                            break;
                        case "Delete":
                            me.MapDelete(route.Template, del);
                            break;
                    }
                }
            }
        }
    }
}
