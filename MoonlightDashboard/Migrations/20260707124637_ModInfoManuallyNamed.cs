using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace MoonlightDashboard.Migrations
{
    /// <inheritdoc />
    public partial class ModInfoManuallyNamed : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<bool>(
                name: "IsManuallyNamed",
                table: "ModInfos",
                type: "INTEGER",
                nullable: false,
                defaultValue: false);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "IsManuallyNamed",
                table: "ModInfos");
        }
    }
}
