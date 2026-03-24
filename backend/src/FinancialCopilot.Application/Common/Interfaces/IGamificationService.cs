using FinancialCopilot.Application.DTOs;

namespace FinancialCopilot.Application.Common.Interfaces;

public interface IGamificationService
{
    Task<GamificationStatsDto> GetUserStatsAsync(Guid userId);
    Task UpdateStreakAsync(Guid userId);
    Task AddPointsAsync(Guid userId, int points, string reason, string? description = null);
    Task<List<string>> CheckAndUnlockBadgesAsync(Guid userId);
}
