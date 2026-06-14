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
                name: "Users",
                columns: table => new
                {
                    Id = table.Column<string>(type: "TEXT", nullable: false),
                    Name = table.Column<string>(type: "TEXT", nullable: false),
                    Password = table.Column<string>(type: "TEXT", nullable: false),
                    ActivationTimestamp = table.Column<DateTime>(type: "TEXT", nullable: true),
                    IsAdmin = table.Column<bool>(type: "INTEGER", nullable: false),
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
                    { "arma3creatordlc_019ec6cc-1760-7205-adf6-c908ec83b2a3", DateTime.UtcNow, "233790", "7907683864326938845", "S.O.G. Prairie Fire", "vn", DateTime.UtcNow },
                    { "arma3creatordlc_019ec6cc-1762-70d4-bea1-244015ed52db", DateTime.UtcNow, "233787", "5132611187809370715", "Global Mobilization - Cold War Germany", "gm", DateTime.UtcNow },
                    { "arma3creatordlc_019ec6cc-1762-70d5-98a8-6bf3be2d0456", DateTime.UtcNow, "233786", "4838971061001777332", "Western Sahara", "ws", DateTime.UtcNow },
                    { "arma3creatordlc_019ec6cc-1762-70d6-8732-c6969ccb2c99", DateTime.UtcNow, "1294440", "3088033651234564230", "CSLA Iron Curtain", "csla", DateTime.UtcNow }
                });
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
                name: "Arma3Servers");

            migrationBuilder.DropTable(
                name: "Sessions");

            migrationBuilder.DropTable(
                name: "Users");
        }
    }
}
