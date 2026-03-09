# Backend Dockerfile para .NET 8
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

# Copiar archivos de proyecto
COPY src/FinancialCopilot.API/*.csproj ./src/FinancialCopilot.API/
COPY src/FinancialCopilot.Application/*.csproj ./src/FinancialCopilot.Application/
COPY src/FinancialCopilot.Domain/*.csproj ./src/FinancialCopilot.Domain/
COPY src/FinancialCopilot.Infrastructure/*.csproj ./src/FinancialCopilot.Infrastructure/

# Restaurar dependencias
RUN dotnet restore src/FinancialCopilot.API/FinancialCopilot.API.csproj

# Copiar todo el código
COPY . .

# Build
WORKDIR /app/src/FinancialCopilot.API
RUN dotnet publish -c Release -o /app/publish

# Runtime
FROM mcr.microsoft.com/dotnet/aspnet:8.0
WORKDIR /app
COPY --from=build /app/publish .

# Exponer puerto (Render usa PORT dinámico)
EXPOSE 10000

# Variables de entorno
ENV ASPNETCORE_ENVIRONMENT=Production

# Comando de inicio
# Render asigna el puerto dinámicamente via variable PORT
ENTRYPOINT ["sh", "-c", "dotnet FinancialCopilot.API.dll --urls http://0.0.0.0:${PORT:-10000}"]
