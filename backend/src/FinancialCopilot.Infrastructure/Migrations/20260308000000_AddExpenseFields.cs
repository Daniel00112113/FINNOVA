using Microsoft.EntityFrameworkCore.Migrations;

#nullable disable

namespace FinancialCopilot.Infrastructure.Migrations
{
    /// <inheritdoc />
    public partial class AddExpenseFields : Migration
    {
        /// <inheritdoc />
        protected override void Up(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.AddColumn<string>(
                name: "Location",
                table: "Expenses",
                type: "text",
                nullable: true);

            migrationBuilder.AddColumn<bool>(
                name: "IsRecurring",
                table: "Expenses",
                type: "boolean",
                nullable: false,
                defaultValue: false);

            migrationBuilder.AddColumn<int>(
                name: "RecurrenceType",
                table: "Expenses",
                type: "integer",
                nullable: true);

            migrationBuilder.AddColumn<string[]>(
                name: "Tags",
                table: "Expenses",
                type: "text[]",
                nullable: false,
                defaultValue: new string[] { });
        }

        /// <inheritdoc />
        protected override void Down(MigrationBuilder migrationBuilder)
        {
            migrationBuilder.DropColumn(
                name: "Location",
                table: "Expenses");

            migrationBuilder.DropColumn(
                name: "IsRecurring",
                table: "Expenses");

            migrationBuilder.DropColumn(
                name: "RecurrenceType",
                table: "Expenses");

            migrationBuilder.DropColumn(
                name: "Tags",
                table: "Expenses");
        }
    }
}
