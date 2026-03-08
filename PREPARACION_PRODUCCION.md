# 🚀 Preparación para Producción - Financial Copilot

## Guía Profesional de Despliegue, Seguridad y Escalabilidad

---

## 🔒 SEGURIDAD (CRÍTICO)

### 1. Autenticación y Autorización

#### ❌ Problemas Actuales
- No hay sistema de autenticación real (solo localStorage)
- No hay JWT tokens
- No hay validación de sesiones
- Cualquiera puede acceder a datos de cualquier usuario

#### ✅ Soluciones Requeridas

**Backend - Implementar JWT Authentication**
```csharp
// Program.cs
builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
    .AddJwtBearer(options =>
    {
        options.TokenValidationParameters = new TokenValidationParameters
        {
            ValidateIssuer = true,
            ValidateAudience = true,
            ValidateLifetime = true,
            ValidateIssuerSigningKey = true,
            ValidIssuer = builder.Configuration["Jwt:Issuer"],
            ValidAudience = builder.Configuration["Jwt:Audience"],
            IssuerSigningKey = new SymmetricSecurityKey(
                Encoding.UTF8.GetBytes(builder.Configuration["Jwt:Key"]))
        };
    });

// Agregar [Authorize] a todos los controllers
[Authorize]
[ApiController]
public class ExpensesController : ControllerBase
```

**Frontend - Implementar Auth Context**
```typescript
// lib/auth.ts
export const login = async (email: string, password: string) => {
  const response = await api.post('/auth/login', { email, password })
  const { token, userId } = response.data
  localStorage.setItem('token', token)
  localStorage.setItem('userId', userId)
  api.defaults.headers.common['Authorization'] = `Bearer ${token}`
}

// Interceptor para agregar token a todas las requests
api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})
```

### 2. Protección de Datos Sensibles

#### ❌ Problemas Actuales
- Contraseñas en texto plano en BD
- No hay encriptación de datos financieros
- Conexión strings en código

#### ✅ Soluciones Requeridas

**Encriptar Contraseñas**
```csharp
// Usar BCrypt o ASP.NET Core Identity
using BCrypt.Net;

public class AuthService
{
    public string HashPassword(string password)
    {
        return BCrypt.HashPassword(password, BCrypt.GenerateSalt(12));
    }
    
    public bool VerifyPassword(string password, string hash)
    {
        return BCrypt.Verify(password, hash);
    }
}
```

**Encriptar Datos Sensibles**
```csharp
// Encriptar montos y descripciones sensibles
public class EncryptionService
{
    private readonly byte[] _key;
    
    public string Encrypt(string plainText)
    {
        using var aes = Aes.Create();
        aes.Key = _key;
        // ... implementación AES-256
    }
}
```

**Variables de Entorno**
```bash
# .env (NUNCA commitear)
DATABASE_URL=postgresql://user:pass@host:5432/db
JWT_SECRET=tu-secreto-super-seguro-de-256-bits
ENCRYPTION_KEY=otra-clave-super-segura
AI_ENGINE_URL=http://ai-engine:8001
```

### 3. Validación y Sanitización

#### ✅ Implementar en Backend
```csharp
// DTOs con validación
public class CreateExpenseDto
{
    [Required]
    [Range(0.01, 999999999)]
    public decimal Amount { get; set; }
    
    [Required]
    [StringLength(100)]
    [RegularExpression(@"^[a-zA-Z0-9\s]+$")]
    public string Category { get; set; }
    
    [StringLength(500)]
    public string? Description { get; set; }
}

// Sanitizar inputs
public string SanitizeInput(string input)
{
    return input?.Trim()
        .Replace("<", "&lt;")
        .Replace(">", "&gt;")
        .Replace("'", "&#39;")
        .Replace("\"", "&quot;");
}
```

### 4. Rate Limiting

```csharp
// Program.cs
builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(context =>
        RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.User.Identity?.Name ?? context.Request.Headers.Host.ToString(),
            factory: partition => new FixedWindowRateLimiterOptions
            {
                AutoReplenishment = true,
                PermitLimit = 100,
                QueueLimit = 0,
                Window = TimeSpan.FromMinutes(1)
            }));
});
```

### 5. SQL Injection Protection

#### ✅ Ya implementado con Entity Framework
- EF Core usa parámetros automáticamente
- Nunca usar string concatenation para queries

