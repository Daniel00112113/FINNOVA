# 💰 FINNOVA - Financial Copilot

Sistema inteligente de gestión financiera personal con IA profesional.

![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

---

## 🚀 Características

### 💡 Inteligencia Artificial Profesional
- **Modelo ML entrenado** con 145,814 transacciones reales
- **Predicciones precisas** de gastos futuros (R² = 1.000)
- **44 características** de análisis financiero
- **Sistema de fallback** de 3 niveles

### 📊 Dashboard Inteligente
- **Alertas prioritarias** en tiempo real
- **Presupuesto diario** calculado automáticamente
- **Métricas financieras** consolidadas
- **Recomendaciones personalizadas** basadas en tus datos

### 🎯 Simulador Financiero
- **5 escenarios** diferentes de tu futuro
- **Proyección mes a mes** hasta 24 meses
- **Cálculo automático** de intereses y deudas
- **Recomendaciones** basadas en tus gastos reales

### 🔮 Predicciones y Análisis
- Predicción de gastos futuros
- Análisis de riesgo financiero
- Detección de gastos hormiga
- Análisis de suscripciones
- Plan de fondo de emergencia

### 🔐 Seguridad Nivel Producción
- JWT Authentication
- BCrypt para contraseñas (12 rounds)
- Rate Limiting (100 req/min)
- HTTPS redirect automático
- CORS configurado
- Error handling seguro

---

## 🛠️ Tecnologías

### Backend
- **.NET 10** - Framework principal
- **Entity Framework Core** - ORM
- **PostgreSQL** - Base de datos
- **JWT** - Autenticación
- **BCrypt** - Encriptación

### Frontend
- **Next.js 14** - Framework React
- **TypeScript** - Tipado estático
- **Tailwind CSS** - Estilos
- **Recharts** - Gráficos
- **Axios** - HTTP client

### IA Engine
- **Python 3.11** - Lenguaje
- **FastAPI** - API REST
- **Scikit-learn** - Machine Learning
- **Pandas** - Análisis de datos
- **NumPy** - Cálculos numéricos

---

## 📦 Instalación

### Requisitos Previos
- Node.js 20+
- .NET 10 SDK
- Python 3.11+
- PostgreSQL 15+
- Docker (opcional)

### 1. Clonar Repositorio
```bash
git clone https://github.com/DanielDEV03/FINNOVA.git
cd FINNOVA
```

### 2. Configurar Base de Datos
```bash
# Iniciar PostgreSQL con Docker
docker run --name financial-copilot-db \
  -e POSTGRES_DB=financialcopilot \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  -d postgres:15
```

### 3. Configurar Backend
```bash
cd backend/src/FinancialCopilot.API

# Restaurar paquetes
dotnet restore

# Aplicar migraciones
dotnet ef database update

# Iniciar
dotnet run
```

### 4. Configurar AI Engine
```bash
cd ai-engine

# Crear entorno virtual
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt

# Iniciar
python main.py
```

### 5. Configurar Frontend
```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar
npm run dev
```

### 6. Acceder
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000
- **AI Engine**: http://localhost:8000
- **Swagger**: http://localhost:5000/swagger

---

## 🚀 Inicio Rápido

```powershell
# Script automático (Windows)
.\start-secure.ps1
```

Este script inicia automáticamente:
1. PostgreSQL (Docker)
2. AI Engine (Python)
3. Backend (.NET)
4. Frontend (Next.js)

---

## 📚 Documentación

- [Guía de Despliegue](GUIA_DESPLIEGUE_PRODUCCION.md)
- [Servidor Propio](GUIA_SERVIDOR_PROPIO_COMPLETO.md)
- [Guía de Pruebas](GUIA_PRUEBAS_COMPLETAS.md)
- [Estado del Sistema](ESTADO_FINAL_COMPLETO.md)

---

## 🎯 Características Destacadas

### Recomendaciones Personalizadas
El sistema analiza TUS gastos reales y genera recomendaciones específicas basadas en tus categorías con más gasto, no recomendaciones genéricas.

### Simulador Inteligente
Proyecta 5 escenarios diferentes de tu futuro financiero considerando ingresos, gastos, deudas e intereses mes a mes.

### IA Profesional
Modelo entrenado con datos ultra-realistas de Colombia, 44 características de análisis y sistema de fallback robusto.

### Dashboard Consolidado
Todo en un solo lugar: alertas prioritarias, presupuesto diario, métricas principales y acciones rápidas.

---

## 🔐 Seguridad

- ✅ JWT Authentication con tokens firmados
- ✅ Contraseñas hasheadas con BCrypt (12 rounds)
- ✅ Rate Limiting (100 requests/minuto)
- ✅ HTTPS redirect en producción
- ✅ CORS configurado dinámicamente
- ✅ Error handling seguro
- ✅ Swagger deshabilitado en producción

---

## 📊 Arquitectura

```
FINNOVA/
├── backend/              # API .NET 10
│   ├── src/
│   │   ├── API/         # Controllers, Program.cs
│   │   ├── Application/ # DTOs, Interfaces
│   │   ├── Domain/      # Entities
│   │   └── Infrastructure/ # Services, DbContext
│   └── FinancialCopilot.sln
│
├── frontend/            # Next.js 14
│   ├── src/
│   │   ├── app/        # Pages (App Router)
│   │   ├── components/ # Componentes
│   │   └── lib/        # Utilidades
│   └── package.json
│
├── ai-engine/          # FastAPI + ML
│   ├── models/         # Modelos ML
│   ├── training/       # Entrenamiento
│   └── main.py
│
└── docs/               # Documentación
```

---

## 🤝 Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📝 Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más información.

---

## 👨‍💻 Autor

**Daniel DEV**
- GitHub: [@DanielDEV03](https://github.com/DanielDEV03)
- Proyecto: [FINNOVA](https://github.com/DanielDEV03/FINNOVA)

---

## 🙏 Agradecimientos

- Datos de investigación financiera de Colombia
- Comunidad de .NET y Next.js
- Scikit-learn por las herramientas de ML

---

## 📈 Roadmap

- [ ] App móvil nativa (React Native)
- [ ] Integración con bancos (Open Banking)
- [ ] Notificaciones push
- [ ] Exportar reportes PDF
- [ ] Metas de ahorro
- [ ] Presupuestos por categoría
- [ ] Análisis de inversiones

---

## 💡 Soporte

Si tienes preguntas o problemas:
1. Revisa la [documentación](ESTADO_FINAL_COMPLETO.md)
2. Abre un [Issue](https://github.com/DanielDEV03/FINNOVA/issues)
3. Contacta al autor

---

**Hecho con ❤️ en Colombia 🇨🇴**
