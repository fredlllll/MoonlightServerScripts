namespace MoonlightDashboard.Lib
{
    public class ProcessResult
    {
        public string Output { get; set; } = "";
        public string Error { get; set; } = "";
        public int ExitCode { get; set; } = 0;

        public override string ToString()
        {
            return "ExitCode: " + ExitCode + "<br>\nOutput: " + Output + "<br>\nError: " + Error;
        }
    }
}