#### ⚠️ Verificar queries raw
```csharp
// ❌ NUNCA hacer esto
var query = $"SELECT * FROM Users WHERE Email = '{email}'";

// ✅ Siempre usar parámetros
var user = await _context.Users
    .Where(u => u.Email == email)
    .FirstOrDefaultAsync();
```

### 6. CORS Configuración Segura

```csharp
// Program.cs - Cambiar de "*" a dominios específicos
builder.Services.AddCors(options =>
{
    options.AddPolicy("Production", policy =>
    {
        policy.WithOrigins(
            "https://financialcopilot.com",
            "https://www.financialcopilot.com"
        )
        .AllowedMethods("GET", "POST", "PUT", "DELETE")
        .AllowedHeaders("Content-Type", "Authorization")
        .AllowCredentials();
    });
});
```

### 7. HTTPS Obligatorio

```csharp
// Program.cs
app.UseHttpsRedirection();
app.UseHsts(); // HTTP Strict Transport Security

// appsettings.Production.json
{
  "Kestrel": {
    "Endpoints": {
      "Https": {
        "Url": "https://*:443",
        "Certificate": {
          "Path": "/path/to/cert.pfx",
          "Password": "cert-password"
        }
      }
    }
  }
}
```

### 8. Secrets Management

```bash
# Usar Azure Key Vault, AWS Secrets Manager, o HashiCorp Vault
# NUNCA guardar secretos en código o appsettings.json

# Azure Key Vault
dotnet add package Azure.Extensions.AspNetCore.Configuration.Secrets

# Program.cs
builder.Configuration.AddAzureKeyVault(
    new Uri($"https://{keyVaultName}.vault.azure.net/"),
    new DefaultAzureCredential());
```

---

## 🏗️ ARQUITECTURA Y ESCALABILIDAD

### 1. Separación de Ambientes

```
Desarrollo (Local)
├── Frontend: localhost:3000
├── Backend: localhost:5000
├── AI Engine: localhost:8001
└── PostgreSQL: localhost:5432

Staging (Pre-producción)
├── Frontend: staging.financialcopilot.com
├── Backend: api-staging.financialcopilot.com
├── AI Engine: ai-staging.financialcopilot.com
└── PostgreSQL: RDS/Azure SQL (staging)

Producción
├── Frontend: financialcopilot.com (CDN)
├── Backend: api.financialcopilot.com (Load Balanced)
├── AI Engine: ai.financialcopilot.com (Auto-scaling)
└── PostgreSQL: RDS/Azure SQL (Multi-AZ)
```

### 2. Base de Datos - Optimizaciones

#### Índices Críticos
```sql
-- Índices para mejorar performance
CREATE INDEX idx_expenses_userid_date ON "Expenses"("UserId", "Date" DESC);
CREATE INDEX idx_incomes_userid_date ON "Incomes"("UserId", "Date" DESC);
CREATE INDEX idx_expenses_category ON "Expenses"("Category");
CREATE INDEX idx_users_email ON "Users"("Email");

-- Índice para búsquedas de texto
CREATE INDEX idx_expenses_description ON "Expenses" USING gin(to_tsvector('spanish', "Description"));
```

#### Connection Pooling
```csharp
// appsettings.Production.json
{
  "ConnectionStrings": {
    "DefaultConnection": "Host=db;Database=financialcopilot;Username=user;Password=pass;Pooling=true;MinPoolSize=5;MaxPoolSize=100;ConnectionLifetime=300"
  }
}
```

#### Read Replicas
```csharp
// Para queries de solo lectura, usar replica
public class ApplicationDbContext : DbContext
{
    public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options) 
        : base(options) { }
    
    // Configurar read replica para reportes
    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        if (IsReadOnlyOperation)
        {
            optionsBuilder.UseNpgsql(Configuration["ConnectionStrings:ReadReplica"]);
        }
    }
}
```

### 3. Caché Strategy

#### Redis para Caché Distribuido
```csharp
// Program.cs
builder.Services.AddStackExchangeRedisCache(options =>
{
    options.Configuration = builder.Configuration["Redis:ConnectionString"];
    options.InstanceName = "FinancialCopilot:";
});

// Cachear predicciones de IA (son costosas)
public class CachedAiService
{
    private readonly IDistributedCache _cache;
    private readonly AiService _aiService;
    
    public async Task<PredictionResult> GetPrediction(string userId)
    {
        var cacheKey = $"prediction:{userId}";
        var cached = await _cache.GetStringAsync(cacheKey);
        
        if (cached != null)
            return JsonSerializer.Deserialize<PredictionResult>(cached);
        
        var result = await _aiService.GetPrediction(userId);
        
        await _cache.SetStringAsync(cacheKey, 
            JsonSerializer.Serialize(result),
            new DistributedCacheEntryOptions
            {
                AbsoluteExpirationRelativeToNow = TimeSpan.FromHours(1)
            });
        
        return result;
    }
}
```

