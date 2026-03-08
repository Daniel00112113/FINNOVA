"""
Predictor Profesional - Usa el modelo entrenado
"""
import numpy as np
import pandas as pd
import joblib
import json
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from pathlib import Path
import sys
import os

# Agregar path para imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from training.professional_feature_engineering import ProfessionalFeatureEngineer

class ProfessionalPredictor:
    """
    Predictor que usa el modelo profesional entrenado
    """
    
    def __init__(self, model_path: str = "models/professional"):
        self.model_path = Path(model_path)
        self.model = None
        self.scaler = None
        self.metadata = None
        self.feature_engineer = ProfessionalFeatureEngineer()
        self.load_model()
    
    def load_model(self):
        """Carga el modelo entrenado"""
        try:
            # Cargar modelo
            model_file = self.model_path / "best_model.pkl"
            if model_file.exists():
                self.model = joblib.load(model_file)
                print(f"✅ Modelo cargado: {model_file}")
            else:
                print(f"⚠️ Modelo no encontrado: {model_file}")
                return False
            
            # Cargar scaler
            scaler_file = self.model_path / "scaler.pkl"
            if scaler_file.exists():
                self.scaler = joblib.load(scaler_file)
                print(f"✅ Scaler cargado: {scaler_file}")
            
            # Cargar metadata
            metadata_file = self.model_path / "metadata.json"
            if metadata_file.exists():
                with open(metadata_file, 'r') as f:
                    self.metadata = json.load(f)
                print(f"✅ Metadata cargado: {self.metadata['model_name']}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return False
    
    def is_ready(self) -> bool:
        """Verifica si el modelo está listo"""
        return self.model is not None and self.scaler is not None
    
    def predict_expenses(self, transactions: List[Dict]) -> Dict:
        """
        Predice gastos futuros usando el modelo profesional
        """
        if not self.is_ready():
            return self._fallback_prediction(transactions)
        
        # Verificar que hay suficientes transacciones
        if len(transactions) < 10:
            print(f"ℹ️ Pocas transacciones ({len(transactions)}), usando fallback")
            return self._fallback_prediction(transactions)
        
        try:
            # Preparar datos del usuario
            user_data = {'transactions': transactions}
            
            # Extraer features
            features = self.feature_engineer.extract_all_features(user_data)
            
            # Verificar que tenemos todas las features necesarias
            feature_names = self.metadata['feature_names']
            
            # Convertir a DataFrame y asegurar que todas las columnas existen
            feature_df = pd.DataFrame([features])
            
            # Verificar que todas las features requeridas están presentes
            missing_features = set(feature_names) - set(feature_df.columns)
            if missing_features:
                print(f"⚠️ Features faltantes: {len(missing_features)}, usando fallback")
                return self._fallback_prediction(transactions)
            
            # Seleccionar solo las features que el modelo necesita
            X = feature_df[feature_names]
            
            # Normalizar
            X_scaled = self.scaler.transform(X)
            
            # Predecir
            prediction = self.model.predict(X_scaled)[0]
            
            # Calcular métricas adicionales
            df = pd.DataFrame(transactions)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                expenses = df[df['type'] == 'expense']
                
                current_avg = expenses['amount'].mean() if len(expenses) > 0 else 0
                total_expenses = expenses['amount'].sum() if len(expenses) > 0 else 0
                
                # Calcular tendencia
                if len(expenses) > 10:
                    recent = expenses.tail(5)['amount'].mean()
                    older = expenses.head(5)['amount'].mean()
                    trend = "increasing" if recent > older else "decreasing" if recent < older else "stable"
                else:
                    trend = "stable"
                
                # Calcular confianza
                confidence = self._calculate_confidence(len(transactions))
                
                # Generar recomendaciones
                recommendations = self._generate_smart_recommendations(
                    prediction, current_avg, features, df
                )
                
                return {
                    'predicted_monthly_expenses': float(prediction),
                    'current_average': float(current_avg),
                    'total_expenses': float(total_expenses),
                    'trend': trend,
                    'confidence': confidence,
                    'recommendations': recommendations,
                    'model_used': self.metadata['model_name'],
                    'features_analyzed': len(feature_names)
                }
            else:
                return {
                    'predicted_monthly_expenses': float(prediction),
                    'confidence': 0.5,
                    'recommendations': ['Registra más transacciones para predicciones más precisas'],
                    'model_used': self.metadata['model_name']
                }
                
        except Exception as e:
            print(f"⚠️ Error en predicción profesional: {str(e)[:100]}")
            return self._fallback_prediction(transactions)
    
    def predict_future_balance(self, transactions: List[Dict], months_ahead: int = 3) -> Dict:
        """
        Predice balance futuro usando el modelo profesional
        """
        if not self.is_ready():
            return self._fallback_balance_prediction(transactions, months_ahead)
        
        try:
            # Predecir gastos mensuales
            expense_prediction = self.predict_expenses(transactions)
            predicted_monthly_expense = expense_prediction['predicted_monthly_expenses']
            
            # Calcular ingresos promedio
            df = pd.DataFrame(transactions)
            if not df.empty:
                df['date'] = pd.to_datetime(df['date'])
                incomes = df[df['type'] == 'income']
                avg_monthly_income = incomes['amount'].mean() if len(incomes) > 0 else 0
                
                # Calcular balance actual
                total_income = incomes['amount'].sum() if len(incomes) > 0 else 0
                expenses = df[df['type'] == 'expense']
                total_expenses = expenses['amount'].sum() if len(expenses) > 0 else 0
                current_balance = total_income - total_expenses
                
                # Predecir balance futuro
                predictions = []
                last_date = df['date'].max() if len(df) > 0 else pd.Timestamp.now(tz=timezone.utc)
                
                for i in range(months_ahead):
                    future_balance = current_balance + (avg_monthly_income - predicted_monthly_expense) * (i + 1)
                    future_date = last_date + timedelta(days=30 * (i + 1))
                    
                    predictions.append({
                        'month': future_date.strftime('%Y-%m'),
                        'predicted_balance': float(future_balance),
                        'predicted_income': float(avg_monthly_income),
                        'predicted_expenses': float(predicted_monthly_expense),
                        'confidence': expense_prediction['confidence']
                    })
                
                # Determinar tendencia y riesgo
                final_balance = predictions[-1]['predicted_balance']
                trend = "increasing" if final_balance > current_balance else "decreasing"
                
                if final_balance < 0:
                    risk_level = "high"
                elif final_balance < current_balance * 0.5:
                    risk_level = "medium"
                else:
                    risk_level = "low"
                
                return {
                    'predictions': predictions,
                    'current_balance': float(current_balance),
                    'trend': trend,
                    'risk_level': risk_level,
                    'confidence': expense_prediction['confidence'],
                    'recommendations': expense_prediction['recommendations'],
                    'model_used': self.metadata['model_name']
                }
            else:
                return self._fallback_balance_prediction(transactions, months_ahead)
                
        except Exception as e:
            print(f"⚠️ Error en predicción de balance: {e}")
            return self._fallback_balance_prediction(transactions, months_ahead)
    
    def analyze_financial_health(self, transactions: List[Dict]) -> Dict:
        """
        Analiza salud financiera usando features profesionales
        """
        try:
            # Preparar datos
            user_data = {'transactions': transactions}
            features = self.feature_engineer.extract_all_features(user_data)
            
            # Calcular score de salud (0-100)
            health_score = 100
            factors = []
            recommendations = []
            
            # Factor 1: Ratio de gastos vs ingresos
            expense_ratio = features.get('expense_to_income_ratio', 0)
            if expense_ratio > 0.9:
                health_score -= 30
                factors.append("Gastos muy altos respecto a ingresos")
                recommendations.append("Reduce gastos o busca ingresos adicionales")
            elif expense_ratio > 0.7:
                health_score -= 15
                factors.append("Gastos elevados")
                recommendations.append("Intenta reducir gastos al 70% de ingresos")
            
            # Factor 2: Tasa de ahorro
            savings_rate = features.get('savings_rate', 0)
            if savings_rate < 0:
                health_score -= 25
                factors.append("No estás ahorrando")
                recommendations.append("Establece un presupuesto para ahorrar al menos 10%")
            elif savings_rate < 0.1:
                health_score -= 10
                factors.append("Ahorro bajo")
            
            # Factor 3: Volatilidad de gastos
            expense_volatility = features.get('expense_volatility', 0)
            if expense_volatility > 0.3:
                health_score -= 15
                factors.append("Alta volatilidad en gastos")
                recommendations.append("Establece un presupuesto mensual fijo")
            
            # Factor 4: Diversidad de categorías
            category_diversity = features.get('category_diversity', 0)
            if category_diversity < 0.3:
                health_score -= 10
                factors.append("Gastos concentrados en pocas categorías")
            
            # Factor 5: Consistencia
            spending_consistency = features.get('spending_consistency', 0)
            if spending_consistency < 0.5:
                health_score -= 10
                factors.append("Gastos inconsistentes")
            
            # Determinar nivel
            if health_score >= 80:
                health_level = "excellent"
                if not recommendations:
                    recommendations.append("¡Excelente salud financiera! Mantén tus buenos hábitos")
            elif health_score >= 60:
                health_level = "good"
                if not recommendations:
                    recommendations.append("Buena salud financiera, pero hay espacio para mejorar")
            elif health_score >= 40:
                health_level = "fair"
                if not recommendations:
                    recommendations.append("Salud financiera regular, considera hacer ajustes")
            else:
                health_level = "poor"
                if not recommendations:
                    recommendations.append("⚠️ Atención: Revisa urgentemente tus finanzas")
            
            return {
                'health_score': max(0, min(100, int(health_score))),
                'health_level': health_level,
                'factors': factors,
                'recommendations': recommendations,
                'key_metrics': {
                    'expense_ratio': float(expense_ratio),
                    'savings_rate': float(savings_rate),
                    'expense_volatility': float(expense_volatility),
                    'category_diversity': float(category_diversity)
                }
            }
            
        except Exception as e:
            print(f"⚠️ Error en análisis de salud: {e}")
            return {
                'health_score': 50,
                'health_level': 'unknown',
                'factors': [],
                'recommendations': ['Registra más transacciones para análisis completo']
            }
    
    def _calculate_confidence(self, num_transactions: int) -> float:
        """Calcula confianza basada en cantidad de datos"""
        if num_transactions >= 100:
            return 0.95
        elif num_transactions >= 50:
            return 0.85
        elif num_transactions >= 20:
            return 0.70
        else:
            return 0.50
    
    def _generate_smart_recommendations(self, predicted: float, current: float, 
                                       features: Dict, df: pd.DataFrame) -> List[str]:
        """Genera recomendaciones inteligentes basadas en features"""
        recommendations = []
        
        # Recomendación 1: Cambio en gastos
        change = predicted - current
        if abs(change) > current * 0.1:
            if change > 0:
                recommendations.append(
                    f"⚠️ Tus gastos podrían aumentar ${abs(change):,.0f} COP. "
                    "Revisa tus hábitos de consumo."
                )
            else:
                recommendations.append(
                    f"✅ Tus gastos podrían reducirse ${abs(change):,.0f} COP. "
                    "¡Sigue así!"
                )
        
        # Recomendación 2: Impulsividad
        impulse_score = features.get('impulse_buying_score', 0)
        if impulse_score > 0.3:
            recommendations.append(
                "Detectamos compras impulsivas frecuentes. "
                "Espera 24 horas antes de compras no planificadas."
            )
        
        # Recomendación 3: Fin de semana
        weekend_ratio = features.get('weekend_vs_weekday_ratio', 0)
        if weekend_ratio > 1.5:
            recommendations.append(
                "Gastas mucho más los fines de semana. "
                "Planifica actividades económicas para reducir gastos."
            )
        
        # Recomendación 4: Categoría principal
        top_concentration = features.get('top_category_concentration', 0)
        if top_concentration > 0.5:
            expenses = df[df['type'] == 'expense']
            if not expenses.empty and 'category' in expenses.columns:
                top_cat = expenses.groupby('category')['amount'].sum().idxmax()
                recommendations.append(
                    f"El 50%+ de tus gastos es en {top_cat}. "
                    "Busca alternativas más económicas en esta categoría."
                )
        
        # Recomendación 5: Ahorro
        savings_rate = features.get('savings_rate', 0)
        if savings_rate < 0.1:
            recommendations.append(
                "Intenta ahorrar al menos 10% de tus ingresos. "
                "Automatiza transferencias a una cuenta de ahorros."
            )
        
        return recommendations[:5]
    
    def _fallback_prediction(self, transactions: List[Dict]) -> Dict:
        """Predicción simple si el modelo no está disponible"""
        df = pd.DataFrame(transactions)
        if df.empty:
            return {
                'predicted_monthly_expenses': 0,
                'confidence': 0,
                'recommendations': ['Registra transacciones para obtener predicciones'],
                'model_used': 'fallback'
            }
        
        expenses = df[df['type'] == 'expense']
        avg = expenses['amount'].mean() if len(expenses) > 0 else 0
        
        return {
            'predicted_monthly_expenses': float(avg),
            'confidence': 0.5,
            'recommendations': ['Modelo profesional no disponible. Usando predicción simple.'],
            'model_used': 'fallback'
        }
    
    def _fallback_balance_prediction(self, transactions: List[Dict], months_ahead: int) -> Dict:
        """Predicción simple de balance"""
        return {
            'predictions': [],
            'current_balance': 0,
            'trend': 'unknown',
            'risk_level': 'unknown',
            'confidence': 0,
            'recommendations': ['Modelo profesional no disponible'],
            'model_used': 'fallback'
        }
