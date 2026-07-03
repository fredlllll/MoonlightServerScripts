namespace MoonlightDashboard.Apis.Arma3
{
    public class Arma3ServerRuntimeInfo
    {
        public required string Name;
        public required string Map;
        public required string Mission;
        public required int MaxPlayers;
        public IEnumerable<string> Players = Enumerable.Empty<string>();
    }
}