### 4. Load Balancing

#### Nginx Configuration
```nginx
# nginx.conf
upstream backend {
    least_conn;
    server backend1:5000 weight=3;
    server backend2:5000 weight=3;
    server backend3:5000 weight=2;
}

upstream ai_engine {
    server ai1:8001;
    server ai2:8001;
    server ai3:8001;
}

server {
    listen 443 ssl http2;
    server_name api.financialcopilot.com;
    
    ssl_certificate /etc/ssl/certs/cert.pem;
    ssl_certificate_key /etc/ssl/private/key.pem;
    
    location / {
        proxy_pass http://backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 5. Auto-scaling

#### Kubernetes Deployment
```yaml
# k8s/backend-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: financialcopilot/backend:latest
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "1Gi"
            cpu: "1000m"
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: db-secret
              key: url
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 6. CDN para Frontend

```javascript
// next.config.js
module.exports = {
  assetPrefix: process.env.NODE_ENV === 'production' 
    ? 'https://cdn.financialcopilot.com' 
    : '',
  images: {
    domains: ['cdn.financialcopilot.com'],
    loader: 'cloudinary', // o 'cloudflare', 'imgix'
  }
}
```

### 7. Message Queue para Tareas Pesadas

```csharp
// Para entrenar modelos, generar reportes, etc.
// Usar RabbitMQ, Azure Service Bus, o AWS SQS

public class BackgroundJobService
{
    private readonly IMessageQueue _queue;
    
    public async Task QueueModelTraining(string userId)
    {
        await _queue.PublishAsync(new TrainModelJob
        {
            UserId = userId,
            Timestamp = DateTime.UtcNow
        });
    }
}

// Worker separado procesa jobs
public class ModelTrainingWorker : BackgroundService
{
    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        await foreach (var job in _queue.ConsumeAsync<TrainModelJob>(stoppingToken))
        {
            await TrainModel(job.UserId);
        }
    }
}
```

---

## 📊 MONITOREO Y OBSERVABILIDAD

### 1. Logging Estructurado

```csharp
// Program.cs
builder.Services.AddSerilog((services, lc) => lc
    .ReadFrom.Configuration(builder.Configuration)
    .Enrich.FromLogContext()
    .Enrich.WithMachineName()
    .Enrich.WithEnvironmentName()
    .WriteTo.Console()
    .WriteTo.Elasticsearch(new ElasticsearchSinkOptions(new Uri("http://elasticsearch:9200"))
    {
        AutoRegisterTemplate = true,
        IndexFormat = $"financialcopilot-logs-{DateTime.UtcNow:yyyy-MM}"
    }));

// En controllers
_logger.LogInformation("User {UserId} created expense {ExpenseId} for {Amount}", 
    userId, expense.Id, expense.Amount);
```

### 2. Application Performance Monitoring (APM)

```csharp
// Usar Application Insights, New Relic, o Datadog
builder.Services.AddApplicationInsightsTelemetry(options =>
{
    options.ConnectionString = builder.Configuration["ApplicationInsights:ConnectionString"];
});

// Custom metrics
_telemetryClient.TrackMetric("PredictionLatency", latencyMs);
_telemetryClient.TrackEvent("ModelFallback", new Dictionary<string, string>
{
    { "UserId", userId },
    { "Reason", "InsufficientData" }
});
```

### 3. Health Checks

```csharp
// Program.cs
builder.Services.AddHealthChecks()
    .AddNpgSql(builder.Configuration.GetConnectionString("DefaultConnection"))
    .AddRedis(builder.Configuration["Redis:ConnectionString"])
    .AddUrlGroup(new Uri("http://ai-engine:8001/"), "AI Engine");

app.MapHealthChecks("/health", new HealthCheckOptions
{
    ResponseWriter = UIResponseWriter.WriteHealthCheckUIResponse
});
```

### 4. Alertas

