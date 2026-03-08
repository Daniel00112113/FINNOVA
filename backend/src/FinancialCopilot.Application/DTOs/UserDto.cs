namespace FinancialCopilot.Application.DTOs;

public record UserDto(
    Guid Id,
    string Name,
    string Email,
    DateTime CreatedAt
);

public record CreateUserDto(
    string Name,
    string Email,
    string Password
);

public record LoginDto(
    string Email,
    string Password
);
