using FinancialCopilot.Application.Common.Interfaces;
using FinancialCopilot.Application.DTOs;
using FinancialCopilot.Application.Services;
using Microsoft.EntityFrameworkCore;

namespace FinancialCopilot.Infrastructure.Services;

public class FinancialInsightsService : IFinancialInsightsService
{
    private readonly IApplicationDbContext _context;

    public FinancialInsightsService(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<DailyBudgetDto> GetDailyBudgetAsync(Guid userId)
    {
        var now = DateTime.UtcNow;
        var startOfMonth = new DateTime(now.Year, now.Month, 1, 0, 0, 0, DateTimeKind.Utc);
        var endOfMonth = startOfMonth.AddMonths(1).AddDays(-1);
        var daysInMonth = DateTime.DaysInMonth(now.Year, now.Month);
        var daysRemaining = (endOfMonth - now).Days + 1;

        // Obtener ingresos del mes
        var monthlyIncome = await _context.Incomes
            .Where(i => i.UserId == userId && i.Date >= startOfMonth && i.Date <= endOfMonth)
            .SumAsync(i => i.Amount);

        // Obtener gastos del mes
        var monthlyExpenses = await _context.Expenses
            .Where(e => e.UserId == userId && e.Date >= startOfMonth && e.Date <= endOfMonth)
            .SumAsync(e => e.Amount);

        // Calcular gastos fijos estimados (deudas, suscripciones)
        var fixedExpenses = await _context.Expenses
            .Where(e => e.UserId == userId && e.IsRecurring)
            .SumAsync(e => e.Amount);

        var remainingBudget = monthlyIncome - monthlyExpenses;
        var dailyLimit = daysRemaining > 0 ? remainingBudget / daysRemaining : 0;
        var projectedEndOfMonth = monthlyIncome - (monthlyExpenses + (dailyLimit * daysRemaining));

        // Determinar estado
        string status;
        string message;

        if (dailyLimit < 0)
        {
            status = "Critical";
            message = $"⚠️ ALERTA: Ya excediste tu presupuesto del mes por ${Math.Abs(dailyLimit * daysRemaining):N0}";
        }
        else if (dailyLimit < monthlyIncome * 0.03m) // Menos del 3% del ingreso por día
        {
            status = "Warning";
            message = $"⚠️ Presupuesto ajustado. Limita gastos grandes.";
        }
        else
        {
            status = "Safe";
            message = $"✅ Vas bien. Puedes gastar hasta ${dailyLimit:N0} por día.";
        }

        return new DailyBudgetDto(
            AvailableToday: Math.Max(0, dailyLimit),
            RemainingForPeriod: Math.Max(0, remainingBudget),
            DaysUntilNextIncome: daysRemaining,
            DailyLimit: dailyLimit,
            Status: status,
            Message: message,
            ProjectedEndOfMonth: projectedEndOfMonth
        );
    }

    public async Task<SmallExpensesAnalysisDto> DetectSmallExpensesAsync(Guid userId)
    {
        var thirtyDaysAgo = DateTime.UtcNow.AddDays(-30);
        var now = DateTime.UtcNow;

        // Obtener gastos pequeños (menos de $50,000 por transacción)
        var expenses = await _context.Expenses
            .Where(e => e.UserId == userId && 
                       e.Date >= thirtyDaysAgo && 
                       e.Amount < 50000 &&
                       e.Amount > 1000) // Filtrar gastos muy pequeños
            .ToListAsync();

        // Agrupar por descripción similar y categoría
        var groupedExpenses = expenses
            .GroupBy(e => new { e.Category, Description = NormalizeDescription(e.Description ?? "") })
            .Where(g => g.Count() >= 3) // Al menos 3 ocurrencias
            .Select(g => new
            {
                g.Key.Category,
                g.Key.Description,
                Count = g.Count(),
                TotalAmount = g.Sum(e => e.Amount),
                AvgAmount = g.Average(e => e.Amount)
            })
            .OrderByDescending(g => g.TotalAmount)
            .ToList();

        var smallExpenses = new List<SmallExpenseDto>();
        var monthlyIncome = await _context.Incomes
            .Where(i => i.UserId == userId && i.Date >= thirtyDaysAgo)
            .SumAsync(i => i.Amount);

        foreach (var group in groupedExpenses)
        {
            var monthlyImpact = group.TotalAmount;
            var yearlyImpact = monthlyImpact * 12;
            var occurrencesPerMonth = group.Count;

            // Generar comparación significativa
            var comparison = GenerateComparison(yearlyImpact);
            var recommendation = GenerateRecommendation(group.Category, monthlyImpact, occurrencesPerMonth);

            smallExpenses.Add(new SmallExpenseDto(
                Description: string.IsNullOrEmpty(group.Description) ? group.Category : group.Description,
                Category: group.Category,
                AmountPerOccurrence: group.AvgAmount,
                OccurrencesPerMonth: occurrencesPerMonth,
                MonthlyImpact: monthlyImpact,
                YearlyImpact: yearlyImpact,
                Comparison: comparison,
                Recommendation: recommendation
            ));
        }

        var totalMonthly = smallExpenses.Sum(e => e.MonthlyImpact);
        var totalYearly = totalMonthly * 12;
        var percentageOfIncome = monthlyIncome > 0 ? (totalMonthly / monthlyIncome) * 100 : 0;

        var overallRecommendation = percentageOfIncome > 20
            ? $"⚠️ Los gastos hormiga representan {percentageOfIncome:F1}% de tus ingresos. Reducir estos gastos puede liberar ${totalMonthly * 0.5m:N0}/mes."
            : percentageOfIncome > 10
            ? $"💡 Tienes ${totalMonthly:N0}/mes en gastos pequeños recurrentes. Hay oportunidad de ahorro."
            : $"✅ Tus gastos hormiga están controlados ({percentageOfIncome:F1}% de ingresos).";

        return new SmallExpensesAnalysisDto(
            SmallExpenses: smallExpenses,
            TotalMonthlyImpact: totalMonthly,
            TotalYearlyImpact: totalYearly,
            PercentageOfIncome: percentageOfIncome,
            OverallRecommendation: overallRecommendation
        );
    }

    public async Task<AutomaticAnalysisDto> GetAutomaticAnalysisAsync(Guid userId)
    {
        try
        {
            var now = DateTime.UtcNow;
            var startOfThisMonth = new DateTime(now.Year, now.Month, 1, 0, 0, 0, DateTimeKind.Utc);
            var startOfLastMonth = startOfThisMonth.AddMonths(-1);
            var startOfTwoMonthsAgo = startOfThisMonth.AddMonths(-2);

            // Gastos de este mes
            var thisMonthExpenses = await _context.Expenses
                .Where(e => e.UserId == userId && e.Date >= startOfThisMonth)
                .ToListAsync();

            // Gastos del mes pasado
            var lastMonthExpenses = await _context.Expenses
                .Where(e => e.UserId == userId && 
                           e.Date >= startOfLastMonth && 
                           e.Date < startOfThisMonth)
                .ToListAsync();

            // Gastos de hace 2 meses
            var twoMonthsAgoExpenses = await _context.Expenses
                .Where(e => e.UserId == userId && 
                           e.Date >= startOfTwoMonthsAgo && 
                           e.Date < startOfLastMonth)
                .ToListAsync();

            var totalThisMonth = thisMonthExpenses.Sum(e => e.Amount);
            var totalLastMonth = lastMonthExpenses.Sum(e => e.Amount);
            var totalTwoMonthsAgo = twoMonthsAgoExpenses.Sum(e => e.Amount);

            // Si no hay gastos, retornar análisis vacío
            if (!thisMonthExpenses.Any() && !lastMonthExpenses.Any())
            {
                return new AutomaticAnalysisDto(
                    CategoryBreakdown: new List<CategoryBreakdownDto>(),
                    MonthlyComparison: new List<MonthComparisonDto>(),
                    TotalSpentThisMonth: 0,
                    TotalSpentLastMonth: 0,
                    AverageDailySpending: 0,
                    TopCategory: "N/A",
                    BiggestIncrease: "N/A",
                    KeyInsights: new List<string> { "No hay suficientes datos para generar insights. Registra algunas transacciones." },
                    ActionableRecommendations: new List<string> { "Empieza registrando tus gastos diarios para obtener análisis personalizados." }
                );
            }

            // Análisis por categoría
            var categoryBreakdown = thisMonthExpenses
                .GroupBy(e => e.Category ?? "Sin categoría")
                .Select(g =>
                {
                    var categoryTotal = g.Sum(e => e.Amount);
                    var percentage = totalThisMonth > 0 ? (categoryTotal / totalThisMonth) * 100 : 0;
                    var transactionCount = g.Count();
                    var avgTransaction = transactionCount > 0 ? categoryTotal / transactionCount : 0;

                    // Comparar con mes anterior
                    var lastMonthCategory = lastMonthExpenses
                        .Where(e => (e.Category ?? "Sin categoría") == g.Key)
                        .Sum(e => e.Amount);

                    var changeAmount = categoryTotal - lastMonthCategory;
                    var trend = lastMonthCategory > 0
                        ? (changeAmount / lastMonthCategory) > 0.1m ? "Up" 
                        : (changeAmount / lastMonthCategory) < -0.1m ? "Down" 
                        : "Stable"
                        : "New";

                    var insight = GenerateCategoryInsight(g.Key, percentage, trend, changeAmount);

                    return new CategoryBreakdownDto(
                        Category: g.Key,
                        Amount: categoryTotal,
                        Percentage: percentage,
                        TransactionCount: transactionCount,
                        AverageTransaction: avgTransaction,
                        Trend: trend,
                        ChangeFromLastMonth: changeAmount,
                        Insight: insight
                    );
                })
                .OrderByDescending(c => c.Amount)
                .ToList();

            // Comparación mensual
            var monthlyComparison = new List<MonthComparisonDto>
            {
                new MonthComparisonDto(
                    Month: startOfTwoMonthsAgo.ToString("MMM yyyy"),
                    TotalSpent: totalTwoMonthsAgo,
                    ChangeFromPrevious: 0,
                    PercentageChange: 0
                ),
                new MonthComparisonDto(
                    Month: startOfLastMonth.ToString("MMM yyyy"),
                    TotalSpent: totalLastMonth,
                    ChangeFromPrevious: totalLastMonth - totalTwoMonthsAgo,
                    PercentageChange: totalTwoMonthsAgo > 0 
                        ? ((totalLastMonth - totalTwoMonthsAgo) / totalTwoMonthsAgo) * 100 
                        : 0
                ),
                new MonthComparisonDto(
                    Month: startOfThisMonth.ToString("MMM yyyy"),
                    TotalSpent: totalThisMonth,
                    ChangeFromPrevious: totalThisMonth - totalLastMonth,
                    PercentageChange: totalLastMonth > 0 
                        ? ((totalThisMonth - totalLastMonth) / totalLastMonth) * 100 
                        : 0
                )
            };

            var daysInMonth = (now - startOfThisMonth).Days;
            var avgDaily = daysInMonth > 0 && thisMonthExpenses.Any() 
                ? totalThisMonth / daysInMonth 
                : 0;

            var topCategory = categoryBreakdown.FirstOrDefault()?.Category ?? "N/A";
            var biggestIncrease = categoryBreakdown
                .Where(c => c.ChangeFromLastMonth > 0)
                .OrderByDescending(c => c.ChangeFromLastMonth)
                .FirstOrDefault()?.Category ?? "N/A";

            // Generar insights clave
            var keyInsights = GenerateKeyInsights(
                totalThisMonth, 
                totalLastMonth, 
                categoryBreakdown, 
                avgDaily
            );

            // Generar recomendaciones accionables
            var recommendations = GenerateRecommendations(
                categoryBreakdown, 
                totalThisMonth, 
                totalLastMonth
            );

            return new AutomaticAnalysisDto(
                CategoryBreakdown: categoryBreakdown,
                MonthlyComparison: monthlyComparison,
                TotalSpentThisMonth: totalThisMonth,
                TotalSpentLastMonth: totalLastMonth,
                AverageDailySpending: avgDaily,
                TopCategory: topCategory,
                BiggestIncrease: biggestIncrease,
                KeyInsights: keyInsights,
                ActionableRecommendations: recommendations
            );
        }
        catch (Exception ex)
        {
            // Log the error and return empty analysis
            Console.WriteLine($"Error in GetAutomaticAnalysisAsync: {ex.Message}");
            return new AutomaticAnalysisDto(
                CategoryBreakdown: new List<CategoryBreakdownDto>(),
                MonthlyComparison: new List<MonthComparisonDto>(),
                TotalSpentThisMonth: 0,
                TotalSpentLastMonth: 0,
                AverageDailySpending: 0,
                TopCategory: "N/A",
                BiggestIncrease: "N/A",
                KeyInsights: new List<string> { "Error al generar análisis. Por favor intenta más tarde." },
                ActionableRecommendations: new List<string> { "Verifica que tengas transacciones registradas." }
            );
        }
    }

    public async Task<SubscriptionsAnalysisDto> DetectSubscriptionsAsync(Guid userId)
    {
        var ninetyDaysAgo = DateTime.UtcNow.AddDays(-90);
        
        // Detectar gastos recurrentes
        var recurringExpenses = await _context.Expenses
            .Where(e => e.UserId == userId && 
                       e.IsRecurring && 
                       e.Date >= ninetyDaysAgo)
            .OrderByDescending(e => e.Date)
            .ToListAsync();

        var subscriptions = new List<SubscriptionDto>();
        var processedCategories = new HashSet<string>();

        foreach (var expense in recurringExpenses)
        {
            var key = $"{expense.Category}_{expense.Amount}";
            if (processedCategories.Contains(key)) continue;
            processedCategories.Add(key);

            var daysSinceLastCharge = (DateTime.UtcNow - expense.Date).Days;
            var monthlyAmount = expense.Amount;
            var yearlyAmount = monthlyAmount * 12;

            // Determinar estado basado en uso
            string status;
            string recommendation;

            if (daysSinceLastCharge > 60)
            {
                status = "Unused";
                recommendation = $"⚠️ No has usado esto en {daysSinceLastCharge} días. Considera cancelar y ahorra ${yearlyAmount:N0}/año.";
            }
            else if (daysSinceLastCharge > 30)
            {
                status = "Rarely Used";
                recommendation = $"💡 Uso poco frecuente. Evalúa si realmente lo necesitas.";
            }
            else
            {
                status = "Active";
                recommendation = $"✅ Suscripción activa y en uso.";
            }

            subscriptions.Add(new SubscriptionDto(
                ExpenseId: expense.Id,
                Name: expense.Description ?? expense.Category,
                MonthlyAmount: monthlyAmount,
                YearlyAmount: yearlyAmount,
                LastCharge: expense.Date,
                DaysSinceLastUse: daysSinceLastCharge,
                Status: status,
                Recommendation: recommendation
            ));
        }

        var totalMonthly = subscriptions.Sum(s => s.MonthlyAmount);
        var totalYearly = totalMonthly * 12;
        var unusedCount = subscriptions.Count(s => s.Status == "Unused");
        var potentialSavings = subscriptions
            .Where(s => s.Status == "Unused" || s.Status == "Rarely Used")
            .Sum(s => s.YearlyAmount);

        var overallRecommendation = unusedCount > 0
            ? $"⚠️ Tienes {unusedCount} suscripción(es) sin usar. Cancelándolas ahorras ${potentialSavings:N0}/año."
            : $"✅ Tus suscripciones están activas. Total: ${totalMonthly:N0}/mes.";

        return new SubscriptionsAnalysisDto(
            Subscriptions: subscriptions,
            TotalMonthly: totalMonthly,
            TotalYearly: totalYearly,
            PotentialSavings: potentialSavings,
            UnusedCount: unusedCount,
            Recommendation: overallRecommendation
        );
    }

    public async Task<EmergencyFundDto> GetEmergencyFundPlanAsync(Guid userId)
    {
        var now = DateTime.UtcNow;
        var threeMonthsAgo = now.AddMonths(-3);

        // Calcular gastos esenciales promedio (últimos 3 meses)
        var monthlyExpenses = await _context.Expenses
            .Where(e => e.UserId == userId && e.Date >= threeMonthsAgo)
            .GroupBy(e => new { e.Date.Year, e.Date.Month })
            .Select(g => g.Sum(e => e.Amount))
            .ToListAsync();

        var avgMonthlyExpenses = monthlyExpenses.Any() ? monthlyExpenses.Average() : 0;

        // Calcular ingresos promedio
        var monthlyIncomes = await _context.Incomes
            .Where(i => i.UserId == userId && i.Date >= threeMonthsAgo)
            .GroupBy(i => new { i.Date.Year, i.Date.Month })
            .Select(g => g.Sum(i => i.Amount))
            .ToListAsync();

        var avgMonthlyIncome = monthlyIncomes.Any() ? monthlyIncomes.Average() : 0;

        // Balance actual (simulado como ahorro disponible)
        var totalIncome = await _context.Incomes
            .Where(i => i.UserId == userId)
            .SumAsync(i => i.Amount);

        var totalExpenses = await _context.Expenses
            .Where(e => e.UserId == userId)
            .SumAsync(e => e.Amount);

        var currentAmount = Math.Max(0, totalIncome - totalExpenses);

        // Meta: 3-6 meses de gastos
        var targetMonths = 3;
        var targetAmount = avgMonthlyExpenses * targetMonths;
        var monthsCovered = avgMonthlyExpenses > 0 ? (int)(currentAmount / avgMonthlyExpenses) : 0;
        var progressPercentage = targetAmount > 0 ? (currentAmount / targetAmount) * 100 : 0;

        // Capacidad de ahorro
        var savingCapacity = avgMonthlyIncome - avgMonthlyExpenses;
        var suggestedMonthlySaving = Math.Max(savingCapacity * 0.1m, 10000); // 10% o mínimo $10K
        var suggestedWeeklySaving = suggestedMonthlySaving / 4;

        var monthsToTarget = suggestedMonthlySaving > 0 
            ? (int)Math.Ceiling((targetAmount - currentAmount) / suggestedMonthlySaving)
            : 0;

        // Determinar estado
        string status;
        string message;

        if (monthsCovered == 0)
        {
            status = "None";
            message = "No tienes fondo de emergencia. ¡Empieza hoy!";
        }
        else if (monthsCovered < 1)
        {
            status = "Building";
            message = $"Tienes {progressPercentage:F0}% de tu meta. ¡Sigue así!";
        }
        else if (monthsCovered < 3)
        {
            status = "Building";
            message = $"Cubres {monthsCovered} mes(es). Meta: {targetMonths} meses.";
        }
        else if (monthsCovered < 6)
        {
            status = "Adequate";
            message = $"¡Bien! Cubres {monthsCovered} meses de gastos.";
        }
        else
        {
            status = "Strong";
            message = $"¡Excelente! Tienes {monthsCovered} meses cubiertos.";
        }

        var microSavingTips = new List<string>
        {
            "Redondea tus compras al múltiplo de $1,000 y ahorra la diferencia",
            "Ahorra 10% de cada ingreso extra (bonos, regalos)",
            "Transfiere automáticamente cada quincena",
            "Cancela una suscripción y destina ese dinero al fondo",
            "Reduce un gasto hormiga y ahorra esa cantidad"
        };

        return new EmergencyFundDto(
            CurrentAmount: currentAmount,
            TargetAmount: targetAmount,
            MonthlyExpenses: avgMonthlyExpenses,
            MonthsCovered: monthsCovered,
            TargetMonths: targetMonths,
            ProgressPercentage: Math.Min(100, progressPercentage),
            SuggestedWeeklySaving: suggestedWeeklySaving,
            SuggestedMonthlySaving: suggestedMonthlySaving,
            MonthsToTarget: Math.Max(0, monthsToTarget),
            MicroSavingTips: microSavingTips,
            Status: status,
            Message: message
        );
    }

    public async Task<AlertsDto> GetSmartAlertsAsync(Guid userId)
    {
        var alerts = new List<AlertDto>();
        var now = DateTime.UtcNow;
        var startOfMonth = new DateTime(now.Year, now.Month, 1, 0, 0, 0, DateTimeKind.Utc);

        // Obtener datos necesarios
        var dailyBudget = await GetDailyBudgetAsync(userId);
        var subscriptions = await DetectSubscriptionsAsync(userId);
        var smallExpenses = await DetectSmallExpensesAsync(userId);

        // ALERTAS PREVENTIVAS
        if (dailyBudget.Status == "Critical")
        {
            alerts.Add(new AlertDto(
                Type: "Preventive",
                Severity: "Critical",
                Title: "⚠️ Presupuesto Excedido",
                Message: $"Ya excediste tu presupuesto del mes. Evita gastos no esenciales.",
                Icon: "⚠️",
                ActionLabel: "Ver Presupuesto",
                ActionUrl: "/insights?tab=budget",
                CreatedAt: now
            ));
        }
        else if (dailyBudget.Status == "Warning")
        {
            alerts.Add(new AlertDto(
                Type: "Preventive",
                Severity: "Warning",
                Title: "⚠️ Presupuesto Ajustado",
                Message: $"Solo puedes gastar ${dailyBudget.AvailableToday:N0} hoy para llegar a fin de mes.",
                Icon: "⚠️",
                ActionLabel: "Ver Detalles",
                ActionUrl: "/insights?tab=budget",
                CreatedAt: now
            ));
        }

        // Alerta de gastos hormiga
        if (smallExpenses.PercentageOfIncome > 15)
        {
            alerts.Add(new AlertDto(
                Type: "Preventive",
                Severity: "Warning",
                Title: "🐜 Gastos Hormiga Detectados",
                Message: $"Gastos pequeños suman ${smallExpenses.TotalMonthlyImpact:N0}/mes ({smallExpenses.PercentageOfIncome:F0}% de ingresos).",
                Icon: "🐜",
                ActionLabel: "Ver Gastos Hormiga",
                ActionUrl: "/insights?tab=small",
                CreatedAt: now
            ));
        }

        // ALERTAS ACCIONABLES
        if (subscriptions.UnusedCount > 0)
        {
            alerts.Add(new AlertDto(
                Type: "Actionable",
                Severity: "Info",
                Title: "💡 Suscripciones Sin Usar",
                Message: $"Tienes {subscriptions.UnusedCount} suscripción(es) sin usar. Ahorro potencial: ${subscriptions.PotentialSavings:N0}/año.",
                Icon: "💡",
                ActionLabel: "Ver Suscripciones",
                ActionUrl: "/insights?tab=subscriptions",
                CreatedAt: now
            ));
        }

        // Alerta de fondo de emergencia
        var emergencyFund = await GetEmergencyFundPlanAsync(userId);
        if (emergencyFund.Status == "None" || emergencyFund.Status == "Building")
        {
            alerts.Add(new AlertDto(
                Type: "Actionable",
                Severity: "Info",
                Title: "🚨 Fondo de Emergencia",
                Message: emergencyFund.Status == "None" 
                    ? "No tienes fondo de emergencia. Empieza con $10,000/semana."
                    : $"Tienes {emergencyFund.ProgressPercentage:F0}% de tu meta. ¡Sigue así!",
                Icon: "🚨",
                ActionLabel: "Ver Plan",
                ActionUrl: "/insights?tab=emergency",
                CreatedAt: now
            ));
        }

        // ALERTAS POSITIVAS
        if (dailyBudget.Status == "Safe" && dailyBudget.ProjectedEndOfMonth > 0)
        {
            alerts.Add(new AlertDto(
                Type: "Positive",
                Severity: "Success",
                Title: "✅ Vas Excelente",
                Message: $"Llevas buen ritmo. Proyección de ahorro este mes: ${dailyBudget.ProjectedEndOfMonth:N0}.",
                Icon: "✅",
                ActionLabel: "Ver Progreso",
                ActionUrl: "/insights",
                CreatedAt: now
            ));
        }

        // Contar por tipo
        var preventiveCount = alerts.Count(a => a.Type == "Preventive");
        var positiveCount = alerts.Count(a => a.Type == "Positive");
        var actionableCount = alerts.Count(a => a.Type == "Actionable");

        return new AlertsDto(
            Alerts: alerts.OrderByDescending(a => a.Severity == "Critical" ? 3 : a.Severity == "Warning" ? 2 : 1).ToList(),
            PreventiveCount: preventiveCount,
            PositiveCount: positiveCount,
            ActionableCount: actionableCount
        );
    }

    // Helper methods
    private string NormalizeDescription(string description)
    {
        return description.ToLower().Trim();
    }

    private string GenerateComparison(decimal yearlyAmount)
    {
        if (yearlyAmount >= 1000000)
            return $"Equivale a ${yearlyAmount / 1000000:F1}M al año";
        else if (yearlyAmount >= 500000)
            return "Equivale a un viaje familiar";
        else if (yearlyAmount >= 200000)
            return "Equivale a 2-3 meses de servicios";
        else
            return $"${yearlyAmount:N0} al año";
    }

    private string GenerateRecommendation(string category, decimal monthlyImpact, int occurrences)
    {
        if (category.Contains("Café") || category.Contains("Coffee") || category.Contains("Comida"))
        {
            return $"💡 Reducir a {occurrences / 2} veces/mes ahorra ${monthlyImpact * 0.5m:N0}/mes";
        }
        else if (category.Contains("Transporte") || category.Contains("Uber"))
        {
            return $"💡 Considera alternativas de transporte para ahorrar ${monthlyImpact * 0.3m:N0}/mes";
        }
        else
        {
            return $"💡 Evalúa si puedes reducir frecuencia o buscar alternativas más económicas";
        }
    }

    private string GenerateCategoryInsight(string category, decimal percentage, string trend, decimal change)
    {
        if (percentage > 30)
            return $"⚠️ {category} representa {percentage:F1}% de tus gastos. Es tu mayor categoría.";
        else if (trend == "Up" && change > 50000)
            return $"📈 {category} aumentó ${change:N0} vs mes anterior.";
        else if (trend == "Down" && change < -50000)
            return $"📉 {category} disminuyó ${Math.Abs(change):N0} vs mes anterior. ¡Bien hecho!";
        else
            return $"✅ {category} se mantiene estable.";
    }

    private List<string> GenerateKeyInsights(
        decimal totalThisMonth, 
        decimal totalLastMonth, 
        List<CategoryBreakdownDto> categories,
        decimal avgDaily)
    {
        var insights = new List<string>();

        // Insight 1: Comparación mensual
        var monthChange = totalThisMonth - totalLastMonth;
        if (Math.Abs(monthChange) > 50000)
        {
            if (monthChange > 0)
                insights.Add($"📈 Gastaste ${monthChange:N0} MÁS que el mes pasado ({((monthChange / totalLastMonth) * 100):F1}% más)");
            else
                insights.Add($"📉 Gastaste ${Math.Abs(monthChange):N0} MENOS que el mes pasado. ¡Excelente!");
        }

        // Insight 2: Categoría dominante
        var topCategory = categories.FirstOrDefault();
        if (topCategory != null && topCategory.Percentage > 25)
        {
            insights.Add($"🎯 {topCategory.Category} es tu mayor gasto: ${topCategory.Amount:N0} ({topCategory.Percentage:F1}%)");
        }

        // Insight 3: Promedio diario
        insights.Add($"💰 Promedio diario: ${avgDaily:N0}/día");

        return insights;
    }

    private List<string> GenerateRecommendations(
        List<CategoryBreakdownDto> categories,
        decimal totalThisMonth,
        decimal totalLastMonth)
    {
        var recommendations = new List<string>();

        // Recomendación 1: Categoría más alta
        var topCategory = categories.FirstOrDefault();
        if (topCategory != null && topCategory.Percentage > 30)
        {
            recommendations.Add($"💡 Reduce {topCategory.Category} en 20% y ahorra ${topCategory.Amount * 0.2m:N0}/mes");
        }

        // Recomendación 2: Mayor aumento
        var biggestIncrease = categories
            .Where(c => c.ChangeFromLastMonth > 50000)
            .OrderByDescending(c => c.ChangeFromLastMonth)
            .FirstOrDefault();

        if (biggestIncrease != null)
        {
            recommendations.Add($"⚠️ {biggestIncrease.Category} aumentó ${biggestIncrease.ChangeFromLastMonth:N0}. Revisa qué cambió.");
        }

        // Recomendación 3: General
        if (totalThisMonth > totalLastMonth * 1.2m)
        {
            recommendations.Add($"🎯 Tus gastos aumentaron significativamente. Establece un límite diario.");
        }

        return recommendations;
    }
}
