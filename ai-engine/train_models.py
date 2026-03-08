"""
Script para entrenar modelos de IA con datos reales de usuarios
Ejecutar: python train_models.py
"""
import sys
import os

# Agregar path del proyecto
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from training.data_collector import FinancialDataCollector
from training.smart_recommender import SmartRecommender

def main():
    print("=" * 60)
    print("🤖 ENTRENAMIENTO DE IA - FINANCIAL COPILOT")
    print("=" * 60)
    print()
    
    # Configuración de base de datos
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'FinancialCopilotDB',
        'user': 'postgres',
        'password': 'postgres'
    }
    
    # PASO 1: Recolectar datos
    print("📊 PASO 1: Recolectando datos de usuarios...")
    print("-" * 60)
    
    collector = FinancialDataCollector(db_config)
    
    try:
        dataset = collector.create_training_dataset('training_data.json')
        print(f"✅ Dataset creado: {len(dataset)} usuarios")
    except Exception as e:
        print(f"❌ Error recolectando datos: {e}")
        print("\n💡 Asegúrate de que:")
        print("  1. PostgreSQL esté corriendo")
        print("  2. La base de datos exista")
        print("  3. Haya usuarios con datos")
        return
    
    print()
    
    # PASO 2: Entrenar modelos
    print("🤖 PASO 2: Entrenando modelos de IA...")
    print("-" * 60)
    
    recommender = SmartRecommender()
    
    try:
        success = recommender.train('training_data.json')
        
        if success:
            print()
            print("=" * 60)
            print("🎉 ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
            print("=" * 60)
            print()
            print("Los modelos están listos para usar en producción.")
            print("Se guardarán en: ai-engine/models/")
            print()
            print("Próximos pasos:")
            print("  1. Reiniciar el AI Engine: python main.py")
            print("  2. Los nuevos modelos se cargarán automáticamente")
            print("  3. Las recomendaciones serán más precisas")
        else:
            print("⚠️ El entrenamiento no se completó correctamente")
    
    except Exception as e:
        print(f"❌ Error entrenando modelos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
