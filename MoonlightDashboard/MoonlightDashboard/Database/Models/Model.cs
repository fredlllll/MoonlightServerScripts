using System.ComponentModel.DataAnnotations;

namespace MoonlightDashboard.Database.Models
{
    public class Model
    {
        public Model()
        {
            Created = Updated = DateTime.UtcNow;
        }
        [Key]
        public required string Id { get; set; }
        public DateTime Created { get; set; }
        public DateTime Updated { get; set; }
    }
}
