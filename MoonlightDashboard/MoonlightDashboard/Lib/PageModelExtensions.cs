using Microsoft.AspNetCore.Mvc.RazorPages;
using System.Runtime.CompilerServices;

namespace MoonlightDashboard.Lib
{
    public static class PageModelExtensions
    {
        public static void SetError(this PageModel pageModel, string error)
        {
            pageModel.TempData["Error"] = error;
        }
        public static string? GetError(this PageModel pageModel)
        {
            if (pageModel.TempData.ContainsKey("Error"))
            {
                return pageModel.TempData["Error"] as string;
            }
            return null;
        }
    }
}
