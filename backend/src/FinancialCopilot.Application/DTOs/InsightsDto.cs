namespace FinancialCopilot.Application.DTOs;

// 1. PRESUPUESTO DIARIO INTELIGENTE
public record DailyBudgetDto(
    decimal AvailableToday,
    decimal RemainingForPeriod,
    int DaysUntilNextIncome,
    decimal DailyLimit,
    string Status, // "Safe", "Warning", "Critical"
    string Message,
    decimal ProjectedEndOfMonth
);

// 2. DETECTOR DE GASTOS HORMIGA
public record SmallExpenseDto(
    string Description,
    string Category,
    decimal AmountPerOccurrence,
    int OccurrencesPerMonth,
    decimal MonthlyImpact,
    decimal YearlyImpact,
    string Comparison,
    string Recommendation
);

public record SmallExpensesAnalysisDto(
    List<SmallExpenseDto> SmallExpenses,
    decimal TotalMonthlyImpact,
    decimal TotalYearlyImpact,
    decimal PercentageOfIncome,
    string OverallRecommendation
);

// 3. ANÁLISIS AUTOMÁTICO DE GASTOS
public record CategoryBreakdownDto(
    string Category,
    decimal Amount,
    decimal Percentage,
    int TransactionCount,
    decimal AverageTransaction,
    string Trend, // "Up", "Down", "Stable"
    decimal ChangeFromLastMonth,
    string Insight
);

public record MonthComparisonDto(
    string Month,
    decimal TotalSpent,
    decimal ChangeFromPrevious,
    decimal PercentageChange
);

public record AutomaticAnalysisDto(
    List<CategoryBreakdownDto> CategoryBreakdown,
    List<MonthComparisonDto> MonthlyComparison,
    decimal TotalSpentThisMonth,
    decimal TotalSpentLastMonth,
    decimal AverageDailySpending,
    string TopCategory,
    string BiggestIncrease,
    List<string> KeyInsights,
    List<string> ActionableRecommendations
);

// DTO para suscripciones recurrentes
public record SubscriptionDto(
    Guid ExpenseId,
    string Name,
    decimal MonthlyAmount,
    decimal YearlyAmount,
    DateTime LastCharge,
    int DaysSinceLastUse,
    string Status, // "Active", "Unused", "Rarely Used"
    string Recommendation
);

public record SubscriptionsAnalysisDto(
    List<SubscriptionDto> Subscriptions,
    decimal TotalMonthly,
    decimal TotalYearly,
    decimal PotentialSavings,
    int UnusedCount,
    string Recommendation
);

// 4. PLAN DE FONDO DE EMERGENCIA
public record EmergencyFundDto(
    decimal CurrentAmount,
    decimal TargetAmount,
    decimal MonthlyExpenses,
    int MonthsCovered,
    int TargetMonths,
    decimal ProgressPercentage,
    decimal SuggestedWeeklySaving,
    decimal SuggestedMonthlySaving,
    int MonthsToTarget,
    List<string> MicroSavingTips,
    string Status, // "None", "Building", "Adequate", "Strong"
    string Message
);

// 5. ALERTAS INTELIGENTES
public record AlertDto(
    string Type, // "Preventive", "Positive", "Actionable"
    string Severity, // "Info", "Warning", "Critical", "Success"
    string Title,
    string Message,
    string Icon,
    string ActionLabel,
    string ActionUrl,
    DateTime CreatedAt
);

public record AlertsDto(
    List<AlertDto> Alerts,
    int PreventiveCount,
    int PositiveCount,
    int ActionableCount
);
