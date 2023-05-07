using Microsoft.AspNetCore.Mvc;
using System.Net.WebSockets;
using System.Text;

namespace MoonlightDashboard.Endpoints.Websockets
{
    public class FrontendLib : ControllerBase
    {
        [HttpGet("/api/v1/frontendlib")]
        public async Task Get()
        {
            if (HttpContext.WebSockets.IsWebSocketRequest)
            {
                using var webSocket = await HttpContext.WebSockets.AcceptWebSocketAsync();
                if (webSocket != null)
                {
                    await Lib.Websockets.AddSocket(webSocket);
                    await SocketLoop(webSocket);
                    await Lib.Websockets.RemoveSocket(webSocket);
                }
            }
            else
            {
                HttpContext.Response.StatusCode = StatusCodes.Status400BadRequest;
            }
        }
        async Task SocketLoop(WebSocket webSocket)
        {
            var buffer = new byte[1024 * 4];
            var receiveResult = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
            byte[] message = Array.Empty<byte>();

            while (!receiveResult.CloseStatus.HasValue)
            {
                byte[] tmp = new byte[message.Length + receiveResult.Count];
                Array.Copy(message, tmp, message.Length);
                Array.Copy(buffer, 0, tmp, message.Length, receiveResult.Count);
                message = tmp;
                //await webSocket.SendAsync(new ArraySegment<byte>(buffer, 0, receiveResult.Count), receiveResult.MessageType, receiveResult.EndOfMessage, CancellationToken.None);
                if (receiveResult.EndOfMessage)
                {
                    await HandleMessage(message, receiveResult.MessageType);
                    message = Array.Empty<byte>();
                }

                receiveResult = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), CancellationToken.None);
            }

            await webSocket.CloseAsync(receiveResult.CloseStatus.Value, receiveResult.CloseStatusDescription, CancellationToken.None);
        }
        async Task HandleMessage(byte[] message, WebSocketMessageType messageType)
        {
            string text = Encoding.UTF8.GetString(message);

            //TODO: dont need this yet

            Console.WriteLine(text);
        }
    }
}
