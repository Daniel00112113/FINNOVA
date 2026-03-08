using FinancialCopilot.Application.Common.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinancialCopilot.API.Controllers;

[Authorize]
[ApiController]
[Route("api/users/{userId}/[controller]")]
public class DashboardController : ControllerBase
{
    private readonly IApplicationDbContext _context;

    public DashboardController(IApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<DashboardDto>> GetDashboard(Guid userId)
    {
        try
        {
            var user = await _context.Users.FindAsync(userId);
            if (user == null)
                return NotFound("User not found");

            // Ejecutar consultas secuencialmente para evitar problemas de concurrencia
            var incomes = await _context.Incomes
                .Where(i => i.UserId == userId)
                .Select(i => i.Amount)
                .ToListAsync();

            var expenses = await _context.Expenses
                .Where(e => e.UserId == userId)
                .Select(e => new { e.Amount, e.Date })
                .ToListAsync();

            var debts = await _context.Debts
                .Where(d => d.UserId == userId)
                .Select(d => d.RemainingAmount)
                .ToListAsync();

            var recentTransactions = await _context.Expenses
                .Where(e => e.UserId == userId)
                .OrderByDescending(e => e.Date)
                .Take(5)
                .Select(e => new TransactionDto(
                    e.Id,
                    "expense",
                    e.Amount,
                    e.Category,
                    e.Date,
                    e.Description
                ))
                .ToListAsync();

            var totalIncome = incomes.Sum();
            var totalExpenses = expenses.Sum(e => e.Amount);
            var totalDebt = debts.Sum();
            var balance = totalIncome - totalExpenses;

            return Ok(new DashboardDto(
                totalIncome,
                totalExpenses,
                balance,
                totalDebt,
                recentTransactions
            ));
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Dashboard Error: {ex.Message}");
            Console.WriteLine($"Stack: {ex.StackTrace}");
            return StatusCode(500, new { error = ex.Message, details = ex.InnerException?.Message });
        }
    }
}

public record DashboardDto(
    decimal TotalIncome,
    decimal TotalExpenses,
    decimal Balance,
    decimal TotalDebt,
    List<TransactionDto> RecentTransactions
);

public record TransactionDto(
    Guid Id,
    string Type,
    decimal Amount,
    string Category,
    DateTime Date,
    string? Description
);

