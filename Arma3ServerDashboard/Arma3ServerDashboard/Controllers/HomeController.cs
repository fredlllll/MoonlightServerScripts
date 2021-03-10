using Arma3ServerDashboard.Data;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Arma3ServerDashboard.Controllers
{
    public class HomeController : Controller
    {
        private readonly DashboardDbContext dbContext;

        public HomeController(DashboardDbContext dbContext)
        {
            this.dbContext = dbContext;
        }
        
        public IActionResult Index()
        {
            ViewData["Title"] = "dis a title";
            ViewData["Users"] = dbContext.Users.All(x => true);

            return View();
        }
    }
}
