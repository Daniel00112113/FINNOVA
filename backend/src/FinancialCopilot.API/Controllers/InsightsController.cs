using FinancialCopilot.Application.DTOs;
using FinancialCopilot.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace FinancialCopilot.API.Controllers;

[Authorize]
[ApiController]
[Route("api/users/{userId}/[controller]")]
public class InsightsController : ControllerBase
{
    private readonly IFinancialInsightsService _insightsService;

    public InsightsController(IFinancialInsightsService insightsService)
    {
        _insightsService = insightsService;
    }

    /// <summary>
    /// Obtiene el presupuesto diario disponible
    /// </summary>
    [HttpGet("daily-budget")]
    public async Task<ActionResult<DailyBudgetDto>> GetDailyBudget(Guid userId)
    {
        try
        {
            var budget = await _insightsService.GetDailyBudgetAsync(userId);
            return Ok(budget);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }

    /// <summary>
    /// Detecta gastos hormiga (pequeños gastos recurrentes)
    /// </summary>
    [HttpGet("small-expenses")]
    public async Task<ActionResult<SmallExpensesAnalysisDto>> GetSmallExpenses(Guid userId)
    {
        try
        {
            var analysis = await _insightsService.DetectSmallExpensesAsync(userId);
            return Ok(analysis);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }

    /// <summary>
    /// Obtiene análisis automático completo de gastos
    /// </summary>
    [HttpGet("automatic-analysis")]
    public async Task<ActionResult<AutomaticAnalysisDto>> GetAutomaticAnalysis(Guid userId)
    {
        try
        {
            var analysis = await _insightsService.GetAutomaticAnalysisAsync(userId);
            return Ok(analysis);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }

    /// <summary>
    /// Detecta suscripciones recurrentes y su uso
    /// </summary>
    [HttpGet("subscriptions")]
    public async Task<ActionResult<SubscriptionsAnalysisDto>> GetSubscriptions(Guid userId)
    {
        try
        {
            var analysis = await _insightsService.DetectSubscriptionsAsync(userId);
            return Ok(analysis);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }

    /// <summary>
    /// Obtiene el plan de fondo de emergencia
    /// </summary>
    [HttpGet("emergency-fund")]
    public async Task<ActionResult<EmergencyFundDto>> GetEmergencyFund(Guid userId)
    {
        try
        {
            var plan = await _insightsService.GetEmergencyFundPlanAsync(userId);
            return Ok(plan);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }

    /// <summary>
    /// Obtiene alertas inteligentes personalizadas
    /// </summary>
    [HttpGet("alerts")]
    public async Task<ActionResult<AlertsDto>> GetAlerts(Guid userId)
    {
        try
        {
            var alerts = await _insightsService.GetSmartAlertsAsync(userId);
            return Ok(alerts);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }

    /// <summary>
    /// Obtiene todos los insights en una sola llamada
    /// </summary>
    [HttpGet("all")]
    public async Task<ActionResult<object>> GetAllInsights(Guid userId)
    {
        try
        {
            var dailyBudget = await _insightsService.GetDailyBudgetAsync(userId);
            var smallExpenses = await _insightsService.DetectSmallExpensesAsync(userId);
            var automaticAnalysis = await _insightsService.GetAutomaticAnalysisAsync(userId);
            var subscriptions = await _insightsService.DetectSubscriptionsAsync(userId);
            var emergencyFund = await _insightsService.GetEmergencyFundPlanAsync(userId);
            var alerts = await _insightsService.GetSmartAlertsAsync(userId);

            return Ok(new
            {
                dailyBudget,
                smallExpenses,
                automaticAnalysis,
                subscriptions,
                emergencyFund,
                alerts
            });
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }
}

