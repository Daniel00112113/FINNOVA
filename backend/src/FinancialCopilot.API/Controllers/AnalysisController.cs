using FinancialCopilot.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace FinancialCopilot.API.Controllers;

[Authorize]
[ApiController]
[Route("api/users/{userId}/[controller]")]
public class AnalysisController : ControllerBase
{
    private readonly IAnalysisService _analysisService;

    public AnalysisController(IAnalysisService analysisService)
    {
        _analysisService = analysisService;
    }

    [HttpGet("spending")]
    public async Task<ActionResult<SpendingAnalysisDto>> GetSpendingAnalysis(
        Guid userId,
        [FromQuery] DateTime? startDate = null,
        [FromQuery] DateTime? endDate = null)
    {
        var analysis = await _analysisService.GetSpendingAnalysisAsync(userId, startDate, endDate);
        return Ok(analysis);
    }

    [HttpPost("analyze")]
    public async Task<IActionResult> RunAnalysis(Guid userId)
    {
        await _analysisService.AnalyzeSpendingPatternsAsync(userId);
        await _analysisService.GenerateAlertsAsync(userId);
        return Ok(new { message = "Análisis completado exitosamente" });
    }
}

