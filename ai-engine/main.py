from fastapi import FastAPI, HTTPException, Depends, Security
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timedelta
import numpy as np
from models.predictor import FinancialPredictor
from models.simulator import FinancialSimulator
import os
import sys

# Agregar path para training modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# API Key security
API_KEY = os.getenv("AI_ENGINE_API_KEY", "")
api_key_header = APIKeyHeader(name="X-AI-Engine-Key", auto_error=False)

def verify_api_key(key: str = Security(api_key_header)):
    # Si no hay API_KEY configurada, solo permitir en desarrollo
    if not API_KEY:
        return True
    if key != API_KEY:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")
    return True

# Intentar cargar Predictor Profesional (NUEVO)
try:
    from models.professional_predictor import ProfessionalPredictor
    professional_predictor = ProfessionalPredictor()
    PROFESSIONAL_AI_ENABLED = professional_predictor.is_ready()
    if PROFESSIONAL_AI_ENABLED:
        print("✅ Predictor Profesional cargado (Modelo entrenado)")
        print(f"   Modelo: {professional_predictor.metadata['model_name']}")
        print(f"   Features: {professional_predictor.metadata['num_features']}")
    else:
        print("⚠️ Predictor Profesional no disponible (modelo no encontrado)")
except Exception as e:
    PROFESSIONAL_AI_ENABLED = False
    professional_predictor = None
    print(f"⚠️ Predictor Profesional no disponible: {e}")

# Intentar cargar módulos avanzados
try:
    from models.advanced_predictor import AdvancedFinancialPredictor
    from models.financial_knowledge import FinancialKnowledgeEngine
    advanced_predictor = AdvancedFinancialPredictor()
    knowledge_engine = FinancialKnowledgeEngine()
    ADVANCED_AI_ENABLED = True
    print("✅ Advanced AI cargado")
except Exception as e:
    ADVANCED_AI_ENABLED = False
    print(f"⚠️ Advanced AI no disponible: {e}")

# Intentar cargar Smart Recommender (opcional)
try:
    from training.smart_recommender import SmartRecommender
    smart_recommender = SmartRecommender()
    smart_recommender.load_models()
    SMART_AI_ENABLED = True
    print("✅ Smart AI Recommender cargado (opcional)")
except Exception as e:
    SMART_AI_ENABLED = False
    print("ℹ️  Smart AI Recommender no disponible (opcional - no afecta funcionalidad principal)")

app = FastAPI(title="Financial Copilot AI Engine")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

predictor = FinancialPredictor()
simulator = FinancialSimulator()

class Transaction(BaseModel):
    amount: float
    date: str
    type: str  # income or expense
    category: Optional[str] = None

class PredictionRequest(BaseModel):
    user_id: str
    transactions: List[Transaction]
    months_ahead: int = 3

class SimulationRequest(BaseModel):
    current_balance: float
    monthly_income: float
    monthly_expenses: float
    debt: float
    interest_rate: float
    months: int = 12
    scenarios: Optional[dict] = None

@app.get("/")
def read_root():
    return {
        "message": "Financial Copilot AI Engine",
        "status": "running",
        "professional_ai": PROFESSIONAL_AI_ENABLED,
        "advanced_ai": ADVANCED_AI_ENABLED,
        "smart_ai": SMART_AI_ENABLED,
        "model": professional_predictor.metadata['model_name'] if PROFESSIONAL_AI_ENABLED else "basic"
    }

