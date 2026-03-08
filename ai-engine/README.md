# Financial Copilot - AI Engine

Motor de inteligencia artificial para predicciones y simulaciones financieras.

## 🚀 Instalación

```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## 🏃 Ejecutar

```bash
python main.py
```

API disponible en: http://localhost:8000
Documentación: http://localhost:8000/docs

## 📋 Endpoints

### Predicción de Balance
`POST /predict/balance`
- Predice balance futuro basado en historial
- Usa regresión lineal
- Retorna tendencia y nivel de riesgo

### Predicción de Gastos
`POST /predict/expenses`
- Predice gastos futuros por categoría
- Detecta tendencias por categoría

### Simulador de Escenarios
`POST /simulate`
- Simula múltiples escenarios financieros
- Compara resultados
- Recomienda mejor estrategia

### Análisis de Riesgo
`POST /analyze/risk`
- Calcula score de riesgo (0-100)
- Identifica factores de riesgo
- Genera recomendaciones

## 🧠 Modelos

### FinancialPredictor
- Regresión lineal para predicción de balance
- Análisis de tendencias por categoría
- Cálculo de riesgo financiero

### FinancialSimulator
- Simulación de escenarios "what-if"
- Comparación de estrategias
- Optimización de pagos de deuda

## 🔧 Tecnologías

- FastAPI
- NumPy
- Pandas
- Scikit-learn
