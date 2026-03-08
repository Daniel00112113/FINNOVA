using FinancialCopilot.Domain.Entities;
using Microsoft.EntityFrameworkCore;

namespace FinancialCopilot.Application.Common.Interfaces;

public interface IApplicationDbContext
{
    DbSet<User> Users { get; }
    DbSet<Income> Incomes { get; }
    DbSet<Expense> Expenses { get; }
    DbSet<Debt> Debts { get; }
    DbSet<Alert> Alerts { get; }
    DbSet<SpendingPattern> SpendingPatterns { get; }
    
    Task<int> SaveChangesAsync(CancellationToken cancellationToken = default);
}
