using Microsoft.EntityFrameworkCore;
using System.ComponentModel.DataAnnotations.Schema;

namespace MoonlightDashboard.Database.Models
{
    [Index(nameof(Name), IsUnique = true)]
    public class User : Model
    {
        public required string Name { get; set; }
        public required string Password { get; set; }
        public required DateTime? ActivationTimestamp { get; set; }
    }
}
