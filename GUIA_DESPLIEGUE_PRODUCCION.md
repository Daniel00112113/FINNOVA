# 🚀 GUÍA COMPLETA DE DESPLIEGUE A PRODUCCIÓN

## ⚠️ CRÍTICO: ANTES DE DESPLEGAR

Esta guía te llevará paso a paso para desplegar tu Financial Copilot de forma segura y profesional.

---

## 📋 CHECKLIST PRE-DESPLIEGUE

### ✅ Seguridad (OBLIGATORIO)
- [ ] Cambiar JWT Key a clave aleatoria segura
- [ ] Habilitar HTTPS
- [ ] Configurar CORS específico (no "*")
- [ ] Implementar Rate Limiting
- [ ] Configurar variables de entorno
- [ ] Deshabilitar Swagger en producción
- [ ] Configurar logs seguros (sin datos sensibles)

### ✅ Base de Datos
- [ ] Configurar PostgreSQL en producción
- [ ] Aplicar todas las migraciones
- [ ] Configurar backups automáticos
- [ ] Configurar SSL para conexión a BD

### ✅ Infraestructura
- [ ] Configurar dominio y DNS
- [ ] Configurar certificados SSL
- [ ] Configurar CDN (opcional)
- [ ] Configurar monitoreo
- [ ] Configurar alertas

---

## 🔐 PASO 1: SEGURIDAD CRÍTICA

### 1.1 Generar JWT Key Segura

```powershell
# PowerShell - Generar clave aleatoria de 64 caracteres
-join ((65..90) + (97..122) + (48..57) | Get-Random -Count 64 | ForEach-Object {[char]$_})
```

Ejemplo de salida:
```
aB3dE7fG9hJ2kL4mN6pQ8rS0tU1vW3xY5zA7bC9dE2fG4hJ6kL8mN0pQ2rS4tU6vW8xY0zA
```

### 1.2 Configurar Variables de Entorno

**Backend - appsettings.Production.json:**
```json
{
  "Jwt": {
    "Key": "TU-CLAVE-GENERADA-AQUI-64-CARACTERES-MINIMO",
    "Issuer": "FinancialCopilot",
    "Audience": "FinancialCopilotUsers",
    "ExpirationDays": 7
  },
  "ConnectionStrings": {
    "DefaultConnection": "Host=tu-servidor-postgres;Database=financialcopilot;Username=tu-usuario;Password=tu-password;SSL Mode=Require"
  },
  "AiEngine": {
    "BaseUrl": "https://ai.tudominio.com"
  },
  "Cors": {
    "AllowedOrigins": ["https://tudominio.com", "https://www.tudominio.com"]
  }
}
```

**Frontend - .env.production:**
```bash
NEXT_PUBLIC_API_URL=https://api.tudominio.com/api
NEXT_PUBLIC_AI_ENGINE_URL=https://ai.tudominio.com
```

**AI Engine - .env:**
```bash
DATABASE_URL=postgresql://usuario:password@host:5432/financialcopilot?sslmode=require
ENVIRONMENT=production
LOG_LEVEL=INFO
```

### 1.3 Actualizar Program.cs para Producción

```csharp
// backend/src/FinancialCopilot.API/Program.cs

var builder = WebApplication.CreateBuilder(args);

// JWT Authentication
var jwtKey = builder.Configuration["Jwt:Key"] 
    ?? throw new InvalidOperationException("JWT Key must be configured in production");
var key = Encoding.UTF8.GetBytes(jwtKey);

builder.Services.AddAuthentication(options =>
{
    options.DefaultAuthenticateScheme = JwtBearerDefaults.AuthenticationScheme;
    options.DefaultChallengeScheme = JwtBearerDefaults.AuthenticationScheme;
})
.AddJwtBearer(options =>
{
    options.RequireHttpsMetadata = true; // ✅ HTTPS obligatorio
    options.SaveToken = true;
    options.TokenValidationParameters = new TokenValidationParameters
    {
        ValidateIssuerSigningKey = true,
        IssuerSigningKey = new SymmetricSecurityKey(key),
        ValidateIssuer = true,
        ValidIssuer = builder.Configuration["Jwt:Issuer"],
        ValidateAudience = true,
        ValidAudience = builder.Configuration["Jwt:Audience"],
        ValidateLifetime = true,
        ClockSkew = TimeSpan.Zero
    };
});

// CORS específico
var allowedOrigins = builder.Configuration.GetSection("Cors:AllowedOrigins").Get<string[]>()
    ?? throw new InvalidOperationException("CORS origins must be configured");

builder.Services.AddCors(options =>
{
    options.AddPolicy("Production", policy =>
    {
        policy.WithOrigins(allowedOrigins)
              .AllowAnyHeader()
              .AllowAnyMethod()
              .AllowCredentials();
    });
});

// Rate Limiting
builder.Services.AddRateLimiter(options =>
{
    options.GlobalLimiter = PartitionedRateLimiter.Create<HttpContext, string>(
        context => RateLimitPartition.GetFixedWindowLimiter(
            partitionKey: context.User.Identity?.Name ?? context.Connection.RemoteIpAddress?.ToString() ?? "anonymous",
            factory: partition => new FixedWindowRateLimiterOptions
            {
                PermitLimit = 100,
                Window = TimeSpan.FromMinutes(1),
                QueueProcessingOrder = QueueProcessingOrder.OldestFirst,
                QueueLimit = 10
            }));
    
    options.OnRejected = async (context, token) =>
    {
        context.HttpContext.Response.StatusCode = 429;
        await context.HttpContext.Response.WriteAsync("Too many requests. Please try again later.", token);
    };
});

var app = builder.Build();

// Configuración de producción
if (app.Environment.IsProduction())
{
    app.UseHsts(); // ✅ HSTS
    app.UseHttpsRedirection(); // ✅ Redirect HTTP → HTTPS
}
else
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseCors("Production"); // ✅ CORS específico
app.UseRateLimiter(); // ✅ Rate limiting
app.UseAuthentication();
app.UseAuthorization();
app.MapControllers();

app.Run();
```

