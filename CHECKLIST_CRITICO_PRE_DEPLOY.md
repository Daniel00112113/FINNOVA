# ⚠️ CHECKLIST CRÍTICO - Implementar ANTES de Producción

## 🔴 SEGURIDAD CRÍTICA (NO NEGOCIABLE)

### 1. Autenticación JWT (URGENTE)
**Riesgo**: Cualquiera puede acceder a datos de cualquier usuario
**Impacto**: Robo de datos financieros, fraude

**Implementación**:
```bash
# Backend
cd backend/src/FinancialCopilot.API
dotnet add package Microsoft.AspNetCore.Authentication.JwtBearer
dotnet add package BCrypt.Net-Next
```

**Archivos a modificar**:
- `Program.cs` - Agregar JWT authentication
- `Controllers/*` - Agregar `[Authorize]` attribute
- Crear `AuthController.cs` - Login/Register endpoints
- Crear `AuthService.cs` - Generar tokens

**Tiempo estimado**: 4-6 horas

---

### 2. Hashear Contraseñas (URGENTE)
**Riesgo**: Contraseñas en texto plano en BD
**Impacto**: Si hackean la BD, tienen todas las contraseñas

**Implementación**:
```csharp
// AuthService.cs
public string HashPassword(string password)
{
    return BCrypt.Net.BCrypt.HashPassword(password, 12);
}

public bool VerifyPassword(string password, string hash)
{
    return BCrypt.Net.BCrypt.Verify(password, hash);
}
```

**Migración de datos existentes**:
```sql
-- Marcar usuarios para reset de contraseña
UPDATE "Users" SET "PasswordHash" = NULL, "RequiresPasswordReset" = TRUE;
```

**Tiempo estimado**: 2 horas

---

### 3. Variables de Entorno (URGENTE)
**Riesgo**: Secretos en código/appsettings.json
**Impacto**: Exposición de credenciales en GitHub

**Crear archivo `.env`** (NO commitear):
```bash
# .env
DATABASE_URL=postgresql://user:pass@host:5432/financialcopilot
JWT_SECRET=tu-secreto-super-seguro-minimo-256-bits-aqui
JWT_ISSUER=FinancialCopilot
JWT_AUDIENCE=FinancialCopilotUsers
ENCRYPTION_KEY=otra-clave-super-segura-para-encriptar-datos
AI_ENGINE_URL=http://ai-engine:8001
REDIS_URL=redis://localhost:6379
```

**Agregar a `.gitignore`**:
```
.env
.env.local
.env.production
appsettings.Production.json
```

**Tiempo estimado**: 1 hora

---

### 4. HTTPS Obligatorio (URGENTE)
**Riesgo**: Datos financieros en texto plano por la red
**Impacto**: Man-in-the-middle attacks

**Obtener certificado SSL**:
```bash
# Opción 1: Let's Encrypt (gratis)
sudo certbot --nginx -d api.tudominio.com

# Opción 2: Cloudflare (gratis + CDN)
# Configurar en panel de Cloudflare
```

**Forzar HTTPS**:
```csharp
// Program.cs
app.UseHttpsRedirection();
app.UseHsts();
```

**Tiempo estimado**: 2 horas

---

### 5. CORS Seguro (URGENTE)
**Riesgo**: Cualquier sitio puede hacer requests a tu API
**Impacto**: CSRF attacks

**Cambiar de `*` a dominios específicos**:
```csharp
// Program.cs
builder.Services.AddCors(options =>
{
    options.AddPolicy("Production", policy =>
    {
        policy.WithOrigins(
            "https://tudominio.com",
            "https://www.tudominio.com"
        )
        .AllowedMethods("GET", "POST", "PUT", "DELETE")
        .AllowedHeaders("Content-Type", "Authorization")
        .AllowCredentials();
    });
});

app.UseCors("Production");
```

**Tiempo estimado**: 30 minutos

---

