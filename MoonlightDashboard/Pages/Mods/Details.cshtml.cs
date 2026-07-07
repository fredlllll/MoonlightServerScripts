using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Steam.Local;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Filters;

namespace MoonlightDashboard.Pages.Mods
{
    [LoggedIn]
    public class DetailsModel : PageModel
    {
        private readonly DatabaseContext _db;
        public ModInfo Info = null!;

        public DetailsModel(DatabaseContext db)
        {
            this._db = db;
        }

        public async Task OnGet(string id)
        {
            Info = await Apis.Steam.Local.Mods.GetModInfo(_db, id);
        }

        public IActionResult OnPostUpdate(string id, string name)
        {
            Info = _db.ModInfos.First(x => x.ModId == id);
            Info.IsManuallyNamed = Info.Name != name;
            Info.Name = name;
            _db.SaveChanges();
            return RedirectToPage();
        }

    }
}
