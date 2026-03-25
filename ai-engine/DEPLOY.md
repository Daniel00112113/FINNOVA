# AI Engine — Deploy

FastAPI con modelos de ML para predicciones y simulaciones financieras, desplegado como Docker en Render.

## Stack

- Python 3.11
- FastAPI + Uvicorn
- scikit-learn, pandas, numpy
- xgboost, lightgbm (modelo profesional)

## Variables de entorno

| Variable            | Descripción                                      | Requerida |
|---------------------|--------------------------------------------------|-----------|
| `PORT`              | Puerto de escucha (Render lo asigna dinámicamente) | ✅      |
| `AI_ENGINE_API_KEY` | Clave para autenticar requests del backend       | ✅ en prod |

> Si `AI_ENGINE_API_KEY` está vacía, el engine acepta cualquier request (solo para desarrollo local).

## Deploy en Render

Render usa el `Dockerfile` de esta carpeta. El `CMD` usa `${PORT:-8000}` para respetar el puerto dinámico de Render.

La API key se comparte automáticamente desde el backend via `render.yaml`:

```yaml
- key: AI_ENGINE_API_KEY
  fromService:
    name: finnova-backend
    type: web
    envVarKey: AiEngine__ApiKey
```

## Deploy local

```bash
cd ai-engine

# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate
# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
pip install xgboost lightgbm  # opcional, para modelo profesional

# Ejecutar
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
# → http://localhost:8000
# → Docs: http://localhost:8000/docs
```

## Docker local

```bash
docker build -t finnova-ai .
docker run -p 8000:8000 -e PORT=8000 finnova-ai
```

## Endpoints

Todos los endpoints (excepto `/` y `/health`) requieren el header:
```
X-AI-Engine-Key: <valor de AI_ENGINE_API_KEY>
```

| Método | Endpoint                    | Descripción                              |
|--------|-----------------------------|------------------------------------------|
| GET    | `/`                         | Estado del engine y modelos cargados     |
| POST   | `/predict/balance`          | Predice balance futuro (3/6/12 meses)    |
| POST   | `/predict/expenses`         | Predice gastos por categoría             |
| POST   | `/simulate`                 | Simula 5 escenarios financieros          |
| POST   | `/analyze/risk`             | Calcula score de riesgo (0-100)          |
| POST   | `/analyze/financial-health` | Análisis de salud financiera             |
| GET    | `/smart/status`             | Estado del Smart AI Recommender          |

## Modelos de IA

### Jerarquía de predictores (orden de prioridad)

```
1. ProfessionalPredictor   → Modelo entrenado con XGBoost/LightGBM
                             Requiere: models/professional/best_model.pkl
                             Si no existe → cae al siguiente

2. AdvancedPredictor       → GradientBoosting + RandomForest de sklearn
                             Siempre disponible (no requiere archivos externos)

3. BasicPredictor          → Regresión lineal simple
                             Fallback final
```

### Modelo profesional (opcional)

Los archivos `.pkl` no están en git (son pesados). Para entrenar localmente:

```bash
# Generar datos sintéticos
python generate_realistic_data.py

# Entrenar modelo profesional
python train_professional.py

# Los archivos se guardan en models/professional/
# best_model.pkl, scaler.pkl, metadata.json
```

`metadata.json` sí está en git y es necesario para que el predictor profesional funcione correctamente.

### Fallback automático

Si el AI Engine no responde, el backend `.NET` tiene un fallback que calcula predicciones y simulaciones usando los datos reales del usuario directamente, sin llamar al engine. El usuario nunca ve un error — solo datos calculados localmente.

## Estructura

```
ai-engine/
├── main.py                     → FastAPI app, endpoints, auth middleware
├── models/
│   ├── predictor.py            → Predictor básico (regresión lineal)
│   ├── advanced_predictor.py   → Predictor avanzado (GradientBoosting)
│   ├── professional_predictor.py → Predictor con modelo entrenado
│   ├── simulator.py            → Simulador de escenarios
│   ├── financial_knowledge.py  → Motor de conocimiento financiero
│   └── professional/
│       └── metadata.json       → Metadatos del modelo (en git)
│       └── best_model.pkl      → Modelo entrenado (NO en git)
│       └── scaler.pkl          → Scaler (NO en git)
└── training/
    ├── professional_trainer.py       → Entrenamiento del modelo
    ├── professional_feature_engineering.py → 44 features financieras
    ├── smart_recommender.py          → Recomendaciones ML
    └── data_collector.py             → Recolección de datos
```

## Notas de producción

- En Render free tier, el servicio se duerme tras 15 min de inactividad. El primer request tarda ~30s en despertar. El backend tiene timeout de 25s y fallback automático.
- El modelo profesional no está disponible en producción (`.pkl` no en git). El engine usa el `AdvancedPredictor` que sí funciona sin archivos externos.
- Para habilitar el modelo profesional en producción, necesitarías un servicio con almacenamiento persistente o subir los `.pkl` a un bucket S3/R2 y descargarlos al arrancar.
