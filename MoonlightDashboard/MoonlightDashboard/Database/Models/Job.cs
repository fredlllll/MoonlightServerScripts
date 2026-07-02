namespace MoonlightDashboard.Database.Models
{
    public enum JobType
    {
        None,
        DownloadMod,
        UpdateServer,
        LoginSteam,
    }

    public class Job : Model
    {
        public required JobType JobType { get; set; }
        public bool IsRunning { get; set; } = false;
        public bool IsComplete { get; set; } = false;
        public bool IsSuccessful { get; set; } = false;
        public bool CancellationRequested { get; set; } = false;
        public string? ErrorMessage { get; set; } = null;
        public string? Result { get; set; } = null;
        public string? Data { get; set; } = null;

        public bool IsPending()
        {
            return !IsRunning && !IsComplete;
        }
    }
}
