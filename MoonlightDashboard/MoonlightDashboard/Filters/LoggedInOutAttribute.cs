using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Filters;
using MoonlightDashboard.Lib;


namespace MoonlightDashboard.Filters
{
    public class LoggedInAttribute : Attribute, IPageFilter
    {
        public void OnPageHandlerSelected(PageHandlerSelectedContext context)
        {
            
        }

        public void OnPageHandlerExecuting(PageHandlerExecutingContext context)
        {
            if (!context.HttpContext.IsLoggedIn())
            {
                context.Result = new RedirectToPageResult("/Login");
            }
        }

        public void OnPageHandlerExecuted(PageHandlerExecutedContext context)
        {
           
        }
    }

    public class LoggedOutAttribute : Attribute, IPageFilter
    {
        public void OnPageHandlerSelected(PageHandlerSelectedContext context)
        {

        }

        public void OnPageHandlerExecuting(PageHandlerExecutingContext context)
        {
            if (context.HttpContext.IsLoggedIn())
            {
                context.Result = new RedirectToPageResult("/");
            }
        }

        public void OnPageHandlerExecuted(PageHandlerExecutedContext context)
        {

        }
    }
}
