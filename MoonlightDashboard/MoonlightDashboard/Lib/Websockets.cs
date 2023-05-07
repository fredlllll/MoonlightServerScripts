using System.Net.WebSockets;
using System.Text;
using System.Text.Json;
using System.Text.Unicode;
using System.Threading.Channels;

namespace MoonlightDashboard.Lib
{
    public static class Websockets
    {
        static readonly List<WebSocket> websockets = new();
        static readonly SemaphoreSlim websocketsLock = new(1, 1);

        class ChannelBroadcastMessage
        {
            public string MessageType { get; } = "channel";
            public Dictionary<string, string> Payload { get; set; } = new Dictionary<string, string>();
        }

        public static async Task AddSocket(WebSocket websocket)
        {
            await websocketsLock.WaitAsync();
            try
            {
                websockets.Add(websocket);
            }
            finally { websocketsLock.Release(); }
        }

        public static async Task RemoveSocket(WebSocket websocket)
        {
            await websocketsLock.WaitAsync();
            try
            {
                websockets.Remove(websocket);
            }
            finally { websocketsLock.Release(); }
        }

        public static async Task BroadcastToChannel(string channel, string data)
        {
            ChannelBroadcastMessage msg = new();
            msg.Payload["channel"] = channel;
            msg.Payload["data"] = data;
            string msgString = JsonSerializer.Serialize(msg);
            byte[] msgBytes = Encoding.UTF8.GetBytes(msgString);
            await websocketsLock.WaitAsync();
            List<Task> tasks = new();
            try
            {
                foreach (var socket in websockets)
                {
                    //TODO: delete sockets that are closed or ignore them
                    tasks.Add(socket.SendAsync(msgBytes, WebSocketMessageType.Text, true, CancellationToken.None));
                }
            }
            finally
            {
                websocketsLock.Release();
            }
            await Task.WhenAll(tasks);
        }

        public static async Task CallFunction(int answerId, WebSocket websocket, string functionName, params object[] args)
        {
            //TODO: dont need this yet
        }
    }
}
