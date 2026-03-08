# 🚀 DESPLIEGUE EN RENDER - GUÍA COMPLETA

## 📋 RESUMEN
Necesitas crear 3 servicios en Render:
1. **PostgreSQL** (Base de datos)
2. **AI Engine** (Python/FastAPI)
3. **Backend** (.NET API)
4. **Frontend** (Next.js) - En Vercel (gratis)

---

## 🗄️ PASO 1: CREAR BASE DE DATOS POSTGRESQL

### En Render Dashboard:
1. Click en "New +" → "PostgreSQL"
2. Configurar:
   - **Name**: `finnova-db`
   - **Database**: `financialcopilot`
   - **User**: `postgres` (automático)
   - **Region**: `Oregon (US West)`
   - **Plan**: `Free` ($0/mes)
3. Click "Create Database"
4. **COPIAR** la "Internal Database URL" (la necesitarás)

Ejemplo: `postgresql://postgres:password@dpg-xxx.oregon-postgres.render.com/financialcopilot`

---

## 🤖 PASO 2: CREAR AI ENGINE (Python)

### Configuración:
- **Name**: `finnova-ai-engine`
- **Language**: `Docker`
- **Branch**: `main`
- **Region**: `Oregon (US West)`
- **Root Directory**: `ai-engine`
- **Dockerfile Path**: `ai-engine/Dockerfile`
- **Instance Type**: `Free` ($0/mes) o `Starter` ($7/mes recomendado)

### Environment Variables:
```
DATABASE_URL=postgresql://postgres:password@dpg-xxx.oregon-postgres.render.com/financialcopilot
PORT=8000
```

### ⚠️ IMPORTANTE:
Reemplaza `DATABASE_URL` con la URL que copiaste en el Paso 1.

---

## 🔧 PASO 3: CREAR BACKEND (.NET)

### Configuración:
- **Name**: `finnova-backend`
- **Language**: `Docker`
- **Branch**: `main`
- **Region**: `Oregon (US West)`
- **Root Directory**: `backend`
- **Dockerfile Path**: `backend/Dockerfile`
- **Instance Type**: `Starter` ($7/mes mínimo para .NET)

### Environment Variables:
```
ASPNETCORE_ENVIRONMENT=Production
ConnectionStrings__DefaultConnection=postgresql://postgres:password@dpg-xxx.oregon-postgres.render.com/financialcopilot
Jwt__Key=5MhKNCPWe8S0419g7dykLwzfYQqsXDubAtlxJUjFZTVRIroamc2Hin3B6EvGOp
Jwt__Issuer=FinancialCopilot
Jwt__Audience=FinancialCopilotUsers
Jwt__ExpirationMinutes=60
Cors__AllowedOrigins=https://tu-frontend.vercel.app
AiEngine__BaseUrl=https://finnova-ai-engine.onrender.com
```

### ⚠️ IMPORTANTE:
- Reemplaza `DATABASE_URL` con tu URL de PostgreSQL
- Reemplaza `Cors__AllowedOrigins` después de desplegar el frontend
- Reemplaza `AiEngine__BaseUrl` con la URL del AI Engine (la obtendrás después)

---

## 🎨 PASO 4: DESPLEGAR FRONTEND EN VERCEL

### En tu terminal local:
```powershell
cd frontend

# Instalar Vercel CLI
npm install -g vercel

# Login
vercel login

# Desplegar
vercel --prod
```

### Environment Variables en Vercel:
```
NEXT_PUBLIC_API_URL=https://finnova-backend.onrender.com/api
```

---

## 📝 PASO 5: CREAR DOCKERFILES

Necesitas crear Dockerfiles para Backend y AI Engine.

### 1. Backend Dockerfile
Crear: `backend/Dockerfile`

### 2. AI Engine Dockerfile
Ya existe: `ai-engine/Dockerfile`

---

## ✅ ORDEN DE DESPLIEGUE

1. **PostgreSQL** (primero, para obtener la URL)
2. **AI Engine** (segundo, para obtener su URL)
3. **Backend** (tercero, usando las URLs anteriores)
4. **Frontend** (último, usando la URL del backend)

---

## 🔄 ACTUALIZAR VARIABLES DESPUÉS

Una vez que todos los servicios estén desplegados:

### Backend - Actualizar:
```
Cors__AllowedOrigins=https://tu-frontend.vercel.app
AiEngine__BaseUrl=https://finnova-ai-engine.onrender.com
```

### Frontend - Actualizar:
```
NEXT_PUBLIC_API_URL=https://finnova-backend.onrender.com/api
```

---

## 💰 COSTOS ESTIMADOS

### Opción GRATIS (limitada):
- PostgreSQL: $0 (Free tier)
- AI Engine: $0 (Free tier - se duerme después de 15 min)
- Backend: $7/mes (Starter mínimo para .NET)
- Frontend: $0 (Vercel gratis)
**TOTAL: $7/mes**

### Opción RECOMENDADA:
- PostgreSQL: $7/mes (Starter)
- AI Engine: $7/mes (Starter)
- Backend: $25/mes (Standard)
- Frontend: $0 (Vercel gratis)
**TOTAL: $39/mes**

---

## 🆘 PROBLEMAS COMUNES

### 1. "Dockerfile not found"
- Verifica que el `Root Directory` esté correcto
- Verifica que el `Dockerfile Path` sea relativo al root del repo

### 2. "Build failed"
- Revisa los logs en Render
- Verifica que todas las dependencias estén en el Dockerfile

### 3. "Database connection failed"
- Verifica que la `DATABASE_URL` sea correcta
- Usa la "Internal Database URL" (no la External)

---

## 🎯 SIGUIENTE PASO

Voy a crear los Dockerfiles que faltan para que puedas desplegar.

