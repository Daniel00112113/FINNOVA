# Solución de Errores de Despliegue en Render

## Problemas Identificados y Solucionados

### 1. Error de Versión .NET (RESUELTO ✅)

**Error:**
```
error NETSDK1045: The current .NET SDK does not support targeting .NET 10.0
```

**Causa:** Los proyectos estaban configurados para .NET 10.0, pero Render usa .NET SDK 8.0.

**Solución Aplicada:**
- Cambiados todos los `.csproj` de `net10.0` a `net8.0`
- Actualizado el Dockerfile para usar .NET 8.0
- Ajustadas las versiones de paquetes NuGet para compatibilidad con .NET 8.0

### 2. Error de Ruta AI Engine

**Error:**
```
error: invalid local: resolve : lstat /opt/render/project/src/ai-engine/ai-engine: no such file or directory
```

**Causa:** Posible duplicación de carpeta en la configuración de Render.

**Solución:** Verificar la configuración del servicio AI Engine en Render.

## Configuración Correcta para Render

### Backend Service

```yaml
Build Command: cd backend && dotnet restore && dotnet publish -c Release -o out
Start Command: cd backend/out && dotnet FinancialCopilot.API.dll
Root Directory: /
Docker: No (usar comandos nativos)
```

O si usas Docker:

```yaml
Docker Context Directory: backend
Dockerfile Path: backend/Dockerfile
```

### AI Engine Service

```yaml
Build Command: cd ai-engine && pip install -r requirements.txt
Start Command: cd ai-engine && python main.py
Root Directory: /
Environment: Python 3.11
```

O si usas Docker:

```yaml
Docker Context Directory: ai-engine
Dockerfile Path: ai-engine/Dockerfile
```

### Frontend Service (Vercel recomendado)

Si despliegas en Render:

```yaml
Build Command: cd frontend && npm install && npm run build
Start Command: cd frontend && npm start
Root Directory: /
Environment: Node 18
```

## Variables de Entorno Requeridas

### Backend (.NET)

```env
ASPNETCORE_ENVIRONMENT=Production
ASPNETCORE_URLS=http://+:5000
ConnectionStrings__DefaultConnection=Host=dpg-xxx.oregon-postgres.render.com;Database=finnova_db;Username=finnova_user;Password=xxx
JwtSettings__SecretKey=tu-clave-secreta-generada
JwtSettings__Issuer=FinancialCopilot
JwtSettings__Audience=FinancialCopilotUsers
JwtSettings__ExpirationMinutes=60
AiServiceUrl=https://tu-ai-engine.onrender.com
```

### AI Engine (Python)

```env
DATABASE_URL=postgresql://finnova_user:password@dpg-xxx.oregon-postgres.render.com/finnova_db
PORT=8000
ENVIRONMENT=production
```

### Frontend (Next.js)

```env
NEXT_PUBLIC_API_URL=https://tu-backend.onrender.com
NODE_ENV=production
```

## Pasos para Redesplegar

1. **Commit y Push de los cambios:**

```bash
git add .
git commit -m "fix: Corregir versión .NET a 8.0 para Render"
git push origin main
```

2. **En Render Dashboard:**
   - Ve a cada servicio
   - Click en "Manual Deploy" > "Deploy latest commit"
   - O espera el auto-deploy si está habilitado

3. **Verificar logs:**
   - Backend: Debe mostrar "Now listening on: http://[::]:5000"
   - AI Engine: Debe mostrar "Uvicorn running on http://0.0.0.0:8000"

4. **Probar endpoints:**

```bash
# Backend health check
curl https://tu-backend.onrender.com/health

# AI Engine health check
curl https://tu-ai-engine.onrender.com/health
```

## Checklist de Verificación

- [ ] Todos los `.csproj` usan `net8.0`
- [ ] Dockerfile del backend usa `mcr.microsoft.com/dotnet/sdk:8.0`
- [ ] Variables de entorno configuradas en Render
- [ ] Base de datos PostgreSQL creada y accesible
- [ ] Servicios configurados con las rutas correctas
- [ ] Commits pusheados a GitHub
- [ ] Servicios redespliegados en Render

## Troubleshooting Adicional

### Si el backend sigue fallando:

1. Verifica que la cadena de conexión sea correcta
2. Asegúrate de que la base de datos esté en la misma región
3. Revisa los logs en Render para errores específicos

### Si el AI Engine falla:

1. Verifica que `requirements.txt` esté completo
2. Asegúrate de que Python 3.11 esté seleccionado
3. Verifica que el puerto 8000 esté expuesto

### Si hay problemas de CORS:

Verifica en `Program.cs` que el frontend esté en la lista de orígenes permitidos:

```csharp
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowFrontend",
        policy => policy
            .WithOrigins("https://tu-frontend.vercel.app")
            .AllowAnyMethod()
            .AllowAnyHeader()
            .AllowCredentials());
});
```

## Próximos Pasos

1. Esperar a que los servicios se desplieguen correctamente
2. Verificar que todos los endpoints respondan
3. Probar el flujo completo de la aplicación
4. Configurar el dominio personalizado si lo tienes
5. Habilitar SSL/HTTPS (Render lo hace automáticamente)

## Notas Importantes

- Render puede tardar 5-10 minutos en el primer despliegue
- Los servicios gratuitos se duermen después de 15 minutos de inactividad
- La primera petición después de dormir puede tardar 30-60 segundos
- Considera actualizar a un plan de pago para producción real
