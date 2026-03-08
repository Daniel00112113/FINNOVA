namespace FinancialCopilot.Application.DTOs;

public record ExpenseDto(
    Guid Id,
    decimal Amount,
    string Category,
    DateTime Date,
    string? Description,
    string? Location,
    bool IsRecurring,
    string? RecurrenceType,
    List<string> Tags
);

public record CreateExpenseDto(
    decimal Amount,
    string Category,
    DateTime Date,
    string? Description,
    string? Location = null,
    bool IsRecurring = false,
    string? RecurrenceType = null,
    List<string>? Tags = null
);
