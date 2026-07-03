using Microsoft.EntityFrameworkCore;

namespace MoonlightDashboard.Database.Models
{
    [Index(nameof(Name), IsUnique = true)]
    public class Arma3Modset :Model
    {
        public required string Name { get; set; }
    }
}
