using System;
using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

#pragma warning disable CA1814 // Prefer jagged arrays over multidimensional

namespace MoonlightDashboard.Migrations
{
    /// <inheritdoc />
    public partial class Init : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.CreateTable(
                name: "Arma3CreatorDlcs",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    ShortName = table.Column<string>(type: "TEXT", nullable: false),
                    Depot = table.Column<string>(type: "TEXT", nullable: false),
                    Manifest = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Arma3CreatorDlcs", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Arma3ModsetMods",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    ModsetId = table.Column<string>(type: "TEXT", nullable: false),
                    ModSteamId = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Arma3ModsetMods", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Arma3Modsets",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Arma3Modsets", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Arma3ServerCreatorDlcs",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    Arma3ServerId = table.Column<string>(type: "TEXT", nullable: false),
                    Arma3CreatorDlcId = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Arma3ServerCreatorDlcs", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Arma3Servers",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    Port = table.Column<int>(type: "INTEGER", nullable: false),
                    ActiveModsetId = table.Column<string>(type: "TEXT", nullable: true),
                    AdditionalCommandlineArgs = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Arma3Servers", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Jobs",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    JobType = table.Column<int>(type: "INTEGER", nullable: false),
                    IsRunning = table.Column<bool>(type: "INTEGER", nullable: false),
                    IsComplete = table.Column<bool>(type: "INTEGER", nullable: false),
                    IsSuccessful = table.Column<bool>(type: "INTEGER", nullable: false),
                    CancellationRequested = table.Column<bool>(type: "INTEGER", nullable: false),
                    ErrorMessage = table.Column<string>(type: "TEXT", nullable: true),
                    Data = table.Column<string>(type: "TEXT", nullable: true),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Jobs", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "ModInfos",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    ModId = table.Column<string>(type: "TEXT", nullable: false),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_ModInfos", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Permissions",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Permissions", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Sessions",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    UserId = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Sessions", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "SettingValues",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    Value = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_SettingValues", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "UserPermissions",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    UserId = table.Column<string>(type: "TEXT", nullable: false),
                    PermissionId = table.Column<string>(type: "TEXT", nullable: false),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_UserPermissions", x => x.Id);
                });

            migrationBuilder.CreateTable(
                name: "Users",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    Password = table.Column<string>(type: "TEXT", nullable: false),
                    ActivationTimestamp = table.Column<DateTime>(type: "TEXT", nullable: true),
                    Created = table.Column<DateTime>(type: "TEXT", nullable: false),
                    Updated = table.Column<DateTime>(type: "TEXT", nullable: false)
                },
                constraints: table =>
                {
                    table.PrimaryKey("PK_Users", x => x.Id);
                });

            migrationBuilder.InsertData(
                table: "Arma3CreatorDlcs",
                columns: new[] { "Id", "Created", "Depot", "Manifest", "Name", "ShortName", "Updated" },
                values: new object[,]
                {
                    { "arma3creatordlc_expeditionary_forces", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc), "2647831", "2687171635229708487", "Expeditionary Forces", "ef", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc) },
                    { "arma3creatordlc_global_mobilization", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc), "1042221", "2053062434401462647", "Global Mobilization - Cold War Germany", "gm", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc) },
                    { "arma3creatordlc_iron_courtain", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc), "1294441", "5407594059006667059", "CSLA Iron Curtain", "csla", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc) },
                    { "arma3creatordlc_prairie_fire", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc), "1227701", "8778927882579535691", "S.O.G. Prairie Fire", "vn", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc) },
                    { "arma3creatordlc_reaction_forces", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc), "2647761", "2576413575760136050", "Reaction Forces", "rf", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc) },
                    { "arma3creatordlc_spearhead_1944", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc), "1175381", "6576197082193427041", "Spearhead 1944", "spe", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc) },
                    { "arma3creatordlc_western_sahara", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc), "1681171", "738528337327303663", "Western Sahara", "ws", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc) }
                });

            migrationBuilder.InsertData(
                table: "Permissions",
                columns: new[] { "Id", "Created", "Name", "Updated" },
                values: new object[] { "permission_admin", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc), "Admin", new DateTime(2026, 6, 28, 12, 0, 0, 0, DateTimeKind.Utc) });

            migrationBuilder.CreateIndex(
                name: "IX_Arma3Modsets_Name",
                table: "Arma3Modsets",
                column: "Name",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Arma3Servers_Name",
                table: "Arma3Servers",
                column: "Name",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Arma3Servers_Port",
                table: "Arma3Servers",
                column: "Port",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_ModInfos_ModId",
                table: "ModInfos",
                column: "ModId",
                unique: true);

            migrationBuilder.CreateIndex(
                name: "IX_Users_Name",
                table: "Users",
                column: "Name",
                unique: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropTable(
                name: "Arma3CreatorDlcs");

            migrationBuilder.DropTable(
                name: "Arma3ModsetMods");

            migrationBuilder.DropTable(
                name: "Arma3Modsets");

            migrationBuilder.DropTable(
                name: "Arma3ServerCreatorDlcs");

            migrationBuilder.DropTable(
                name: "Arma3Servers");

            migrationBuilder.DropTable(
                name: "Jobs");

            migrationBuilder.DropTable(
                name: "ModInfos");

            migrationBuilder.DropTable(
                name: "Permissions");

            migrationBuilder.DropTable(
                name: "Sessions");

            migrationBuilder.DropTable(
                name: "SettingValues");

            migrationBuilder.DropTable(
                name: "UserPermissions");

            migrationBuilder.DropTable(
                name: "Users");
        }
    }
}
