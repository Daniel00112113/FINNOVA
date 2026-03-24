# FINNOVA - Financial Copilot

Sistema de gestión financiera personal con IA integrada y gamificación.

## 🚀 Inicio Rápido

### Requisitos
- Docker Desktop
- Node.js 18+
- .NET 8.0+
- PostgreSQL (via Docker)

### Iniciar el Sistema

```powershell
# Iniciar todos los servicios
./start-all.ps1

# Detener todos los servicios
./stop-all.ps1

# Verificar estado del sistema
./verificar-sistema.ps1
```

### URLs
- Frontend: http://localhost:3000
- Backend API: http://localhost:5000
- AI Engine: http://localhost:8000
- Base de datos: localhost:5432

## 📚 Documentación Completa

### Guías Principales
- [Guía de Despliegue](GUIA_DESPLIEGUE_PRODUCCION.md)
- [Guía de Pruebas](GUIA_PRUEBAS_COMPLETAS.md)
- [Guía de Servidor Propio](GUIA_SERVIDOR_PROPIO_COMPLETO.md)
- [Implementación de Seguridad](IMPLEMENTACION_COMPLETA_SEGURIDAD.md)
- [Scripts Disponibles](SCRIPTS_DISPONIBLES.md)
- [Estrategia de Engagement](ESTRATEGIA_ENGAGEMENT_FINNOVA.md)
- [Plan de Gamificación](PLAN_IMPLEMENTACION_GAMIFICACION.md)
- [Mejoras de Producción](MEJORAS_PRODUCCION_IMPLEMENTADAS.md)
- [Sistema Completo](SISTEMA_COMPLETO_LISTO.md)

### Características Implementadas
- ✅ Autenticación JWT con bcrypt
- ✅ Sistema de gamificación (puntos, niveles, rachas, badges)
- ✅ Análisis financiero con IA
- ✅ Predicciones y simulaciones
- ✅ Gestión de gastos, ingresos y deudas
- ✅ Dashboard interactivo
- ✅ Alertas inteligentes
- ✅ Mejoras de producción aplicadas

## 🎮 Sistema de Gamificación

El sistema incluye:
- **Puntos**: Gana puntos por registrar transacciones
  - Gasto registrado: 10 puntos
  - Ingreso registrado: 15 puntos
  - Login diario: 5 puntos
- **Niveles**: Sube de nivel según tus puntos
  - Fórmula: Level = floor(sqrt(points / 100)) + 1
- **Rachas**: Mantén rachas diarias de actividad
  - 7 días consecutivos: 100 puntos bonus
  - 30 días consecutivos: 500 puntos bonus
- **Badges**: Desbloquea logros especiales
  - 🎯 Primer Paso, 🔥 Racha de Fuego, ⚡ Imparable
  - 📝 Registrador, 🎯 Cazador de Gastos, 🏆 Maestro del Registro
  - ⭐ Novato Avanzado, 💎 Experto Financiero
- **Widget flotante**: Visible en todas las páginas

### Endpoints de Gamificación
- `GET /api/users/{userId}/gamification/stats` - Obtener estadísticas
- `POST /api/users/{userId}/gamification/activity` - Registrar actividad
- `GET /api/users/{userId}/gamification/badges` - Obtener badges

## 🔧 Estructura del Proyecto

```
FINNOVA/
├── frontend/              # Next.js + React + TypeScript
│   ├── src/
│   │   ├── app/          # Páginas de la aplicación
│   │   ├── components/   # Componentes reutilizables
│   │   │   └── gamification/  # Componentes de gamificación
│   │   └── lib/          # Utilidades y configuración
│   └── public/           # Archivos estáticos
├── backend/              # .NET 8 + Entity Framework
│   └── src/
│       ├── FinancialCopilot.API/           # Controladores y endpoints
│       ├── FinancialCopilot.Application/   # DTOs e interfaces
│       ├── FinancialCopilot.Domain/        # Entidades del dominio
│       └── FinancialCopilot.Infrastructure/ # Servicios y DbContext
├── ai-engine/            # Python + FastAPI + scikit-learn
│   ├── models/           # Modelos de ML
│   ├── training/         # Scripts de entrenamiento
│   └── main.py          # API de IA
├── design-assets/        # Recursos de diseño
└── logs/                # Logs del sistema
```

## 🛠️ Desarrollo

### Backend
```powershell
cd backend
dotnet build
dotnet run --project src/FinancialCopilot.API
```

### Frontend
```powershell
cd frontend
npm install
npm run dev
```

