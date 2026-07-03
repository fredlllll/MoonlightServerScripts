using System.Text.Json.Nodes;

namespace MoonlightDashboard.Lib
{
    public static class Settings
    {
        static readonly List<Dictionary<string, JsonNode?>> files = new();

        public static void LoadFile(string path)
        {
            if (File.Exists(path))
            {
                var content = JsonNode.Parse(File.ReadAllText(path));
                if (content != null && content is JsonObject obj)
                {
                    Dictionary<string, JsonNode?> values = new();
                    foreach (var kv in obj)
                    {
                        values[kv.Key] = kv.Value;
                    }
                    files.Add(values);
                }
            }
        }

        public static JsonNode? Get(string name)
        {
            foreach (var file in files)
            {
                if (file.TryGetValue(name, out JsonNode? node))
                {
                    return node;
                }
            }
            return null;
        }

        public static T? GetValue<T>(string name, T? defaultValue = default)
        {
            var node = Get(name);
            if (node == null)
            {
                return defaultValue;
            }
            return node.GetValue<T>();
        }
    }
}
