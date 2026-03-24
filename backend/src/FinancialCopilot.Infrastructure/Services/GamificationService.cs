using FinancialCopilot.Application.Common.Interfaces;
using FinancialCopilot.Application.DTOs;
using FinancialCopilot.Domain.Entities;
using FinancialCopilot.Infrastructure.Data;
using Microsoft.EntityFrameworkCore;

namespace FinancialCopilot.Infrastructure.Services;

public class GamificationService : IGamificationService
{
    private readonly ApplicationDbContext _context;

    public GamificationService(ApplicationDbContext context)
    {
        _context = context;
    }

    public async Task<GamificationStatsDto> GetUserStatsAsync(Guid userId)
    {
        var progress = await GetOrCreateProgressAsync(userId);
        var recentAchievements = await _context.Achievements
            .Where(a => a.UserId == userId)
            .OrderByDescending(a => a.CreatedAt)
            .Take(5)
            .Select(a => new AchievementDto
            {
                Type = a.Type,
                PointsEarned = a.PointsEarned,
                Description = a.Description,
                CreatedAt = a.CreatedAt
            })
            .ToListAsync();

        var badges = await GetUnlockedBadgesAsync(userId, progress);
        var motivationalMessage = GetMotivationalMessage(progress);

        var pointsForNextLevel = CalculatePointsForLevel(progress.Level + 1);
        var pointsInCurrentLevel = progress.Points - CalculatePointsForLevel(progress.Level);
        var pointsNeeded = pointsForNextLevel - CalculatePointsForLevel(progress.Level);
        var progressPercentage = pointsNeeded > 0 ? (int)((pointsInCurrentLevel / (double)pointsNeeded) * 100) : 0;

        return new GamificationStatsDto
        {
            Progress = new UserProgressDto
            {
                Points = progress.Points,
                Level = progress.Level,
                CurrentStreak = progress.CurrentStreak,
                LongestStreak = progress.LongestStreak,
                TotalLogins = progress.TotalLogins,
                LastActivityDate = progress.LastActivityDate,
                PointsToNextLevel = pointsForNextLevel - progress.Points,
                ProgressPercentage = progressPercentage
            },
            RecentAchievements = recentAchievements,
            UnlockedBadges = badges,
            MotivationalMessage = motivationalMessage
        };
    }

    public async Task UpdateStreakAsync(Guid userId)
    {
        var progress = await GetOrCreateProgressAsync(userId);
        var today = DateTime.UtcNow.Date;
        var lastActivity = progress.LastActivityDate.Date;
        var daysSince = (today - lastActivity).Days;

        if (daysSince == 0)
        {
            // Same day, just update login count
            progress.TotalLogins++;
        }
        else if (daysSince == 1)
        {
            // Consecutive day - increase streak
            progress.CurrentStreak++;
            if (progress.CurrentStreak > progress.LongestStreak)
            {
                progress.LongestStreak = progress.CurrentStreak;
            }
            progress.LastActivityDate = DateTime.UtcNow;
            progress.TotalLogins++;

            // Award streak milestone points
            if (progress.CurrentStreak == 7)
            {
                await AddPointsAsync(userId, 100, "streak_7_days", "¡7 días consecutivos! 🔥");
            }
            else if (progress.CurrentStreak == 30)
            {
                await AddPointsAsync(userId, 500, "streak_30_days", "¡30 días consecutivos! ⚡");
            }
        }
        else
        {
            // Streak broken
            progress.CurrentStreak = 1;
            progress.LastActivityDate = DateTime.UtcNow;
            progress.TotalLogins++;
        }

        progress.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();
    }