@app.post("/predict/balance")
def predict_balance(request: PredictionRequest, _: bool = Depends(verify_api_key)):
    """Predice el balance futuro basado en historial de transacciones"""
    try:
        # Convertir transacciones a formato procesable
        transactions_data = []
        for t in request.transactions:
            transactions_data.append({
                'amount': t.amount,
                'date': datetime.fromisoformat(t.date.replace('Z', '+00:00')),
                'type': t.type,
                'category': t.category
            })
        
        # PRIORIDAD 1: Usar predictor profesional si está disponible (NUEVO)
        if PROFESSIONAL_AI_ENABLED:
            prediction = professional_predictor.predict_future_balance(
                transactions_data,
                months_ahead=request.months_ahead
            )
            prediction['ai_version'] = 'professional'
        # PRIORIDAD 2: Usar predictor avanzado
        elif ADVANCED_AI_ENABLED:
            prediction = advanced_predictor.predict_future_balance_advanced(
                transactions_data,
                months_ahead=request.months_ahead
            )
            prediction['ai_version'] = 'advanced'
        # PRIORIDAD 3: Fallback a predictor básico
        else:
            prediction = predictor.predict_future_balance(
                transactions_data,
                months_ahead=request.months_ahead
            )
            prediction['ai_version'] = 'basic'
        
        return {
            "user_id": request.user_id,
            **prediction
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/expenses")
def predict_expenses(request: PredictionRequest, _: bool = Depends(verify_api_key)):
    """Predice gastos futuros por categoría"""
    try:
        transactions_data = []
        for t in request.transactions:
            transactions_data.append({
                'amount': t.amount,
                'date': datetime.fromisoformat(t.date.replace('Z', '+00:00')),
                'type': t.type,
                'category': t.category
            })
        
        # PRIORIDAD 1: Usar predictor profesional (NUEVO)
        if PROFESSIONAL_AI_ENABLED:
            prediction = professional_predictor.predict_expenses(transactions_data)
            return {
                "user_id": request.user_id,
                **prediction
            }
        # PRIORIDAD 2: Fallback a predictor básico
        else:
            expenses_data = [t for t in transactions_data if t['type'] == 'expense']
            prediction = predictor.predict_category_expenses(
                expenses_data,
                months_ahead=request.months_ahead
            )
            return {
                "user_id": request.user_id,
                "category_predictions": prediction,
                "ai_version": "basic"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/simulate")
def simulate_scenarios(request: SimulationRequest, _: bool = Depends(verify_api_key)):
    """Simula diferentes escenarios financieros"""
    try:
        result = simulator.simulate_financial_scenarios(
            current_balance=request.current_balance,
            monthly_income=request.monthly_income,
            monthly_expenses=request.monthly_expenses,
            debt=request.debt,
            interest_rate=request.interest_rate,
            months=request.months,
            custom_scenarios=request.scenarios
        )
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/risk")
def analyze_risk(request: PredictionRequest, _: bool = Depends(verify_api_key)):
    """Analiza el riesgo financiero del usuario"""
    try:
        transactions_data = []
        for t in request.transactions:
            transactions_data.append({
                'amount': t.amount,
                'date': datetime.fromisoformat(t.date.replace('Z', '+00:00')),
                'type': t.type,
                'category': t.category
            })
        
        # PRIORIDAD 1: Usar predictor profesional (NUEVO)
        if PROFESSIONAL_AI_ENABLED:
            health_analysis = professional_predictor.analyze_financial_health(transactions_data)
            return {
                "user_id": request.user_id,
                **health_analysis,
                "ai_version": "professional"
            }
        # PRIORIDAD 2: Fallback a predictor básico
        else:
            risk_analysis = predictor.analyze_financial_risk(transactions_data)
            return {
                "user_id": request.user_id,
                "risk_score": risk_analysis['risk_score'],
                "risk_level": risk_analysis['risk_level'],
                "factors": risk_analysis['factors'],
                "recommendations": risk_analysis['recommendations'],
                "metrics": risk_analysis['metrics'],
                "ai_version": "basic"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)


class SmartRecommendationRequest(BaseModel):
    user_id: str
    patterns: dict
    aggregated_data: dict

@app.post("/smart/recommendations")
def get_smart_recommendations(request: SmartRecommendationRequest):
    """
    Obtiene recomendaciones inteligentes basadas en ML
    Aprende de datos reales de usuarios
    """
    if not SMART_AI_ENABLED:
        return {
            "error": "Smart AI no disponible",
            "message": "Ejecuta 'python train_models.py' para entrenar los modelos",
            "fallback": True
        }
    
    try:
        user_data = {
            'patterns': request.patterns,
            'aggregated_data': request.aggregated_data
        }
        
        # Obtener recomendaciones del modelo entrenado
        recommendations = smart_recommender.recommend_savings_strategy(user_data)
        
        # Predecir gastos futuros
        predicted_expenses = smart_recommender.predict_expenses(user_data)
        
        return {
            "user_id": request.user_id,
            "smart_ai_enabled": True,
            "predicted_monthly_expenses": predicted_expenses,
            "has_high_savings_potential": recommendations['has_high_potential'],
            "recommendations": recommendations['recommendations'],
            "total_monthly_savings": recommendations['total_monthly_savings'],
            "total_yearly_savings": recommendations['total_yearly_savings'],
            "model_version": "1.0",
            "trained_with_real_data": True
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/smart/status")
def get_smart_ai_status():
    """
    Verifica el estado del Smart AI
    """
    return {
        "smart_ai_enabled": SMART_AI_ENABLED,
        "advanced_ai_enabled": ADVANCED_AI_ENABLED,
        "models_loaded": smart_recommender.is_trained if SMART_AI_ENABLED else False,
        "message": "Smart AI activo y entrenado" if SMART_AI_ENABLED else "Ejecuta 'python train_models.py' para entrenar"
    }

# Nuevos endpoints para IA avanzada

class FinancialHealthRequest(BaseModel):
    user_id: str
    total_income: float
    total_expenses: float
    total_debt: float
    total_savings: float
    avg_monthly_expenses: float
    expenses_by_type: Optional[dict] = None
    expenses_by_category: Optional[dict] = None

@app.post("/analyze/financial-health")
def analyze_financial_health(request: FinancialHealthRequest):
    """
    Analiza salud financiera según principios expertos
    """
    if not ADVANCED_AI_ENABLED:
        return {
            "error": "Advanced AI no disponible",
            "message": "Módulos avanzados no cargados"
        }
    
    try:
        user_data = {
            'total_income': request.total_income,
            'total_expenses': request.total_expenses,
            'total_debt': request.total_debt,
            'total_savings': request.total_savings,
            'avg_monthly_expenses': request.avg_monthly_expenses,
            'expenses_by_type': request.expenses_by_type or {},
            'expenses_by_category': request.expenses_by_category or {}
        }
        
        health_analysis = knowledge_engine.analyze_financial_health(user_data)
        
        return {
            "user_id": request.user_id,
            **health_analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze/behaviors")
def detect_problematic_behaviors(request: PredictionRequest):
    """
    Detecta comportamientos financieros problemáticos
    """
    if not ADVANCED_AI_ENABLED:
        return {
            "error": "Advanced AI no disponible",
            "message": "Módulos avanzados no cargados"
        }
    
    try:
        transactions_data = []
        for t in request.transactions:
            transactions_data.append({
                'amount': t.amount,
                'date': datetime.fromisoformat(t.date.replace('Z', '+00:00')),
                'type': t.type,
                'category': t.category
            })
        
        behaviors = knowledge_engine.detect_problematic_behaviors(transactions_data)
        
        return {
            "user_id": request.user_id,
            **behaviors
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommendations/actionable")
def get_actionable_recommendations(request: FinancialHealthRequest):
    """
    Obtiene recomendaciones ultra-accionables con impacto calculado
    """
    if not ADVANCED_AI_ENABLED:
        return {
            "error": "Advanced AI no disponible",
            "message": "Módulos avanzados no cargados"
        }
    
    try:
        user_data = {
            'expenses_by_category': request.expenses_by_category or {}
        }
        
        recommendations = knowledge_engine.get_actionable_recommendations(user_data, top_n=5)
        
        return {
            "user_id": request.user_id,
            "recommendations": recommendations,
            "total_recommendations": len(recommendations)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
