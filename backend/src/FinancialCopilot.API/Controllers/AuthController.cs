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
    private readonly IAuditService _auditService;
    private readonly ILogger<AuthController> _logger;

    public AuthController(
        IApplicationDbContext context,
        IAuthService authService,
        IAuditService auditService,
        ILogger<AuthController> logger)
    {
        _context = context;
        _authService = authService;
        _auditService = auditService;
        _logger = logger;
    }

    [HttpPost("register")]
    public async Task<IActionResult> Register([FromBody] RegisterDto dto)
    {
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString();
        try
        {
            if (await _context.Users.AnyAsync(u => u.Email == dto.Email))
            {
                await _auditService.LogAsync("register_failed", "User", ipAddress: ip,
                    success: false, details: $"Email already exists: {dto.Email}");
                return BadRequest(new { message = "El email ya está registrado" });
            }

            var user = new User
            {
                Id = Guid.NewGuid(),
                Name = dto.Name,
                Email = dto.Email,
                PasswordHash = _authService.HashPassword(dto.Password),
                Role = "user",
                CreatedAt = DateTime.UtcNow
            };

            _context.Users.Add(user);
            await _context.SaveChangesAsync();

            var token = _authService.GenerateJwtToken(user);
            var refreshToken = await CreateRefreshToken(user.Id, ip);

            await _auditService.LogAsync("register", "User", user.Id, user.Id.ToString(), ip);

            return Ok(new { token, refreshToken = refreshToken.Token, userId = user.Id, name = user.Name, email = user.Email, role = user.Role });
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
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString();
        var ua = HttpContext.Request.Headers.UserAgent.ToString();
        try
        {
            var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == dto.Email);

            if (user == null)
            {
                await _auditService.LogAsync("login_failed", "User", ipAddress: ip,
                    success: false, details: $"User not found: {dto.Email}");
                return Unauthorized(new { message = "Email o contraseña incorrectos" });
            }

            // Brute force check
            if (AuthService.IsLockedOut(user))
            {
                var remaining = (int)(user.LockedUntil!.Value - DateTime.UtcNow).TotalMinutes + 1;
                await _auditService.LogAsync("login_blocked", "User", user.Id, user.Id.ToString(), ip,
                    success: false, details: "Account locked");
                return StatusCode(429, new { message = $"Cuenta bloqueada. Intenta en {remaining} minutos." });
            }

            if (!_authService.VerifyPassword(dto.Password, user.PasswordHash))
            {
                AuthService.RegisterFailedAttempt(user);
                await _context.SaveChangesAsync();
                await _auditService.LogAsync("login_failed", "User", user.Id, user.Id.ToString(), ip,
                    success: false, details: $"Wrong password. Attempts: {user.FailedLoginAttempts}");
                return Unauthorized(new { message = "Email o contraseña incorrectos" });
            }

            AuthService.ResetFailedAttempts(user);
            await _context.SaveChangesAsync();

            var token = _authService.GenerateJwtToken(user);
            var refreshToken = await CreateRefreshToken(user.Id, ip);

            await _auditService.LogAsync("login", "User", user.Id, user.Id.ToString(), ip, ua);

            return Ok(new { token, refreshToken = refreshToken.Token, userId = user.Id, name = user.Name, email = user.Email, role = user.Role });
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Error en login");
            return StatusCode(500, new { message = "Error al iniciar sesión" });
        }
    }

    [HttpPost("refresh")]
    public async Task<IActionResult> Refresh([FromBody] RefreshTokenDto dto)
    {
        var ip = HttpContext.Connection.RemoteIpAddress?.ToString();
        var stored = await _context.RefreshTokens
            .Include(r => r.User)
            .FirstOrDefaultAsync(r => r.Token == dto.RefreshToken);

        if (stored == null || !stored.IsActive)
            return Unauthorized(new { message = "Refresh token inválido o expirado" });

        // Rotate: revoke old, issue new
        stored.IsRevoked = true;
        var newRefresh = await CreateRefreshToken(stored.UserId, ip);
        await _context.SaveChangesAsync();

        var token = _authService.GenerateJwtToken(stored.User);
        return Ok(new { token, refreshToken = newRefresh.Token });
    }

    [HttpPost("logout")]
    public async Task<IActionResult> Logout([FromBody] RefreshTokenDto dto)
    {
        var stored = await _context.RefreshTokens
            .FirstOrDefaultAsync(r => r.Token == dto.RefreshToken);

        if (stored != null)
        {
            stored.IsRevoked = true;
            await _context.SaveChangesAsync();
        }

        return Ok(new { message = "Sesión cerrada" });
    }

    [HttpPost("validate")]
    public IActionResult ValidateToken([FromBody] ValidateTokenDto dto)
    {
        var userId = _authService.ValidateJwtToken(dto.Token);
        if (userId == null)
            return Unauthorized(new { message = "Token inválido o expirado" });
        return Ok(new { userId, valid = true });
    }

    /// <summary>
    /// Bootstrap: promueve al primer admin. Solo funciona si no existe ningún admin.
    /// Requiere una clave de bootstrap configurada en AdminBootstrap:Key
    /// </summary>
    [HttpPost("bootstrap-admin")]
    public async Task<IActionResult> BootstrapAdmin([FromBody] BootstrapAdminDto dto)
    {
        var bootstrapKey = _context.GetType().Assembly.GetName().Name; // placeholder
        var configKey = HttpContext.RequestServices
            .GetRequiredService<Microsoft.Extensions.Configuration.IConfiguration>()["AdminBootstrap:Key"];

        if (string.IsNullOrEmpty(configKey) || dto.BootstrapKey != configKey)
            return Unauthorized(new { message = "Clave de bootstrap inválida" });

        // Solo si no hay ningún admin
        if (await _context.Users.AnyAsync(u => u.Role == "admin"))
            return BadRequest(new { message = "Ya existe un administrador" });

        var user = await _context.Users.FirstOrDefaultAsync(u => u.Email == dto.Email);
        if (user == null) return NotFound(new { message = "Usuario no encontrado" });

        user.Role = "admin";
        user.UpdatedAt = DateTime.UtcNow;
        await _context.SaveChangesAsync();

        await _auditService.LogAsync("bootstrap_admin", "User", user.Id, user.Id.ToString(),
            HttpContext.Connection.RemoteIpAddress?.ToString());

        return Ok(new { message = $"{user.Email} es ahora administrador" });
    }

    private async Task<RefreshToken> CreateRefreshToken(Guid userId, string? ip)
    {
        // Limpiar tokens viejos del usuario (máximo 5 activos)
        var oldTokens = await _context.RefreshTokens
            .Where(r => r.UserId == userId && !r.IsRevoked)
            .OrderBy(r => r.CreatedAt)
            .ToListAsync();

        if (oldTokens.Count >= 5)
        {
            foreach (var old in oldTokens.Take(oldTokens.Count - 4))
                old.IsRevoked = true;
        }

        var refreshToken = new RefreshToken
        {
            Id = Guid.NewGuid(),
            UserId = userId,
            Token = _authService.GenerateRefreshToken(),
            ExpiresAt = DateTime.UtcNow.AddDays(30),
            CreatedAt = DateTime.UtcNow,
            CreatedByIp = ip
        };

        _context.RefreshTokens.Add(refreshToken);
        await _context.SaveChangesAsync();
        return refreshToken;
    }
}

public record RegisterDto(string Name, string Email, string Password);
public record LoginDto(string Email, string Password);
public record ValidateTokenDto(string Token);
public record RefreshTokenDto(string RefreshToken);
public record BootstrapAdminDto(string Email, string BootstrapKey);
