using System.Net;
using System.Net.Sockets;
using System.Runtime.Intrinsics.Arm;
using System.Text;

namespace MoonlightDashboard.Apis.A2Sharp
{
    public class A2Sharp
    {
        private static readonly byte[] s_infoRequest;

        static A2Sharp()
        {
            using (MemoryStream ms = new MemoryStream())
            using (BinaryWriter bw = new BinaryWriter(ms))
            {
                bw.Write(0xFFFFFFFF); // header
                bw.Write((byte)'T'); // Command: A2S_INFO

                bw.WriteNullTerminatedString("Source Engine Query", Encoding.ASCII);

                s_infoRequest = ms.ToArray();
            }
        }

        public static A2SharpInfo GetInfo(IPAddress address, int port, int timeoutMs = 2000)
        {
            A2SharpInfo info = new A2SharpInfo();

            using (UdpClient udp = new UdpClient())
            {
                udp.Client.ReceiveTimeout = timeoutMs;
                udp.Connect(address, port);
                udp.Send(s_infoRequest, s_infoRequest.Length);

                IPEndPoint? remoteEP = null;
                byte[] response = udp.Receive(ref remoteEP);

                using (MemoryStream ms = new MemoryStream(response))
                using (BinaryReader br = new BinaryReader(ms))
                {
                    if (br.ReadUInt32() != 0xFFFFFFFF)
                    {
                        throw new Exception("Invalid A2S header received");
                    }

                    // Check response type (0x49 is 'I' for Info)
                    byte headerType = br.ReadByte();
                    if (headerType != (byte)'I')
                    {
                        throw new Exception("Not an A2S_INFO response");
                    }

                    info.Protocol = br.ReadByte();
                    info.Name = br.ReadNullTerminatedString();
                    info.Map = br.ReadNullTerminatedString();
                    info.Folder = br.ReadNullTerminatedString();
                    info.Game = br.ReadNullTerminatedString();
                    info.AppId = br.ReadInt16();
                    info.Players = br.ReadByte();
                    info.MaxPlayers = br.ReadByte();
                    info.Bots = br.ReadByte();
                }
            }
            return info;
        }

        public static IEnumerable<A2SharpPlayer> GetPlayers(IPAddress address, int port, int timeoutMs = 2000)
        {
            var players = new List<A2SharpPlayer>();

            using (UdpClient udp = new UdpClient())
            {
                udp.Client.ReceiveTimeout = timeoutMs;
                udp.Connect(address, port);

                SendPlayerRequest(udp);

                System.Net.IPEndPoint? remoteEP = null;
                byte[] response = udp.Receive(ref remoteEP);

                uint challengeToken = 0xFFFFFFFF;

                using (MemoryStream ms = new MemoryStream(response))
                using (BinaryReader br = new BinaryReader(ms))
                {
                    if (br.ReadUInt32() != 0xFFFFFFFF) throw new Exception("Invalid response header");

                    byte type = br.ReadByte();

                    // If type is 0x41 ('A'), the server provided a challenge token
                    if (type == (byte)'A')
                    {
                        challengeToken = br.ReadUInt32();
                    }
                    else
                    {
                        throw new Exception("Server did not return a valid challenge token, type was: " + type);
                    }
                }

                SendPlayerRequest(udp, challengeToken);

                response = udp.Receive(ref remoteEP);

                using (MemoryStream ms = new MemoryStream(response))
                using (BinaryReader br = new BinaryReader(ms))
                {
                    if (br.ReadInt32() != -1) throw new Exception("Invalid response header");

                    byte type = br.ReadByte();
                    if (type != (byte)'D') throw new Exception("Expected player data type");

                    byte playerCount = br.ReadByte();

                    for (int i = 0; i < playerCount; i++)
                    {
                        byte index = br.ReadByte(); // internal index, usually ignored
                        var player = new A2SharpPlayer()
                        {
                            Name = br.ReadNullTerminatedString(),
                            Score = br.ReadInt32(),
                            DurationSeconds = br.ReadSingle()
                        };
                        yield return player;
                    }
                }
            }
        }

        private static void SendPlayerRequest(UdpClient client, uint challenge = 0xFFFFFFFF)
        {
            using var ms = new MemoryStream();
            using var bw = new BinaryWriter(ms);
            bw.Write(0xFFFFFFFF); //header
            bw.Write((byte)'U');   // Command byte for A2S_PLAYER
            bw.Write(challenge);   // Dynamic challenge integer
            var data = ms.ToArray();
            client.Send(data, data.Length);
        }

        public static Dictionary<string, string> GetRules(IPAddress address, int port, int timeoutMs)
        {
            // Using OrdinalIgnoreCase so you can look up rules like "BATTLEYE" or "battleye" interchangeably
            var rules = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

            using (UdpClient udp = new UdpClient())
            {
                udp.Client.ReceiveTimeout = timeoutMs;
                udp.Connect(address, port);

                SendRulesRequest(udp);

                System.Net.IPEndPoint? remoteEP = null;
                byte[] response = udp.Receive(ref remoteEP);

                uint challengeToken = 0xFFFFFFFF;

                using (MemoryStream ms = new MemoryStream(response))
                using (BinaryReader br = new BinaryReader(ms))
                {
                    if (br.ReadInt32() != -1) throw new Exception("Invalid response header");

                    byte type = br.ReadByte();

                    // If type is 0x41 ('A'), the server provided a challenge token
                    if (type == (byte)'A')
                    {
                        challengeToken = br.ReadUInt32();
                    }
                    else
                    {
                        throw new Exception("Server did not return a valid challenge token, type was: " + type);
                    }
                }

                SendRulesRequest(udp, challengeToken);

                response = udp.Receive(ref remoteEP);

                using (MemoryStream ms = new MemoryStream(response))
                using (BinaryReader br = new BinaryReader(ms))
                {
                    if (br.ReadInt32() != -1) throw new Exception("Invalid response header");

                    byte type = br.ReadByte();
                    if (type != (byte)'E') throw new Exception("Expected rules data type (0x45/'E')");

                    short ruleCount = br.ReadInt16();

                    for (int i = 0; i < ruleCount; i++)
                    {
                        string ruleName = br.ReadNullTerminatedString();
                        string ruleValue = br.ReadNullTerminatedString();

                        if (!string.IsNullOrWhiteSpace(ruleName))
                        {
                            rules[ruleName] = ruleValue;
                        }
                    }
                }
            }

            return rules;
        }

        private static void SendRulesRequest(UdpClient client, uint challenge = 0xFFFFFFFF)
        {
            using var ms = new MemoryStream();
            using var bw = new BinaryWriter(ms);
            bw.Write(0xFFFFFFFF); //header
            bw.Write((byte)'V');   // Command byte for A2S_RULES
            bw.Write(challenge);   // Dynamic challenge integer
            var data = ms.ToArray();
            client.Send(data, data.Length);
        }
    }
}
