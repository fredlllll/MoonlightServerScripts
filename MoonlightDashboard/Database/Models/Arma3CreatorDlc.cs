namespace MoonlightDashboard.Database.Models
{
    public class Arma3CreatorDlc : Model
    {
        public required string Name { get; set; }
        public required string ShortName { get; set; }
        public required string Depot { get; set; }
        public required string Manifest { get; set; }
    }
}
