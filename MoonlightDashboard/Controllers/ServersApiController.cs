using Microsoft.AspNetCore.Mvc;
using MoonlightDashboard.Database;
using MoonlightDashboard.ServerLogs;
using MoonlightDashboard.Services;

namespace MoonlightDashboard.Controllers
{
    [ApiController]
    [Route("api/servers")]
    public class ServersApiController : ControllerBase
    {

        private readonly ServerService _serverService;
        private readonly SystemdLogChannelManager _logChannelManager;
        private readonly DatabaseContext _db;

        public ServersApiController(ServerService serverService, SystemdLogChannelManager logChannelManager, DatabaseContext db)
        {
            _serverService = serverService;
            _logChannelManager = logChannelManager;
            _db = db;
        }

        [HttpPost("{id}")]
        public async Task<IActionResult> HandleAction([FromRoute] string id, [FromForm] string actionName, [FromForm] string returnUrl)
        {
            switch (actionName.ToLower())
            {
                case "start":
                    await _serverService.Start(id);
                    break;
                case "stop":
                    _serverService.Stop(id);
                    break;
                case "restart":
                    await _serverService.Restart(id);
                    break;
                case "enable":
                    _serverService.Enable(id);
                    break;
                case "disable":
                    _serverService.Disable(id);
                    break;
                case "delete":
                    _serverService.Delete(id);
                    if (returnUrl.Contains(id)) //from details page, we cant return there after delete
                    {
                        return LocalRedirect("/Servers");
                    }
                    break;
                default: return BadRequest("Unknown action");
            }

            if (!string.IsNullOrEmpty(returnUrl) && Url.IsLocalUrl(returnUrl))
            {
                return LocalRedirect(returnUrl);
            }
            return LocalRedirect("/");
        }

        [HttpGet("{id}/ws")]
        public async Task GetLogStream(string id)
        {
            var server = _db.Arma3Servers.FirstOrDefault(s => s.Id == id) ?? throw new Exception("Server not found");
            if (HttpContext.WebSockets.IsWebSocketRequest)
            {
                // Accept the incoming socket connection
                using var webSocket = await HttpContext.WebSockets.AcceptWebSocketAsync();
                var connectionId = Guid.NewGuid();

                // Pass execution to the manager to stream the journalctl output
                await _logChannelManager.SubscribeAsync(server.Id, connectionId, webSocket, HttpContext.RequestAborted);
            }
            else
            {
                // Fallback if someone hits the endpoint with a normal browser HTTP GET
                HttpContext.Response.StatusCode = StatusCodes.Status400BadRequest;
            }
        }

    }
}