### AI Engine
```powershell
cd ai-engine
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## 📊 Base de Datos

### Tablas Principales
- `Users` - Usuarios del sistema
- `Expenses` - Gastos registrados
- `Incomes` - Ingresos registrados
- `Debts` - Deudas activas
- `Alerts` - Alertas financieras
- `SpendingPatterns` - Patrones de gasto
- `user_progress` - Progreso de gamificación
- `achievements` - Logros desbloqueados

### Migraciones Aplicadas
- ✅ Estructura base (Users, Expenses, Incomes, Debts)
- ✅ Campos adicionales de Expenses (Location, Tags, IsRecurring)
- ✅ User Consent
- ✅ Gamificación (user_progress, achievements)

### Aplicar Migraciones
```powershell
cd backend
dotnet ef database update
```

## 🔐 Seguridad

- **Autenticación JWT**: Tokens seguros con expiración
- **Passwords hasheados**: bcrypt con salt
- **CORS configurado**: Solo orígenes permitidos
- **Rate limiting**: Protección contra abuso
- **HTTPS redirect**: En producción
- **Variables de entorno**: Para secretos

## 📈 Mejoras de Producción

- ✅ Manejo de errores mejorado con try-catch
- ✅ Logging estructurado en consola
- ✅ Validación de datos en DTOs
- ✅ Optimización de consultas con índices
- ✅ Caché implementado en servicios
- ✅ Monitoreo de salud con /health endpoint
- ✅ Manejo graceful de columnas duplicadas en migraciones

## 🎯 Componentes de Gamificación

### Frontend
- `GamificationWidget.tsx` - Widget principal para dashboard
- `FloatingGamification.tsx` - Widget flotante para todas las páginas
- `AchievementToast.tsx` - Notificaciones de logros
- `GamificationProvider.tsx` - Context provider global
- `ClientGamification.tsx` - Wrapper para componentes cliente

### Backend
- `GamificationController.cs` - Endpoints de gamificación
- `GamificationService.cs` - Lógica de negocio
- `UserProgress.cs` - Entidad de progreso
- `Achievement.cs` - Entidad de logros

## 📝 Notas Importantes

1. **Docker debe estar ejecutándose** antes de iniciar el sistema
2. **Las migraciones se aplican automáticamente** al iniciar el backend
3. **El AI Engine es opcional** - el sistema funciona sin él con fallback
4. **Usa variables de entorno** para configuración sensible en producción
5. **El widget de gamificación** se muestra en todas las páginas automáticamente

## 🐛 Solución de Problemas

### Backend no inicia
- Verifica que Docker esté ejecutándose
- Verifica que el puerto 5000 esté libre
- Revisa los logs en la consola
- Ejecuta: `Get-Process -Name "FinancialCopilot.API" | Stop-Process -Force`

### Frontend no conecta
- Verifica que el backend esté ejecutándose en http://localhost:5000
- Verifica la URL del API en las variables de entorno
- Revisa la consola del navegador (F12)
- Limpia caché del navegador

### Base de datos no conecta
- Verifica que el contenedor de PostgreSQL esté ejecutándose
- Verifica las credenciales en appsettings.json
- Ejecuta: `docker ps` para ver contenedores activos
- Ejecuta: `docker logs financial-copilot-db` para ver logs

### Gamificación muestra errores 500
- Verifica que las tablas `user_progress` y `achievements` existan
- Ejecuta: `docker exec financial-copilot-db psql -U postgres -d financialcopilot -c "\dt"`
- Si no existen, aplica la migración: `docker cp backend/MIGRACION_GAMIFICACION.sql financial-copilot-db:/tmp/gamification.sql`
- Luego: `docker exec financial-copilot-db psql -U postgres -d financialcopilot -f /tmp/gamification.sql`

## 📞 Soporte

Para problemas o preguntas:
1. Revisa esta documentación
2. Consulta las guías específicas en la carpeta raíz
3. Revisa los comentarios en el código
4. Ejecuta `./verificar-sistema.ps1` para diagnóstico

## 🔄 Actualizaciones Recientes

### Marzo 2026
- ✅ Sistema de gamificación implementado y funcionando
- ✅ Widget flotante en todas las páginas
- ✅ Notificaciones de logros en tiempo real
- ✅ Integración con transacciones (gastos/ingresos)
- ✅ Tablas de base de datos configuradas correctamente
- ✅ DbContext mapeado a nombres de tabla en minúsculas
- ✅ Limpieza de documentación duplicada

---

**Versión**: 1.0.0  
**Última actualización**: 11 de Marzo 2026  
**Estado**: ✅ Producción Ready
