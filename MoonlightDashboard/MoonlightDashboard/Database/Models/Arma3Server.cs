using Microsoft.EntityFrameworkCore;

namespace MoonlightDashboard.Database.Models
{
    [Index(nameof(Name), IsUnique = true)]
    [Index(nameof(Port), IsUnique = true)]
    public class Arma3Server : Model
    {
        public required string Name { get; set; }
        public required int Port { get; set; }
        public string? ActiveModsetId { get; set; }
        public string AdditionalCommandlineArgs { get; set; } = "";
    }
}
