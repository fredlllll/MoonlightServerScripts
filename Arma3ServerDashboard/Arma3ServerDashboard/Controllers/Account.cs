using Arma3ServerDashboard.Data;
using Arma3ServerDashboard.Models;
using Arma3ServerDashboard.Util;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace Arma3ServerDashboard.Controllers
{
    public class Account : Controller
    {
        private readonly DashboardDbContext dbContext;

        public Account(DashboardDbContext dbContext)
        {
            this.dbContext = dbContext;
        }

        public IActionResult Index() //Login/signup
        {
            ViewData["Title"] = "Login / Signup";
            return View();
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Login(string user, string password)
        {
            return Redirect("/");
        }

        [HttpPost]
        [ValidateAntiForgeryToken]
        public IActionResult Register(string user, string password, string password1)
        {
            ViewData["Title"] = "Login / Signup";

            if (password != password1)
            {
                ViewData["error"] = "Passwords didnt match";
                return View("Index");
            }

            if(password == null || password.Length < 6)
            {
                ViewData["error"] = "Password has to be at least 6 characters long";
                return View("Index");
            }

            if(user == null || user.Length < 3)
            {
                ViewData["error"] = "User has to be at least 3 characters long";
                return View("Index");
            }

            if (dbContext.Users.Where(x => x.Name == user).Count() > 0)
            {
                ViewData["error"] = "User already exists";
                return View("Index");
            }

            var u = new User();

            u.Name = user;
            u.Password = PasswordHasher.Hash(password);

            HttpContext.Session.SetString("userId", u.Id.ToString(System.Globalization.CultureInfo.InvariantCulture));

            dbContext.Users.Add(u);
            dbContext.SaveChanges();
            return Redirect("/");
        }

        public IActionResult Logout()
        {
            HttpContext.Session.Clear();
            ViewData["Title"] = "Logout";
            return View();
        }

        public IActionResult AccessDenied()
        {
            ViewData["Title"] = "Access Denied";
            return View();
        }
    }
}
