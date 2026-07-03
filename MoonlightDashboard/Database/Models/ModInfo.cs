using Microsoft.EntityFrameworkCore;

namespace MoonlightDashboard.Database.Models
{
    [Index(nameof(ModId), IsUnique = true)]
    public class ModInfo :Model
    {
        public required string ModId { get; set; }
        public required string Name { get; set; }

    }
}
