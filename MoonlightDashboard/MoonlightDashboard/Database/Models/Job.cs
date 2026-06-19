namespace MoonlightDashboard.Database.Models
{
    public enum JobType
    {
        None,
        DownloadMod,
        UpdateServer
    }

    public class Job : Model
    {
        public JobType JobType { get; set; }
        public bool IsRunning { get; set; }
        public bool IsComplete { get; set; }
        public bool IsSuccessful { get; set; }
        public bool CancellationRequested { get; set; }
        public string? ErrorMessage { get; set; }
        public string? Data { get; set; }
    }
}
