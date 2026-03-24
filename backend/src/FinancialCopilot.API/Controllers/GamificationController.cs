using FinancialCopilot.Application.Common.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using System.Security.Claims;

namespace FinancialCopilot.API.Controllers;

[Authorize]
[ApiController]
[Route("api/users/{userId}/[controller]")]
public class GamificationController : ControllerBase
{
    private readonly IGamificationService _gamificationService;

    public GamificationController(IGamificationService gamificationService)
    {
        _gamificationService = gamificationService;
    }

    [HttpGet("stats")]
    public async Task<IActionResult> GetStats(Guid userId)
    {
        var currentUserId = Guid.Parse(User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? string.Empty);
        if (userId != currentUserId)
        {
            return Forbid();
        }

        var stats = await _gamificationService.GetUserStatsAsync(userId);
        return Ok(stats);
    }

    [HttpPost("activity")]
    public async Task<IActionResult> TrackActivity(Guid userId)
    {
        var currentUserId = Guid.Parse(User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? string.Empty);
        if (userId != currentUserId)
        {
            return Forbid();
        }

        await _gamificationService.UpdateStreakAsync(userId);
        return Ok(new { message = "Activity tracked successfully" });
    }

    [HttpGet("badges")]
    public async Task<IActionResult> GetBadges(Guid userId)
    {
        var currentUserId = Guid.Parse(User.FindFirst(ClaimTypes.NameIdentifier)?.Value ?? string.Empty);
        if (userId != currentUserId)
        {
            return Forbid();
        }

        var badges = await _gamificationService.CheckAndUnlockBadgesAsync(userId);
        return Ok(badges);
    }
}
