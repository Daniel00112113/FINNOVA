namespace FinancialCopilot.Domain.Entities;

public class Alert
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string Type { get; set; } = string.Empty; // HighSpending, LowBalance, DebtWarning
    public string Severity { get; set; } = string.Empty; // Info, Warning, Critical
    public string Message { get; set; } = string.Empty;
    public string? Details { get; set; }
    public bool IsRead { get; set; }
    public DateTime CreatedAt { get; set; }
    
    public User User { get; set; } = null!;
}
