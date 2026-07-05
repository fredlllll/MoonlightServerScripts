using System.Collections.Concurrent;
using System.Diagnostics;
using System.Net.WebSockets;
using System.Text;

namespace MoonlightDashboard.ServerLogs
{
    public class SystemdLogChannelManager
    {
        private sealed class ChannelContext
        {
            public int SubscriberCount;
            public CancellationTokenSource Cts = new();
            public Task? WatcherTask;
            public readonly ConcurrentDictionary<Guid, WebSocket> Sockets = new();
        }

        private readonly ConcurrentDictionary<string, ChannelContext> _channels = new();

        public async Task SubscribeAsync(string unitId, Guid connectionId, WebSocket webSocket, CancellationToken ct)
        {
            var channel = _channels.GetOrAdd(unitId, _ => new ChannelContext());

            lock (channel)
            {
                channel.Sockets[connectionId] = webSocket;
                channel.SubscriberCount++;

                if (channel.SubscriberCount == 1)
                {
                    // First subscriber: spin up the journalctl process
                    channel.Cts = new CancellationTokenSource();
                    channel.WatcherTask = Task.Run(() => StartJournalctlWatcher(unitId, channel), channel.Cts.Token);
                }
            }

            // Keep the connection alive until client disconnects
            var buffer = new byte[1024 * 4];
            try
            {
                while (webSocket.State == WebSocketState.Open)
                {
                    var result = await webSocket.ReceiveAsync(new ArraySegment<byte>(buffer), ct);
                    if (result.MessageType == WebSocketMessageType.Close) break;
                }
            }
            finally
            {
                await UnsubscribeAsync(unitId, connectionId);
            }
        }

        private async Task UnsubscribeAsync(string unitId, Guid connectionId)
        {
            if (!_channels.TryGetValue(unitId, out var channel)) return;

            bool shouldStop = false;

            lock (channel)
            {
                channel.Sockets.TryRemove(connectionId, out _);
                channel.SubscriberCount--;

                if (channel.SubscriberCount <= 0)
                {
                    shouldStop = true;
                    channel.Cts.Cancel();
                    _channels.TryRemove(unitId, out _);
                }
            }

            if (shouldStop && channel.WatcherTask != null)
            {
                try { await channel.WatcherTask; } catch (OperationCanceledException) { }
                channel.Cts.Dispose();
            }
        }

        private async Task StartJournalctlWatcher(string unitId, ChannelContext channel)
        {
            var token = channel.Cts.Token;
            using var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "journalctl",
                    Arguments = $"-u {unitId} -f -n 0",
                    RedirectStandardOutput = true,
                    UseShellExecute = false,
                    CreateNoWindow = true
                }
            };

            if (!process.Start()) return;

            try
            {
                // Read lines asynchronously from the stream
                while (!token.IsCancellationRequested && !process.StandardOutput.EndOfStream)
                {
                    var line = await process.StandardOutput.ReadLineAsync(token);
                    if (string.IsNullOrEmpty(line)) continue;

                    var bytes = Encoding.UTF8.GetBytes(line);
                    var segment = new ArraySegment<byte>(bytes);

                    // Broadcast to all sockets listening to this unit
                    foreach (var kvp in channel.Sockets)
                    {
                        if (kvp.Value.State == WebSocketState.Open)
                        {
                            // Fire and forget send, or await them sequentially. 
                            // Using a simple sequential await for thread safety per-socket.
                            try
                            {
                                await kvp.Value.SendAsync(segment, WebSocketMessageType.Text, true, CancellationToken.None);
                            }
                            catch { /* Socket likely died, Unsubscribe will clean it up */ }
                        }
                    }
                }
            }
            catch (OperationCanceledException) { }
            finally
            {
                if (!process.HasExited)
                {
                    process.Kill(entireProcessTree: true);
                }
            }
        }
    }
}