    public async Task AddPointsAsync(Guid userId, int points, string reason, string? description = null)
    {
        var progress = await GetOrCreateProgressAsync(userId);
        var oldLevel = progress.Level;

        progress.Points += points;
        progress.Level = CalculateLevel(progress.Points);
        progress.UpdatedAt = DateTime.UtcNow;

        // Log achievement
        var achievement = new Achievement
        {
            Id = Guid.NewGuid(),
            UserId = userId,
            Type = reason,
            PointsEarned = points,
            Description = description,
            CreatedAt = DateTime.UtcNow
        };
        _context.Achievements.Add(achievement);

        // Check for level up
        if (progress.Level > oldLevel)
        {
            var levelUpAchievement = new Achievement
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                Type = "level_up",
                PointsEarned = 0,
                Description = $"¡Subiste al nivel {progress.Level}! 🎉",
                CreatedAt = DateTime.UtcNow
            };
            _context.Achievements.Add(levelUpAchievement);
        }

        await _context.SaveChangesAsync();
    }

    public async Task<List<string>> CheckAndUnlockBadgesAsync(Guid userId)
    {
        var progress = await GetOrCreateProgressAsync(userId);
        return await GetUnlockedBadgesAsync(userId, progress);
    }

    private async Task<UserProgress> GetOrCreateProgressAsync(Guid userId)
    {
        var progress = await _context.UserProgress
            .FirstOrDefaultAsync(p => p.UserId == userId);

        if (progress == null)
        {
            progress = new UserProgress
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                Points = 0,
                Level = 1,
                CurrentStreak = 1,
                LongestStreak = 1,
                LastActivityDate = DateTime.UtcNow,
                TotalLogins = 1,
                CreatedAt = DateTime.UtcNow,
                UpdatedAt = DateTime.UtcNow
            };
            _context.UserProgress.Add(progress);
            await _context.SaveChangesAsync();
        }

        return progress;
    }

    private int CalculateLevel(int points)
    {
        // Level formula: Level = floor(sqrt(points / 100)) + 1
        return (int)Math.Floor(Math.Sqrt(points / 100.0)) + 1;
    }

    private int CalculatePointsForLevel(int level)
    {
        // Inverse: points = (level - 1)^2 * 100
        return (int)Math.Pow(level - 1, 2) * 100;
    }

    private async Task<List<string>> GetUnlockedBadgesAsync(Guid userId, UserProgress progress)
    {
        var badges = new List<string>();
        
        // Count user activities
        var expenseCount = await _context.Expenses.CountAsync(e => e.UserId == userId);
        var incomeCount = await _context.Incomes.CountAsync(i => i.UserId == userId);
        var debtCount = await _context.Debts.CountAsync(d => d.UserId == userId);

        // Streak badges
        if (progress.CurrentStreak >= 1) badges.Add("🎯 Primer Paso");
        if (progress.CurrentStreak >= 7) badges.Add("🔥 Racha de Fuego");
        if (progress.CurrentStreak >= 30) badges.Add("⚡ Imparable");

        // Activity badges
        if (expenseCount >= 10) badges.Add("📝 Registrador");
        if (expenseCount >= 50) badges.Add("🎯 Cazador de Gastos");
        if (expenseCount >= 100) badges.Add("🏆 Maestro del Registro");

        // Level badges
        if (progress.Level >= 5) badges.Add("⭐ Novato Avanzado");
        if (progress.Level >= 10) badges.Add("💎 Experto Financiero");

        // Points badges
        if (progress.Points >= 500) badges.Add("💰 Ahorrador Novato");
        if (progress.Points >= 2000) badges.Add("💵 Ahorrador Experto");

        return badges;
    }

    private string GetMotivationalMessage(UserProgress progress)
    {
        var messages = new List<string>();

        if (progress.CurrentStreak >= 7)
        {
            messages.Add($"¡Increíble! Llevas {progress.CurrentStreak} días consecutivos 🔥");
        }
        else if (progress.CurrentStreak >= 3)
        {
            messages.Add($"¡Vas muy bien! {progress.CurrentStreak} días seguidos 💪");
        }
        else
        {
            messages.Add("¡Sigue así! Cada día cuenta 🎯");
        }

        if (progress.Level >= 10)
        {
            messages.Add("Eres un experto financiero 💎");
        }
        else if (progress.Level >= 5)
        {
            messages.Add("¡Estás progresando genial! ⭐");
        }

        return messages[new Random().Next(messages.Count)];
    }
}
