using FinancialCopilot.Application.Common.Interfaces;
using FinancialCopilot.Application.DTOs;
using FinancialCopilot.Domain.Entities;
using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinancialCopilot.API.Controllers;

[Authorize]
[ApiController]
[Route("api/users/{userId}/[controller]")]
public class DebtsController : ControllerBase
{
    private readonly IApplicationDbContext _context;

    public DebtsController(IApplicationDbContext context)
    {
        _context = context;
    }

    [HttpPost]
    public async Task<ActionResult<DebtDto>> Create(Guid userId, CreateDebtDto dto)
    {
        try
        {
            var user = await _context.Users.FindAsync(userId);
            if (user == null)
                return NotFound("User not found");

            var debt = new Debt
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                TotalAmount = dto.TotalAmount,
                RemainingAmount = dto.TotalAmount, // Inicialmente es el total
                InterestRate = dto.InterestRate,
                StartDate = DateTime.UtcNow,
                EndDate = null,
                Description = dto.Description,
                CreatedAt = DateTime.UtcNow
            };

            _context.Debts.Add(debt);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById), new { userId, id = debt.Id },
                new DebtDto(
                    debt.Id,
                    debt.Description,
                    debt.TotalAmount,
                    debt.RemainingAmount,
                    debt.InterestRate,
                    debt.StartDate,
                    debt.EndDate
                ));
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Debt Create Error: {ex.Message}");
            Console.WriteLine($"Stack: {ex.StackTrace}");
            return StatusCode(500, new { error = ex.Message, details = ex.InnerException?.Message });
        }
    }

    [HttpGet]
    public async Task<ActionResult<List<DebtDto>>> GetAll(Guid userId)
    {
        var debts = await _context.Debts
            .Where(d => d.UserId == userId)
            .OrderByDescending(d => d.RemainingAmount)
            .Select(d => new DebtDto(
                d.Id,
                d.Description,
                d.TotalAmount,
                d.RemainingAmount,
                d.InterestRate,
                d.StartDate,
                d.EndDate
            ))
            .ToListAsync();

        return Ok(debts);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<DebtDto>> GetById(Guid userId, Guid id)
    {
        var debt = await _context.Debts
            .FirstOrDefaultAsync(d => d.Id == id && d.UserId == userId);

        if (debt == null)
            return NotFound();

        return new DebtDto(
            debt.Id,
            debt.Description,
            debt.TotalAmount,
            debt.RemainingAmount,
            debt.InterestRate,
            debt.StartDate,
            debt.EndDate
        );
    }

    [HttpPut("{id}/payment")]
    public async Task<ActionResult<DebtDto>> RegisterPayment(Guid userId, Guid id, [FromBody] PaymentDto payment)
    {
        try
        {
            var debt = await _context.Debts
                .FirstOrDefaultAsync(d => d.Id == id && d.UserId == userId);

            if (debt == null)
                return NotFound();

            debt.RemainingAmount -= payment.Amount;
            
            // Si la deuda está pagada, marcar como finalizada
            if (debt.RemainingAmount <= 0)
            {
                debt.RemainingAmount = 0;
                debt.EndDate = DateTime.UtcNow;
            }

            await _context.SaveChangesAsync();

            return Ok(new DebtDto(
                debt.Id,
                debt.Description,
                debt.TotalAmount,
                debt.RemainingAmount,
                debt.InterestRate,
                debt.StartDate,
                debt.EndDate
            ));
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Payment Error: {ex.Message}");
            return StatusCode(500, new { error = ex.Message });
        }
    }

    [HttpDelete("{id}")]
    public async Task<IActionResult> Delete(Guid userId, Guid id)
    {
        var debt = await _context.Debts
            .FirstOrDefaultAsync(d => d.Id == id && d.UserId == userId);

        if (debt == null)
            return NotFound();

        _context.Debts.Remove(debt);
        await _context.SaveChangesAsync();

        return NoContent();
    }
}

public record DebtDto(
    Guid Id,
    string Description,
    decimal TotalAmount,
    decimal RemainingAmount,
    decimal InterestRate,
    DateTime StartDate,
    DateTime? EndDate
);

public record CreateDebtDto(
    string Description,
    decimal TotalAmount,
    decimal InterestRate
);

public record PaymentDto(
    decimal Amount
);

