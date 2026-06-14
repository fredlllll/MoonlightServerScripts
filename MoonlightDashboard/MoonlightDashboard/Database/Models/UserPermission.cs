namespace MoonlightDashboard.Database.Models
{
    public class UserPermission : Model
    {
        public required string UserId { get; set; }
        public required string PermissionId { get; set; }
    }
}
