# Base de Datos — Deploy

PostgreSQL 16 gestionado por Render (plan free) o local con Docker.

## Render (producción)

La DB se crea automáticamente desde `render.yaml`:

```yaml
databases:
  - name: finnova-db
    databaseName: financialcopilot
    user: postgres
    plan: free
```

La connection string se inyecta automáticamente al backend:

```yaml
- key: ConnectionStrings__DefaultConnection
  fromDatabase:
    name: finnova-db
    property: connectionString
```

### Límites del plan free de Render

| Recurso       | Límite          |
|---------------|-----------------|
| Storage        | 1 GB            |
| Conexiones     | 97 simultáneas  |
| Expiración     | 90 días sin uso |
| Backups        | No incluidos    |

> Después de 90 días sin actividad, Render elimina la DB. Haz backups periódicos.

### Backup manual

```bash
# Desde Render Dashboard → finnova-db → Connections → copiar External URL
pg_dump "postgresql://user:pass@host/finnova_db" > backup_$(date +%Y%m%d).sql
```

### Restore

```bash
psql "postgresql://user:pass@host/finnova_db" < backup_20260324.sql
```

---

## Local con Docker

```bash
docker compose up postgres -d

# Verificar que está corriendo
docker exec financialcopilot-db pg_isready -U postgres -d financialcopilot
```

Connection string local:
```
Host=localhost;Database=financialcopilot;Username=postgres;Password=postgres
```

## Local sin Docker

```bash
# Instalar PostgreSQL 16
# Crear DB
createdb financialcopilot

# Connection string
Host=localhost;Database=financialcopilot;Username=postgres;Password=<tu_password>
```

---

## Esquema

Las migraciones se aplican automáticamente al arrancar el backend. El esquema actual incluye:

| Tabla              | Descripción                              |
|--------------------|------------------------------------------|
| `Users`            | Usuarios con roles, brute force, tokens  |
| `Incomes`          | Ingresos de usuarios                     |
| `Expenses`         | Gastos con categorías, tags, recurrencia |
| `Debts`            | Deudas con interés y fechas              |
| `Alerts`           | Alertas del sistema y broadcasts admin   |
| `SpendingPatterns` | Patrones de gasto analizados             |
| `RefreshTokens`    | Tokens de sesión rotativos (30 días)     |
| `AuditLogs`        | Log de todas las acciones sensibles      |
| `user_progress`    | Gamificación: puntos, nivel, racha       |
| `achievements`     | Logros desbloqueados por usuario         |

## Migraciones aplicadas

| Migración                              | Descripción                                    |
|----------------------------------------|------------------------------------------------|
| `20260305184615_InitialCreate`         | Tablas base: Users, Incomes, Expenses, Debts   |
| `20260308000000_AddExpenseFields`      | Location, IsRecurring, RecurrenceType, Tags    |
| `20260324223353_AddRolesAuditRefreshTokens` | Role, brute force, RefreshTokens, AuditLogs |

## Índices importantes

```sql
-- Rendimiento en queries frecuentes
CREATE INDEX idx_expenses_user_id ON "Expenses"("UserId");
CREATE INDEX idx_incomes_user_id ON "Incomes"("UserId");
CREATE INDEX idx_audit_logs_user_id ON "AuditLogs"("UserId");
CREATE INDEX idx_audit_logs_created_at ON "AuditLogs"("CreatedAt");
CREATE INDEX idx_refresh_tokens_token ON "RefreshTokens"("Token");
CREATE UNIQUE INDEX idx_user_progress_user_id ON user_progress(user_id);
```

## Queries útiles de administración

```sql
-- Ver todos los admins
SELECT id, name, email, role, "LastLoginAt" FROM "Users" WHERE role = 'admin';

-- Usuarios bloqueados actualmente
SELECT name, email, "FailedLoginAttempts", "LockedUntil"
FROM "Users" WHERE "LockedUntil" > NOW();

-- Actividad reciente (últimas 24h)
SELECT action, entity, "IpAddress", success, "CreatedAt"
FROM "AuditLogs" WHERE "CreatedAt" > NOW() - INTERVAL '24 hours'
ORDER BY "CreatedAt" DESC LIMIT 50;

-- IPs sospechosas (múltiples fallos en 1h)
SELECT "IpAddress", COUNT(*) as intentos
FROM "AuditLogs"
WHERE action = 'login_failed' AND "CreatedAt" > NOW() - INTERVAL '1 hour'
GROUP BY "IpAddress" HAVING COUNT(*) >= 3
ORDER BY intentos DESC;

-- Volumen financiero total
SELECT
  SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as total_ingresos,
  SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as total_gastos
FROM (
  SELECT amount, 'income' as type FROM "Incomes"
  UNION ALL
  SELECT amount, 'expense' as type FROM "Expenses"
) t;

-- Limpiar refresh tokens expirados (mantenimiento)
DELETE FROM "RefreshTokens" WHERE "ExpiresAt" < NOW() OR "IsRevoked" = true;

-- Limpiar audit logs viejos (>90 días)
DELETE FROM "AuditLogs" WHERE "CreatedAt" < NOW() - INTERVAL '90 days';
```
