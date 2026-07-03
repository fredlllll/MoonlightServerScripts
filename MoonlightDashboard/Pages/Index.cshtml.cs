using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using MoonlightDashboard.Apis.Arma3;
using MoonlightDashboard.Apis.SystemD;
using MoonlightDashboard.Database;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Filters;

namespace MoonlightDashboard.Pages
{
    [LoggedIn]
    public class IndexModel : PageModel
    {
        public IEnumerable<Arma3Server> Servers = Enumerable.Empty<Arma3Server>();
        public Dictionary<string, SystemDUnit> SystemDUnits = new();
        public Dictionary<string, SystemDUnitInfo> ServerUnitInfos = new();
        public Dictionary<string, Arma3ServerApi> ServerApis = new();
        public Dictionary<string, Arma3ServerRuntimeInfo?> ServerRuntimeInfos = new();

        private DatabaseContext db;
        public IndexModel(DatabaseContext db)
        {
            this.db = db;
        }
        public void OnGet()
        {
            Servers = db.Arma3Servers;
            foreach (var server in Servers)
            {
                var unit = new SystemDUnit(server.Id);
                SystemDUnits[server.Id] = unit;
                ServerUnitInfos[server.Id] = unit.GetInfo();
                var api = ServerApis[server.Id] = new Arma3ServerApi(server.Id);
                ServerRuntimeInfos[server.Id] = api.GetRuntimeInfo(server);
            }
        }
    }
}