---

## 🏗️ PASO 2: OPCIONES DE DESPLIEGUE

### Opción A: Azure (RECOMENDADO para .NET)

#### 2.1 Crear Recursos en Azure

```bash
# Instalar Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# Login
az login

# Crear Resource Group
az group create --name financial-copilot-rg --location eastus

# Crear PostgreSQL
az postgres flexible-server create \
  --resource-group financial-copilot-rg \
  --name financial-copilot-db \
  --location eastus \
  --admin-user adminuser \
  --admin-password "TuPasswordSeguro123!" \
  --sku-name Standard_B1ms \
  --tier Burstable \
  --storage-size 32 \
  --version 15

# Crear App Service Plan
az appservice plan create \
  --name financial-copilot-plan \
  --resource-group financial-copilot-rg \
  --sku B1 \
  --is-linux

# Crear Web App para Backend
az webapp create \
  --resource-group financial-copilot-rg \
  --plan financial-copilot-plan \
  --name financial-copilot-api \
  --runtime "DOTNET|8.0"

# Crear Web App para AI Engine
az webapp create \
  --resource-group financial-copilot-rg \
  --plan financial-copilot-plan \
  --name financial-copilot-ai \
  --runtime "PYTHON|3.11"
```

#### 2.2 Configurar Variables de Entorno en Azure

```bash
# Backend
az webapp config appsettings set \
  --resource-group financial-copilot-rg \
  --name financial-copilot-api \
  --settings \
    Jwt__Key="TU-CLAVE-GENERADA" \
    ConnectionStrings__DefaultConnection="Host=financial-copilot-db.postgres.database.azure.com;Database=financialcopilot;Username=adminuser;Password=TuPasswordSeguro123!;SSL Mode=Require"

# AI Engine
az webapp config appsettings set \
  --resource-group financial-copilot-rg \
  --name financial-copilot-ai \
  --settings \
    DATABASE_URL="postgresql://adminuser:TuPasswordSeguro123!@financial-copilot-db.postgres.database.azure.com:5432/financialcopilot?sslmode=require"
```

#### 2.3 Desplegar Backend

```bash
cd backend/src/FinancialCopilot.API

# Publicar
dotnet publish -c Release -o ./publish

# Crear ZIP
Compress-Archive -Path ./publish/* -DestinationPath ./app.zip

# Desplegar
az webapp deployment source config-zip \
  --resource-group financial-copilot-rg \
  --name financial-copilot-api \
  --src ./app.zip
```

#### 2.4 Desplegar AI Engine

```bash
cd ai-engine

# Crear ZIP con requirements.txt
Compress-Archive -Path ./* -DestinationPath ./app.zip

# Desplegar
az webapp deployment source config-zip \
  --resource-group financial-copilot-rg \
  --name financial-copilot-ai \
  --src ./app.zip
```

#### 2.5 Desplegar Frontend en Vercel

```bash
cd frontend

# Instalar Vercel CLI
npm i -g vercel

# Login
vercel login

# Configurar variables de entorno
vercel env add NEXT_PUBLIC_API_URL production
# Valor: https://financial-copilot-api.azurewebsites.net/api

# Desplegar
vercel --prod
```

---

### Opción B: Railway (MÁS FÁCIL)

#### 2.1 Crear Cuenta en Railway
https://railway.app

#### 2.2 Desplegar PostgreSQL
1. New Project → PostgreSQL
2. Copiar DATABASE_URL

