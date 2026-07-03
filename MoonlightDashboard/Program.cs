using Microsoft.EntityFrameworkCore;
using MoonlightDashboard.Database;
using MoonlightDashboard.Middleware;
using MoonlightDashboard.Services;
using System.Globalization;

namespace MoonlightDashboard
{
    public class Program
    {
        public static void Main(string[] args)
        {
            var builder = WebApplication.CreateBuilder(args);
            builder.Services.AddRazorPages().AddRazorPagesOptions((o) => {
                //extra routes go here
            });
            builder.Services.AddDbContext<DatabaseContext>(options => options.UseSqlite($"Data Source=db.sqlite").ConfigureWarnings(w=>w.Log(Microsoft.EntityFrameworkCore.Diagnostics.RelationalEventId.PendingModelChangesWarning)));
            builder.Services.AddHostedService<JobService>();
            builder.Services.AddScoped<ServerService>();
            builder.Services.AddControllers();
            builder.WebHost.UseUrls("http://0.0.0.0:8080");

            var app = builder.Build();

            if (app.Environment.IsDevelopment())
            {
                app.UseDeveloperExceptionPage();
            }

            using (var scope = app.Services.CreateScope())
            {
                var services = scope.ServiceProvider;

                var context = services.GetRequiredService<DatabaseContext>();
                context.Database.Migrate();
            }

            var culture = CultureInfo.InvariantCulture;
            app.UseRequestLocalization(new RequestLocalizationOptions
            {
                DefaultRequestCulture = new Microsoft.AspNetCore.Localization.RequestCulture(culture),
                SupportedCultures = new[] { culture },
                SupportedUICultures = new[] { culture }
            });

            app.UseRouting();
            app.UseStaticFiles();
            app.UseWebSockets();
            app.MapRazorPages();
            app.MapControllers();
            app.UseUserSessions();

            app.Run();
        }
    }
}