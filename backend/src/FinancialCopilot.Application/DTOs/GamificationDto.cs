namespace FinancialCopilot.Application.DTOs;

public class UserProgressDto
{
    public int Points { get; set; }
    public int Level { get; set; }
    public int CurrentStreak { get; set; }
    public int LongestStreak { get; set; }
    public int TotalLogins { get; set; }
    public DateTime LastActivityDate { get; set; }
    public int PointsToNextLevel { get; set; }
    public int ProgressPercentage { get; set; }
}

public class AchievementDto
{
    public string Type { get; set; } = string.Empty;
    public int PointsEarned { get; set; }
    public string? Description { get; set; }
    public DateTime CreatedAt { get; set; }
}

public class GamificationStatsDto
{
    public UserProgressDto Progress { get; set; } = null!;
    public List<AchievementDto> RecentAchievements { get; set; } = new();
    public List<string> UnlockedBadges { get; set; } = new();
    public string MotivationalMessage { get; set; } = string.Empty;
}
