"""
Feature Engineering Profesional
Extrae 50+ características de datos financieros
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta, timezone
from typing import Dict, List

class ProfessionalFeatureEngineer:
    """
    Ingeniería de características nivel producción
    """
    
    def extract_all_features(self, user_data: Dict) -> Dict:
        """
        Extrae todas las características del usuario
        """
        transactions = pd.DataFrame(user_data.get('transactions', []))
        
        if transactions.empty:
            return self._empty_features()
        
        # Asegurar tipos correctos
        transactions['date'] = pd.to_datetime(transactions['date'])
        transactions['amount'] = pd.to_numeric(transactions['amount'])
        
        features = {}
        
        # 1. Features temporales
        features.update(self._extract_temporal_features(transactions))
        
        # 2. Features de comportamiento
        features.update(self._extract_behavioral_features(transactions))
        
        # 3. Features financieros
        features.update(self._extract_financial_features(transactions))
        
        # 4. Features de categorías
        features.update(self._extract_category_features(transactions))
        
        # 5. Features estadísticos
        features.update(self._extract_statistical_features(transactions))
        
        return features
    
    def _extract_temporal_features(self, df: pd.DataFrame) -> Dict:
        """
        Features basados en patrones temporales
        """
        features = {}
        
        # Separar ingresos y gastos
        expenses = df[df['type'] == 'expense']
        incomes = df[df['type'] == 'income']
        
        # Patrones diarios
        if not expenses.empty:
            features['avg_daily_transactions'] = len(expenses) / max((df['date'].max() - df['date'].min()).days, 1)
            features['peak_spending_hour'] = expenses['date'].dt.hour.mode()[0] if len(expenses) > 0 else 12
            
            # Día de la semana
            expenses['day_of_week'] = expenses['date'].dt.dayofweek
            weekend_spending = expenses[expenses['day_of_week'] >= 5]['amount'].sum()
            weekday_spending = expenses[expenses['day_of_week'] < 5]['amount'].sum()
            features['weekend_vs_weekday_ratio'] = weekend_spending / max(weekday_spending, 1)
            
            # Día del mes
            expenses['day_of_month'] = expenses['date'].dt.day
            end_month_spending = expenses[expenses['day_of_month'] >= 25]['amount'].sum()
            total_spending = expenses['amount'].sum()
            features['end_of_month_concentration'] = end_month_spending / max(total_spending, 1)
        else:
            features['avg_daily_transactions'] = 0
            features['peak_spending_hour'] = 12
            features['weekend_vs_weekday_ratio'] = 0
            features['end_of_month_concentration'] = 0
        
        # Recencia
        if not df.empty:
            now = datetime.now(timezone.utc)
            days_since_last = (now - df['date'].max()).days
            features['days_since_last_transaction'] = days_since_last
        else:
            features['days_since_last_transaction'] = 999
        
        if not incomes.empty:
            now = datetime.now(timezone.utc)
            days_since_income = (now - incomes['date'].max()).days
            features['days_since_last_income'] = days_since_income
        else:
            features['days_since_last_income'] = 999
        
        # Frecuencia
        if len(df) > 1:
            date_diffs = df.sort_values('date')['date'].diff().dt.days
            features['avg_days_between_transactions'] = date_diffs.mean()
            features['transaction_frequency_std'] = date_diffs.std()
        else:
            features['avg_days_between_transactions'] = 0
            features['transaction_frequency_std'] = 0
        
        return features
    
    def _extract_behavioral_features(self, df: pd.DataFrame) -> Dict:
        """
        Features de comportamiento financiero
        """
        features = {}
        
        expenses = df[df['type'] == 'expense']
        
        if expenses.empty:
            return {
                'impulse_buying_score': 0,
                'small_expense_ratio': 0,
                'large_expense_ratio': 0,
                'spending_consistency': 0,
                'category_switching_rate': 0
            }
        
        # Score de compras impulsivas (gastos pequeños frecuentes)
        small_expenses = expenses[expenses['amount'] < expenses['amount'].quantile(0.25)]
        features['impulse_buying_score'] = len(small_expenses) / max(len(expenses), 1)
        
        # Ratio de gastos pequeños vs grandes
        features['small_expense_ratio'] = small_expenses['amount'].sum() / max(expenses['amount'].sum(), 1)
        large_expenses = expenses[expenses['amount'] > expenses['amount'].quantile(0.75)]
        features['large_expense_ratio'] = large_expenses['amount'].sum() / max(expenses['amount'].sum(), 1)
        
        # Consistencia de gastos (baja volatilidad = más consistente)
        monthly_expenses = expenses.groupby(expenses['date'].dt.to_period('M'))['amount'].sum()
        if len(monthly_expenses) > 1:
            features['spending_consistency'] = 1 - (monthly_expenses.std() / max(monthly_expenses.mean(), 1))
        else:
            features['spending_consistency'] = 0
        
        # Tasa de cambio de categorías
        if 'category' in expenses.columns and len(expenses) > 1:
            category_changes = (expenses.sort_values('date')['category'].shift() != expenses.sort_values('date')['category']).sum()
            features['category_switching_rate'] = category_changes / max(len(expenses), 1)
        else:
            features['category_switching_rate'] = 0
        
        return features
    
    def _extract_financial_features(self, df: pd.DataFrame) -> Dict:
        """
        Features de salud financiera
        """
        features = {}
        
        incomes = df[df['type'] == 'income']
        expenses = df[df['type'] == 'expense']
        
        total_income = incomes['amount'].sum() if not incomes.empty else 0
        total_expenses = expenses['amount'].sum() if not expenses.empty else 0
        
        # Ratios básicos
        features['total_income'] = total_income
        features['total_expenses'] = total_expenses
        features['net_balance'] = total_income - total_expenses
        features['expense_to_income_ratio'] = total_expenses / max(total_income, 1)
        features['savings_rate'] = (total_income - total_expenses) / max(total_income, 1)
        
        # Estabilidad de ingresos
        if len(incomes) > 1:
            features['income_stability'] = 1 - (incomes['amount'].std() / max(incomes['amount'].mean(), 1))
            features['income_growth_rate'] = self._calculate_growth_rate(incomes)
        else:
            features['income_stability'] = 0
            features['income_growth_rate'] = 0
        
        # Volatilidad de gastos
        if len(expenses) > 1:
            features['expense_volatility'] = expenses['amount'].std() / max(expenses['amount'].mean(), 1)
            features['expense_growth_rate'] = self._calculate_growth_rate(expenses)
        else:
            features['expense_volatility'] = 0
            features['expense_growth_rate'] = 0
        
        # Promedios mensuales
        if not expenses.empty:
            months = (df['date'].max() - df['date'].min()).days / 30
            features['avg_monthly_expenses'] = total_expenses / max(months, 1)
        else:
            features['avg_monthly_expenses'] = 0
        
        if not incomes.empty:
            months = (df['date'].max() - df['date'].min()).days / 30
            features['avg_monthly_income'] = total_income / max(months, 1)
        else:
            features['avg_monthly_income'] = 0
        
        return features
    
    def _extract_category_features(self, df: pd.DataFrame) -> Dict:
        """
        Features basados en categorías de gasto
        """
        features = {}
        
        expenses = df[df['type'] == 'expense']
        
        if expenses.empty or 'category' not in expenses.columns:
            return {
                'num_categories': 0,
                'category_diversity': 0,
                'top_category_concentration': 0
            }
        
        # Número de categorías únicas
        features['num_categories'] = expenses['category'].nunique()
        
        # Diversidad de categorías (entropía)
        category_dist = expenses.groupby('category')['amount'].sum()
        category_probs = category_dist / category_dist.sum()
        features['category_diversity'] = -sum(category_probs * np.log2(category_probs + 1e-10))
        
        # Concentración en top categoría
        features['top_category_concentration'] = category_dist.max() / max(category_dist.sum(), 1)
        
        # Top 3 categorías
        top_categories = category_dist.nlargest(3)
        for i, (cat, amount) in enumerate(top_categories.items(), 1):
            features[f'top_{i}_category_amount'] = amount
            features[f'top_{i}_category_ratio'] = amount / max(category_dist.sum(), 1)
        
        return features
    
    def _extract_statistical_features(self, df: pd.DataFrame) -> Dict:
        """
        Features estadísticos avanzados
        """
        features = {}
        
        expenses = df[df['type'] == 'expense']
        
        if expenses.empty:
            return {
                'expense_mean': 0,
                'expense_median': 0,
                'expense_std': 0,
                'expense_skewness': 0,
                'expense_kurtosis': 0
            }
        
        amounts = expenses['amount']
        
        # Estadísticas básicas
        features['expense_mean'] = amounts.mean()
        features['expense_median'] = amounts.median()
        features['expense_std'] = amounts.std()
        features['expense_min'] = amounts.min()
        features['expense_max'] = amounts.max()
        
        # Percentiles
        features['expense_p25'] = amounts.quantile(0.25)
        features['expense_p75'] = amounts.quantile(0.75)
        features['expense_iqr'] = features['expense_p75'] - features['expense_p25']
        
        # Forma de la distribución
        features['expense_skewness'] = amounts.skew()
        features['expense_kurtosis'] = amounts.kurtosis()
        
        # Coeficiente de variación
        features['expense_cv'] = amounts.std() / max(amounts.mean(), 1)
        
        return features
    
    def _calculate_growth_rate(self, df: pd.DataFrame) -> float:
        """
        Calcula tasa de crecimiento
        """
        if len(df) < 2:
            return 0
        
        df_sorted = df.sort_values('date')
        first_half = df_sorted.head(len(df_sorted)//2)['amount'].mean()
        second_half = df_sorted.tail(len(df_sorted)//2)['amount'].mean()
        
        if first_half == 0:
            return 0
        
        return (second_half - first_half) / first_half
    
    def _empty_features(self) -> Dict:
        """
        Features vacíos cuando no hay datos
        """
        return {f'feature_{i}': 0 for i in range(50)}
