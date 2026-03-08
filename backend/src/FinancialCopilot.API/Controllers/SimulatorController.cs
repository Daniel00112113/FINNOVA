using FinancialCopilot.Application.Services;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace FinancialCopilot.API.Controllers;

[Authorize]
[ApiController]
[Route("api/users/{userId}/[controller]")]
public class SimulatorController : ControllerBase
{
    private readonly IAiService _aiService;

    public SimulatorController(IAiService aiService)
    {
        _aiService = aiService;
    }

    [HttpGet]
    public async Task<ActionResult<SimulationResultDto>> SimulateScenarios(
        Guid userId,
        [FromQuery] int months = 12)
    {
        try
        {
            var result = await _aiService.SimulateScenarios(userId, months);
            return Ok(result);
        }
        catch (Exception ex)
        {
            Console.WriteLine($"═══════════════════════════════════════");
            Console.WriteLine($"Simulator Error: {ex.Message}");
            Console.WriteLine($"Stack: {ex.StackTrace}");
            if (ex.InnerException != null)
            {
                Console.WriteLine($"Inner Exception: {ex.InnerException.Message}");
            }
            Console.WriteLine($"═══════════════════════════════════════");
            return StatusCode(500, new { error = ex.Message, details = ex.InnerException?.Message });
        }
    }
}

