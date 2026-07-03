using System.Diagnostics;

namespace MoonlightDashboard.Apis.SystemD
{
    public static class SystemDUtil
    {
        public static Process SystemCtl(bool redirectOutput = false, params string[] args)
        {
            var psi = new ProcessStartInfo("sudo");
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            if (redirectOutput)
            {
                psi.RedirectStandardOutput = true;
                psi.RedirectStandardError = true;
            }
            psi.ArgumentList.Add("systemctl");
            foreach (var arg in args)
            {
                psi.ArgumentList.Add(arg);
            }
            var p = Process.Start(psi);
            if (p == null)
            {
                throw new Exception("could not start process");
            }
            return p;
        }

        public static Process SystemCtl(params string[] args)
        {
            return SystemCtl(false, args);
        }

        public static Process JournalCtl(bool redirectOutput = true, params string[] args)
        {
            var psi = new ProcessStartInfo("sudo");
            psi.UseShellExecute = false;
            psi.CreateNoWindow = true;
            if (redirectOutput)
            {
                psi.RedirectStandardOutput = true;
                psi.RedirectStandardError = true;
            }
            psi.ArgumentList.Add("journalctl");
            foreach (var arg in args)
            {
                psi.ArgumentList.Add(arg);
            }
            var p = Process.Start(psi);
            if (p == null)
            {
                throw new Exception("could not start process");
            }
            return p;
        }

        public static Process JournalCtl(params string[] args)
        {
            return JournalCtl(true, args);
        }
    }
}
