"""
Smart Recommender - Sistema de recomendaciones basado en ML
Aprende de usuarios reales para hacer recomendaciones personalizadas
"""
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
from datetime import datetime

class SmartRecommender:
    """
    Sistema de recomendaciones que aprende de datos reales de usuarios
    """
    
    def __init__(self):
        self.expense_predictor = GradientBoostingRegressor(n_estimators=100, random_state=42)
        self.savings_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.scaler = StandardScaler()
        self.is_trained = False
    
    def load_training_data(self, file_path='training_data.json'):
        """
        Carga datos de entrenamiento
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return data
    
    def prepare_features(self, user_data):
        """
        Prepara features para el modelo
        """
        patterns = user_data.get('patterns', {})
        aggregated = user_data.get('aggregated_data', {})
        
        features = {
            # Gastos
            'avg_monthly_expense': patterns.get('avg_monthly_expense', 0),
            'expense_volatility': patterns.get('expense_volatility', 0),
            'total_expenses': aggregated.get('total_expenses', 0),
            
            # Ingresos
            'total_incomes': aggregated.get('total_incomes', 0),
            
            # Deuda
            'total_debt': aggregated.get('total_debt', 0),
            'debt_to_income_ratio': aggregated.get('total_debt', 0) / max(aggregated.get('total_incomes', 1), 1),
            
            # Patrones temporales
            'weekend_spending': patterns.get('weekend_spending', 0),
            'weekday_spending': patterns.get('weekday_spending', 0),
            'weekend_ratio': patterns.get('weekend_spending', 0) / max(patterns.get('weekday_spending', 1), 1),
            
            # Gastos recurrentes
            'recurring_expenses': patterns.get('recurring_expenses', 0),
            
            # Actividad
            'num_transactions': aggregated.get('num_transactions', 0)
        }
        
        return list(features.values())
    
    def calculate_savings_potential(self, user_data):
        """
        Calcula el potencial de ahorro basado en patrones
        """
        patterns = user_data.get('patterns', {})
        small_expenses = patterns.get('small_expenses', {})
        
        # Sumar gastos pequeños que se pueden reducir
        total_small = sum(cat['sum'] for cat in small_expenses.values() if isinstance(cat, dict))
        
        # Potencial de ahorro: 30-50% de gastos pequeños
        savings_potential = total_small * 0.4
        
        return savings_potential
    
    def train(self, training_data_file='training_data.json'):
        """
        Entrena los modelos con datos reales
        """
        print("🤖 Iniciando entrenamiento de IA...")
        
        # Cargar datos
        data = self.load_training_data(training_data_file)
        print(f"📊 Datos cargados: {len(data)} usuarios")
        
        if len(data) < 10:
            print("⚠️ Necesitas al menos 10 usuarios para entrenar")
            return False
        
        # Preparar features y labels
        X = []
        y_expense = []
        y_savings = []
        
        for user in data:
            try:
                features = self.prepare_features(user)
                X.append(features)
                
                # Label 1: Predicción de gastos futuros
                y_expense.append(user['aggregated_data']['total_expenses'])
                
                # Label 2: Potencial de ahorro
                savings_potential = self.calculate_savings_potential(user)
                y_savings.append(1 if savings_potential > 100000 else 0)  # Alto potencial si > 100K
            
            except Exception as e:
                print(f"⚠️ Error procesando usuario: {e}")
                continue
        
        X = np.array(X)
        y_expense = np.array(y_expense)
        y_savings = np.array(y_savings)
        
        # Normalizar features
        X_scaled = self.scaler.fit_transform(X)
        
        # Split train/test
        X_train, X_test, y_exp_train, y_exp_test, y_sav_train, y_sav_test = train_test_split(
            X_scaled, y_expense, y_savings, test_size=0.2, random_state=42
        )
        
        # Entrenar predictor de gastos
        print("📈 Entrenando predictor de gastos...")
        self.expense_predictor.fit(X_train, y_exp_train)
        exp_score = self.expense_predictor.score(X_test, y_exp_test)
        print(f"  ✅ Accuracy: {exp_score:.2%}")
        
        # Entrenar clasificador de ahorro
        print("💰 Entrenando clasificador de ahorro...")
        self.savings_classifier.fit(X_train, y_sav_train)
        sav_score = self.savings_classifier.score(X_test, y_sav_test)
        print(f"  ✅ Accuracy: {sav_score:.2%}")
        
        self.is_trained = True
        
        # Guardar modelos
        self.save_models()
        
        print("🎉 Entrenamiento completado!")
        return True
    
    def predict_expenses(self, user_data):
        """
        Predice gastos futuros del usuario
        """
        if not self.is_trained:
            print("⚠️ Modelo no entrenado. Usando predicción básica...")
            return user_data['aggregated_data']['total_expenses']
        
        features = self.prepare_features(user_data)
        features_scaled = self.scaler.transform([features])
        
        prediction = self.expense_predictor.predict(features_scaled)[0]
        return prediction
    
    def recommend_savings_strategy(self, user_data):
        """
        Recomienda estrategia de ahorro personalizada
        """
        if not self.is_trained:
            return self._basic_recommendations(user_data)
        
        features = self.prepare_features(user_data)
        features_scaled = self.scaler.transform([features])
        
        # Clasificar potencial de ahorro
        has_high_potential = self.savings_classifier.predict(features_scaled)[0]
        
        # Generar recomendaciones basadas en patrones
        recommendations = []
        patterns = user_data.get('patterns', {})
        
        # Analizar gastos pequeños
        small_expenses = patterns.get('small_expenses', {})
        for category, data in small_expenses.items():
            if isinstance(data, dict) and data.get('sum', 0) > 50000:
                monthly_impact = data['sum']
                count = data['count']
                recommendations.append({
                    'type': 'reduce_small_expenses',
                    'category': category,
                    'current_monthly': monthly_impact,
                    'suggested_reduction': monthly_impact * 0.5,
                    'monthly_savings': monthly_impact * 0.5,
                    'yearly_savings': monthly_impact * 0.5 * 12,
                    'message': f"Reduce {category} de {count} a {count//2} veces/mes = ahorra ${monthly_impact * 0.5:,.0f}/mes"
                })
        
        # Analizar gastos de fin de semana
        weekend_ratio = patterns.get('weekend_spending', 0) / max(patterns.get('weekday_spending', 1), 1)
        if weekend_ratio > 0.4:  # Más del 40% en fin de semana
            weekend_spending = patterns.get('weekend_spending', 0)
            recommendations.append({
                'type': 'reduce_weekend_spending',
                'current_monthly': weekend_spending,
                'suggested_reduction': weekend_spending * 0.3,
                'monthly_savings': weekend_spending * 0.3,
                'yearly_savings': weekend_spending * 0.3 * 12,
                'message': f"Reduce gastos de fin de semana en 30% = ahorra ${weekend_spending * 0.3:,.0f}/mes"
            })
        
        # Ordenar por impacto
        recommendations.sort(key=lambda x: x['monthly_savings'], reverse=True)
        
        return {
            'has_high_potential': bool(has_high_potential),
            'recommendations': recommendations[:5],  # Top 5
            'total_monthly_savings': sum(r['monthly_savings'] for r in recommendations[:5]),
            'total_yearly_savings': sum(r['yearly_savings'] for r in recommendations[:5])
        }
    
    def _basic_recommendations(self, user_data):
        """
        Recomendaciones básicas cuando el modelo no está entrenado
        """
        patterns = user_data.get('patterns', {})
        recommendations = []
        
        # Reglas simples
        avg_expense = patterns.get('avg_monthly_expense', 0)
        if avg_expense > 0:
            recommendations.append({
                'type': 'reduce_expenses',
                'message': f"Reduce gastos mensuales en 20% = ahorra ${avg_expense * 0.2:,.0f}/mes",
                'monthly_savings': avg_expense * 0.2,
                'yearly_savings': avg_expense * 0.2 * 12
            })
        
        return {
            'has_high_potential': True,
            'recommendations': recommendations,
            'total_monthly_savings': sum(r['monthly_savings'] for r in recommendations),
            'total_yearly_savings': sum(r['yearly_savings'] for r in recommendations)
        }
    
    def save_models(self, prefix='models/smart_recommender'):
        """
        Guarda modelos entrenados
        """
        joblib.dump(self.expense_predictor, f'{prefix}_expense.pkl')
        joblib.dump(self.savings_classifier, f'{prefix}_savings.pkl')
        joblib.dump(self.scaler, f'{prefix}_scaler.pkl')
        
        # Guardar metadata
        metadata = {
            'trained_at': datetime.now().isoformat(),
            'is_trained': self.is_trained
        }
        with open(f'{prefix}_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"💾 Modelos guardados en {prefix}_*.pkl")
    
    def load_models(self, prefix='models/smart_recommender'):
        """
        Carga modelos entrenados
        """
        try:
            self.expense_predictor = joblib.load(f'{prefix}_expense.pkl')
            self.savings_classifier = joblib.load(f'{prefix}_savings.pkl')
            self.scaler = joblib.load(f'{prefix}_scaler.pkl')
            
            with open(f'{prefix}_metadata.json', 'r') as f:
                metadata = json.load(f)
            
            self.is_trained = metadata['is_trained']
            print(f"✅ Modelos cargados (entrenados el {metadata['trained_at']})")
            return True
        
        except FileNotFoundError:
            print("⚠️ No se encontraron modelos entrenados")
            return False


# Ejemplo de uso
if __name__ == "__main__":
    # 1. Crear y entrenar modelo
    recommender = SmartRecommender()
    
    # Intentar cargar modelos existentes
    if not recommender.load_models():
        # Si no existen, entrenar con datos
        recommender.train('training_data.json')
    
    # 2. Hacer predicción para un usuario nuevo
    new_user_data = {
        'patterns': {
            'avg_monthly_expense': 1500000,
            'expense_volatility': 200000,
            'small_expenses': {
                'Café': {'count': 20, 'sum': 160000},
                'Snacks': {'count': 25, 'sum': 300000}
            },
            'weekend_spending': 600000,
            'weekday_spending': 900000,
            'recurring_expenses': 200000
        },
        'aggregated_data': {
            'total_expenses': 1500000,
            'total_incomes': 2000000,
            'total_debt': 500000,
            'num_transactions': 45
        }
    }
    
    # Predecir gastos futuros
    predicted_expenses = recommender.predict_expenses(new_user_data)
    print(f"\n📊 Gastos predichos: ${predicted_expenses:,.0f}")
    
    # Obtener recomendaciones
    recommendations = recommender.recommend_savings_strategy(new_user_data)
    print(f"\n💡 Recomendaciones:")
    print(f"  Potencial alto: {'Sí' if recommendations['has_high_potential'] else 'No'}")
    print(f"  Ahorro mensual total: ${recommendations['total_monthly_savings']:,.0f}")
    print(f"  Ahorro anual total: ${recommendations['total_yearly_savings']:,.0f}")
    print(f"\n  Top recomendaciones:")
    for i, rec in enumerate(recommendations['recommendations'][:3], 1):
        print(f"    {i}. {rec['message']}")
