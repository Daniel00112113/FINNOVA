"""
Generador de Datos Sintéticos
Para pruebas cuando no hay suficientes usuarios reales
"""
import random
import uuid
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_values

def generate_synthetic_users(n_users=50, db_config=None):
    """
    Genera usuarios sintéticos con transacciones realistas
    """
    if db_config is None:
        db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'FinancialCopilotDB',
            'user': 'postgres',
            'password': 'postgres'
        }
    
    print(f"🔧 Generando {n_users} usuarios sintéticos...")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Perfiles de usuario
        profiles = [
            {'name': 'Joven Profesional', 'income': (1800000, 2500000), 'expense_ratio': (0.75, 0.85)},
            {'name': 'Familia', 'income': (2500000, 4000000), 'expense_ratio': (0.80, 0.90)},
            {'name': 'Freelancer', 'income': (1500000, 3500000), 'expense_ratio': (0.70, 0.85)},
            {'name': 'Emprendedor', 'income': (2000000, 5000000), 'expense_ratio': (0.65, 0.80)},
        ]
        
        categories = {
            'Transporte': (0.15, 0.25),
            'Comida': (0.20, 0.30),
            'Entretenimiento': (0.10, 0.20),
            'Servicios': (0.15, 0.25),
            'Salud': (0.05, 0.15),
            'Educación': (0.05, 0.15),
            'Otros': (0.05, 0.10)
        }
        
        for i in range(n_users):
            # Seleccionar perfil aleatorio
            profile = random.choice(profiles)
            
            # Generar ID único
            user_id = str(uuid.uuid4())
            
            # Crear usuario
            try:
                cur.execute("""
                    INSERT INTO Users (Id, Email, Name, CreatedAt) 
                    VALUES (%s, %s, %s, %s)
                """, (
                    user_id,
                    f'synthetic_{i}@test.com',
                    f'Usuario Sintético {i}',
                    datetime.now()
                ))
            except:
                # Usuario ya existe
                continue
            
            # Dar consentimiento
            try:
                cur.execute("""
                    INSERT INTO UserConsent (UserId, AllowDataForTraining, ConsentDate)
                    VALUES (%s, TRUE, %s)
                """, (user_id, datetime.now()))
            except:
                pass
            
            # Generar transacciones (6-12 meses)
            months = random.randint(6, 12)
            base_income = random.randint(*profile['income'])
            expense_ratio = random.uniform(*profile['expense_ratio'])
            base_expense = base_income * expense_ratio
            
            incomes_data = []
            expenses_data = []
            
            for month in range(months):
                # Fecha del mes
                days_ago = 30 * month + random.randint(0, 5)
                date = datetime.now() - timedelta(days=days_ago)
                
                # Ingreso mensual (con variación)
                income_variation = random.uniform(0.9, 1.1)
                monthly_income = base_income * income_variation
                
                incomes_data.append((
                    str(uuid.uuid4()),
                    user_id,
                    monthly_income,
                    'Salario',
                    date
                ))
                
                # Gastos por categoría
                for category, (min_ratio, max_ratio) in categories.items():
                    # Número de transacciones en esta categoría
                    num_transactions = random.randint(2, 8)
                    category_budget = base_expense * random.uniform(min_ratio, max_ratio)
                    
                    for _ in range(num_transactions):
                        # Distribuir el presupuesto
                        amount = category_budget / num_transactions * random.uniform(0.7, 1.3)
                        
                        # Fecha aleatoria en el mes
                        transaction_date = date + timedelta(days=random.randint(0, 28))
                        
                        expenses_data.append((
                            str(uuid.uuid4()),
                            user_id,
                            amount,
                            category,
                            transaction_date,
                            f'Gasto en {category}',
                            None,  # Location
                            False,  # IsRecurring
                            None   # Tags
                        ))
            
            # Insertar ingresos
            if incomes_data:
                execute_values(cur, """
                    INSERT INTO Incomes (Id, UserId, Amount, Type, Date)
                    VALUES %s
                """, incomes_data)
            
            # Insertar gastos
            if expenses_data:
                execute_values(cur, """
                    INSERT INTO Expenses (Id, UserId, Amount, Category, Date, Description, Location, IsRecurring, Tags)
                    VALUES %s
                """, expenses_data)
            
            if (i + 1) % 10 == 0:
                print(f"  ✅ Generados {i + 1}/{n_users} usuarios...")
                conn.commit()
        
        conn.commit()
        cur.close()
        conn.close()
        
        print(f"\n✅ {n_users} usuarios sintéticos generados exitosamente")
        print(f"   Cada usuario tiene {months} meses de transacciones")
        print(f"   Total de transacciones: ~{n_users * months * 30}")
        
        return True
    
    except Exception as e:
        print(f"\n❌ Error generando datos: {e}")
        return False

def clean_synthetic_data(db_config=None):
    """
    Elimina todos los datos sintéticos
    """
    if db_config is None:
        db_config = {
            'host': 'localhost',
            'port': 5432,
            'database': 'FinancialCopilotDB',
            'user': 'postgres',
            'password': 'postgres'
        }
    
    print("🧹 Limpiando datos sintéticos...")
    
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Eliminar transacciones
        cur.execute("DELETE FROM Expenses WHERE UserId IN (SELECT Id FROM Users WHERE Email LIKE 'synthetic_%')")
        cur.execute("DELETE FROM Incomes WHERE UserId IN (SELECT Id FROM Users WHERE Email LIKE 'synthetic_%')")
        
        # Eliminar consentimientos
        cur.execute("DELETE FROM UserConsent WHERE UserId IN (SELECT Id FROM Users WHERE Email LIKE 'synthetic_%')")
        
        # Eliminar usuarios
        cur.execute("DELETE FROM Users WHERE Email LIKE 'synthetic_%'")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("✅ Datos sintéticos eliminados")
        return True
    
    except Exception as e:
        print(f"❌ Error limpiando datos: {e}")
        return False

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'clean':
        clean_synthetic_data()
    else:
        n_users = int(sys.argv[1]) if len(sys.argv) > 1 else 50
        generate_synthetic_users(n_users)
