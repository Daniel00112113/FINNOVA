# Backend Dockerfile para .NET 10
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

# Exponer puerto
EXPOSE 5000

# Variables de entorno
ENV ASPNETCORE_URLS=http://+:5000
ENV ASPNETCORE_ENVIRONMENT=Production

# Comando de inicio
ENTRYPOINT ["dotnet", "FinancialCopilot.API.dll"]