#### 2.3 Desplegar Backend
```bash
cd backend

# Crear railway.json
{
  "build": {
    "builder": "NIXPACKS",
    "buildCommand": "dotnet publish src/FinancialCopilot.API/FinancialCopilot.API.csproj -c Release -o out"
  },
  "deploy": {
    "startCommand": "cd out && dotnet FinancialCopilot.API.dll",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}

# Desplegar
railway up
```

#### 2.4 Desplegar AI Engine
```bash
cd ai-engine

# Railway detecta automáticamente Python
railway up
```

#### 2.5 Desplegar Frontend en Vercel
```bash
cd frontend
vercel --prod
```

---

### Opción C: Docker + VPS (MÁS CONTROL)

#### 2.1 Crear Dockerfiles

**Backend Dockerfile:**
```dockerfile
# backend/Dockerfile
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src
COPY ["src/FinancialCopilot.API/FinancialCopilot.API.csproj", "src/FinancialCopilot.API/"]
COPY ["src/FinancialCopilot.Application/FinancialCopilot.Application.csproj", "src/FinancialCopilot.Application/"]
COPY ["src/FinancialCopilot.Domain/FinancialCopilot.Domain.csproj", "src/FinancialCopilot.Domain/"]
COPY ["src/FinancialCopilot.Infrastructure/FinancialCopilot.Infrastructure.csproj", "src/FinancialCopilot.Infrastructure/"]
RUN dotnet restore "src/FinancialCopilot.API/FinancialCopilot.API.csproj"
COPY . .
WORKDIR "/src/src/FinancialCopilot.API"
RUN dotnet build "FinancialCopilot.API.csproj" -c Release -o /app/build

FROM build AS publish
RUN dotnet publish "FinancialCopilot.API.csproj" -c Release -o /app/publish

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "FinancialCopilot.API.dll"]
```

**AI Engine Dockerfile:**
```dockerfile
# ai-engine/Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Frontend Dockerfile:**
```dockerfile
# frontend/Dockerfile
FROM node:20-alpine AS base

FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm ci

FROM base AS builder
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
RUN npm run build

FROM base AS runner
WORKDIR /app
ENV NODE_ENV production
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static

EXPOSE 3000
CMD ["node", "server.js"]
```

#### 2.2 Docker Compose para Producción

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: financialcopilot
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    networks:
      - app-network
    restart: unless-stopped

  backend:
    build: ./backend
    environment:
      Jwt__Key: ${JWT_KEY}
      ConnectionStrings__DefaultConnection: "Host=postgres;Database=financialcopilot;Username=${DB_USER};Password=${DB_PASSWORD}"
      AiEngine__BaseUrl: "http://ai-engine:8000"
    depends_on:
      - postgres
    networks:
      - app-network
    restart: unless-stopped

  ai-engine:
    build: ./ai-engine
    environment:
      DATABASE_URL: "postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/financialcopilot"
    depends_on:
      - postgres
    networks:
      - app-network
    restart: unless-stopped

  frontend:
    build: ./frontend
    environment:
      NEXT_PUBLIC_API_URL: "https://api.tudominio.com/api"
    depends_on:
      - backend
    networks:
      - app-network
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - frontend
      - backend
      - ai-engine
    networks:
      - app-network
    restart: unless-stopped

volumes:
  postgres_data:

networks:
  app-network:
    driver: bridge
```

#### 2.3 Configurar Nginx

```nginx
# nginx.conf
events {
    worker_connections 1024;
}

http {
    upstream frontend {
        server frontend:3000;
    }

    upstream backend {
        server backend:80;
    }

    upstream ai-engine {
        server ai-engine:8000;
    }

    # Redirect HTTP to HTTPS
    server {
        listen 80;
        server_name tudominio.com www.tudominio.com;
        return 301 https://$server_name$request_uri;
    }

    # Frontend
    server {
        listen 443 ssl http2;
        server_name tudominio.com www.tudominio.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://frontend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
    }

    # Backend API
    server {
        listen 443 ssl http2;
        server_name api.tudominio.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://backend;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
    }

    # AI Engine
    server {
        listen 443 ssl http2;
        server_name ai.tudominio.com;

        ssl_certificate /etc/nginx/ssl/cert.pem;
        ssl_certificate_key /etc/nginx/ssl/key.pem;

        location / {
            proxy_pass http://ai-engine;
            proxy_http_version 1.1;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}
```

#### 2.4 Desplegar en VPS

```bash
# En tu VPS (DigitalOcean, Linode, AWS EC2, etc.)

# Clonar repositorio
git clone https://github.com/tu-usuario/financial-copilot.git
cd financial-copilot

# Crear .env
cat > .env << EOF
DB_USER=postgres
DB_PASSWORD=tu-password-seguro
JWT_KEY=tu-clave-jwt-generada
EOF

# Iniciar con Docker Compose
docker-compose -f docker-compose.prod.yml up -d

# Ver logs
docker-compose -f docker-compose.prod.yml logs -f
```

