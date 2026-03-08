using FinancialCopilot.Application.Common.Interfaces;
using FinancialCopilot.Application.Services;
using FinancialCopilot.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace FinancialCopilot.Infrastructure.Services;

public class AnalysisService : IAnalysisService
{
    private readonly IApplicationDbContext _context;

    public AnalysisService(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task AnalyzeSpendingPatternsAsync(Guid userId)
    {
        var threeMonthsAgo = DateTime.UtcNow.AddMonths(-3);
        var oneMonthAgo = DateTime.UtcNow.AddMonths(-1);

        var expenses = await _context.Expenses
            .Where(e => e.UserId == userId && e.Date >= threeMonthsAgo)
            .ToListAsync();

        var categories = expenses.Select(e => e.Category).Distinct();

        foreach (var category in categories)
        {
            var categoryExpenses = expenses.Where(e => e.Category == category).ToList();
            var oldExpenses = categoryExpenses.Where(e => e.Date < oneMonthAgo).ToList();
            var recentExpenses = categoryExpenses.Where(e => e.Date >= oneMonthAgo).ToList();

            var averageMonthly = oldExpenses.Any() 
                ? oldExpenses.Average(e => e.Amount) 
                : 0;
            var currentMonth = recentExpenses.Sum(e => e.Amount);

            var percentageChange = averageMonthly > 0 
                ? ((currentMonth - averageMonthly) / averageMonthly) * 100 
                : 0;

            var trend = percentageChange > 10 ? "Increasing" 
                : percentageChange < -10 ? "Decreasing" 
                : "Stable";

            var pattern = new SpendingPattern
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                Category = category,
                AverageMonthly = averageMonthly,
                CurrentMonth = currentMonth,
                PercentageChange = percentageChange,
                Trend = trend,
                AnalyzedAt = DateTime.UtcNow
            };

            _context.SpendingPatterns.Add(pattern);
        }

        await _context.SaveChangesAsync();
    }

    public async Task GenerateAlertsAsync(Guid userId)
    {
        var user = await _context.Users.FindAsync(userId);
        if (user == null) return;

        // Clear old unread alerts
        var oldAlerts = await _context.Alerts
            .Where(a => a.UserId == userId && !a.IsRead)
            .ToListAsync();
        
        foreach (var alert in oldAlerts)
        {
            _context.Alerts.Remove(alert);
        }

        var thirtyDaysAgo = DateTime.UtcNow.AddDays(-30);
        
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

        var totalIncome = incomes.Sum();
        var totalExpenses = expenses.Sum(e => e.Amount);
        var balance = totalIncome - totalExpenses;

        // Alert 1: Low Balance
        if (balance < 1000)
        {
            _context.Alerts.Add(new Alert
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                Type = "LowBalance",
                Severity = balance < 500 ? "Critical" : "Warning",
                Message = "Balance bajo detectado",
                Details = $"Tu balance actual es ${balance:F2}. Considera reducir gastos.",
                IsRead = false,
                CreatedAt = DateTime.UtcNow
            });
        }

        // Alert 2: High Spending This Month
        var thisMonthExpenses = expenses.Where(e => e.Date >= thirtyDaysAgo).Sum(e => e.Amount);
        var previousMonthExpenses = expenses
            .Where(e => e.Date >= thirtyDaysAgo.AddMonths(-1) && e.Date < thirtyDaysAgo)
            .Sum(e => e.Amount);

        if (previousMonthExpenses > 0 && thisMonthExpenses > previousMonthExpenses * 1.3m)
        {
            var increase = ((thisMonthExpenses - previousMonthExpenses) / previousMonthExpenses) * 100;
            _context.Alerts.Add(new Alert
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                Type = "HighSpending",
                Severity = "Warning",
                Message = "Gastos elevados este mes",
                Details = $"Tus gastos aumentaron {increase:F1}% comparado con el mes anterior.",
                IsRead = false,
                CreatedAt = DateTime.UtcNow
            });
        }

        // Alert 3: Debt Warning
        var totalDebt = debts.Sum();

        if (totalDebt > balance * 2)
        {
            _context.Alerts.Add(new Alert
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                Type = "DebtWarning",
                Severity = "Critical",
                Message = "Nivel de deuda preocupante",
                Details = $"Tu deuda total (${totalDebt:F2}) es más del doble de tu balance actual.",
                IsRead = false,
                CreatedAt = DateTime.UtcNow
            });
        }

        await _context.SaveChangesAsync();
    }

    public async Task<SpendingAnalysisDto> GetSpendingAnalysisAsync(Guid userId, DateTime? startDate = null, DateTime? endDate = null)
    {
        startDate ??= DateTime.UtcNow.AddMonths(-3);
        endDate ??= DateTime.UtcNow;

        var expenses = await _context.Expenses
            .Where(e => e.UserId == userId && e.Date >= startDate && e.Date <= endDate)
            .ToListAsync();

        if (!expenses.Any())
        {
            return new SpendingAnalysisDto(
                new Dictionary<string, decimal>(),
                new Dictionary<string, decimal>(),
                new List<CategoryInsight>(),
                0,
                "N/A"
            );
        }

        // Spending by category
        var spendingByCategory = expenses
            .GroupBy(e => e.Category)
            .ToDictionary(g => g.Key, g => g.Sum(e => e.Amount));

        // Monthly trends
        var monthlyTrends = expenses
            .GroupBy(e => e.Date.ToString("yyyy-MM"))
            .ToDictionary(g => g.Key, g => g.Sum(e => e.Amount));

        // Calculate insights
        var totalSpending = expenses.Sum(e => e.Amount);
        var insights = new List<CategoryInsight>();

        foreach (var category in spendingByCategory)
        {
            var percentage = (category.Value / totalSpending) * 100;
            var categoryExpenses = expenses.Where(e => e.Category == category.Key).ToList();
            
            var trend = "Stable";
            var recommendation = "";

            if (percentage > 30)
            {
                trend = "High";
                recommendation = $"Considera reducir gastos en {category.Key}. Representa {percentage:F1}% de tus gastos.";
            }
            else if (percentage < 5)
            {
                trend = "Low";
                recommendation = $"Gastos controlados en {category.Key}.";
            }

            insights.Add(new CategoryInsight(
                category.Key,
                category.Value,
                percentage,
                trend,
                recommendation
            ));
        }

        var topCategory = spendingByCategory.OrderByDescending(x => x.Value).First().Key;
        var days = (endDate.Value - startDate.Value).Days;
        var averageDaily = days > 0 ? totalSpending / days : 0;

        return new SpendingAnalysisDto(
            spendingByCategory,
            monthlyTrends,
            insights.OrderByDescending(i => i.Amount).ToList(),
            averageDaily,
            topCategory
        );
    }
}
