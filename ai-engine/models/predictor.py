import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import List, Dict
from sklearn.linear_model import LinearRegression
from collections import defaultdict

class FinancialPredictor:
    def __init__(self):
        self.model = LinearRegression()
    
    def predict_future_balance(self, transactions: List[Dict], months_ahead: int = 3) -> Dict:
        """Predice el balance futuro basado en transacciones históricas"""
        if not transactions:
            return self._empty_prediction()
        
        # Convertir a DataFrame
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date')
        
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
        
        # Preparar datos para modelo
        X = np.arange(len(monthly_data)).reshape(-1, 1)
        y = monthly_data['cumulative_balance'].values
        
        # Entrenar modelo
        self.model.fit(X, y)
        
        # Predecir meses futuros
        future_X = np.arange(len(monthly_data), len(monthly_data) + months_ahead).reshape(-1, 1)
        predictions = self.model.predict(future_X)
        
        # Calcular tendencia
        trend = "increasing" if predictions[-1] > y[-1] else "decreasing"
        
        # Calcular nivel de riesgo
        risk_level = self._calculate_risk_level(predictions, y)
        
        # Generar recomendaciones
        recommendations = self._generate_recommendations(predictions, y, df)
        
        # Calcular confianza
        confidence = self._calculate_confidence(monthly_data)
        
        # Formatear predicciones
        last_date = df['date'].max()
        prediction_list = []
        for i, pred in enumerate(predictions):
            future_date = last_date + timedelta(days=30 * (i + 1))
            prediction_list.append({
                'month': future_date.strftime('%Y-%m'),
                'predicted_balance': float(pred),
                'confidence': confidence
            })
        
        return {
            'predictions': prediction_list,
            'confidence': confidence,
            'trend': trend,
            'risk_level': risk_level,
            'recommendations': recommendations,
            'current_balance': float(y[-1])
        }
    
    def predict_category_expenses(self, transactions: List[Dict], months_ahead: int = 3) -> Dict:
        """Predice gastos futuros por categoría"""
        if not transactions:
            return {}
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        # Agrupar por categoría y mes
        category_monthly = df.groupby(['category', 'month'])['amount'].sum().reset_index()
        
        predictions = {}
        for category in df['category'].unique():
            if pd.isna(category):
                continue
                
            cat_data = category_monthly[category_monthly['category'] == category]
            
            if len(cat_data) < 2:
                avg = cat_data['amount'].mean()
                predictions[category] = {
                    'average': float(avg),
                    'predicted_next_month': float(avg),
                    'trend': 'stable'
                }
            else:
                avg = cat_data['amount'].mean()
                recent_avg = cat_data.tail(3)['amount'].mean()
                trend = "increasing" if recent_avg > avg else "decreasing" if recent_avg < avg else "stable"
                
                predictions[category] = {
                    'average': float(avg),
                    'predicted_next_month': float(recent_avg),
                    'trend': trend
                }
        
        return predictions
    
    def analyze_financial_risk(self, transactions: List[Dict]) -> Dict:
        """Analiza el riesgo financiero del usuario"""
        if not transactions:
            return {
                'risk_score': 0,
                'risk_level': 'unknown',
                'factors': [],
                'recommendations': []
            }
        
        df = pd.DataFrame(transactions)
        df['date'] = pd.to_datetime(df['date'])
        
        # Calcular métricas
        total_income = df[df['type'] == 'income']['amount'].sum()
        total_expenses = df[df['type'] == 'expense']['amount'].sum()
        
        if total_income == 0:
            expense_ratio = 1.0
        else:
            expense_ratio = total_expenses / total_income
        
        # Calcular volatilidad
        df['month'] = df['date'].dt.to_period('M')
        monthly_expenses = df[df['type'] == 'expense'].groupby('month')['amount'].sum()
        volatility = monthly_expenses.std() / monthly_expenses.mean() if len(monthly_expenses) > 1 else 0
        
        # Calcular score de riesgo (0-100)
        risk_score = 0
        factors = []
        
        if expense_ratio > 0.9:
            risk_score += 40
            factors.append("Gastos muy cercanos a ingresos")
        elif expense_ratio > 0.7:
            risk_score += 20
            factors.append("Gastos elevados respecto a ingresos")
        
        if volatility > 0.3:
            risk_score += 30
            factors.append("Alta volatilidad en gastos mensuales")
        elif volatility > 0.15:
            risk_score += 15
            factors.append("Volatilidad moderada en gastos")
        
        balance = total_income - total_expenses
        if balance < 0:
            risk_score += 30
            factors.append("Balance negativo")
        
        # Determinar nivel de riesgo
        if risk_score >= 70:
            risk_level = "high"
        elif risk_score >= 40:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        # Generar recomendaciones
        recommendations = []
        if expense_ratio > 0.8:
            recommendations.append("Reduce gastos o aumenta ingresos para mejorar tu situación financiera")
        if volatility > 0.2:
            recommendations.append("Establece un presupuesto mensual para estabilizar tus gastos")
        if balance < 0:
            recommendations.append("Urgente: Revisa tus gastos y elimina los no esenciales")
        
        if not recommendations:
            recommendations.append("Mantén tus buenos hábitos financieros")
        
        return {
            'risk_score': int(risk_score),
            'risk_level': risk_level,
            'factors': factors,
            'recommendations': recommendations,
            'metrics': {
                'expense_ratio': float(expense_ratio),
                'volatility': float(volatility),
                'balance': float(balance)
            }
        }
    
    def _empty_prediction(self) -> Dict:
        return {
            'predictions': [],
            'confidence': 0,
            'trend': 'unknown',
            'risk_level': 'unknown',
            'recommendations': ['Registra más transacciones para obtener predicciones'],
            'current_balance': 0
        }
    
    def _simple_prediction(self, df: pd.DataFrame, months_ahead: int) -> Dict:
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
                'confidence': 0.5
            })
        
        # Determinar tendencia
        trend = "increasing" if avg_monthly_change > 0 else "decreasing" if avg_monthly_change < 0 else "stable"
        
        # Calcular nivel de riesgo
        final_prediction = predictions[-1]['predicted_balance'] if predictions else current_balance
        if final_prediction < 0:
            risk_level = "high"
        elif final_prediction < current_balance * 0.5:
            risk_level = "medium"
        else:
            risk_level = "low"
        
        return {
            'predictions': predictions,
            'confidence': 0.5,
            'trend': trend,
            'risk_level': risk_level,
            'recommendations': ['Registra más transacciones para predicciones más precisas'],
            'current_balance': float(current_balance)
        }
    
    def _calculate_risk_level(self, predictions: np.ndarray, historical: np.ndarray) -> str:
        final_prediction = predictions[-1]
        current_balance = historical[-1]
        
        if final_prediction < 0:
            return "high"
        elif final_prediction < current_balance * 0.5:
            return "medium"
        else:
            return "low"
    
    def _generate_recommendations(self, predictions: np.ndarray, historical: np.ndarray, df: pd.DataFrame) -> List[str]:
        recommendations = []
        
        final_prediction = predictions[-1]
        current_balance = historical[-1]
        balance_change = final_prediction - current_balance
        
        # Calcular métricas adicionales
        incomes = df[df['type'] == 'income']['amount']
        expenses = df[df['type'] == 'expense']['amount']
        
        avg_income = incomes.mean() if len(incomes) > 0 else 0
        avg_expense = expenses.mean() if len(expenses) > 0 else 0
        
        # Recomendación 1: Tendencia del balance
        if balance_change < 0:
            recommendations.append(
                f"Tu balance podría disminuir ${abs(balance_change):,.0f} COP. "
                "Considera reducir gastos no esenciales o buscar ingresos adicionales."
            )
        elif balance_change > 0:
            recommendations.append(
                f"¡Excelente! Tu balance podría aumentar ${balance_change:,.0f} COP. "
                "Mantén tus buenos hábitos financieros."
            )
        
        # Recomendación 2: Balance negativo
        if final_prediction < 0:
            recommendations.append(
                "⚠️ ALERTA: Se predice balance negativo. "
                "Revisa urgentemente tus gastos y prioriza solo lo esencial."
            )
        
        # Recomendación 3: Ratio de gastos
        if avg_income > 0:
            expense_ratio = avg_expense / avg_income
            if expense_ratio > 0.8:
                recommendations.append(
                    f"Tus gastos representan el {expense_ratio*100:.0f}% de tus ingresos. "
                    "Intenta reducirlos al 70% o menos para mayor estabilidad."
                )
        
        # Recomendación 4: Categorías de mayor gasto
        expenses_df = df[df['type'] == 'expense']
        if not expenses_df.empty and 'category' in expenses_df.columns:
            category_totals = expenses_df.groupby('category')['amount'].sum().sort_values(ascending=False)
            if len(category_totals) > 0:
                top_category = category_totals.index[0]
                top_amount = category_totals.iloc[0]
                percentage = (top_amount / category_totals.sum()) * 100
                recommendations.append(
                    f"Tu mayor gasto es en {top_category} (${top_amount:,.0f} COP, {percentage:.0f}% del total). "
                    "Busca formas de optimizar en esta categoría."
                )
        
        # Recomendación 5: Ahorro
        if final_prediction > 0 and balance_change > 0:
            monthly_saving = balance_change / len(predictions)
            recommendations.append(
                f"Podrías ahorrar aproximadamente ${monthly_saving:,.0f} COP por mes. "
                "Considera crear un fondo de emergencia de 3-6 meses de gastos."
            )
        
        # Si no hay suficientes datos
        if len(df) < 10:
            recommendations.append(
                "📊 Registra más transacciones para obtener predicciones más precisas y personalizadas."
            )
        
        return recommendations[:5]  # Máximo 5 recomendaciones
    
    def _calculate_confidence(self, monthly_data: pd.DataFrame) -> float:
        """Calcula confianza basada en cantidad de datos"""
        data_points = len(monthly_data)
        
        if data_points >= 6:
            return 0.9
        elif data_points >= 3:
            return 0.7
        else:
            return 0.5
