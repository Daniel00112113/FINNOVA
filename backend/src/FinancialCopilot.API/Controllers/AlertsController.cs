using FinancialCopilot.Application.Common.Interfaces;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinancialCopilot.API.Controllers;

[Authorize]
[ApiController]
[Route("api/users/{userId}/[controller]")]
public class AlertsController : ControllerBase
{
    private readonly IApplicationDbContext _context;

    public AlertsController(IApplicationDbContext context)
    {
        _context = context;
    }

    [HttpGet]
    public async Task<ActionResult<List<AlertDto>>> GetAlerts(Guid userId)
    {
        var alerts = await _context.Alerts
            .Where(a => a.UserId == userId)
            .OrderByDescending(a => a.CreatedAt)
            .Select(a => new AlertDto(
                a.Id,
                a.Type,
                a.Severity,
                a.Message,
                a.Details,
                a.IsRead,
                a.CreatedAt
            ))
            .ToListAsync();

        return Ok(alerts);
    }

    [HttpPut("{alertId}/read")]
    public async Task<IActionResult> MarkAsRead(Guid userId, Guid alertId)
    {
        var alert = await _context.Alerts
            .FirstOrDefaultAsync(a => a.Id == alertId && a.UserId == userId);

        if (alert == null)
            return NotFound();

        alert.IsRead = true;
        await _context.SaveChangesAsync();

        return NoContent();
    }

    [HttpDelete("{alertId}")]
    public async Task<IActionResult> DeleteAlert(Guid userId, Guid alertId)
    {
        var alert = await _context.Alerts
            .FirstOrDefaultAsync(a => a.Id == alertId && a.UserId == userId);

        if (alert == null)
            return NotFound();

        _context.Alerts.Remove(alert);
        await _context.SaveChangesAsync();

        return NoContent();
    }
}

public record AlertDto(
    Guid Id,
    string Type,
    string Severity,
    string Message,
    string? Details,
    bool IsRead,
    DateTime CreatedAt
);

