"""
Script Principal de Entrenamiento Profesional
Ejecuta el pipeline completo de entrenamiento
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from training.data_collector import FinancialDataCollector
from training.professional_feature_engineering import ProfessionalFeatureEngineer
from training.professional_trainer import ProfessionalTrainer
import warnings
warnings.filterwarnings('ignore')

def main():
    """
    Pipeline completo de entrenamiento profesional
    """
    print("=" * 70)
    print("🚀 ENTRENAMIENTO PROFESIONAL DE IA - FINANCIAL COPILOT")
    print("=" * 70)
    
    # PASO 1: Configuración de base de datos
    print("\n📊 PASO 1: Configuración")
    print("-" * 70)
    
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'financialcopilot',
        'user': 'postgres',
        'password': 'postgres'
    }
    
    print(f"Base de datos: {db_config['database']}")
    print(f"Host: {db_config['host']}:{db_config['port']}")
    
    # PASO 2: Recolectar datos
    print("\n📥 PASO 2: Recolección de Datos")
    print("-" * 70)
    
    try:
        collector = FinancialDataCollector(db_config)
        collector.connect()
        
        # Obtener usuarios con consentimiento
        users = collector.get_users_with_consent()
        print(f"✅ Usuarios con consentimiento: {len(users)}")
        
        if len(users) < 10:
            print(f"\n⚠️ ADVERTENCIA: Solo {len(users)} usuarios disponibles")
            print("   Recomendado: 50+ usuarios para entrenamiento profesional")
            print("   Mínimo: 10 usuarios")
            
            if len(users) < 10:
                print("\n❌ Insuficientes datos para entrenar")
                print("   Soluciones:")
                print("   1. Espera a tener más usuarios")
                print("   2. Usa datos sintéticos para pruebas")
                collector.disconnect()
                return
        
        # Recolectar datos de cada usuario
        print("\n📦 Recolectando transacciones...")
        dataset = []
        
        for i, user_id in enumerate(users):
            try:
                transactions = collector.collect_user_transactions(user_id, months=12)
                
                # Validar que tenga suficientes datos
                if len(transactions['expenses']) < 10:
                    continue
                
                # Combinar transacciones
                all_transactions = []
                
                for _, row in transactions['expenses'].iterrows():
                    all_transactions.append({
                        'date': row['date'],
                        'amount': row['amount'],
                        'type': 'expense',
                        'category': row.get('category', 'Other')
                    })
                
                for _, row in transactions['incomes'].iterrows():
                    all_transactions.append({
                        'date': row['date'],
                        'amount': row['amount'],
                        'type': 'income',
                        'category': 'Income'
                    })
                
                if len(all_transactions) >= 20:  # Mínimo 20 transacciones
                    dataset.append({
                        'user_id': user_id,
                        'transactions': all_transactions
                    })
                
                if (i + 1) % 10 == 0:
                    print(f"  Procesados {i + 1}/{len(users)} usuarios...")
            
            except Exception as e:
                print(f"  ⚠️ Error con usuario {user_id}: {e}")
                continue
        
        collector.disconnect()
        
        print(f"\n✅ Dataset recolectado: {len(dataset)} usuarios válidos")
        
        if len(dataset) < 10:
            print("\n❌ Insuficientes usuarios con datos válidos")
            return
    
    except Exception as e:
        print(f"\n❌ Error en recolección de datos: {e}")
        print("\n💡 Solución: Verifica que PostgreSQL esté corriendo")
        print("   y que la base de datos exista")
        return
    
    # PASO 3: Feature Engineering
    print("\n🔧 PASO 3: Feature Engineering")
    print("-" * 70)
    
    feature_engineer = ProfessionalFeatureEngineer()
    
    X_data = []
    y_data = []
    
    print("Extrayendo features...")
    for user in dataset:
        try:
            # Extraer features
            features = feature_engineer.extract_all_features(user)
            
            # Target: gastos del próximo mes
            transactions_df = pd.DataFrame(user['transactions'])
            transactions_df['date'] = pd.to_datetime(transactions_df['date'])
            expenses = transactions_df[transactions_df['type'] == 'expense']
            
            if not expenses.empty:
                # Calcular gastos promedio mensual
                months = (expenses['date'].max() - expenses['date'].min()).days / 30
                avg_monthly_expense = expenses['amount'].sum() / max(months, 1)
                
                X_data.append(list(features.values()))
                y_data.append(avg_monthly_expense)
        
        except Exception as e:
            print(f"  ⚠️ Error procesando usuario: {e}")
            continue
    
    X = np.array(X_data)
    y = np.array(y_data)
    
    print(f"✅ Features extraídos: {X.shape[1]} características")
    print(f"✅ Samples: {X.shape[0]} usuarios")
    print(f"✅ Target: Gastos mensuales promedio")
    
    # PASO 4: Split de datos
    print("\n✂️ PASO 4: División de Datos")
    print("-" * 70)
    
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, random_state=42
    )
    
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, random_state=42
    )
    
    print(f"Train: {len(X_train)} samples ({len(X_train)/len(X)*100:.1f}%)")
    print(f"Val:   {len(X_val)} samples ({len(X_val)/len(X)*100:.1f}%)")
    print(f"Test:  {len(X_test)} samples ({len(X_test)/len(X)*100:.1f}%)")
    
    # PASO 5: Entrenamiento
    print("\n🎯 PASO 5: Entrenamiento de Modelos")
    print("-" * 70)
    
    trainer = ProfessionalTrainer()
    trainer.prepare_models()
    trainer.feature_names = list(features.keys())
    
    # Normalizar datos
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)
    X_test_scaled = scaler.transform(X_test)
    
    trainer.scaler = scaler
    
    # Entrenar todos los modelos
    results = trainer.train_all_models(X_train_scaled, y_train, X_val_scaled, y_val)
    
    # PASO 6: Validación Cruzada
    print("\n🔄 PASO 6: Validación Cruzada")
    print("-" * 70)
    
    X_combined = np.vstack([X_train_scaled, X_val_scaled])
    y_combined = np.concatenate([y_train, y_val])
    
    cv_results = trainer.cross_validate(X_combined, y_combined, n_splits=5)
    
    # PASO 7: Evaluación Final en Test Set
    print("\n📊 PASO 7: Evaluación Final")
    print("-" * 70)
    
    y_test_pred = trainer.best_model.predict(X_test_scaled)
    
    from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
    
    test_mae = mean_absolute_error(y_test, y_test_pred)
    test_rmse = np.sqrt(mean_squared_error(y_test, y_test_pred))
    test_r2 = r2_score(y_test, y_test_pred)
    
    print(f"Test MAE:  ${test_mae:,.0f}")
    print(f"Test RMSE: ${test_rmse:,.0f}")
    print(f"Test R²:   {test_r2:.3f}")
    
    # Comparar con baseline
    baseline_mae = np.mean(np.abs(y_test - np.mean(y_train)))
    improvement = (baseline_mae - test_mae) / baseline_mae * 100
    
    print(f"\nBaseline MAE: ${baseline_mae:,.0f}")
    print(f"Mejora: {improvement:.1f}%")
    
    # PASO 8: Guardar modelo
    print("\n💾 PASO 8: Guardando Modelo")
    print("-" * 70)
    
    trainer.save_model('models/professional')
    
    # PASO 9: Resumen Final
    print("\n" + "=" * 70)
    print("✅ ENTRENAMIENTO COMPLETADO")
    print("=" * 70)
    
    print(f"\n📊 Resumen:")
    print(f"  Modelo: {trainer.best_model_name}")
    print(f"  Usuarios entrenados: {len(dataset)}")
    print(f"  Features: {X.shape[1]}")
    print(f"  Test MAE: ${test_mae:,.0f}")
    print(f"  Test R²: {test_r2:.3f}")
    print(f"  Mejora vs baseline: {improvement:.1f}%")
    
    print(f"\n📁 Archivos generados:")
    print(f"  models/professional/best_model.pkl")
    print(f"  models/professional/scaler.pkl")
    print(f"  models/professional/metadata.json")
    
    print(f"\n🚀 Próximos pasos:")
    print(f"  1. Reinicia AI Engine: python ai-engine/main.py")
    print(f"  2. El modelo se cargará automáticamente")
    print(f"  3. Prueba con: python ai-engine/test_mejoras.py")

if __name__ == "__main__":
    main()
