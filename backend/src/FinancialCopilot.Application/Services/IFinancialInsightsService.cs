using FinancialCopilot.Application.DTOs;

namespace FinancialCopilot.Application.Services;

public interface IFinancialInsightsService
{
    /// <summary>
    /// Calcula el presupuesto diario disponible basado en ingresos y gastos
    /// </summary>
    Task<DailyBudgetDto> GetDailyBudgetAsync(Guid userId);
    
    /// <summary>
    /// Detecta gastos pequeños recurrentes (gastos hormiga)
    /// </summary>
    Task<SmallExpensesAnalysisDto> DetectSmallExpensesAsync(Guid userId);
    
    /// <summary>
    /// Análisis automático completo de gastos con insights
    /// </summary>
    Task<AutomaticAnalysisDto> GetAutomaticAnalysisAsync(Guid userId);
    
    /// <summary>
    /// Detecta suscripciones recurrentes y su uso
    /// </summary>
    Task<SubscriptionsAnalysisDto> DetectSubscriptionsAsync(Guid userId);
    
    /// <summary>
    /// Calcula el plan de fondo de emergencia
    /// </summary>
    Task<EmergencyFundDto> GetEmergencyFundPlanAsync(Guid userId);
    
    /// <summary>
    /// Genera alertas inteligentes personalizadas
    /// </summary>
    Task<AlertsDto> GetSmartAlertsAsync(Guid userId);
}
