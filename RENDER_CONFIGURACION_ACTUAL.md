# 🚀 CONFIGURACIÓN PARA RENDER - ACTUALIZADA

## ⚠️ ERRORES CORREGIDOS

### ✅ Problema 1: Versión .NET (RESUELTO)
- **Error:** SDK 8.0 no soporta .NET 10.0
- **Solución:** Todos los proyectos cambiados a `net8.0`
- **Acción:** Hacer commit y push de los cambios

### ⚠️ Problema 2: Ruta AI Engine
- **Error:** Ruta duplicada en configuración
- **Solución:** Usar configuración correcta abajo

---

## 📋 ORDEN CORRECTO DE DESPLIEGUE

1. ✅ Crear PostgreSQL
2. ✅ Crear AI Engine
3. ✅ Crear Backend (con los cambios de .NET 8)
4. ✅ Desplegar Frontend en Vercel

---

## 🗄️ PASO 1: CREAR POSTGRESQL

1. Click en "New +" (arriba derecha)
2. Selecciona "PostgreSQL"
3. Configurar:
   - **Name**: `finnova-db`
   - **Database**: `financialcopilot`
   - **Region**: `Oregon (US West)`
   - **Plan**: `Free`
4. Click "Create Database"
5. **ESPERA** a que termine (2-3 minutos)
6. **COPIA** la "Internal Database URL"

---

## 🤖 PASO 2: CREAR AI ENGINE

### Configuración del Servicio:

**Name:**
```
finnova-ai-engine
```

**Language:**
```
Docker
```

**Repository:**
```
DanielDEV03/FINNOVA
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
Free
```

**Environment Variables:**

| Key | Value |
|-----|-------|
| `DATABASE_URL` | `postgresql://finnova_user:password@dpg-xxx.oregon-postgres.render.com/finnova_db` |
| `PORT` | `8000` |
| `ENVIRONMENT` | `production` |

⚠️ Reemplaza `DATABASE_URL` con la URL Internal de tu PostgreSQL.

**Deploy:**
Click "Create Web Service"

**COPIA** la URL del servicio (ejemplo: `https://finnova-ai-engine.onrender.com`)

---

## 🔧 PASO 3: HACER COMMIT DE LOS CAMBIOS

**IMPORTANTE:** Antes de desplegar el backend, necesitas hacer commit de los cambios de .NET 8:

```bash
git add .
git commit -m "fix: Cambiar de .NET 10 a .NET 8 para compatibilidad con Render"
git push origin main
```

---

## 🔧 PASO 4: CREAR BACKEND

### Configuración del Servicio:

**Name:**
```
finnova-backend
```

**Language:**
```
Docker
```

**Repository:**
```
DanielDEV03/FINNOVA
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

| Key | Value |
|-----|-------|
| `ASPNETCORE_ENVIRONMENT` | `Production` |
| `ASPNETCORE_URLS` | `http://+:5000` |
| `ConnectionStrings__DefaultConnection` | `Host=dpg-xxx.oregon-postgres.render.com;Database=finnova_db;Username=finnova_user;Password=xxx` |
| `JwtSettings__SecretKey` | `5MhKNCPWe8S0419g7dykLwzfYQqsXDubAtlxJUjFZTVRIroamc2Hin3B6EvGOp` |
| `JwtSettings__Issuer` | `FinancialCopilot` |
| `JwtSettings__Audience` | `FinancialCopilotUsers` |
| `JwtSettings__ExpirationMinutes` | `60` |
| `AiServiceUrl` | `https://finnova-ai-engine.onrender.com` |

⚠️ Reemplaza:
- `ConnectionStrings__DefaultConnection` con tu cadena de conexión de PostgreSQL
- `AiServiceUrl` con la URL del AI Engine

**Deploy:**
Click "Create Web Service"

**COPIA** la URL del backend (ejemplo: `https://finnova-backend.onrender.com`)

---

## 🎨 PASO 5: DESPLEGAR FRONTEND EN VERCEL

### Opción A: Desde la terminal

```bash
cd frontend

# Instalar Vercel CLI si no lo tienes
npm i -g vercel

# Configurar variables de entorno
echo "NEXT_PUBLIC_API_URL=https://finnova-backend.onrender.com" > .env.production

# Desplegar
vercel --prod
```

### Opción B: Desde Vercel Dashboard

1. Ve a [vercel.com](https://vercel.com)
2. Click "Add New" → "Project"
3. Importa tu repositorio `DanielDEV03/FINNOVA`
4. Configurar:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`
5. Agregar variable de entorno:
   - `NEXT_PUBLIC_API_URL` = `https://finnova-backend.onrender.com`
6. Click "Deploy"

**COPIA** la URL del frontend (ejemplo: `https://finnova.vercel.app`)

---

## � PASO 6: ACTUALIZAR CORS EN BACKEND

### En Render, ve al servicio Backend:
1. Click en "Environment"
2. Agrega nueva variable:
   - Key: `CorsOrigins`
   - Value: `https://finnova.vercel.app,http://localhost:3000`
3. Click "Save Changes"
4. El servicio se reiniciará automáticamente

---

## ✅ VERIFICAR QUE TODO FUNCIONA

### 1. PostgreSQL:
En Render → finnova-db:
```
Status: Available
```

### 2. AI Engine:
```bash
curl https://finnova-ai-engine.onrender.com/health
```
Debería responder: `{"status":"healthy"}`

### 3. Backend:
```bash
curl https://finnova-backend.onrender.com/health
```
Debería responder con status 200

### 4. Frontend:
Abre: `https://finnova.vercel.app`
Deberías ver la landing page

---

## 🐛 TROUBLESHOOTING

### Backend falla con error .NET:
✅ **YA RESUELTO** - Los archivos ya están actualizados a .NET 8.0
- Solo necesitas hacer commit y push

### AI Engine falla con error de ruta:
- Verifica que "Root Directory" sea exactamente: `ai-engine`
- Verifica que "Dockerfile Path" sea: `ai-engine/Dockerfile`

### Backend no conecta a la base de datos:
- Usa la URL "Internal" no la "External"
- Formato correcto: `Host=xxx;Database=xxx;Username=xxx;Password=xxx`

### Frontend no conecta al backend:
- Verifica que `NEXT_PUBLIC_API_URL` esté correcta
- Verifica que CORS incluya la URL de Vercel

---

## 💰 COSTO TOTAL

- PostgreSQL Free: $0
- AI Engine Free: $0
- Backend Starter: $7/mes
- Frontend Vercel: $0

**TOTAL: $7/mes**

⚠️ Los servicios Free se duermen después de 15 minutos de inactividad.

---

## 📝 CHECKLIST FINAL

- [ ] PostgreSQL creado y disponible
- [ ] AI Engine desplegado y respondiendo
- [ ] Cambios de .NET 8 commiteados y pusheados
- [ ] Backend desplegado correctamente
- [ ] Frontend desplegado en Vercel
- [ ] CORS configurado con URL de Vercel
- [ ] Todos los servicios responden correctamente

---

## 🆘 SOPORTE ADICIONAL

Ver documentación detallada en:
- `SOLUCION_ERRORES_RENDER.md` - Detalles técnicos de los errores
- `GUIA_DESPLIEGUE_PRODUCCION.md` - Guía completa de producción

**¡Ahora sí, todo está listo para desplegar!**
