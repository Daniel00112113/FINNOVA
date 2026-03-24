namespace FinancialCopilot.Domain.Entities;

public class Achievement
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public User User { get; set; } = null!;
    
    public string Type { get; set; } = string.Empty; // expense_logged, goal_reached, etc.
    public int PointsEarned { get; set; }
    public string? Description { get; set; }
    
    public DateTime CreatedAt { get; set; }
}
