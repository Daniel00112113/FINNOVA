namespace FinancialCopilot.Application.DTOs;

public record IncomeDto(
    Guid Id,
    decimal Amount,
    DateTime Date,
    string Type,
    string? Description
);

public record CreateIncomeDto(
    decimal Amount,
    DateTime Date,
    string Type,
    string? Description
);
