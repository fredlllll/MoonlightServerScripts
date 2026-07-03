using MoonlightDashboard.Database;

namespace MoonlightDashboard.Lib
{
    public class JobCancellationMonitor : IDisposable
    {
        private readonly CancellationToken _parentToken;
        private readonly CancellationTokenRegistration _parentRegistration;
        private readonly CancellationTokenSource _cts;
        private readonly string _jobId;
        private readonly IServiceScope _scope; // Inject your DB check logic here
        private readonly Timer _timer;
        private bool _isCancelled = false;

        public JobCancellationMonitor(CancellationToken parentToken, IServiceScope scope, string jobId)
        {
            _parentToken = parentToken;
            _scope = scope;
            _jobId = jobId;
            _cts = new CancellationTokenSource();

            _parentRegistration = _parentToken.Register(Cancel);

            // Check database every 1000ms (1 second)
            _timer = new Timer(CheckDatabaseAsync, null, TimeSpan.Zero, TimeSpan.FromSeconds(1));
        }

        public CancellationToken Token => _cts.Token;

        private void Cancel()
        {
            if (!_isCancelled)
            {
                _isCancelled = true;
                try
                {
                    _cts.Cancel(); // Triggers the cancellation token
                }
                catch (ObjectDisposedException)
                {
                    // Ignore if the token source is already disposed
                }
                _timer?.Change(Timeout.InfiniteTimeSpan, Timeout.InfiniteTimeSpan);
            }
        }

        private void CheckDatabaseAsync(object? state)
        {
            // Prevent re-entrancy and redundant checks after cancellation
            if (_isCancelled || _cts.IsCancellationRequested)
            {
                _timer?.Change(Timeout.InfiniteTimeSpan, Timeout.InfiniteTimeSpan);
                return;
            }

            try
            {
                var db = _scope.ServiceProvider.GetRequiredService<DatabaseContext>();
                var job = db.Jobs.FirstOrDefault(j => j.Id == _jobId);
                if (job == null || job.CancellationRequested)
                {
                    Cancel();
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Cancellation check failed: {ex.Message}");
            }
        }

        public void Dispose()
        {
            _timer?.Dispose();
            _parentRegistration.Unregister();
            _cts?.Dispose();
        }
    }
}
