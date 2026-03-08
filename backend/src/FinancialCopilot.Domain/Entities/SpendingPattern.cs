namespace FinancialCopilot.Domain.Entities;

public class SpendingPattern
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string Category { get; set; } = string.Empty;
    public decimal AverageMonthly { get; set; }
    public decimal CurrentMonth { get; set; }
    public decimal PercentageChange { get; set; }
    public string Trend { get; set; } = string.Empty; // Increasing, Decreasing, Stable
    public DateTime AnalyzedAt { get; set; }
    
    public User User { get; set; } = null!;
}
