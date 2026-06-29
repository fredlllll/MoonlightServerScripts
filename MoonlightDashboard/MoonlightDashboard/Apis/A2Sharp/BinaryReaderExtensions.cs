using System.Text;

namespace MoonlightDashboard.Apis.A2Sharp
{
    public static class BinaryReaderExtensions
    {
        public static string ReadNullTerminatedString(this BinaryReader br, Encoding encoding = null)
        {
            // Default to UTF-8
            encoding ??= Encoding.UTF8;

            List<byte> bytes = new List<byte>();
            byte b;

            while ((b = br.ReadByte()) != 0x00)
            {
                bytes.Add(b);
            }

            return encoding.GetString(bytes.ToArray());
        }
    }
}
