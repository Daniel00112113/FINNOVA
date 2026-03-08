"""
Advanced Predictor - Predictor financiero avanzado con ML mejorado
Usa técnicas más sofisticadas para predicciones más precisas
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class AdvancedFinancialPredictor:
    """
    Predictor financiero con ML avanzado y conocimiento experto
    """
    
    def __init__(self):
        # Usar Gradient Boosting en lugar de regresión lineal simple
        self.balance_model = GradientBoostingRegressor(
            n_estimators=100,
            learning_rate=0.1,
            max_depth=5,
            random_state=42
        )
        
        self.expense_model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42
        )
        
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def predict_future_balance_advanced(
        self, 
        transactions: List[Dict], 
        months_ahead: int = 3
    ) -> Dict:
        """
        Predicción avanzada de balance futuro
        """
        if not transactions:
            return self._empty_prediction()
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
        # Extraer features avanzados
        features = self._extract_advanced_features(df)
        
        # Calcular balance acumulado
        df['balance_change'] = df.apply(
            lambda x: x['amount'] if x['type'] == 'income' else -x['amount'],
            axis=1
        )
        df['cumulative_balance'] = df['balance_change'].cumsum()
        
        # Agrupar por mes
        df['month'] = df['date'].dt.to_period('M')
        monthly_data = df.groupby('month').agg({
            'balance_change': 'sum',
            'cumulative_balance': 'last'
        }).reset_index()
        
        if len(monthly_data) < 2:
            return self._simple_prediction(df, months_ahead)
        
        # Preparar datos para modelo avanzado
        X = self._prepare_features_for_model(monthly_data, features)
        y = monthly_data['cumulative_balance'].values
        
        # Entrenar modelo
        try:
            if len(X) >= 3:  # Necesitamos al menos 3 puntos
                self.balance_model.fit(X, y)
                self.is_trained = True
        except:
            return self._simple_prediction(df, months_ahead)
        
        # Predecir meses futuros
        future_features = self._prepare_future_features(
            monthly_data, features, months_ahead
        )
        predictions = self.balance_model.predict(future_features)
        
        # Calcular tendencia y confianza
        trend = self._calculate_trend(predictions, y)
        confidence = self._calculate_confidence_advanced(monthly_data, features)
        risk_level = self._calculate_risk_level_advanced(predictions, y, features)
        
        # Generar recomendaciones avanzadas
        recommendations = self._generate_advanced_recommendations(
            predictions, y, df, features
        )
        
        # Formatear predicciones
        last_date = df['date'].max()
        prediction_list = []
        for i, pred in enumerate(predictions):
            future_date = last_date + timedelta(days=30 * (i + 1))
            prediction_list.append({
                'month': future_date.strftime('%Y-%m'),
                'predicted_balance': float(pred),
                'confidence': confidence,
                'lower_bound': float(pred * 0.9),  # Intervalo de confianza
                'upper_bound': float(pred * 1.1)
            })
        
        return {
            'predictions': prediction_list,
            'confidence': confidence,
            'trend': trend,
            'risk_level': risk_level,
            'recommendations': recommendations,
            'current_balance': float(y[-1]),
            'features': {
                'income_stability': features.get('income_stability', 0),
                'expense_volatility': features.get('expense_volatility', 0),
                'savings_rate': features.get('savings_rate', 0)
            }
        }

    
    def _extract_advanced_features(self, df: pd.DataFrame) -> Dict:
        """
        Extrae características avanzadas de las transacciones
        """
        features = {}
        
        # 1. Estabilidad de ingresos
        incomes = df[df['type'] == 'income']['amount']
        if len(incomes) > 1:
            features['income_stability'] = 1 - (incomes.std() / incomes.mean())
        else:
            features['income_stability'] = 0
        
        # 2. Volatilidad de gastos
        expenses = df[df['type'] == 'expense']['amount']
        if len(expenses) > 1:
            features['expense_volatility'] = expenses.std() / expenses.mean()
        else:
            features['expense_volatility'] = 0
        
        # 3. Tasa de ahorro
        total_income = incomes.sum()
        total_expenses = expenses.sum()
        if total_income > 0:
            features['savings_rate'] = (total_income - total_expenses) / total_income
        else:
            features['savings_rate'] = 0
        
        # 4. Tendencia de gastos (creciente/decreciente)
        if len(expenses) >= 3:
            recent_expenses = expenses.tail(len(expenses)//2).mean()
            old_expenses = expenses.head(len(expenses)//2).mean()
            features['expense_trend'] = (recent_expenses - old_expenses) / old_expenses if old_expenses > 0 else 0
        else:
            features['expense_trend'] = 0
        
        # 5. Frecuencia de transacciones
        days_span = (df['date'].max() - df['date'].min()).days
        if days_span > 0:
            features['transaction_frequency'] = len(df) / days_span
        else:
            features['transaction_frequency'] = 0
        
        # 6. Ratio de gastos grandes vs pequeños
        large_expenses = expenses[expenses > expenses.median()]
        if len(expenses) > 0:
            features['large_expense_ratio'] = len(large_expenses) / len(expenses)
        else:
            features['large_expense_ratio'] = 0
        
        return features
    
    def _prepare_features_for_model(
        self, 
        monthly_data: pd.DataFrame, 
        features: Dict
    ) -> np.ndarray:
        """
        Prepara features para el modelo ML
        """
        X = []
        for i in range(len(monthly_data)):
            month_features = [
                i,  # Índice temporal
                features.get('income_stability', 0),
                features.get('expense_volatility', 0),
                features.get('savings_rate', 0),
                features.get('expense_trend', 0),
                features.get('transaction_frequency', 0),
                features.get('large_expense_ratio', 0)
            ]
            X.append(month_features)
        
        return np.array(X)
    
    def _prepare_future_features(
        self, 
        monthly_data: pd.DataFrame, 
        features: Dict, 
        months_ahead: int
    ) -> np.ndarray:
        """
        Prepara features para predicciones futuras
        """
        last_index = len(monthly_data)
        future_X = []
        
        for i in range(months_ahead):
            future_features = [
                last_index + i,
                features.get('income_stability', 0),
                features.get('expense_volatility', 0),
                features.get('savings_rate', 0),
                features.get('expense_trend', 0),
                features.get('transaction_frequency', 0),
                features.get('large_expense_ratio', 0)
            ]
            future_X.append(future_features)
        
        return np.array(future_X)
    
    def _calculate_trend(self, predictions: np.ndarray, historical: np.ndarray) -> str:
        """
        Calcula tendencia con más precisión
        """
        if len(predictions) == 0:
            return "stable"
        
        final_pred = predictions[-1]
        current = historical[-1]
        change_pct = (final_pred - current) / current if current != 0 else 0
        
        if change_pct > 0.10:
            return "strongly_increasing"
        elif change_pct > 0.02:
            return "increasing"
        elif change_pct < -0.10:
            return "strongly_decreasing"
        elif change_pct < -0.02:
            return "decreasing"
        else:
            return "stable"
    
    def _calculate_confidence_advanced(
        self, 
        monthly_data: pd.DataFrame, 
        features: Dict
    ) -> float:
        """
        Calcula confianza basada en múltiples factores
        """
        confidence = 0.5  # Base
        
        # Factor 1: Cantidad de datos
        data_points = len(monthly_data)
        if data_points >= 12:
            confidence += 0.3
        elif data_points >= 6:
            confidence += 0.2
        elif data_points >= 3:
            confidence += 0.1
        
        # Factor 2: Estabilidad de ingresos
        income_stability = features.get('income_stability', 0)
        confidence += income_stability * 0.1
        
        # Factor 3: Baja volatilidad de gastos
        expense_volatility = features.get('expense_volatility', 0)
        if expense_volatility < 0.3:
            confidence += 0.1
        
        return min(confidence, 0.95)  # Máximo 95%
    
    def _calculate_risk_level_advanced(
        self, 
        predictions: np.ndarray, 
        historical: np.ndarray, 
        features: Dict
    ) -> str:
        """
        Calcula nivel de riesgo con análisis avanzado
        """
        risk_score = 0
        
        # Factor 1: Balance futuro
        final_prediction = predictions[-1]
        if final_prediction < 0:
            risk_score += 40
        elif final_prediction < historical[-1] * 0.5:
            risk_score += 20
        
        # Factor 2: Tendencia negativa
        trend_slope = (predictions[-1] - predictions[0]) / len(predictions)
        if trend_slope < 0:
            risk_score += 20
        
        # Factor 3: Baja tasa de ahorro
        savings_rate = features.get('savings_rate', 0)
        if savings_rate < 0.10:
            risk_score += 20
        elif savings_rate < 0.20:
            risk_score += 10
        
        # Factor 4: Alta volatilidad
        expense_volatility = features.get('expense_volatility', 0)
        if expense_volatility > 0.5:
            risk_score += 20
        elif expense_volatility > 0.3:
            risk_score += 10
        
        # Determinar nivel
        if risk_score >= 60:
            return "high"
        elif risk_score >= 30:
            return "medium"
        else:
            return "low"
    
    def _generate_advanced_recommendations(
        self, 
        predictions: np.ndarray, 
        historical: np.ndarray, 
        df: pd.DataFrame, 
        features: Dict
    ) -> List[str]:
        """
        Genera recomendaciones más inteligentes y accionables
        """
        recommendations = []
        
        final_pred = predictions[-1]
        current = historical[-1]
        change = final_pred - current
        
        # 1. Análisis de tendencia
        if change < 0:
            monthly_loss = abs(change) / len(predictions)
            recommendations.append(
                f"⚠️ Tu balance podría disminuir ${abs(change):,.0f} COP en {len(predictions)} meses "
                f"(${monthly_loss:,.0f} COP/mes). Actúa ahora para revertir esta tendencia."
            )
        else:
            recommendations.append(
                f"✅ Tu balance podría aumentar ${change:,.0f} COP. "
                f"Mantén tus buenos hábitos y considera invertir el excedente."
            )
        
        # 2. Análisis de tasa de ahorro
        savings_rate = features.get('savings_rate', 0)
        if savings_rate < 0.10:
            target_savings = 0.20
            income = df[df['type'] == 'income']['amount'].sum()
            needed_reduction = income * (target_savings - savings_rate)
            recommendations.append(
                f"💰 Tu tasa de ahorro es solo {savings_rate*100:.0f}% (objetivo: 20%). "
                f"Reduce gastos en ${needed_reduction:,.0f} COP/mes para alcanzar la meta."
            )
        
        # 3. Análisis de volatilidad
        expense_volatility = features.get('expense_volatility', 0)
        if expense_volatility > 0.3:
            recommendations.append(
                f"📊 Tus gastos varían mucho mes a mes (volatilidad: {expense_volatility:.1%}). "
                f"Establece un presupuesto mensual fijo para mayor estabilidad."
            )
        
        # 4. Análisis de categorías (top gastador)
        expenses_df = df[df['type'] == 'expense']
        if not expenses_df.empty and 'category' in expenses_df.columns:
            category_totals = expenses_df.groupby('category')['amount'].sum().sort_values(ascending=False)
            if len(category_totals) > 0:
                top_category = category_totals.index[0]
                top_amount = category_totals.iloc[0]
                percentage = (top_amount / category_totals.sum()) * 100
                
                if percentage > 30:
                    reduction = top_amount * 0.20
                    recommendations.append(
                        f"🎯 {top_category} representa {percentage:.0f}% de tus gastos (${top_amount:,.0f} COP). "
                        f"Reducir 20% ahorraría ${reduction:,.0f} COP/mes."
                    )
        
        # 5. Predicción de crisis
        if final_pred < 0:
            months_to_crisis = self._estimate_months_to_crisis(predictions)
            recommendations.append(
                f"🚨 ALERTA: Podrías tener balance negativo en {months_to_crisis} meses. "
                f"Toma acción inmediata: reduce gastos 30% o aumenta ingresos."
            )
        
        return recommendations[:5]
    
    def _estimate_months_to_crisis(self, predictions: np.ndarray) -> int:
        """
        Estima en cuántos meses el balance será negativo
        """
        for i, pred in enumerate(predictions):
            if pred < 0:
                return i + 1
        return len(predictions)
    
    def _simple_prediction(self, df: pd.DataFrame, months_ahead: int) -> Dict:
        """
        Predicción simple cuando no hay suficientes datos
        """
        current_balance = df['cumulative_balance'].iloc[-1] if len(df) > 0 else 0
        avg_monthly_change = df['balance_change'].mean() if len(df) > 0 else 0
        
        predictions = []
        last_date = df['date'].max() if len(df) > 0 else pd.Timestamp.now()
        
        for i in range(months_ahead):
            future_balance = current_balance + (avg_monthly_change * (i + 1))
            future_date = last_date + timedelta(days=30 * (i + 1))
            predictions.append({
                'month': future_date.strftime('%Y-%m'),
                'predicted_balance': float(future_balance),
                'confidence': 0.5,
                'lower_bound': float(future_balance * 0.8),
                'upper_bound': float(future_balance * 1.2)
            })
        
        trend = "increasing" if avg_monthly_change > 0 else "decreasing" if avg_monthly_change < 0 else "stable"
        
        return {
            'predictions': predictions,
            'confidence': 0.5,
            'trend': trend,
            'risk_level': 'medium',
            'recommendations': ['Registra más transacciones para predicciones más precisas'],
            'current_balance': float(current_balance),
            'features': {}
        }
    
    def _empty_prediction(self) -> Dict:
        return {
            'predictions': [],
            'confidence': 0,
            'trend': 'unknown',
            'risk_level': 'unknown',
            'recommendations': ['Registra transacciones para obtener predicciones'],
            'current_balance': 0,
            'features': {}
        }
