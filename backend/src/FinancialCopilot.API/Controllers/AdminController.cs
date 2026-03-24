using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FinancialCopilot.Application.Common.Interfaces;

namespace FinancialCopilot.API.Controllers;

[Authorize(Roles = "admin")]
[ApiController]
[Route("api/admin")]
public class AdminController : ControllerBase
{
    private readonly IApplicationDbContext _context;

    public AdminController(IApplicationDbContext context)
    {
        _context = context;
    }

    /// <summary>Métricas globales de la plataforma</summary>
    [HttpGet("metrics")]
    public async Task<IActionResult> GetMetrics()
    {
        var now = DateTime.UtcNow;
        var thirtyDaysAgo = now.AddDays(-30);
        var sevenDaysAgo = now.AddDays(-7);
        var today = now.Date;

        var totalUsers = await _context.Users.CountAsync();
        var activeUsers30d = await _context.Users
            .CountAsync(u => u.LastLoginAt >= thirtyDaysAgo);
        var newUsers7d = await _context.Users
            .CountAsync(u => u.CreatedAt >= sevenDaysAgo);
        var newUsersToday = await _context.Users
            .CountAsync(u => u.CreatedAt >= today);

        var totalExpenses = await _context.Expenses.CountAsync();
        var totalIncomes = await _context.Incomes.CountAsync();
        var totalDebts = await _context.Debts.CountAsync();

        var totalExpenseAmount = await _context.Expenses.SumAsync(e => (decimal?)e.Amount) ?? 0;
        var totalIncomeAmount = await _context.Incomes.SumAsync(i => (decimal?)i.Amount) ?? 0;

        var lockedUsers = await _context.Users
            .CountAsync(u => u.LockedUntil != null && u.LockedUntil > now);

        var usersByRole = await _context.Users
            .GroupBy(u => u.Role)
            .Select(g => new { role = g.Key, count = g.Count() })
            .ToListAsync();

        // Registros por día (últimos 7 días)
        var registrationsByDay = await _context.Users
            .Where(u => u.CreatedAt >= sevenDaysAgo)
            .GroupBy(u => u.CreatedAt.Date)
            .Select(g => new { date = g.Key, count = g.Count() })
            .OrderBy(x => x.date)
            .ToListAsync();

        // Top usuarios por actividad
        var topUsers = await _context.Users
            .OrderByDescending(u => u.LastLoginAt)
            .Take(10)
            .Select(u => new { u.Id, u.Name, u.Email, u.Role, u.LastLoginAt, u.CreatedAt })
            .ToListAsync();

        return Ok(new
        {
            users = new
            {
                total = totalUsers,
                active30d = activeUsers30d,
                newLast7d = newUsers7d,
                newToday = newUsersToday,
                locked = lockedUsers,
                byRole = usersByRole
            },
            transactions = new
            {
                totalExpenses,
                totalIncomes,
                totalDebts,
                totalExpenseAmount,
                totalIncomeAmount,
                netBalance = totalIncomeAmount - totalExpenseAmount
            },
            registrationsByDay,
            topUsers,
            generatedAt = now
        });
    }

    /// <summary>Audit log con filtros</summary>
    [HttpGet("audit-logs")]
    public async Task<IActionResult> GetAuditLogs(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 50,
        [FromQuery] string? action = null,
        [FromQuery] Guid? userId = null,
        [FromQuery] bool? success = null)
    {
        var query = _context.AuditLogs.AsQueryable();

        if (!string.IsNullOrEmpty(action))
            query = query.Where(l => l.Action.Contains(action));
        if (userId.HasValue)
            query = query.Where(l => l.UserId == userId);
        if (success.HasValue)
            query = query.Where(l => l.Success == success);

        var total = await query.CountAsync();
        var logs = await query
            .OrderByDescending(l => l.CreatedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .ToListAsync();

        return Ok(new { total, page, pageSize, logs });
    }

    /// <summary>Lista de usuarios con gestión</summary>
    [HttpGet("users")]
    public async Task<IActionResult> GetUsers(
        [FromQuery] int page = 1,
        [FromQuery] int pageSize = 20,
        [FromQuery] string? search = null,
        [FromQuery] string? role = null)
    {
        var query = _context.Users.AsQueryable();

        if (!string.IsNullOrEmpty(search))
            query = query.Where(u => u.Name.Contains(search) || u.Email.Contains(search));
        if (!string.IsNullOrEmpty(role))
            query = query.Where(u => u.Role == role);

        var total = await query.CountAsync();
        var users = await query
            .OrderByDescending(u => u.CreatedAt)
            .Skip((page - 1) * pageSize)
            .Take(pageSize)
            .Select(u => new
            {
                u.Id, u.Name, u.Email, u.Role, u.CreatedAt,
                u.LastLoginAt, u.FailedLoginAttempts,
                isLocked = u.LockedUntil != null && u.LockedUntil > DateTime.UtcNow
            })
            .ToListAsync();

        return Ok(new { total, page, pageSize, users });
    }

    /// <summary>Cambiar rol de un usuario</summary>
    [HttpPatch("users/{id}/role")]
    public async Task<IActionResult> UpdateRole(Guid id, [FromBody] UpdateRoleDto dto)
    {
        var validRoles = new[] { "user", "admin", "support" };
        if (!validRoles.Contains(dto.Role))
            return BadRequest(new { message = "Rol inválido. Usa: user, admin, support" });

        var user = await _context.Users.FindAsync(id);
        if (user == null) return NotFound();

        user.Role = dto.Role;
        user.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        return Ok(new { message = $"Rol actualizado a {dto.Role}", userId = id });
    }

    /// <summary>Desbloquear cuenta de usuario</summary>
    [HttpPost("users/{id}/unlock")]
    public async Task<IActionResult> UnlockUser(Guid id)
    {
        var user = await _context.Users.FindAsync(id);
        if (user == null) return NotFound();

        user.LockedUntil = null;
        user.FailedLoginAttempts = 0;
        user.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        return Ok(new { message = "Cuenta desbloqueada", userId = id });
    }

    /// <summary>Estado del sistema</summary>
    [HttpGet("system-status")]
    public async Task<IActionResult> GetSystemStatus()
    {
        var recentErrors = await _context.AuditLogs
            .Where(l => !l.Success && l.CreatedAt >= DateTime.UtcNow.AddHours(-24))
            .CountAsync();

        var recentLogins = await _context.AuditLogs
            .Where(l => l.Action == "login" && l.CreatedAt >= DateTime.UtcNow.AddHours(-1))
            .CountAsync();

        var failedLogins24h = await _context.AuditLogs
            .Where(l => l.Action == "login_failed" && l.CreatedAt >= DateTime.UtcNow.AddHours(-24))
            .CountAsync();

        return Ok(new
        {
            status = "healthy",
            recentErrors24h = recentErrors,
            loginsLastHour = recentLogins,
            failedLogins24h,
            timestamp = DateTime.UtcNow
        });
    }
}

public record UpdateRoleDto(string Role);
