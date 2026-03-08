using FinancialCopilot.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace FinancialCopilot.API.Controllers;

[Authorize]
[ApiController]
[Route("api/users/{userId}/[controller]")]
public class PredictionsController : ControllerBase
{
    private readonly IAiService _aiService;

    public PredictionsController(IAiService aiService)
    {
        _aiService = aiService;
    }

    [HttpGet("balance")]
    public async Task<ActionResult<BalancePredictionDto>> PredictBalance(
        Guid userId,
        [FromQuery] int monthsAhead = 3)
    {
        try
        {
            var prediction = await _aiService.PredictBalanceAsync(userId, monthsAhead);
            return Ok(prediction);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }

    [HttpGet("expenses")]
    public async Task<ActionResult<ExpensePredictionDto>> PredictExpenses(
        Guid userId,
        [FromQuery] int monthsAhead = 3)
    {
        try
        {
            var prediction = await _aiService.PredictExpensesAsync(userId, monthsAhead);
            return Ok(prediction);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }

    [HttpGet("risk")]
    public async Task<ActionResult<RiskAnalysisDto>> AnalyzeRisk(Guid userId)
    {
        try
        {
            var analysis = await _aiService.AnalyzeRiskAsync(userId);
            return Ok(analysis);
        }
        catch (Exception ex)
        {
            return StatusCode(500, new { error = ex.Message });
        }
    }
}

