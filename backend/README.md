# Financial Copilot - Backend API

## 🏗️ Arquitectura

Clean Architecture con 4 capas:

- **Domain**: Entidades del negocio
- **Application**: Lógica de aplicación, DTOs, interfaces
- **Infrastructure**: Implementación de base de datos
- **API**: Controllers y configuración

## 🚀 Comenzar

### Requisitos
- .NET 8 SDK
- PostgreSQL

### Configuración

1. Instalar PostgreSQL y crear base de datos:
```bash
createdb financialcopilot
```

2. Actualizar connection string en `appsettings.json`

3. Ejecutar migraciones:
```bash
cd src/FinancialCopilot.API
dotnet ef migrations add InitialCreate --project ../FinancialCopilot.Infrastructure
dotnet ef database update
```

4. Ejecutar API:
```bash
dotnet run
```

API disponible en: https://localhost:5001

Swagger UI: https://localhost:5001/swagger

## 📋 Endpoints

### Users
- POST /api/users/register - Registrar usuario
- GET /api/users/{id} - Obtener usuario

### Incomes
- POST /api/users/{userId}/incomes - Crear ingreso
- GET /api/users/{userId}/incomes - Listar ingresos

### Expenses
- POST /api/users/{userId}/expenses - Crear gasto
- GET /api/users/{userId}/expenses - Listar gastos

### Dashboard
- GET /api/users/{userId}/dashboard - Dashboard financiero
