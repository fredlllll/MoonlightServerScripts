namespace MoonlightDashboard.Database.Models
{
    public class User :Model
    {
        public required string Name { get; set; }
        public required string Password { get; set; }
        public required DateTime? ActivationTimestamp { get; set; }
        public required bool IsAdmin { get; set; }
    }
}