---

## 🔒 PASO 3: CONFIGURAR SSL/HTTPS

### Opción A: Let's Encrypt (GRATIS)

```bash
# Instalar Certbot
sudo apt-get update
sudo apt-get install certbot python3-certbot-nginx

# Obtener certificado
sudo certbot --nginx -d tudominio.com -d www.tudominio.com -d api.tudominio.com -d ai.tudominio.com

# Renovación automática
sudo certbot renew --dry-run
```

### Opción B: Cloudflare (GRATIS + CDN)

1. Agregar dominio a Cloudflare
2. Cambiar nameservers
3. SSL/TLS → Full (strict)
4. Automático ✅

---

## 📊 PASO 4: MONITOREO Y LOGS

### 4.1 Application Insights (Azure)

```bash
# Instalar paquete
dotnet add package Microsoft.ApplicationInsights.AspNetCore

# Configurar en Program.cs
builder.Services.AddApplicationInsightsTelemetry();
```

### 4.2 Sentry (Errores)

```bash
# Frontend
npm install @sentry/nextjs

# Backend
dotnet add package Sentry.AspNetCore
```

### 4.3 Logs Estructurados

```csharp
// Program.cs
builder.Logging.AddJsonConsole();
```

---

## 💾 PASO 5: BACKUPS AUTOMÁTICOS

### PostgreSQL Backups

```bash
# Script de backup diario
#!/bin/bash
# backup.sh

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/backups"
DB_NAME="financialcopilot"

# Crear backup
pg_dump -h localhost -U postgres $DB_NAME | gzip > $BACKUP_DIR/backup_$DATE.sql.gz

# Mantener solo últimos 30 días
find $BACKUP_DIR -name "backup_*.sql.gz" -mtime +30 -delete

# Subir a S3 (opcional)
aws s3 cp $BACKUP_DIR/backup_$DATE.sql.gz s3://tu-bucket/backups/
```

```bash
# Agregar a crontab
crontab -e
# Agregar: 0 2 * * * /path/to/backup.sh
```

---

## 📈 PASO 6: ESCALABILIDAD

### 6.1 Configurar Auto-scaling (Azure)

```bash
az monitor autoscale create \
  --resource-group financial-copilot-rg \
  --resource financial-copilot-api \
  --resource-type Microsoft.Web/serverfarms \
  --name autoscale-plan \
  --min-count 1 \
  --max-count 5 \
  --count 1

az monitor autoscale rule create \
  --resource-group financial-copilot-rg \
  --autoscale-name autoscale-plan \
  --condition "Percentage CPU > 70 avg 5m" \
  --scale out 1
```

### 6.2 CDN para Assets Estáticos

```bash
# Azure CDN
az cdn profile create \
  --resource-group financial-copilot-rg \
  --name financial-copilot-cdn \
  --sku Standard_Microsoft
```

---

## ✅ CHECKLIST POST-DESPLIEGUE

- [ ] Verificar que HTTPS funciona
- [ ] Probar registro de usuario
- [ ] Probar login
- [ ] Verificar que API requiere token
- [ ] Probar todas las features principales
- [ ] Verificar logs
- [ ] Configurar alertas
- [ ] Documentar URLs de producción
- [ ] Configurar dominio personalizado
- [ ] Probar desde diferentes dispositivos

---

## 🎯 URLS FINALES

Después del despliegue tendrás:

- **Frontend**: https://tudominio.com
- **Backend API**: https://api.tudominio.com
- **AI Engine**: https://ai.tudominio.com (interno)
- **Swagger**: Deshabilitado en producción

---

## 💰 COSTOS ESTIMADOS

### Azure (Opción A)
- PostgreSQL: ~$20/mes
- App Service (2x): ~$30/mes
- Total: ~$50/mes

### Railway (Opción B)
- PostgreSQL: $5/mes
- Backend: $5/mes
- AI Engine: $5/mes
- Total: ~$15/mes

### VPS (Opción C)
- DigitalOcean Droplet: $12-24/mes
- Total: ~$12-24/mes

### Frontend (Todas las opciones)
- Vercel: GRATIS (Hobby plan)

---

## 🆘 SOPORTE POST-DESPLIEGUE

### Comandos Útiles

```bash
# Ver logs (Azure)
az webapp log tail --name financial-copilot-api --resource-group financial-copilot-rg

# Ver logs (Docker)
docker-compose logs -f backend

# Reiniciar servicio (Azure)
az webapp restart --name financial-copilot-api --resource-group financial-copilot-rg

# Reiniciar servicio (Docker)
docker-compose restart backend
```

---

**Última actualización**: 2026-03-08
**Tiempo estimado de despliegue**: 2-4 horas
**Dificultad**: Media-Alta

¡Tu Financial Copilot está listo para producción! 🚀
