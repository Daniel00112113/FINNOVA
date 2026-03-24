using FinancialCopilot.Application.Common.Interfaces;
using FinancialCopilot.Domain.Entities;

namespace FinancialCopilot.Infrastructure.Services;

public interface IAuditService
{
    Task LogAsync(string action, string entity, Guid? userId = null,
        string? entityId = null, string? ipAddress = null,
        string? userAgent = null, bool success = true, string? details = null);
}

public class AuditService : IAuditService
{
    private readonly IApplicationDbContext _context;

    public AuditService(IApplicationDbContext context)
    {
        _context = context;
    }

    public async Task LogAsync(string action, string entity, Guid? userId = null,
        string? entityId = null, string? ipAddress = null,
        string? userAgent = null, bool success = true, string? details = null)
    {
        _context.AuditLogs.Add(new AuditLog
        {
            Id = Guid.NewGuid(),
            Action = action,
            Entity = entity,
            UserId = userId,
            EntityId = entityId,
            IpAddress = ipAddress,
            UserAgent = userAgent,
            Success = success,
            Details = details,
            CreatedAt = DateTime.UtcNow
        });

        await _context.SaveChangesAsync();
    }
}
