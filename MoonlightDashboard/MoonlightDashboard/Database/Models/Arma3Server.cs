namespace MoonlightDashboard.Database.Models
{
    public class Arma3Server : Model
    {
        public required string Name { get; set; }
        public required int Port { get; set; }
        public string? ActiveModsetId { get; set; }
        public string AdditionalCommandlineArgs { get; set; } = "";
    }
}