```yaml
# Prometheus alerts
groups:
- name: financialcopilot
  rules:
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
    for: 5m
    annotations:
      summary: "High error rate detected"
      
  - alert: DatabaseConnectionPoolExhausted
    expr: db_connection_pool_usage > 0.9
    for: 2m
    
  - alert: AIEngineSlow
    expr: ai_prediction_duration_seconds > 5
    for: 1m
```

---

## 🔐 COMPLIANCE Y PRIVACIDAD

### 1. GDPR / Protección de Datos

```csharp
// Implementar derecho al olvido
public class DataPrivacyService
{
    public async Task DeleteUserData(Guid userId)
    {
        // Anonimizar en lugar de eliminar (para mantener integridad de datos)
        var user = await _context.Users.FindAsync(userId);
        user.Email = $"deleted-{userId}@deleted.com";
        user.Name = "Usuario Eliminado";
        
        // Encriptar datos financieros con clave que se destruye
        await AnonymizeFinancialData(userId);
        
        await _context.SaveChangesAsync();
    }
    
    public async Task<byte[]> ExportUserData(Guid userId)
    {
        // Exportar todos los datos del usuario en formato JSON
        var data = new
        {
            User = await _context.Users.FindAsync(userId),
            Expenses = await _context.Expenses.Where(e => e.UserId == userId).ToListAsync(),
            Incomes = await _context.Incomes.Where(i => i.UserId == userId).ToListAsync()
        };
        
        return Encoding.UTF8.GetBytes(JsonSerializer.Serialize(data));
    }
}
```

### 2. Auditoría

```csharp
// Tabla de auditoría
public class AuditLog
{
    public Guid Id { get; set; }
    public Guid UserId { get; set; }
    public string Action { get; set; } // "Create", "Update", "Delete", "View"
    public string Entity { get; set; } // "Expense", "Income", etc.
    public string Changes { get; set; } // JSON con cambios
    public string IpAddress { get; set; }
    public DateTime Timestamp { get; set; }
}

// Interceptor para auditar cambios
public override int SaveChanges()
{
    var entries = ChangeTracker.Entries()
        .Where(e => e.State == EntityState.Added || 
                    e.State == EntityState.Modified || 
                    e.State == EntityState.Deleted);
    
    foreach (var entry in entries)
    {
        _context.AuditLogs.Add(new AuditLog
        {
            UserId = GetCurrentUserId(),
            Action = entry.State.ToString(),
            Entity = entry.Entity.GetType().Name,
            Changes = JsonSerializer.Serialize(entry.CurrentValues.ToObject()),
            IpAddress = GetClientIpAddress(),
            Timestamp = DateTime.UtcNow
        });
    }
    
    return base.SaveChanges();
}
```

---

## 🧪 TESTING Y CI/CD

### 1. Tests Automatizados

```csharp
// Tests unitarios
[Fact]
public async Task CreateExpense_ValidData_ReturnsCreated()
{
    // Arrange
    var expense = new CreateExpenseDto { Amount = 100, Category = "Food" };
    
    // Act
    var result = await _controller.Create(userId, expense);
    
    // Assert
    Assert.IsType<CreatedAtActionResult>(result);
}

// Tests de integración
[Fact]
public async Task GetExpenses_ReturnsUserExpensesOnly()
{
    // Verificar que un usuario no puede ver gastos de otro
    var expenses = await _client.GetAsync($"/api/users/{userId}/expenses");
    var data = await expenses.Content.ReadAsAsync<List<Expense>>();
    
    Assert.All(data, e => Assert.Equal(userId, e.UserId));
}

// Tests de seguridad
[Fact]
public async Task GetExpenses_WithoutAuth_Returns401()
{
    _client.DefaultRequestHeaders.Authorization = null;
    var response = await _client.GetAsync($"/api/users/{userId}/expenses");
    Assert.Equal(HttpStatusCode.Unauthorized, response.StatusCode);
}
```

