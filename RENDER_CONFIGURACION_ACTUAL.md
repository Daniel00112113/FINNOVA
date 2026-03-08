# 🚀 CONFIGURACIÓN PARA LA PANTALLA ACTUAL DE RENDER

## 📋 LO QUE VES AHORA

Estás en la pantalla de crear un nuevo Web Service. Aquí está EXACTAMENTE qué poner:

---

## ⚠️ IMPORTANTE: ORDEN CORRECTO

**NO DESPLIEGUES EL BACKEND TODAVÍA**. Primero necesitas:
1. Crear PostgreSQL
2. Crear AI Engine
3. Luego Backend

---

## 🗄️ PRIMERO: CREAR POSTGRESQL

### Sal de esta pantalla y:
1. Click en "New +" (arriba derecha)
2. Selecciona "PostgreSQL"
3. Configurar:
   - **Name**: `finnova-db`
   - **Database**: `financialcopilot`
   - **Region**: `Oregon (US West)`
   - **Plan**: `Free`
4. Click "Create Database"
5. **ESPERA** a que termine de crear (2-3 minutos)
6. **COPIA** la "Internal Database URL"

---

## 🤖 SEGUNDO: CREAR AI ENGINE

### Vuelve a "New +" → "Web Service":

**Source Code:**
- Repository: `DanielDEV03/FINNOVA`
- Branch: `main`

**Name:**
```
finnova-ai-engine
```

**Language:**
```
Docker
```

**Branch:**
```
main
```

**Region:**
```
Oregon (US West)
```

**Root Directory:**
```
ai-engine
```

**Dockerfile Path:**
```
ai-engine/Dockerfile
```

**Instance Type:**
```
Free (o Starter si quieres mejor rendimiento)
```

**Environment Variables:**
Click "Add Environment Variable" y agrega:

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://postgres:xxx@dpg-xxx.oregon-postgres.render.com/financialcopilot` |
| `PORT` | `8000` |

⚠️ Reemplaza `DATABASE_URL` con la URL que copiaste de PostgreSQL.

**Deploy:**
Click "Deploy Web Service"

**ESPERA** a que termine (5-10 minutos)

**COPIA** la URL del servicio (ejemplo: `https://finnova-ai-engine.onrender.com`)

---

## 🔧 TERCERO: CREAR BACKEND

### Vuelve a "New +" → "Web Service":

**Source Code:**
- Repository: `DanielDEV03/FINNOVA`
- Branch: `main`

**Name:**
```
finnova-backend
```

**Language:**
```
Docker
```

**Branch:**
```
main
```

**Region:**
```
Oregon (US West)
```

**Root Directory:**
```
backend
```

**Dockerfile Path:**
```
backend/Dockerfile
```

**Instance Type:**
```
Starter ($7/mes) - MÍNIMO para .NET
```

**Environment Variables:**
Click "Add Environment Variable" y agrega TODAS estas:

| Key | Value |
|-----|-------|
| `ASPNETCORE_ENVIRONMENT` | `Production` |
| `ConnectionStrings__DefaultConnection` | `postgresql://postgres:xxx@dpg-xxx.oregon-postgres.render.com/financialcopilot` |
| `Jwt__Key` | `5MhKNCPWe8S0419g7dykLwzfYQqsXDubAtlxJUjFZTVRIroamc2Hin3B6EvGOp` |
| `Jwt__Issuer` | `FinancialCopilot` |
| `Jwt__Audience` | `FinancialCopilotUsers` |
| `Jwt__ExpirationMinutes` | `60` |
| `Cors__AllowedOrigins` | `http://localhost:3000` |
| `AiEngine__BaseUrl` | `https://finnova-ai-engine.onrender.com` |

⚠️ Reemplaza:
- `ConnectionStrings__DefaultConnection` con tu URL de PostgreSQL
- `AiEngine__BaseUrl` con la URL del AI Engine que copiaste

**Deploy:**
Click "Deploy Web Service"

**ESPERA** a que termine (10-15 minutos)

**COPIA** la URL del backend (ejemplo: `https://finnova-backend.onrender.com`)

---

## 🎨 CUARTO: DESPLEGAR FRONTEND EN VERCEL

### En tu terminal local:

```powershell
cd frontend

# Crear archivo .env.production
echo "NEXT_PUBLIC_API_URL=https://finnova-backend.onrender.com/api" > .env.production

# Desplegar
npx vercel --prod
```

Sigue las instrucciones de Vercel.

**COPIA** la URL del frontend (ejemplo: `https://finnova.vercel.app`)

---

## 🔄 QUINTO: ACTUALIZAR CORS EN BACKEND

### En Render, ve al Backend:
1. Click en "Environment"
2. Edita `Cors__AllowedOrigins`
3. Cambia a: `https://finnova.vercel.app` (tu URL de Vercel)
4. Click "Save Changes"
5. El servicio se reiniciará automáticamente

---

## ✅ VERIFICAR QUE TODO FUNCIONA

### 1. PostgreSQL:
```
Status: Available
```

### 2. AI Engine:
Abre: `https://finnova-ai-engine.onrender.com/docs`
Deberías ver la documentación de FastAPI.

### 3. Backend:
Abre: `https://finnova-backend.onrender.com/health`
Deberías ver: `{"status":"healthy"}`

### 4. Frontend:
Abre: `https://finnova.vercel.app`
Deberías ver la landing page.

---

## 💰 COSTO TOTAL

- PostgreSQL Free: $0
- AI Engine Free: $0
- Backend Starter: $7/mes
- Frontend Vercel: $0

**TOTAL: $7/mes**

⚠️ Los servicios Free se duermen después de 15 minutos de inactividad. La primera request después de dormir tarda ~30 segundos.

---

## 🎯 RESUMEN DE PASOS

1. ✅ Crear PostgreSQL → Copiar URL
2. ✅ Crear AI Engine → Copiar URL
3. ✅ Crear Backend → Copiar URL
4. ✅ Desplegar Frontend en Vercel
5. ✅ Actualizar CORS en Backend
6. ✅ Probar todo

---

## 🆘 SI ALGO FALLA

### Backend no inicia:
- Revisa los logs en Render
- Verifica que todas las variables de entorno estén correctas
- Verifica que la DATABASE_URL sea la "Internal" no la "External"

### AI Engine no inicia:
- Revisa los logs
- Verifica que DATABASE_URL esté correcta

### Frontend no conecta:
- Verifica que NEXT_PUBLIC_API_URL sea correcta
- Verifica que CORS esté configurado con la URL de Vercel

---

**¡Ahora sí, comienza con el Paso 1: Crear PostgreSQL!**

