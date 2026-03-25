using MailKit.Net.Smtp;
using MailKit.Security;
using Microsoft.Extensions.Configuration;
using Microsoft.Extensions.Logging;
using MimeKit;

namespace FinancialCopilot.Infrastructure.Services;

public interface IEmailService
{
    Task SendWelcomeAsync(string toEmail, string userName);
    Task SendLoginNotificationAsync(string toEmail, string userName, string ipAddress);
    Task SendPasswordChangedAsync(string toEmail, string userName);
    Task<bool> IsConfiguredAsync();
}

public class EmailService : IEmailService
{
    private readonly IConfiguration _config;
    private readonly ILogger<EmailService> _logger;

    private string SmtpHost     => _config["Email:SmtpHost"] ?? "smtp.gmail.com";
    private int    SmtpPort     => int.Parse(_config["Email:SmtpPort"] ?? "587");
    private string SmtpUser     => _config["Email:SmtpUser"] ?? "";
    private string SmtpPassword => _config["Email:SmtpPassword"] ?? "";
    private string FromName     => _config["Email:FromName"] ?? "FINNOVA";
    private string FromEmail    => _config["Email:FromEmail"] ?? SmtpUser;

    public EmailService(IConfiguration config, ILogger<EmailService> logger)
    {
        _config = config;
        _logger = logger;
    }

    public Task<bool> IsConfiguredAsync() =>
        Task.FromResult(!string.IsNullOrEmpty(SmtpUser) && !string.IsNullOrEmpty(SmtpPassword));

