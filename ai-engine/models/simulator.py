import numpy as np
from typing import Dict, List

class FinancialSimulator:
    def simulate_financial_scenarios(
        self,
        current_balance: float,
        monthly_income: float,
        monthly_expenses: float,
        debt: float,
        interest_rate: float,
        months: int = 12,
        custom_scenarios: Dict = None
    ) -> Dict:
        """Simula diferentes escenarios financieros"""
        
        scenarios = {}
        
        # Escenario 1: Situación actual (sin cambios)
        scenarios['current'] = self._simulate_scenario(
            current_balance, monthly_income, monthly_expenses, debt, interest_rate, months
        )
        
        # Escenario 2: Reducir gastos 20%
        scenarios['reduce_expenses_20'] = self._simulate_scenario(
            current_balance, monthly_income, monthly_expenses * 0.8, debt, interest_rate, months
        )
        
        # Escenario 3: Aumentar ingresos 15%
        scenarios['increase_income_15'] = self._simulate_scenario(
            current_balance, monthly_income * 1.15, monthly_expenses, debt, interest_rate, months
        )
        
        # Escenario 4: Pagar deuda agresivamente (50% del ahorro mensual)
        scenarios['aggressive_debt_payment'] = self._simulate_aggressive_debt_payment(
            current_balance, monthly_income, monthly_expenses, debt, interest_rate, months
        )
        
        # Escenario 5: Optimizado (reducir gastos 10% + aumentar ingresos 10%)
        scenarios['optimized'] = self._simulate_scenario(
            current_balance, monthly_income * 1.1, monthly_expenses * 0.9, debt, interest_rate, months
        )
        
        # Escenarios personalizados
        if custom_scenarios:
            for name, params in custom_scenarios.items():
                scenarios[name] = self._simulate_scenario(
                    current_balance,
                    params.get('monthly_income', monthly_income),
                    params.get('monthly_expenses', monthly_expenses),
                    params.get('debt', debt),
                    params.get('interest_rate', interest_rate),
                    months
                )
        
        # Comparación y recomendaciones
        comparison = self._compare_scenarios(scenarios)
        
        return {
            'scenarios': scenarios,
            'comparison': comparison,
            'best_scenario': comparison['best_scenario'],
            'recommendations': self._generate_scenario_recommendations(scenarios, comparison)
        }
    
    def _simulate_scenario(
        self,
        initial_balance: float,
        monthly_income: float,
        monthly_expenses: float,
        debt: float,
        interest_rate: float,
        months: int
    ) -> Dict:
        """Simula un escenario específico mes a mes"""
        
        balance = initial_balance
        remaining_debt = debt
        monthly_interest_rate = interest_rate / 12 / 100
        
        timeline = []
        total_interest_paid = 0
        
        for month in range(months):
            # Calcular interés de deuda
            interest_payment = remaining_debt * monthly_interest_rate if remaining_debt > 0 else 0
            total_interest_paid += interest_payment
            
            # Flujo de caja mensual
            net_income = monthly_income - monthly_expenses - interest_payment
            balance += net_income
            
            # Pago mínimo de deuda (5% del saldo o $50, lo que sea mayor)
            if remaining_debt > 0:
                min_payment = max(remaining_debt * 0.05, 50)
                if balance >= min_payment:
                    payment = min(min_payment, remaining_debt)
                    balance -= payment
                    remaining_debt -= payment
            
            timeline.append({
                'month': month + 1,
                'balance': round(balance, 2),
                'debt': round(remaining_debt, 2),
                'net_income': round(net_income, 2)
            })
        
        final_balance = balance
        final_debt = remaining_debt
        total_saved = final_balance - initial_balance
        
        return {
            'timeline': timeline,
            'final_balance': round(final_balance, 2),
            'final_debt': round(final_debt, 2),
            'total_saved': round(total_saved, 2),
            'total_interest_paid': round(total_interest_paid, 2),
            'debt_paid_off': debt - final_debt > 0,
            'months_to_positive': self._months_to_positive(timeline)
        }
    
    def _simulate_aggressive_debt_payment(
        self,
        initial_balance: float,
        monthly_income: float,
        monthly_expenses: float,
        debt: float,
        interest_rate: float,
        months: int
    ) -> Dict:
        """Simula pago agresivo de deuda"""
        
        balance = initial_balance
        remaining_debt = debt
        monthly_interest_rate = interest_rate / 12 / 100
        
        timeline = []
        total_interest_paid = 0
        
        for month in range(months):
            # Calcular interés
            interest_payment = remaining_debt * monthly_interest_rate if remaining_debt > 0 else 0
            total_interest_paid += interest_payment
            
            # Flujo de caja
            net_income = monthly_income - monthly_expenses - interest_payment
            balance += net_income
            
            # Pago agresivo: 50% del ahorro disponible
            if remaining_debt > 0 and balance > 500:  # Mantener reserva de $500
                available_for_debt = (balance - 500) * 0.5
                payment = min(available_for_debt, remaining_debt)
                if payment > 0:
                    balance -= payment
                    remaining_debt -= payment
            
            timeline.append({
                'month': month + 1,
                'balance': round(balance, 2),
                'debt': round(remaining_debt, 2),
                'net_income': round(net_income, 2)
            })
        
        return {
            'timeline': timeline,
            'final_balance': round(balance, 2),
            'final_debt': round(remaining_debt, 2),
            'total_saved': round(balance - initial_balance, 2),
            'total_interest_paid': round(total_interest_paid, 2),
            'debt_paid_off': remaining_debt == 0,
            'months_to_positive': self._months_to_positive(timeline)
        }
    
    def _months_to_positive(self, timeline: List[Dict]) -> int:
        """Calcula cuántos meses hasta tener balance positivo"""
        for entry in timeline:
            if entry['balance'] > 0:
                return entry['month']
        return -1  # Nunca positivo
    
    def _compare_scenarios(self, scenarios: Dict) -> Dict:
        """Compara todos los escenarios"""
        
        comparison = {}
        best_balance = -float('inf')
        best_scenario = None
        
        for name, scenario in scenarios.items():
            final_balance = scenario['final_balance']
            final_debt = scenario['final_debt']
            
            # Score: balance final - deuda final
            score = final_balance - final_debt
            
            comparison[name] = {
                'final_balance': final_balance,
                'final_debt': final_debt,
                'score': round(score, 2),
                'debt_paid_off': scenario['debt_paid_off']
            }
            
            if score > best_balance:
                best_balance = score
                best_scenario = name
        
        comparison['best_scenario'] = best_scenario
        
        return comparison
    
    def _generate_scenario_recommendations(self, scenarios: Dict, comparison: Dict) -> List[str]:
        """Genera recomendaciones basadas en simulaciones"""
        
        recommendations = []
        best = comparison['best_scenario']
        
        # Nombres legibles
        scenario_names = {
            'current': 'mantener tu situación actual',
            'reduce_expenses_20': 'reducir gastos en 20%',
            'increase_income_15': 'aumentar ingresos en 15%',
            'aggressive_debt_payment': 'pagar deuda agresivamente',
            'optimized': 'optimizar (reducir gastos 10% + aumentar ingresos 10%)'
        }
        
        best_name = scenario_names.get(best, best)
        best_data = scenarios[best]
        current_data = scenarios['current']
        
        # Recomendación principal
        recommendations.append(
            f"🏆 Tu mejor estrategia es {best_name}. "
            f"Esto te permitirá alcanzar un balance de {self._format_cop(best_data['final_balance'])} "
            f"en {len(best_data['timeline'])} meses."
        )
        
        # Comparación con situación actual
        improvement = best_data['final_balance'] - current_data['final_balance']
        if improvement > 100000:
            recommendations.append(
                f"💰 Siguiendo esta estrategia, mejorarás tu balance en {self._format_cop(improvement)} "
                f"comparado con mantener tu situación actual."
            )
        
        # Análisis de deuda
        if best_data['debt_paid_off'] and best_data['final_debt'] == 0:
            recommendations.append(
                f"✅ ¡Excelente noticia! Con esta estrategia podrás eliminar completamente tu deuda "
                f"y ahorrarás {self._format_cop(best_data['total_interest_paid'])} en intereses."
            )
        elif current_data['final_debt'] > 0:
            debt_reduction = current_data['final_debt'] - best_data['final_debt']
            if debt_reduction > 0:
                recommendations.append(
                    f"📉 Reducirás tu deuda en {self._format_cop(debt_reduction)}, "
                    f"de {self._format_cop(current_data['final_debt'])} a {self._format_cop(best_data['final_debt'])}."
                )
        
        # Recomendaciones específicas por escenario
        if best == 'reduce_expenses_20':
            recommendations.append(
                "💡 Enfócate en reducir gastos no esenciales: entretenimiento, comidas fuera, "
                "suscripciones innecesarias. Pequeños cambios generan grandes resultados."
            )
        elif best == 'increase_income_15':
            recommendations.append(
                "💡 Considera opciones para aumentar ingresos: trabajo freelance, vender productos, "
                "pedir aumento salarial, o desarrollar una habilidad monetizable."
            )
        elif best == 'aggressive_debt_payment':
            recommendations.append(
                "💡 Prioriza el pago de deudas con mayor interés primero. "
                "Destina cualquier ingreso extra al pago de deuda para ahorrar en intereses."
            )
        elif best == 'optimized':
            recommendations.append(
                "💡 La combinación de reducir gastos y aumentar ingresos es la estrategia más efectiva. "
                "Trabaja en ambos frentes simultáneamente para mejores resultados."
            )
        
        # Análisis de ahorro
        if best_data['total_saved'] > 0:
            monthly_saving = best_data['total_saved'] / len(best_data['timeline'])
            recommendations.append(
                f"💵 Podrás ahorrar aproximadamente {self._format_cop(monthly_saving)} por mes, "
                f"acumulando {self._format_cop(best_data['total_saved'])} en total."
            )
        
        # Advertencia si la situación es crítica
        if current_data['final_balance'] < 0:
            recommendations.append(
                "⚠️ Tu situación actual proyecta un balance negativo. "
                "Es urgente tomar acción para evitar problemas financieros."
            )
        
        return recommendations[:6]  # Máximo 6 recomendaciones
    
    def _format_cop(self, amount: float) -> str:
        """Formatea cantidad en pesos colombianos"""
        return f"${amount:,.0f} COP"
