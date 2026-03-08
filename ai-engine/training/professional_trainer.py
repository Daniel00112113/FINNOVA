"""
Sistema de Entrenamiento Profesional
Entrena múltiples modelos y selecciona el mejor
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.linear_model import Ridge, Lasso, ElasticNet
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
import xgboost as xgb
import lightgbm as lgb
import joblib
import json
from datetime import datetime
from typing import Dict, List, Tuple
import warnings
warnings.filterwarnings('ignore')

class ProfessionalTrainer:
    """
    Entrenador profesional de modelos ML
    """
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.scaler = StandardScaler()
        self.feature_names = []
        
    def prepare_models(self):
        """
        Prepara todos los modelos a probar
        """
        self.models = {
            'ridge': Ridge(alpha=1.0, random_state=42),
            'lasso': Lasso(alpha=1.0, random_state=42),
            'elastic_net': ElasticNet(alpha=1.0, l1_ratio=0.5, random_state=42),
            'random_forest': RandomForestRegressor(
                n_estimators=100,
                max_depth=10,
                min_samples_split=5,
                random_state=42,
                n_jobs=-1
            ),
            'gradient_boosting': GradientBoostingRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42
            ),
            'xgboost': xgb.XGBRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
                n_jobs=-1
            ),
            'lightgbm': lgb.LGBMRegressor(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=42,
                n_jobs=-1,
                verbose=-1
            )
        }
        
        print(f"✅ {len(self.models)} modelos preparados")
        return self.models
    
    def train_all_models(
        self, 
        X_train: np.ndarray, 
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray
    ) -> Dict:
        """
        Entrena todos los modelos y compara resultados
        """
        print("\n🚀 Iniciando entrenamiento de modelos...")
        print("=" * 60)
        
        results = {}
        
        for name, model in self.models.items():
            print(f"\n📊 Entrenando {name}...")
            
            try:
                # Entrenar
                import time
                start_time = time.time()
                model.fit(X_train, y_train)
                training_time = time.time() - start_time
                
                # Predecir
                y_pred_train = model.predict(X_train)
                y_pred_val = model.predict(X_val)
                
                # Calcular métricas
                metrics = {
                    'train': self._calculate_metrics(y_train, y_pred_train),
                    'val': self._calculate_metrics(y_val, y_pred_val),
                    'training_time': training_time
                }
                
                results[name] = {
                    'model': model,
                    'metrics': metrics
                }
                
                # Mostrar resultados
                print(f"  Train MAE: ${metrics['train']['mae']:,.0f}")
                print(f"  Val MAE:   ${metrics['val']['mae']:,.0f}")
                print(f"  Val RMSE:  ${metrics['val']['rmse']:,.0f}")
                print(f"  Val R²:    {metrics['val']['r2']:.3f}")
                print(f"  Time:      {training_time:.2f}s")
                
                # Detectar overfitting
                overfit_ratio = metrics['train']['mae'] / max(metrics['val']['mae'], 1)
                if overfit_ratio < 0.7:
                    print(f"  ⚠️ Posible overfitting (ratio: {overfit_ratio:.2f})")
                
            except Exception as e:
                print(f"  ❌ Error: {e}")
                continue
        
        # Seleccionar mejor modelo
        print("\n" + "=" * 60)
        self._select_best_model(results)
        
        return results
    
    def _calculate_metrics(self, y_true: np.ndarray, y_pred: np.ndarray) -> Dict:
        """
        Calcula métricas de evaluación
        """
        return {
            'mae': mean_absolute_error(y_true, y_pred),
            'rmse': np.sqrt(mean_squared_error(y_true, y_pred)),
            'r2': r2_score(y_true, y_pred),
            'mape': np.mean(np.abs((y_true - y_pred) / np.maximum(y_true, 1))) * 100
        }
    
    def _select_best_model(self, results: Dict):
        """
        Selecciona el mejor modelo basado en MAE de validación
        """
        best_mae = float('inf')
        best_name = None
        
        for name, result in results.items():
            val_mae = result['metrics']['val']['mae']
            if val_mae < best_mae:
                best_mae = val_mae
                best_name = name
        
        if best_name:
            self.best_model = results[best_name]['model']
            self.best_model_name = best_name
            
            print(f"\n🏆 MEJOR MODELO: {best_name}")
            print(f"   MAE: ${best_mae:,.0f}")
            print(f"   RMSE: ${results[best_name]['metrics']['val']['rmse']:,.0f}")
            print(f"   R²: {results[best_name]['metrics']['val']['r2']:.3f}")
    
    def cross_validate(
        self, 
        X: np.ndarray, 
        y: np.ndarray, 
        n_splits: int = 5
    ) -> Dict:
        """
        Validación cruzada para series temporales
        """
        print(f"\n🔄 Validación cruzada ({n_splits} folds)...")
        
        tscv = TimeSeriesSplit(n_splits=n_splits)
        scores = []
        
        for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
            print(f"  Fold {fold + 1}/{n_splits}...", end=" ")
            
            X_train, X_val = X[train_idx], X[val_idx]
            y_train, y_val = y[train_idx], y[val_idx]
            
            # Entrenar mejor modelo
            self.best_model.fit(X_train, y_train)
            
            # Evaluar
            y_pred = self.best_model.predict(X_val)
            mae = mean_absolute_error(y_val, y_pred)
            scores.append(mae)
            
            print(f"MAE: ${mae:,.0f}")
        
        avg_mae = np.mean(scores)
        std_mae = np.std(scores)
        
        print(f"\n  📊 Promedio: ${avg_mae:,.0f} ± ${std_mae:,.0f}")
        
        return {
            'scores': scores,
            'mean': avg_mae,
            'std': std_mae
        }
    
    def save_model(self, output_dir: str = 'models/professional'):
        """
        Guarda el mejor modelo y metadatos
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Guardar modelo
        model_path = f'{output_dir}/best_model.pkl'
        joblib.dump(self.best_model, model_path)
        print(f"✅ Modelo guardado: {model_path}")
        
        # Guardar scaler
        scaler_path = f'{output_dir}/scaler.pkl'
        joblib.dump(self.scaler, scaler_path)
        print(f"✅ Scaler guardado: {scaler_path}")
        
        # Guardar metadatos
        metadata = {
            'model_name': self.best_model_name,
            'trained_at': datetime.now().isoformat(),
            'feature_names': self.feature_names,
            'num_features': len(self.feature_names)
        }
        
        metadata_path = f'{output_dir}/metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        print(f"✅ Metadata guardado: {metadata_path}")
    
    def load_model(self, model_dir: str = 'models/professional'):
        """
        Carga modelo entrenado
        """
        try:
            model_path = f'{model_dir}/best_model.pkl'
            self.best_model = joblib.load(model_path)
            
            scaler_path = f'{model_dir}/scaler.pkl'
            self.scaler = joblib.load(scaler_path)
            
            metadata_path = f'{model_dir}/metadata.json'
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            self.best_model_name = metadata['model_name']
            self.feature_names = metadata['feature_names']
            
            print(f"✅ Modelo cargado: {self.best_model_name}")
            print(f"   Entrenado: {metadata['trained_at']}")
            print(f"   Features: {metadata['num_features']}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return False
