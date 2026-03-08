namespace FinancialCopilot.Domain.Entities;

public class Expense
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public decimal Amount { get; set; }
    public string Category { get; set; } = string.Empty;
    public DateTime Date { get; set; }
    public string? Description { get; set; }
    
    // Nuevos campos
    public string? Location { get; set; }
    public bool IsRecurring { get; set; }
    public RecurrenceType? RecurrenceType { get; set; }
    public List<string> Tags { get; set; } = new();
    
    public DateTime CreatedAt { get; set; }
    
    public User User { get; set; } = null!;
}

public enum RecurrenceType
{
    Daily,
    Weekly,
    Monthly,
    Yearly
}
