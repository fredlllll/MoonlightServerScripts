using Microsoft.AspNetCore.Mvc;
using MoonlightDashboard.Services;

namespace MoonlightDashboard.Controllers
{
    [ApiController]
    [Route("api/servers")]
    public class ServersApiController : ControllerBase
    {

        private readonly ServerService _serverService;

        public ServersApiController(ServerService serverService)
        {
            _serverService = serverService;
        }

        [HttpPost("{id}/{actionName}")]
        public async Task<IActionResult> HandleAction([FromRoute] string id, [FromRoute] string actionName, [FromForm] string returnUrl)
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
    }
}
