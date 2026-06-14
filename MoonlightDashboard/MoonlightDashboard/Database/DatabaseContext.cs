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


        public DatabaseContext(DbContextOptions<DatabaseContext> options) : base(options) { }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            modelBuilder.Entity<Arma3CreatorDlc>().HasData(
                new Arma3CreatorDlc
                {
                    Id = Util.GetNewId<Arma3CreatorDlc>(),
                    ShortName = "vn",
                    Name = "S.O.G. Prairie Fire",
                    Depot = "233790",
                    Manifest = "7907683864326938845"
                },
                new Arma3CreatorDlc
                {
                    Id = Util.GetNewId<Arma3CreatorDlc>(),
                    ShortName = "gm",
                    Name = "Global Mobilization - Cold War Germany",
                    Depot = "233787",
                    Manifest = "5132611187809370715"
                },
                new Arma3CreatorDlc
                {
                    Id = Util.GetNewId<Arma3CreatorDlc>(),
                    ShortName = "ws",
                    Name = "Western Sahara",
                    Depot = "233786",
                    Manifest = "4838971061001777332"
                },
                new Arma3CreatorDlc
                {
                    Id = Util.GetNewId<Arma3CreatorDlc>(),
                    ShortName = "csla",
                    Name = "CSLA Iron Curtain",
                    Depot = "1294440",
                    Manifest = "3088033651234564230"
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

            //doesnt work, creates a seperate table for Model and links to it with an id
            //modelBuilder.Entity<Models.Model>().Property(p => p.Updated).HasComputedColumnSql("datetime('now')").ValueGeneratedOnAddOrUpdate();
            //modelBuilder.Entity<Models.Model>().Property(p => p.Created).HasComputedColumnSql("datetime('now')").ValueGeneratedOnAdd();

        }

        protected override void OnConfiguring(DbContextOptionsBuilder options)
        {
            options.UseSqlite($"Data Source=db.sqlite");
        }
    }
}
