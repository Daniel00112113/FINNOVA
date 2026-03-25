# Backend — Deploy

API REST en .NET 10 con Clean Architecture, desplegada como Docker en Render.

## Stack

- .NET 10 / ASP.NET Core
- Entity Framework Core + PostgreSQL (Npgsql)
- JWT Bearer Authentication
- BCrypt para hashing de contraseñas

## Variables de entorno

| Variable                          | Descripción                              | Requerida |
|-----------------------------------|------------------------------------------|-----------|
| `ConnectionStrings__DefaultConnection` | Connection string de PostgreSQL     | ✅        |
| `Jwt__Key`                        | Clave secreta JWT (mín. 32 chars)        | ✅        |
| `Jwt__Issuer`                     | Issuer del JWT                           | ✅        |
| `Jwt__Audience`                   | Audience del JWT                         | ✅        |
| `AiEngine__Url`                   | URL del AI Engine                        | ✅        |
| `AiEngine__ApiKey`                | API key para autenticar al AI Engine     | ✅        |
| `ASPNETCORE_ENVIRONMENT`          | `Production` o `Development`             | ✅        |
| `ASPNETCORE_URLS`                 | Puerto de escucha (`http://+:8080`)      | ✅        |
| `AdminBootstrap__Email`           | Email del primer admin (usar una vez)    | ⚠️ temporal |
| `AdminBootstrap__Password`        | Password del primer admin (usar una vez) | ⚠️ temporal |
| `Cors__AllowedOrigins__0`         | Origen CORS adicional permitido          | opcional  |

> Las variables con `__` son la notación de .NET para configuración jerárquica (`AiEngine:Url` → `AiEngine__Url`).

## Deploy en Render

Render usa el `Dockerfile` de esta carpeta. La DB se conecta automáticamente via `fromDatabase` en `render.yaml`.

```yaml
- key: ConnectionStrings__DefaultConnection
  fromDatabase:
    name: finnova-db
    property: connectionString
```

Las migraciones de EF Core se aplican **automáticamente al arrancar** en `Program.cs`.

## Deploy local

```bash
cd backend
cp .env.example .env
# Editar .env con tus valores locales

# Opción 1: dotnet run
cd src/FinancialCopilot.API
dotnet run
# → http://localhost:5000

# Opción 2: Docker
docker build -t finnova-backend .
docker run -p 5000:8080 \
  -e ConnectionStrings__DefaultConnection="Host=localhost;Database=financialcopilot;Username=postgres;Password=postgres" \
  -e Jwt__Key="clave-local-de-desarrollo-minimo-32-chars" \
  -e Jwt__Issuer="FinancialCopilot" \
  -e Jwt__Audience="FinancialCopilotUsers" \
  -e AiEngine__Url="http://localhost:8000" \
  finnova-backend
```

## Migraciones

```bash
# Crear nueva migración
dotnet ef migrations add NombreMigracion \
  --project src/FinancialCopilot.Infrastructure \
  --startup-project src/FinancialCopilot.API

# Aplicar manualmente
dotnet ef database update \
  --project src/FinancialCopilot.Infrastructure \
  --startup-project src/FinancialCopilot.API
```

En producción las migraciones se aplican automáticamente al arrancar. Si una migración falla por tabla existente, usa `IF NOT EXISTS` en el SQL de la migración.

## Arquitectura

```
backend/src/
├── FinancialCopilot.API/
│   ├── Controllers/        → Endpoints REST
│   │   ├── AdminController     → Panel admin (rol: admin, support)
│   │   ├── AuthController      → Login, register, refresh, logout
│   │   ├── DashboardController → Resumen financiero
│   │   ├── ExpensesController  → CRUD gastos
│   │   ├── IncomesController   → CRUD ingresos
│   │   ├── DebtsController     → CRUD deudas
│   │   ├── GamificationController → Puntos y logros
│   │   ├── PredictionsController  → Predicciones IA
│   │   └── SimulatorController    → Simulador de escenarios
│   └── Program.cs          → DI, JWT, CORS, Rate Limiting, migraciones
│
├── FinancialCopilot.Application/
│   ├── Common/Interfaces/  → IApplicationDbContext, IGamificationService
│   ├── DTOs/               → Data Transfer Objects
│   └── Services/           → Interfaces de servicios
│
├── FinancialCopilot.Domain/
│   └── Entities/           → User, Income, Expense, Debt, AuditLog, RefreshToken...
│
└── FinancialCopilot.Infrastructure/
    ├── Data/               → ApplicationDbContext
    ├── Migrations/         → Migraciones EF Core
    └── Services/           → AuthService, AiService, GamificationService, AuditService
```

## Seguridad implementada

- JWT con expiración de 2h + refresh tokens rotativos (30 días)
- Brute force: bloqueo tras 5 intentos fallidos por 15 minutos
- Rate limiting: 100 req/min por usuario/IP
- Audit log de todas las acciones sensibles
- Roles: `user`, `admin`, `support`, `suspended`
- AI Engine protegido con API key en header `X-AI-Engine-Key`
- HTTPS obligatorio en producción

## Endpoints principales

```
POST   /api/auth/register          → Registro
POST   /api/auth/login             → Login (devuelve JWT + refresh token)
POST   /api/auth/refresh           → Renovar JWT
POST   /api/auth/logout            → Cerrar sesión

GET    /api/users/{id}/dashboard   → Resumen financiero
GET    /api/users/{id}/insights/*  → Alertas, presupuesto diario

GET    /api/admin/metrics          → Métricas globales (admin/support)
GET    /api/admin/users            → Lista usuarios (admin/support)
GET    /api/admin/audit-logs       → Audit log (admin/support)
POST   /api/admin/users/{id}/suspend    → Suspender usuario (admin)
POST   /api/admin/users/{id}/force-logout → Revocar sesiones (admin)
DELETE /api/admin/users/{id}       → Eliminar usuario (admin)
POST   /api/admin/broadcast-alert  → Alerta a todos (admin)
GET    /api/admin/export/users     → CSV usuarios (admin)

GET    /health                     → Health check (público)
```
