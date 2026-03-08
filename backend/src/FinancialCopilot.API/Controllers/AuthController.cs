using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using FinancialCopilot.Application.Common.Interfaces;
using FinancialCopilot.Domain.Entities;
using FinancialCopilot.Infrastructure.Services;

namespace FinancialCopilot.API.Controllers;

[ApiController]
[Route("api/[controller]")]
public class AuthController : ControllerBase
{
    private readonly IApplicationDbContext _context;
    private readonly IAuthService _authService;
    private readonly ILogger<AuthController> _logger;

    public AuthController(
        IApplicationDbContext context,
        IAuthService authService,
        ILogger<AuthController> logger)
    {
        _context = context;
        _authService = authService;
        _logger = logger;
    }

    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterDto dto)
    {
        try
        {
            // Validar que el email no exista
            if (await _context.Users.AnyAsync(u => u.Email == dto.Email))
            {
                return BadRequest(new { message = "El email ya está registrado" });
            }

            // Crear usuario
            var user = new User
            {
                Id = Guid.NewGuid(),
                Name = dto.Name,
                Email = dto.Email,
                PasswordHash = _authService.HashPassword(dto.Password),
                CreatedAt = DateTime.UtcNow
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync(CancellationToken.None);

            // Generar token
            var token = _authService.GenerateJwtToken(user);

            _logger.LogInformation("Usuario registrado: {Email}", dto.Email);

            return Ok(new
            {
                token,
                userId = user.Id,
                name = user.Name,
                email = user.Email
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error en registro");
            return StatusCode(500, new { message = "Error al registrar usuario" });
        }
    }

    [HttpPost("login")]
    public async Task<IActionResult> Login([FromBody] LoginDto dto)
    {
        try
        {
            // Buscar usuario
            var user = await _context.Users
                .FirstOrDefaultAsync(u => u.Email == dto.Email);

            if (user == null)
            {
                return Unauthorized(new { message = "Email o contraseña incorrectos" });
            }

            // Verificar contraseña
            if (!_authService.VerifyPassword(dto.Password, user.PasswordHash))
            {
                return Unauthorized(new { message = "Email o contraseña incorrectos" });
            }

            // Generar token
            var token = _authService.GenerateJwtToken(user);

            _logger.LogInformation("Usuario autenticado: {Email}", dto.Email);

            return Ok(new
            {
                token,
                userId = user.Id,
                name = user.Name,
                email = user.Email
            });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error en login");
            return StatusCode(500, new { message = "Error al iniciar sesión" });
        }
    }

    [HttpPost("validate")]
    public IActionResult ValidateToken([FromBody] ValidateTokenDto dto)
    {
        var userId = _authService.ValidateJwtToken(dto.Token);
        
        if (userId == null)
        {
            return Unauthorized(new { message = "Token inválido o expirado" });
        }

        return Ok(new { userId, valid = true });
    }
}

public record RegisterDto(string Name, string Email, string Password);
public record LoginDto(string Email, string Password);
public record ValidateTokenDto(string Token);