    public async Task SendWelcomeAsync(string toEmail, string userName)
    {
        var subject = "🎉 ¡Bienvenido a FINNOVA!";
        var html = $@"
        {BaseTemplate($@"
            <h1 style='color:#10b981;font-size:28px;margin:0 0 8px'>¡Hola, {userName}! 👋</h1>
            <p style='color:#9ca3af;font-size:16px;margin:0 0 24px'>Tu cuenta en FINNOVA ha sido creada exitosamente.</p>

            <div style='background:#0f2027;border:1px solid rgba(16,185,129,0.2);border-radius:12px;padding:20px;margin:24px 0'>
                <p style='color:#d1fae5;font-size:14px;margin:0 0 12px;font-weight:600'>🚀 ¿Qué puedes hacer ahora?</p>
                <ul style='color:#9ca3af;font-size:14px;margin:0;padding-left:20px;line-height:2'>
                    <li>Registrar tus ingresos y gastos</li>
                    <li>Ver predicciones de IA sobre tu futuro financiero</li>
                    <li>Simular escenarios financieros</li>
                    <li>Recibir alertas inteligentes</li>
                </ul>
            </div>

            <a href='https://finnova-frontend.onrender.com/dashboard'
               style='display:inline-block;background:linear-gradient(135deg,#10b981,#059669);color:white;padding:14px 32px;border-radius:12px;text-decoration:none;font-weight:700;font-size:15px;margin:8px 0'>
                Ir a mi Dashboard →
            </a>

            <p style='color:#6b7280;font-size:13px;margin:24px 0 0'>
                Si no creaste esta cuenta, ignora este mensaje o escríbenos a
                <a href='mailto:ctslabscartagena@gmail.com' style='color:#10b981'>ctslabscartagena@gmail.com</a>
            </p>
        ")}";

        await SendAsync(toEmail, userName, subject, html);
    }

    public async Task SendLoginNotificationAsync(string toEmail, string userName, string ipAddress)
    {
        var subject = "🔐 Nuevo inicio de sesión en FINNOVA";
        var html = $@"
        {BaseTemplate($@"
            <h1 style='color:#10b981;font-size:24px;margin:0 0 8px'>Nuevo inicio de sesión</h1>
            <p style='color:#9ca3af;font-size:15px;margin:0 0 24px'>Hola <strong style='color:#e5e7eb'>{userName}</strong>, detectamos un nuevo acceso a tu cuenta.</p>

            <div style='background:#0f2027;border:1px solid rgba(16,185,129,0.2);border-radius:12px;padding:20px;margin:24px 0'>
                <table style='width:100%;border-collapse:collapse'>
                    <tr>
                        <td style='color:#6b7280;font-size:13px;padding:6px 0'>📅 Fecha</td>
                        <td style='color:#e5e7eb;font-size:13px;padding:6px 0;text-align:right'>{DateTime.UtcNow:dd/MM/yyyy HH:mm} UTC</td>
                    </tr>
                    <tr>
                        <td style='color:#6b7280;font-size:13px;padding:6px 0'>🌐 IP</td>
                        <td style='color:#e5e7eb;font-size:13px;padding:6px 0;text-align:right'>{ipAddress}</td>
                    </tr>
                </table>
            </div>

            <p style='color:#9ca3af;font-size:14px'>
                ¿No fuiste tú? Cambia tu contraseña inmediatamente y contáctanos en
                <a href='mailto:ctslabscartagena@gmail.com' style='color:#10b981'>ctslabscartagena@gmail.com</a>
            </p>
        ")}";

        await SendAsync(toEmail, userName, subject, html);
    }

    public async Task SendPasswordChangedAsync(string toEmail, string userName)
    {
        var subject = "🔑 Tu contraseña fue cambiada — FINNOVA";
        var html = $@"
        {BaseTemplate($@"
            <h1 style='color:#f59e0b;font-size:24px;margin:0 0 8px'>Contraseña actualizada</h1>
            <p style='color:#9ca3af;font-size:15px;margin:0 0 24px'>Hola <strong style='color:#e5e7eb'>{userName}</strong>, tu contraseña fue cambiada el {DateTime.UtcNow:dd/MM/yyyy} a las {DateTime.UtcNow:HH:mm} UTC.</p>
            <p style='color:#9ca3af;font-size:14px'>
                Si no realizaste este cambio, contáctanos de inmediato en
                <a href='mailto:ctslabscartagena@gmail.com' style='color:#10b981'>ctslabscartagena@gmail.com</a>
            </p>
        ")}";

        await SendAsync(toEmail, userName, subject, html);
    }

    // ── Helpers ──────────────────────────────────────────────────────────────

    private string BaseTemplate(string content) => $@"
    <!DOCTYPE html>
    <html>
    <head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1'></head>
    <body style='margin:0;padding:0;background:#030712;font-family:-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif'>
        <table width='100%' cellpadding='0' cellspacing='0' style='background:#030712;padding:40px 20px'>
            <tr><td align='center'>
                <table width='100%' style='max-width:560px'>
                    <!-- Header -->
                    <tr><td style='background:linear-gradient(135deg,#0a1628,#0f2027);border:1px solid rgba(16,185,129,0.15);border-radius:16px 16px 0 0;padding:28px 32px;text-align:center'>
                        <span style='font-size:26px;font-weight:900;background:linear-gradient(90deg,#10b981,#34d399);-webkit-background-clip:text;-webkit-text-fill-color:transparent'>FINNOVA</span>
                        <p style='color:#6b7280;font-size:12px;margin:4px 0 0'>Tu copiloto financiero impulsado por IA</p>
                    </td></tr>
                    <!-- Body -->
                    <tr><td style='background:#0a1628;border:1px solid rgba(16,185,129,0.1);border-top:none;padding:32px'>
                        {content}
                    </td></tr>
                    <!-- Footer -->
                    <tr><td style='background:#020810;border:1px solid rgba(255,255,255,0.05);border-top:none;border-radius:0 0 16px 16px;padding:20px 32px;text-align:center'>
                        <p style='color:#374151;font-size:12px;margin:0'>© 2026 FINNOVA by CTS Labs Cartagena 🇨🇴</p>
                        <p style='color:#374151;font-size:11px;margin:4px 0 0'>
                            <a href='mailto:ctslabscartagena@gmail.com' style='color:#10b981;text-decoration:none'>ctslabscartagena@gmail.com</a>
                        </p>
                    </td></tr>
                </table>
            </td></tr>
        </table>
    </body>
    </html>";

    private async Task SendAsync(string toEmail, string toName, string subject, string htmlBody)
    {
        if (!await IsConfiguredAsync())
        {
            _logger.LogWarning("Email service not configured — skipping send to {Email}", toEmail);
            return;
        }

        try
        {
            var message = new MimeMessage();
            message.From.Add(new MailboxAddress(FromName, FromEmail));
            message.To.Add(new MailboxAddress(toName, toEmail));
            message.Subject = subject;
            message.Body = new BodyBuilder { HtmlBody = htmlBody }.ToMessageBody();

            using var client = new SmtpClient();
            await client.ConnectAsync(SmtpHost, SmtpPort, SecureSocketOptions.StartTls);
            await client.AuthenticateAsync(SmtpUser, SmtpPassword);
            await client.SendAsync(message);
            await client.DisconnectAsync(true);

            _logger.LogInformation("Email sent to {Email}: {Subject}", toEmail, subject);
        }
        catch (Exception ex)
        {
            _logger.LogError(ex, "Failed to send email to {Email}", toEmail);
            // No lanzar — el email es best-effort, no debe romper el flujo
        }
    }
}
