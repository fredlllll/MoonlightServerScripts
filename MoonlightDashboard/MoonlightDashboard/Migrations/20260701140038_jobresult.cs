using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace MoonlightDashboard.Migrations
{
    /// <inheritdoc />
    public partial class jobresult : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Result",
                table: "Jobs",
                type: "TEXT",
                nullable: true);
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Result",
                table: "Jobs");
        }
    }
}