### 6. Rate Limiting (IMPORTANTE)
**Riesgo**: DDoS, brute force attacks
**Impacto**: Caída del servicio, costos elevados

```csharp
// Program.cs
builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(context =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.User.Identity?.Name ?? context.Request.Headers.Host.ToString(),
            factory: partition => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 100,
                Window = TimeSpan.FromMinutes(1)
            }));
});

app.UseRateLimiter();
```

**Tiempo estimado**: 1 hora

---

### 7. Validación de Inputs (IMPORTANTE)
**Riesgo**: SQL injection, XSS, data corruption
**Impacto**: Hackeo, pérdida de datos

**Ya implementado parcialmente con DTOs**, verificar:
```csharp
// Todos los DTOs deben tener validación
[Required]
[Range(0.01, 999999999)]
public decimal Amount { get; set; }

[Required]
[StringLength(100)]
[RegularExpression(@"^[a-zA-Z0-9\sáéíóúñÁÉÍÓÚÑ]+$")]
public string Category { get; set; }
```

**Tiempo estimado**: 2 horas (revisar todos los endpoints)

---

## 🟡 BASE DE DATOS (IMPORTANTE)

### 8. Backups Automáticos
**Riesgo**: Pérdida de datos
**Impacto**: Pérdida total de información de usuarios

**PostgreSQL en Docker**:
```bash
# Script de backup diario
#!/bin/bash
# backup-db.sh
docker exec financial-copilot-db pg_dump -U postgres financialcopilot > backup_$(date +%Y%m%d).sql

# Subir a S3/Azure Blob
aws s3 cp backup_$(date +%Y%m%d).sql s3://tu-bucket/backups/
```

**Cron job**:
```bash
# Ejecutar diariamente a las 3 AM
0 3 * * * /path/to/backup-db.sh
```

**Tiempo estimado**: 1 hora

---

### 9. Índices de BD
**Riesgo**: Queries lentas, timeouts
**Impacto**: Mala experiencia de usuario

```sql
-- Ejecutar en producción
CREATE INDEX idx_expenses_userid_date ON "Expenses"("UserId", "Date" DESC);
CREATE INDEX idx_incomes_userid_date ON "Incomes"("UserId", "Date" DESC);
CREATE INDEX idx_expenses_category ON "Expenses"("Category");
CREATE INDEX idx_users_email ON "Users"("Email");
```

**Tiempo estimado**: 30 minutos

---

### 10. Connection Pooling
**Riesgo**: Agotamiento de conexiones
**Impacto**: Errores 500, caída del servicio

```json
// appsettings.Production.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=db;Database=financialcopilot;Username=user;Password=pass;Pooling=true;MinPoolSize=5;MaxPoolSize=50;ConnectionLifetime=300"
  }
}
```

**Tiempo estimado**: 15 minutos

---

## 🟢 MONITOREO (RECOMENDADO)

### 11. Logging Básico
**Riesgo**: No saber qué pasa cuando algo falla
**Impacto**: Debugging imposible

```csharp
// Program.cs
builder.Logging.AddConsole();
builder.Logging.AddDebug();

// En producción, agregar Serilog
builder.Host.UseSerilog((context, configuration) =>
    configuration.ReadFrom.Configuration(context.Configuration));
```

**Tiempo estimado**: 1 hora

---

### 12. Health Checks
**Riesgo**: No saber si el servicio está caído
**Impacto**: Downtime prolongado

```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddNpgSql(builder.Configuration.GetConnectionString("DefaultConnection"));

app.MapHealthChecks("/health");
```

**Tiempo estimado**: 30 minutos

---

## 📋 ORDEN DE IMPLEMENTACIÓN RECOMENDADO

### Día 1 (6-8 horas)
1. ✅ Variables de entorno (.env)
2. ✅ Hashear contraseñas (BCrypt)
3. ✅ JWT Authentication
4. ✅ CORS seguro

