using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Internal;
using MoonlightDashboard.Database.Models;
using MoonlightDashboard.Lib;
using System;
using System.Threading.Channels;
using UUIDNext;

namespace MoonlightDashboard.Database
{
    public class DatabaseContext : DbContext
    {
        public DbSet<User> Users { get; set; }
        public DbSet<Permission> Permissions { get; set; }
        public DbSet<UserPermission> UserPermissions { get; set; }
        public DbSet<Session> Sessions { get; set; }
        public DbSet<Arma3Server> Arma3Servers { get; set; }
        public DbSet<Arma3Modset> Arma3Modsets { get; set; }
        public DbSet<Arma3ModsetMod> Arma3ModsetMods { get; set; }
        public DbSet<Arma3CreatorDlc> Arma3CreatorDlcs { get; set; }
        public DbSet<Arma3ServerCreatorDlc> Arma3ServerCreatorDlcs { get; set; }
        public DbSet<Job> Jobs { get; set; }
        public DbSet<ModInfo> ModInfos { get; set; }


        public DatabaseContext(DbContextOptions<DatabaseContext> options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            //NOTE: the depot and manifest numbers will change over time with updates and can be retrieved from steamdb
            modelBuilder.Entity<Arma3CreatorDlc>().HasData(
                new Arma3CreatorDlc
                {
                    //https://steamdb.info/sub/425631/
                    Id = "arma3creatordlc_prairie_fire",
                    Created = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    Updated = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    ShortName = "vn",
                    Name = "S.O.G. Prairie Fire",
                    Depot = "1227701",
                    Manifest = "8778927882579535691" // 10.12.2024
                },
                new Arma3CreatorDlc
                {
                    //https://steamdb.info/sub/347210/
                    Id = "arma3creatordlc_global_mobilization",
                    Created = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    Updated = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    ShortName = "gm",
                    Name = "Global Mobilization - Cold War Germany",
                    Depot = "1042221",
                    Manifest = "2053062434401462647" // 29.05.2025
                },
                new Arma3CreatorDlc
                {
                    //https://steamdb.info/sub/598229/
                    Id = "arma3creatordlc_western_sahara",
                    Created = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    Updated = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    ShortName = "ws",
                    Name = "Western Sahara",
                    Depot = "1681171",
                    Manifest = "738528337327303663" // 16.12.2025
                },
                new Arma3CreatorDlc
                {
                    //https://steamdb.info/sub/451576/
                    Id = "arma3creatordlc_iron_courtain",
                    Created = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    Updated = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    ShortName = "csla",
                    Name = "CSLA Iron Curtain",
                    Depot = "1294441",
                    Manifest = "5407594059006667059" // 25.03.2025
                },
                new Arma3CreatorDlc
                {
                    //https://steamdb.info/sub/949174/
                    Id = "arma3creatordlc_expeditionary_forces",
                    Created = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    Updated = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    ShortName = "ef",
                    Name = "Expeditionary Forces",
                    Depot = "2647831",
                    Manifest = "2687171635229708487" // 07.04.2026
                },
                new Arma3CreatorDlc
                {
                    //https://steamdb.info/sub/949153/
                    Id = "arma3creatordlc_reaction_forces",
                    Created = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    Updated = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    ShortName = "rf",
                    Name = "Reaction Forces",
                    Depot = "2647761",
                    Manifest = "2576413575760136050" // 08.12.2025
                },
                new Arma3CreatorDlc
                {
                    //https://steamdb.info/sub/402602/
                    Id = "arma3creatordlc_spearhead_1944",
                    Created = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    Updated = new DateTime(2026, 06, 28, 12, 0, 0, DateTimeKind.Utc),
                    ShortName = "spe",
                    Name = "Spearhead 1944",
                    Depot = "1175381",
                    Manifest = "6576197082193427041" // 28.08.2025
                }
                );

            modelBuilder.Entity<Permission>().HasData(
                new Permission { Id = Util.GetNewId<Permission>(), Name = "Admin" }
                );

            modelBuilder.Entity<User>().ToTable(nameof(Users));
            modelBuilder.Entity<Permission>().ToTable(nameof(Permissions));
            modelBuilder.Entity<UserPermission>().ToTable(nameof(UserPermissions));
            modelBuilder.Entity<Session>().ToTable(nameof(Sessions));
            modelBuilder.Entity<Arma3Server>().ToTable(nameof(Arma3Servers));
            modelBuilder.Entity<Arma3Modset>().ToTable(nameof(Arma3Modsets));
            modelBuilder.Entity<Arma3ModsetMod>().ToTable(nameof(Arma3ModsetMods));
            modelBuilder.Entity<Arma3CreatorDlc>().ToTable(nameof(Arma3CreatorDlcs));
            modelBuilder.Entity<Arma3ServerCreatorDlc>().ToTable(nameof(Arma3ServerCreatorDlcs));
            modelBuilder.Entity<Job>().ToTable(nameof(Jobs));
            modelBuilder.Entity<ModInfo>().ToTable(nameof(ModInfos));
        }

        protected override void OnConfiguring(DbContextOptionsBuilder options)
        {
            options.UseSqlite($"Data Source=db.sqlite");
        }

        public void GiveUserPermission(User user, string name)
        {
            var perm = Permissions.FirstOrDefault(p => p.Name.ToLower() == name.ToLower());
            if (perm == null)
            {
                throw new Exception("no such permission");
            }

            var userPerm = new UserPermission
            {
                Id = Util.GetNewId<UserPermission>(),
                UserId = user.Id,
                PermissionId = perm.Id
            };
            UserPermissions.Add(userPerm);
        }
    }
}
