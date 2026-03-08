"""
Data Collector - Recolecta datos de usuarios para entrenamiento
"""
import psycopg2
import pandas as pd
from datetime import datetime, timedelta
import hashlib
import json

class FinancialDataCollector:
    """
    Recolecta y prepara datos de usuarios para entrenamiento de IA
    """
    
    def __init__(self, db_config):
        self.db_config = db_config
        self.conn = None
    
    def connect(self):
        """Conecta a la base de datos"""
        self.conn = psycopg2.connect(**self.db_config)
    
    def disconnect(self):
        """Cierra conexión"""
        if self.conn:
            self.conn.close()
    
    def get_users_with_consent(self):
        """
        Obtiene usuarios que dieron consentimiento para usar sus datos
        """
        query = """
        SELECT userid 
        FROM userconsent 
        WHERE allowdatafortraining = TRUE
        """
        
        df = pd.read_sql(query, self.conn)
        return df['userid'].tolist()
    
    def collect_user_transactions(self, user_id, months=12):
        """
        Recolecta transacciones de un usuario
        """
        start_date = datetime.now() - timedelta(days=months*30)
        
        # Gastos
        expenses_query = """
        SELECT 
            "Amount", "Category", "Date", "Description"
        FROM "Expenses"
        WHERE "UserId" = %s AND "Date" >= %s
        ORDER BY "Date"
        """
        
        expenses = pd.read_sql(expenses_query, self.conn, params=(user_id, start_date))
        # Normalizar nombres de columnas inmediatamente
        if not expenses.empty:
            expenses.columns = expenses.columns.str.lower()
        
        # Ingresos
        incomes_query = """
        SELECT "Amount", "Type", "Date"
        FROM "Incomes"
        WHERE "UserId" = %s AND "Date" >= %s
        ORDER BY "Date"
        """
        
        incomes = pd.read_sql(incomes_query, self.conn, params=(user_id, start_date))
        # Normalizar nombres de columnas inmediatamente
        if not incomes.empty:
            incomes.columns = incomes.columns.str.lower()
        
        # Deudas (opcional)
        try:
            debts_query = """
            SELECT "TotalAmount", "RemainingAmount", "InterestRate"
            FROM "Debts"
            WHERE "UserId" = %s
            """
            debts = pd.read_sql(debts_query, self.conn, params=(user_id,))
            if not debts.empty:
                debts.columns = debts.columns.str.lower()
        except:
            debts = pd.DataFrame()
        
        return {
            'expenses': expenses,
            'incomes': incomes,
            'debts': debts
        }
    
    def extract_patterns(self, transactions):
        """
        Extrae patrones de comportamiento de las transacciones
        """
        expenses = transactions['expenses'].copy()
        
        if expenses.empty:
            return {}
        
        # Normalizar nombres de columnas a minúsculas
        expenses.columns = expenses.columns.str.lower()
        
        patterns = {
            # Patrones de gasto
            'avg_monthly_expense': expenses.groupby(expenses['date'].dt.to_period('M'))['amount'].sum().mean(),
            'expense_volatility': expenses.groupby(expenses['date'].dt.to_period('M'))['amount'].sum().std(),
            'top_categories': expenses.groupby('category')['amount'].sum().nlargest(5).to_dict(),
            
            # Gastos pequeños recurrentes
            'small_expenses': expenses[expenses['amount'] < 50000].groupby('category')['amount'].agg(['count', 'sum']).to_dict(),
            
            # Patrones temporales
            'weekend_spending': expenses[expenses['date'].dt.dayofweek >= 5]['amount'].sum(),
            'weekday_spending': expenses[expenses['date'].dt.dayofweek < 5]['amount'].sum(),
        }
        
        return patterns
    
    def anonymize_data(self, user_id, data):
        """
        Anonimiza datos sensibles (GDPR compliant)
        """
        # Hash del user_id
        hashed_id = hashlib.sha256(str(user_id).encode()).hexdigest()
        
        expenses = data['expenses'].copy()
        incomes = data['incomes'].copy()
        debts = data['debts'].copy()
        
        # Normalizar nombres de columnas
        if not expenses.empty:
            expenses.columns = expenses.columns.str.lower()
        if not incomes.empty:
            incomes.columns = incomes.columns.str.lower()
        if not debts.empty:
            debts.columns = debts.columns.str.lower()
        
        anonymized = {
            'user_hash': hashed_id,
            'patterns': data['patterns'],
            'aggregated_data': {
                'total_expenses': expenses['amount'].sum() if not expenses.empty else 0,
                'total_incomes': incomes['amount'].sum() if not incomes.empty else 0,
                'total_debt': debts['remainingamount'].sum() if not debts.empty and 'remainingamount' in debts.columns else 0,
                'num_transactions': len(expenses)
            }
        }
        
        # NO incluir: nombres, emails, descripciones específicas, ubicaciones exactas
        
        return anonymized
    
    def create_training_dataset(self, output_file='training_data.json'):
        """
        Crea dataset completo de entrenamiento
        """
        self.connect()
        
        try:
            users = self.get_users_with_consent()
            print(f"📊 Recolectando datos de {len(users)} usuarios...")
            
            dataset = []
            
            for i, user_id in enumerate(users):
                try:
                    # Recolectar transacciones
                    transactions = self.collect_user_transactions(user_id)
                    
                    # Extraer patrones
                    patterns = self.extract_patterns(transactions)
                    
                    # Anonimizar
                    anonymized = self.anonymize_data(user_id, {
                        'expenses': transactions['expenses'],
                        'incomes': transactions['incomes'],
                        'debts': transactions['debts'],
                        'patterns': patterns
                    })
                    
                    dataset.append(anonymized)
                    
                    if (i + 1) % 10 == 0:
                        print(f"  Procesados {i + 1}/{len(users)} usuarios...")
                
                except Exception as e:
                    print(f"  ⚠️ Error con usuario {user_id}: {e}")
                    continue
            
            # Guardar dataset
            with open(output_file, 'w') as f:
                json.dump(dataset, f, indent=2, default=str)
            
            print(f"✅ Dataset guardado en {output_file}")
            print(f"📈 Total de usuarios: {len(dataset)}")
            
            return dataset
        
        finally:
            self.disconnect()


# Ejemplo de uso
if __name__ == "__main__":
    # Configuración de base de datos
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'FinancialCopilotDB',
        'user': 'postgres',
        'password': 'postgres'
    }
    
    collector = FinancialDataCollector(db_config)
    dataset = collector.create_training_dataset()
    
    print(f"\n🎉 Dataset creado con {len(dataset)} usuarios!")
