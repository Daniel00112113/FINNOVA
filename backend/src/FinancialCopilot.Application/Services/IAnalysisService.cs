namespace FinancialCopilot.Application.Services;

public interface IAnalysisService
{
    Task AnalyzeSpendingPatternsAsync(Guid userId);
    Task GenerateAlertsAsync(Guid userId);
    Task<SpendingAnalysisDto> GetSpendingAnalysisAsync(Guid userId, DateTime? startDate = null, DateTime? endDate = null);
}

public record SpendingAnalysisDto(
    Dictionary<string, decimal> SpendingByCategory,
    Dictionary<string, decimal> MonthlyTrends,
    List<CategoryInsight> Insights,
    decimal AverageDailySpending,
    string TopCategory
);

public record CategoryInsight(
    string Category,
    decimal Amount,
    decimal PercentageOfTotal,
    string Trend,
    string Recommendation
);
