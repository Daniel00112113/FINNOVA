"""
Script de prueba para demostrar las mejoras de IA
"""
import requests
import json
from datetime import datetime, timedelta

# URL del AI Engine
BASE_URL = "http://localhost:8000"

def test_status():
    """Verifica que la IA avanzada esté activa"""
    print("🔍 Verificando estado de IA...")
    response = requests.get(f"{BASE_URL}/smart/status")
    data = response.json()
    
    print(f"✅ Smart AI: {'Activo' if data['smart_ai_enabled'] else 'Inactivo'}")
    print(f"✅ Advanced AI: {'Activo' if data['advanced_ai_enabled'] else 'Inactivo'}")
    print()

def test_financial_health():
    """Prueba análisis de salud financiera"""
    print("💊 Probando análisis de salud financiera...")
    
    request_data = {
        "user_id": "test-user-123",
        "total_income": 2000000,
        "total_expenses": 1500000,
        "total_debt": 500000,
        "total_savings": 300000,
        "avg_monthly_expenses": 1500000,
        "expenses_by_type": {
            "needs": 1000000,
            "wants": 400000,
            "savings": 100000
        },
        "expenses_by_category": {
            "Transporte": 700000,
            "Comida": 400000,
            "Entretenimiento": 200000,
            "Servicios": 200000
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/analyze/financial-health",
        json=request_data
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📊 Score de Salud: {data['overall_score']}/100")
        print(f"🎯 Nivel: {data['health_level']}")
        print(f"💬 Mensaje: {data['health_message']}")
        print(f"\n📈 Métricas:")
        for key, value in data['metrics'].items():
            print(f"  - {key}: {value}")
        print(f"\n💡 Recomendaciones:")
        for i, rec in enumerate(data['recommendations'][:3], 1):
            print(f"  {i}. {rec}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_advanced_predictions():
    """Prueba predicciones avanzadas"""
    print("🔮 Probando predicciones avanzadas...")
    
    # Generar transacciones de ejemplo
    transactions = []
    base_date = datetime.now() - timedelta(days=180)
    
    for i in range(6):  # 6 meses de datos
        month_date = base_date + timedelta(days=30*i)
        
        # Ingresos mensuales
        transactions.append({
            "amount": 2000000,
            "date": month_date.isoformat(),
            "type": "income",
            "category": "Salario"
        })
        
        # Gastos variados
        transactions.append({
            "amount": 700000,
            "date": (month_date + timedelta(days=5)).isoformat(),
            "type": "expense",
            "category": "Transporte"
        })
        transactions.append({
            "amount": 400000,
            "date": (month_date + timedelta(days=10)).isoformat(),
            "type": "expense",
            "category": "Comida"
        })
        transactions.append({
            "amount": 200000,
            "date": (month_date + timedelta(days=15)).isoformat(),
            "type": "expense",
            "category": "Entretenimiento"
        })
    
    request_data = {
        "user_id": "test-user-123",
        "transactions": transactions,
        "months_ahead": 3
    }
    
    response = requests.post(
        f"{BASE_URL}/predict/balance",
        json=request_data
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n🤖 Versión de IA: {data.get('ai_version', 'unknown')}")
        print(f"📊 Balance actual: ${data['current_balance']:,.0f} COP")
        print(f"🎯 Confianza: {data['confidence']*100:.0f}%")
        print(f"📈 Tendencia: {data['trend']}")
        print(f"⚠️ Nivel de riesgo: {data['risk_level']}")
        
        if 'features' in data and data['features']:
            print(f"\n🔍 Features detectados:")
            for key, value in data['features'].items():
                print(f"  - {key}: {value:.2%}" if isinstance(value, float) else f"  - {key}: {value}")
        
        print(f"\n🔮 Predicciones:")
        for pred in data['predictions']:
            print(f"  {pred['month']}: ${pred['predicted_balance']:,.0f} COP")
            if 'lower_bound' in pred:
                print(f"    Rango: ${pred['lower_bound']:,.0f} - ${pred['upper_bound']:,.0f}")
        
        print(f"\n💡 Recomendaciones:")
        for i, rec in enumerate(data['recommendations'][:3], 1):
            print(f"  {i}. {rec}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def test_actionable_recommendations():
    """Prueba recomendaciones accionables"""
    print("🎯 Probando recomendaciones accionables...")
    
    request_data = {
        "user_id": "test-user-123",
        "total_income": 2000000,
        "total_expenses": 1500000,
        "total_debt": 500000,
        "total_savings": 300000,
        "avg_monthly_expenses": 1500000,
        "expenses_by_category": {
            "Transporte": 700000,
            "Comida": 400000,
            "Entretenimiento": 200000,
            "Servicios": 200000
        }
    }
    
    response = requests.post(
        f"{BASE_URL}/recommendations/actionable",
        json=request_data
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\n📋 Total de recomendaciones: {data['total_recommendations']}")
        
        for i, rec in enumerate(data['recommendations'], 1):
            print(f"\n{i}. {rec['category']}")
            print(f"   Gasto actual: ${rec['current_monthly']:,.0f} COP/mes")
            print(f"   Representa: {rec['percentage_of_total']:.1f}% del total")
            print(f"   Acción: {rec['action']}")
            print(f"   Opciones:")
            for opt in rec['options']:
                print(f"     - {opt['reduction']}: Ahorra ${opt['monthly_savings']:,.0f}/mes (${opt['yearly_savings']:,.0f}/año) [{opt['difficulty']}]")
            print(f"   Tips:")
            for tip in rec['specific_tips'][:2]:
                print(f"     • {tip}")
    else:
        print(f"❌ Error: {response.text}")
    print()

def main():
    """Ejecuta todas las pruebas"""
    print("=" * 60)
    print("🚀 PRUEBA DE MEJORAS DE IA - FINANCIAL COPILOT")
    print("=" * 60)
    print()
    
    try:
        test_status()
        test_financial_health()
        test_advanced_predictions()
        test_actionable_recommendations()
        
        print("=" * 60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar al AI Engine")
        print("   Asegúrate de que esté corriendo: python ai-engine/main.py")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main()
