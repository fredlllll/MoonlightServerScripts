using System.Text;

namespace MoonlightDashboard.Lib
{
    public class ProcessResult
    {
        public readonly List<ProcessOutputItem> OutputItems = new();
        /*public string Output { get; set; } = "";
        public string Error { get; set; } = "";*/
        public int ExitCode { get; set; } = 0;

        public string GetCompleteOutputAsMarkup()
        {
            StringBuilder sb = new();
            sb.AppendLine("Exit Code: " + ExitCode + "<br>");
            foreach (var item in OutputItems)
            {
                if (item.IsError)
                {
                    sb.Append("<span style=\"font-style: italic;\">");
                }
                sb.Append(AnsiConsoleToHtml.AnsiConsole.ToHtml(item.Text));
                if (item.IsError)
                {
                    sb.Append("</span>");
                }
                sb.AppendLine();
            }
            return sb.ToString();
        }
    }

    public class ProcessOutputItem
    {
        public string Text { get; set; } = "";
        public bool IsError { get; set; } = false;
    }
}