### 2. CI/CD Pipeline

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Run Tests
        run: |
          dotnet test backend/
          npm test --prefix frontend/
          
      - name: Security Scan
        run: |
          dotnet tool install --global security-scan
          security-scan backend/
          
      - name: Dependency Check
        run: |
          npm audit --prefix frontend/
          dotnet list package --vulnerable
  
  build:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - name: Build Docker Images
        run: |
          docker build -t financialcopilot/backend:${{ github.sha }} backend/
          docker build -t financialcopilot/frontend:${{ github.sha }} frontend/
          docker build -t financialcopilot/ai-engine:${{ github.sha }} ai-engine/
          
      - name: Push to Registry
        run: |
          docker push financialcopilot/backend:${{ github.sha }}
          docker push financialcopilot/frontend:${{ github.sha }}
          docker push financialcopilot/ai-engine:${{ github.sha }}
  
  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/backend backend=financialcopilot/backend:${{ github.sha }}
          kubectl set image deployment/frontend frontend=financialcopilot/frontend:${{ github.sha }}
          kubectl set image deployment/ai-engine ai-engine=financialcopilot/ai-engine:${{ github.sha }}
          kubectl rollout status deployment/backend
```

---

## 📝 CHECKLIST PRE-PRODUCCIÓN

### Seguridad
- [ ] JWT Authentication implementado
- [ ] Contraseñas hasheadas con BCrypt
- [ ] HTTPS configurado con certificado válido
- [ ] CORS configurado para dominios específicos
- [ ] Rate limiting implementado
- [ ] Validación de inputs en todos los endpoints
- [ ] SQL injection protegido (EF Core)
- [ ] XSS protegido (sanitización)
- [ ] CSRF tokens implementados
- [ ] Secrets en variables de entorno (no en código)
- [ ] Auditoría de accesos implementada

### Base de Datos
- [ ] Índices creados en columnas frecuentes
- [ ] Connection pooling configurado
- [ ] Backups automáticos configurados
- [ ] Read replicas para queries pesadas
- [ ] Migraciones documentadas
- [ ] Datos sensibles encriptados

### Performance
- [ ] Caché implementado (Redis)
- [ ] CDN configurado para frontend
- [ ] Compresión gzip/brotli habilitada
- [ ] Lazy loading de imágenes
- [ ] Code splitting en frontend
- [ ] Database query optimization

### Escalabilidad
- [ ] Load balancer configurado
- [ ] Auto-scaling configurado
- [ ] Message queue para tareas pesadas
- [ ] Stateless backend (no sesiones en memoria)
- [ ] Horizontal scaling probado

### Monitoreo
- [ ] Logging estructurado (ELK/Splunk)
- [ ] APM configurado (Application Insights/New Relic)
- [ ] Health checks implementados
- [ ] Alertas configuradas
- [ ] Dashboards de métricas

### Testing
- [ ] Tests unitarios (>80% coverage)
- [ ] Tests de integración
- [ ] Tests de seguridad
- [ ] Tests de carga (JMeter/k6)
- [ ] Tests de penetración

### Compliance
- [ ] Política de privacidad
- [ ] Términos de servicio
- [ ] Consentimiento de cookies
- [ ] Derecho al olvido implementado
- [ ] Exportación de datos implementada
- [ ] Auditoría de accesos

### DevOps
- [ ] CI/CD pipeline configurado
- [ ] Ambientes separados (dev/staging/prod)
- [ ] Rollback strategy definida
- [ ] Disaster recovery plan
- [ ] Documentación actualizada

---

## 💰 COSTOS ESTIMADOS (Mensual)

### Opción 1: AWS
- EC2 (3x t3.medium): $100
- RDS PostgreSQL (db.t3.medium): $80
- ElastiCache Redis: $50
- S3 + CloudFront: $30
- Load Balancer: $20
- **Total: ~$280/mes** (hasta 10k usuarios)

### Opción 2: Azure
- App Service (3x B2): $120
- Azure SQL Database: $90
- Redis Cache: $50
- CDN: $30
- **Total: ~$290/mes**

### Opción 3: DigitalOcean (Más económico)
- Droplets (3x 4GB): $72
- Managed PostgreSQL: $60
- Managed Redis: $40
- Spaces CDN: $20
- Load Balancer: $12
- **Total: ~$204/mes**

---

## 🎯 PRIORIDADES

### Fase 1 (Antes de lanzar) - CRÍTICO
1. Implementar autenticación JWT
2. Hashear contraseñas
3. HTTPS obligatorio
4. Validación de inputs
5. Rate limiting básico
6. Backups automáticos de BD

### Fase 2 (Primera semana)
1. Logging estructurado
2. Health checks
3. Caché básico
4. Monitoreo APM
5. CI/CD pipeline

### Fase 3 (Primer mes)
1. Auto-scaling
2. Read replicas
3. CDN
4. Tests automatizados
5. Alertas avanzadas

---

**Última actualización**: 2026-03-08
**Nivel**: Producción Profesional
