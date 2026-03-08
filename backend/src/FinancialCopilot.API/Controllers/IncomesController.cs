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
public class IncomesController : ControllerBase
{
    private readonly IApplicationDbContext _context;

    public IncomesController(IApplicationDbContext context)
    {
        _context = context;
    }

    [HttpPost]
    public async Task<ActionResult<IncomeDto>> Create(Guid userId, CreateIncomeDto dto)
    {
        try
        {
            var user = await _context.Users.FindAsync(userId);
            if (user == null)
                return NotFound("User not found");

            var income = new Income
            {
                Id = Guid.NewGuid(),
                UserId = userId,
                Amount = dto.Amount,
                Date = DateTime.SpecifyKind(dto.Date, DateTimeKind.Utc),
                Type = dto.Type,
                Description = dto.Description,
                CreatedAt = DateTime.UtcNow
            };

            _context.Incomes.Add(income);
            await _context.SaveChangesAsync();

            return CreatedAtAction(nameof(GetById), new { userId, id = income.Id },
                new IncomeDto(income.Id, income.Amount, income.Date, income.Type, income.Description));
        }
        catch (Exception ex)
        {
            Console.WriteLine($"Income Create Error: {ex.Message}");
            Console.WriteLine($"Stack: {ex.StackTrace}");
            return StatusCode(500, new { error = ex.Message, details = ex.InnerException?.Message });
        }
    }

    [HttpGet]
    public async Task<ActionResult<List<IncomeDto>>> GetAll(Guid userId)
    {
        var incomes = await _context.Incomes
            .Where(i => i.UserId == userId)
            .OrderByDescending(i => i.Date)
            .Select(i => new IncomeDto(i.Id, i.Amount, i.Date, i.Type, i.Description))
            .ToListAsync();

        return Ok(incomes);
    }

    [HttpGet("{id}")]
    public async Task<ActionResult<IncomeDto>> GetById(Guid userId, Guid id)
    {
        var income = await _context.Incomes
            .FirstOrDefaultAsync(i => i.Id == id && i.UserId == userId);

        if (income == null)
            return NotFound();

        return new IncomeDto(income.Id, income.Amount, income.Date, income.Type, income.Description);
    }
}

