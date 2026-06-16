namespace MoonlightDashboard.Database.Models
{
    public class User : Model
    {
        public required string Name { get; set; }
        public required string PasswordHash { get; set; }
        public required string PasswordSalt { get; set; }
        public required DateTime? ActivationTimestamp { get; set; }
    }
}
