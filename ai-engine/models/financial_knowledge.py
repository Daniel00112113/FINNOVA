"""
Financial Knowledge Engine - Motor de conocimiento financiero experto
Aplica principios financieros probados para análisis y recomendaciones
"""
from typing import Dict, List
from datetime import datetime
import numpy as np

class FinancialKnowledgeEngine:
    """
    Motor que entiende y aplica conceptos financieros expertos
    """
    
    # Reglas financieras universales
    RULE_50_30_20 = {
        'needs': 0.50,      # 50% necesidades
        'wants': 0.30,      # 30% deseos
        'savings': 0.20     # 20% ahorro
    }
    
    EMERGENCY_FUND_MONTHS = 6  # 6 meses de gastos
    MAX_DEBT_TO_INCOME = 0.36  # 36% máximo
    MIN_SAVINGS_RATE = 0.20    # 20% mínimo
    
    def __init__(self):
        self.financial_profiles = {
            'young_professional': {
                'age_range': (22, 35),
                'savings_target': 0.25,
                'risk_tolerance': 'high',
                'priorities': ['emergency_fund', 'career_growth', 'lifestyle']
            },
            'family': {
                'age_range': (30, 50),
                'savings_target': 0.30,
                'risk_tolerance': 'medium',
                'priorities': ['emergency_fund', 'education', 'housing']
            },
            'freelancer': {
                'age_range': (25, 45),
                'savings_target': 0.35,  # Mayor por inestabilidad
                'risk_tolerance': 'medium',
                'priorities': ['emergency_fund', 'tax_reserve', 'income_stability']
            }
        }
    
    def analyze_financial_health(self, user_data: Dict) -> Dict:
        """
        Analiza salud financiera según principios expertos
        """
        income = user_data.get('total_income', 0)
        expenses = user_data.get('total_expenses', 0)
        debt = user_data.get('total_debt', 0)
        savings = user_data.get('total_savings', 0)
        
        if income == 0:
            return self._empty_health_analysis()
        
        # Calcular métricas clave
        expense_ratio = expenses / income
        debt_to_income = debt / income
        savings_rate = (income - expenses) / income if income > expenses else 0
        
        # Evaluar según regla 50/30/20
        rule_50_30_20_score = self._evaluate_50_30_20_rule(user_data)
        
        # Evaluar fondo de emergencia
        emergency_fund_score = self._evaluate_emergency_fund(user_data)
        
        # Evaluar gestión de deuda
        debt_score = self._evaluate_debt_management(debt_to_income)
        
        # Score general (0-100)
        overall_score = (
            rule_50_30_20_score * 0.3 +
            emergency_fund_score * 0.3 +
            debt_score * 0.2 +
            (savings_rate * 100) * 0.2
        )
        
        # Nivel de salud financiera
        if overall_score >= 80:
            health_level = 'excellent'
            health_message = '¡Excelente! Tu salud financiera es muy buena'
        elif overall_score >= 60:
            health_level = 'good'
            health_message = 'Bien, pero hay áreas de mejora'
        elif overall_score >= 40:
            health_level = 'fair'
            health_message = 'Regular, necesitas mejorar varios aspectos'
        else:
            health_level = 'poor'
            health_message = 'Crítico, requiere atención inmediata'
        
        return {
            'overall_score': round(overall_score, 1),
            'health_level': health_level,
            'health_message': health_message,
            'metrics': {
                'expense_ratio': round(expense_ratio, 2),
                'debt_to_income': round(debt_to_income, 2),
                'savings_rate': round(savings_rate, 2),
                'rule_50_30_20_score': round(rule_50_30_20_score, 1),
                'emergency_fund_score': round(emergency_fund_score, 1),
                'debt_score': round(debt_score, 1)
            },
            'recommendations': self._generate_health_recommendations(
                expense_ratio, debt_to_income, savings_rate, emergency_fund_score
            )
        }

    
    def _evaluate_50_30_20_rule(self, user_data: Dict) -> float:
        """
        Evalúa qué tan bien sigue la regla 50/30/20
        """
        expenses_by_type = user_data.get('expenses_by_type', {})
        total_income = user_data.get('total_income', 0)
        
        if total_income == 0:
            return 0
        
        needs = expenses_by_type.get('needs', 0)
        wants = expenses_by_type.get('wants', 0)
        savings = user_data.get('total_savings', 0)
        
        # Calcular ratios actuales
        needs_ratio = needs / total_income
        wants_ratio = wants / total_income
        savings_ratio = savings / total_income
        
        # Calcular desviación de lo ideal
        needs_deviation = abs(needs_ratio - self.RULE_50_30_20['needs'])
        wants_deviation = abs(wants_ratio - self.RULE_50_30_20['wants'])
        savings_deviation = abs(savings_ratio - self.RULE_50_30_20['savings'])
        
        # Score: 100 si perfecto, 0 si muy desviado
        total_deviation = needs_deviation + wants_deviation + savings_deviation
        score = max(0, 100 - (total_deviation * 100))
        
        return score
    
    def _evaluate_emergency_fund(self, user_data: Dict) -> float:
        """
        Evalúa el fondo de emergencia
        """
        savings = user_data.get('total_savings', 0)
        monthly_expenses = user_data.get('avg_monthly_expenses', 0)
        
        if monthly_expenses == 0:
            return 0
        
        # Calcular meses de cobertura
        months_covered = savings / monthly_expenses
        
        # Score basado en meses (ideal: 6 meses)
        if months_covered >= self.EMERGENCY_FUND_MONTHS:
            return 100
        else:
            return (months_covered / self.EMERGENCY_FUND_MONTHS) * 100
    
    def _evaluate_debt_management(self, debt_to_income: float) -> float:
        """
        Evalúa la gestión de deuda
        """
        if debt_to_income == 0:
            return 100  # Sin deuda es perfecto
        
        if debt_to_income <= self.MAX_DEBT_TO_INCOME:
            # Deuda manejable
            return 100 - (debt_to_income / self.MAX_DEBT_TO_INCOME) * 30
        else:
            # Deuda excesiva
            excess = debt_to_income - self.MAX_DEBT_TO_INCOME
            return max(0, 70 - (excess * 100))
    
    def _generate_health_recommendations(
        self, 
        expense_ratio: float, 
        debt_to_income: float, 
        savings_rate: float,
        emergency_fund_score: float
    ) -> List[str]:
        """
        Genera recomendaciones basadas en salud financiera
        """
        recommendations = []
        
        # Recomendación 1: Ratio de gastos
        if expense_ratio > 0.80:
            recommendations.append(
                f"🚨 URGENTE: Gastas el {expense_ratio*100:.0f}% de tus ingresos. "
                f"Reduce gastos al 70% o menos para tener margen de ahorro."
            )
        elif expense_ratio > 0.70:
            recommendations.append(
                f"⚠️ Gastas el {expense_ratio*100:.0f}% de tus ingresos. "
                f"Intenta reducir al 70% para mejorar tu capacidad de ahorro."
            )
        
        # Recomendación 2: Deuda
        if debt_to_income > self.MAX_DEBT_TO_INCOME:
            recommendations.append(
                f"🚨 Tu deuda representa el {debt_to_income*100:.0f}% de tus ingresos "
                f"(máximo recomendado: 36%). Prioriza pagar deudas con mayor interés."
            )
        elif debt_to_income > 0.20:
            recommendations.append(
                f"💡 Tu deuda es del {debt_to_income*100:.0f}% de ingresos. "
                f"Considera destinar 10-15% de ingresos extra al pago de deuda."
            )
        
        # Recomendación 3: Ahorro
        if savings_rate < 0.10:
            recommendations.append(
                f"🚨 Solo ahorras el {savings_rate*100:.0f}% de tus ingresos. "
                f"Objetivo mínimo: 20%. Empieza con 10% e incrementa gradualmente."
            )
        elif savings_rate < self.MIN_SAVINGS_RATE:
            recommendations.append(
                f"💡 Ahorras el {savings_rate*100:.0f}% (objetivo: 20%). "
                f"Aumenta {(self.MIN_SAVINGS_RATE - savings_rate)*100:.0f}% más para alcanzar la meta."
            )
        else:
            recommendations.append(
                f"✅ ¡Excelente! Ahorras el {savings_rate*100:.0f}% de tus ingresos. "
                f"Mantén este hábito y considera invertir parte del ahorro."
            )
        
        # Recomendación 4: Fondo de emergencia
        if emergency_fund_score < 50:
            recommendations.append(
                f"🚨 Tu fondo de emergencia cubre menos de 3 meses de gastos. "
                f"Prioriza construir un fondo de 6 meses antes de otras inversiones."
            )
        elif emergency_fund_score < 100:
            recommendations.append(
                f"💡 Tu fondo de emergencia está en construcción. "
                f"Continúa ahorrando hasta cubrir 6 meses de gastos."
            )
        
        # Recomendación 5: Regla 50/30/20
        recommendations.append(
            f"📊 Aplica la regla 50/30/20: 50% necesidades, 30% deseos, 20% ahorro. "
            f"Esta distribución te ayudará a mantener balance financiero."
        )
        
        return recommendations[:5]  # Máximo 5 recomendaciones
    
    def _empty_health_analysis(self) -> Dict:
        return {
            'overall_score': 0,
            'health_level': 'unknown',
            'health_message': 'Registra ingresos y gastos para analizar tu salud financiera',
            'metrics': {},
            'recommendations': ['Comienza registrando tus transacciones diarias']
        }

    
    def detect_problematic_behaviors(self, transactions: List[Dict]) -> Dict:
        """
        Detecta comportamientos financieros problemáticos
        """
        behaviors = []
        
        # 1. Gasto emocional (compras después de eventos estresantes)
        emotional_spending = self._detect_emotional_spending(transactions)
        if emotional_spending['detected']:
            behaviors.append({
                'type': 'emotional_spending',
                'severity': 'medium',
                'description': emotional_spending['description'],
                'recommendation': emotional_spending['recommendation']
            })
        
        # 2. Lifestyle creep (gastos aumentan con ingresos)
        lifestyle_creep = self._detect_lifestyle_creep(transactions)
        if lifestyle_creep['detected']:
            behaviors.append({
                'type': 'lifestyle_creep',
                'severity': 'high',
                'description': lifestyle_creep['description'],
                'recommendation': lifestyle_creep['recommendation']
            })
        
        # 3. Gastos hormiga acumulativos
        small_expenses = self._detect_cumulative_small_expenses(transactions)
        if small_expenses['detected']:
            behaviors.append({
                'type': 'cumulative_small_expenses',
                'severity': 'medium',
                'description': small_expenses['description'],
                'recommendation': small_expenses['recommendation']
            })
        
        # 4. Suscripciones olvidadas
        forgotten_subs = self._detect_forgotten_subscriptions(transactions)
        if forgotten_subs['detected']:
            behaviors.append({
                'type': 'forgotten_subscriptions',
                'severity': 'low',
                'description': forgotten_subs['description'],
                'recommendation': forgotten_subs['recommendation']
            })
        
        return {
            'behaviors_detected': len(behaviors),
            'behaviors': behaviors,
            'overall_risk': self._calculate_behavior_risk(behaviors)
        }
    
    def _detect_emotional_spending(self, transactions: List[Dict]) -> Dict:
        """
        Detecta patrones de gasto emocional
        """
        # Buscar picos de gasto en categorías no esenciales
        # TODO: Implementar detección más sofisticada
        return {
            'detected': False,
            'description': '',
            'recommendation': ''
        }
    
    def _detect_lifestyle_creep(self, transactions: List[Dict]) -> Dict:
        """
        Detecta si los gastos aumentan proporcionalmente con ingresos
        """
        # Analizar si gastos crecen más rápido que ingresos
        # TODO: Implementar análisis temporal
        return {
            'detected': False,
            'description': '',
            'recommendation': ''
        }
    
    def _detect_cumulative_small_expenses(self, transactions: List[Dict]) -> Dict:
        """
        Detecta gastos pequeños que suman mucho
        """
        small_expenses = [t for t in transactions if t.get('amount', 0) < 50000]
        
        if len(small_expenses) > 20:  # Más de 20 gastos pequeños
            total = sum(t.get('amount', 0) for t in small_expenses)
            
            if total > 200000:  # Suman más de 200K
                return {
                    'detected': True,
                    'description': f'Tienes {len(small_expenses)} gastos pequeños que suman ${total:,.0f} COP',
                    'recommendation': f'Reducir estos gastos en 50% te ahorraría ${total*0.5:,.0f} COP/mes'
                }
        
        return {'detected': False, 'description': '', 'recommendation': ''}
    
    def _detect_forgotten_subscriptions(self, transactions: List[Dict]) -> Dict:
        """
        Detecta suscripciones que quizás el usuario olvidó
        """
        # Buscar transacciones recurrentes mensuales
        recurring = [t for t in transactions if t.get('is_recurring', False)]
        
        if len(recurring) > 5:  # Más de 5 suscripciones
            total = sum(t.get('amount', 0) for t in recurring)
            return {
                'detected': True,
                'description': f'Tienes {len(recurring)} suscripciones activas (${total:,.0f} COP/mes)',
                'recommendation': 'Revisa si realmente usas todas. Cancelar las innecesarias puede ahorrar mucho.'
            }
        
        return {'detected': False, 'description': '', 'recommendation': ''}
    
    def _calculate_behavior_risk(self, behaviors: List[Dict]) -> str:
        """
        Calcula riesgo general basado en comportamientos detectados
        """
        if not behaviors:
            return 'low'
        
        severity_scores = {'low': 1, 'medium': 2, 'high': 3}
        total_score = sum(severity_scores.get(b['severity'], 0) for b in behaviors)
        
        if total_score >= 6:
            return 'high'
        elif total_score >= 3:
            return 'medium'
        else:
            return 'low'
    
    def get_actionable_recommendations(self, user_data: Dict, top_n: int = 5) -> List[Dict]:
        """
        Genera recomendaciones ultra-accionables con impacto calculado
        """
        recommendations = []
        
        # Analizar gastos por categoría
        expenses_by_category = user_data.get('expenses_by_category', {})
        total_expenses = sum(expenses_by_category.values())
        
        if total_expenses == 0:
            return []
        
        # Ordenar categorías por monto
        sorted_categories = sorted(
            expenses_by_category.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        
        # Generar recomendaciones específicas por categoría
        for category, amount in sorted_categories[:3]:  # Top 3 categorías
            percentage = (amount / total_expenses) * 100
            
            if percentage > 20:  # Si representa más del 20%
                # Calcular impacto de reducción
                reduction_10 = amount * 0.10
                reduction_20 = amount * 0.20
                
                recommendations.append({
                    'category': category,
                    'current_monthly': amount,
                    'percentage_of_total': round(percentage, 1),
                    'action': f'Reduce {category}',
                    'options': [
                        {
                            'reduction': '10%',
                            'monthly_savings': reduction_10,
                            'yearly_savings': reduction_10 * 12,
                            'difficulty': 'easy'
                        },
                        {
                            'reduction': '20%',
                            'monthly_savings': reduction_20,
                            'yearly_savings': reduction_20 * 12,
                            'difficulty': 'medium'
                        }
                    ],
                    'specific_tips': self._get_category_tips(category)
                })
        
        return recommendations[:top_n]
    
    def _get_category_tips(self, category: str) -> List[str]:
        """
        Obtiene tips específicos por categoría
        """
        tips_by_category = {
            'Transporte': [
                'Usa transporte público 2-3 días/semana',
                'Comparte viajes con compañeros',
                'Considera bicicleta para distancias cortas'
            ],
            'Comida': [
                'Prepara comida en casa 4-5 días/semana',
                'Compra al por mayor productos no perecederos',
                'Planifica menú semanal para evitar desperdicio'
            ],
            'Entretenimiento': [
                'Comparte suscripciones con familia/amigos',
                'Busca actividades gratuitas los fines de semana',
                'Limita salidas a restaurantes a 2-3/mes'
            ],
            'Servicios': [
                'Compara proveedores cada 6 meses',
                'Negocia mejores tarifas',
                'Cancela servicios que no uses'
            ]
        }
        
        return tips_by_category.get(category, [
            'Evalúa si cada gasto es realmente necesario',
            'Busca alternativas más económicas',
            'Establece un presupuesto mensual para esta categoría'
        ])