### Día 2 (4-6 horas)
5. ✅ HTTPS obligatorio
6. ✅ Rate limiting
7. ✅ Validación de inputs (revisar)
8. ✅ Backups automáticos

### Día 3 (2-3 horas)
9. ✅ Índices de BD
10. ✅ Connection pooling
11. ✅ Logging básico
12. ✅ Health checks

---

## 🚨 VULNERABILIDADES ACTUALES

### CRÍTICAS (Arreglar YA)
1. ❌ **No hay autenticación real** - Cualquiera puede acceder a cualquier dato
2. ❌ **Contraseñas sin hashear** - Texto plano en BD
3. ❌ **CORS abierto (*)** - Cualquier sitio puede hacer requests
4. ❌ **No hay HTTPS** - Datos en texto plano por la red
5. ❌ **Secretos en código** - Expuestos en GitHub

### ALTAS (Arreglar esta semana)
6. ⚠️ **No hay rate limiting** - Vulnerable a DDoS
7. ⚠️ **No hay backups** - Riesgo de pérdida de datos
8. ⚠️ **No hay logging** - Debugging imposible

### MEDIAS (Arreglar este mes)
9. ⚠️ **No hay índices** - Queries lentas
10. ⚠️ **No hay monitoreo** - No sabes si está caído
11. ⚠️ **No hay tests** - Bugs en producción

---

## 💡 QUICK WINS (Implementar en 1 hora)

### 1. Agregar .gitignore completo
```bash
# .gitignore
.env
.env.*
appsettings.Production.json
*.log
bin/
obj/
node_modules/
.next/
dist/
```

### 2. Agregar headers de seguridad
```csharp
// Program.cs
app.Use(async (context, next) =>
{
    context.Response.Headers.Add("X-Content-Type-Options", "nosniff");
    context.Response.Headers.Add("X-Frame-Options", "DENY");
    context.Response.Headers.Add("X-XSS-Protection", "1; mode=block");
    context.Response.Headers.Add("Referrer-Policy", "no-referrer");
    await next();
});
```

### 3. Deshabilitar información de versión
```csharp
// Program.cs
app.Use(async (context, next) =>
{
    context.Response.Headers.Remove("Server");
    context.Response.Headers.Remove("X-Powered-By");
    await next();
});
```

---

## 🎯 RESUMEN EJECUTIVO

### Tiempo Total Estimado
- **Crítico (Día 1-2)**: 10-14 horas
- **Importante (Día 3)**: 2-3 horas
- **Total**: 12-17 horas de trabajo

### Costo de NO Implementar
- **Hackeo de datos**: Multas GDPR hasta €20M o 4% ingresos anuales
- **Pérdida de datos**: Pérdida de confianza, usuarios, negocio
- **Downtime**: $5,000-$10,000 por hora (promedio)
- **Reputación**: Irrecuperable

### Costo de Implementar
- **Tiempo**: 2-3 días de desarrollo
- **Dinero**: $0 (todo open source)
- **Beneficio**: Protección, escalabilidad, profesionalismo

---

## 📞 RECURSOS Y AYUDA

### Documentación
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [ASP.NET Core Security](https://docs.microsoft.com/en-us/aspnet/core/security/)
- [PostgreSQL Security](https://www.postgresql.org/docs/current/security.html)

### Tools de Seguridad
- [OWASP ZAP](https://www.zaproxy.org/) - Penetration testing
- [SonarQube](https://www.sonarqube.org/) - Code quality & security
- [Snyk](https://snyk.io/) - Dependency scanning

### Servicios Recomendados
- **Hosting**: DigitalOcean, AWS, Azure
- **SSL**: Let's Encrypt (gratis), Cloudflare
- **Monitoring**: Application Insights, New Relic
- **Logging**: ELK Stack, Splunk

---

**⚠️ IMPORTANTE**: No despliegues a producción sin implementar al menos los puntos 1-7 (Seguridad Crítica).

**Última actualización**: 2026-03-08
