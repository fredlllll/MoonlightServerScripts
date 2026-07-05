using Microsoft.AspNetCore.Mvc.RazorPages;

namespace MoonlightDashboard.Lib
{
    public static class PageModelExtensions
    {
        private static void SetTempData(this PageModel pageModel, string key, object value)
        {
            pageModel.TempData[key] = value;
        }

        private static object? GetTempData(this PageModel pageModel, string key)
        {
            if (pageModel.TempData.ContainsKey(key))
            {
                return pageModel.TempData[key];
            }
            return null;
        }

        public static void SetError(this PageModel pageModel, string error)
        {
            pageModel.SetTempData("Error", error);
        }
        public static string? GetError(this PageModel pageModel)
        {
            return pageModel.GetTempData("Error") as string;
        }

        public static void SetInfo(this PageModel pageModel, string info)
        {
            pageModel.SetTempData("Info", info);
        }
        public static string? GetInfo(this PageModel pageModel)
        {
            return pageModel.GetTempData("Info") as string;
        }
    }
}