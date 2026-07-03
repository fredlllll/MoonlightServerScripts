using System.Text;

namespace MoonlightDashboard.Apis.A2Sharp
{
    public static class BinaryWriterExtensions
    {
        public static void WriteNullTerminatedString(this BinaryWriter writer, string? text, Encoding? encoding = null)
        {
            if (string.IsNullOrEmpty(text))
            {
                //empty string
                writer.Write((byte)0x00);
                return;
            }

            // Default to UTF-8
            encoding ??= Encoding.UTF8;

            byte[] stringBytes = encoding.GetBytes(text);
            writer.Write(stringBytes);
            writer.Write((byte)0x00);
        }
    }
}
