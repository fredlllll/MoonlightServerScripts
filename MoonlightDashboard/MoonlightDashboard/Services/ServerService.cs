using Microsoft.AspNetCore.Hosting.Server;
using MoonlightDashboard.Apis.Arma3;
using MoonlightDashboard.Apis.SystemD;
using MoonlightDashboard.Database;

namespace MoonlightDashboard.Services
{
    public class ServerService
    {
        private DatabaseContext db;

        public ServerService(DatabaseContext db)
        {
            this.db = db;
        }

        public async Task Start(string id)
        {
            var server = db.Arma3Servers.First(s => s.Id == id);
            var serverApi = new Arma3ServerApi(id);
            var serverUnit = new SystemDUnit(id);
            await serverApi.LinkMods(server, db);
            await serverApi.CreateStartupScript(server, db);
            serverUnit.Start();
        }

        public void Stop(string id)
        {
            var server = db.Arma3Servers.First(s => s.Id == id);
            var serverUnit = new SystemDUnit(id);
            serverUnit.Stop();
        }

        public async Task Restart(string id)
        {
            var server = db.Arma3Servers.First(s => s.Id == id);
            var serverApi = new Arma3ServerApi(id);
            var serverUnit = new SystemDUnit(id);
            serverUnit.Stop();
            await serverApi.LinkMods(server, db);
            await serverApi.CreateStartupScript(server, db);
            serverUnit.Start();
        }

        public void Enable(string id)
        {
            var server = db.Arma3Servers.First(s => s.Id == id);
            var serverUnit = new SystemDUnit(id);
            serverUnit.Enable();
        }

        public void Disable(string id)
        {
            var server = db.Arma3Servers.First(s => s.Id == id);
            var serverUnit = new SystemDUnit(id);
            serverUnit.Disable();
        }

        public void Delete(string id)
        {
            var Server = db.Arma3Servers.First(s => s.Id == id);
            var ServerUnit = new SystemDUnit(id);
            ServerUnit.Stop();
            ServerUnit.Disable();
            var ServerApi = new Arma3ServerApi(id);
            System.IO.File.Delete(ServerApi.GetSystemDUnitFilePath());
            System.IO.File.Delete(ServerApi.GetStartupScriptFilePath());
            System.IO.File.Delete(ServerApi.GetBasicConfigFilePath());
            System.IO.File.Delete(ServerApi.GetServerConfigFilePath());
            System.IO.File.Delete(ServerApi.GetServerProfileFilePath());
            db.Arma3Servers.Remove(Server);
            db.Arma3ServerCreatorDlcs.RemoveRange(db.Arma3ServerCreatorDlcs.Where(x => x.Arma3ServerId == id));
            db.SaveChanges();
        }
    }
}
