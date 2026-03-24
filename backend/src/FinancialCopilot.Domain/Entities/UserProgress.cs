namespace FinancialCopilot.Domain.Entities;

public class UserProgress
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public User User { get; set; } = null!;
    
    public int Points { get; set; }
    public int Level { get; set; } = 1;
    public int CurrentStreak { get; set; }
    public int LongestStreak { get; set; }
    public DateTime LastActivityDate { get; set; }
    public int TotalLogins { get; set; }
    
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}
