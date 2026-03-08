"""
Generador de Datos Financieros Ultra-Realistas
Basado en patrones reales de finanzas personales en Colombia
"""
import random
import uuid
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import execute_values
import numpy as np

class RealisticFinancialDataGenerator:
    """
    Genera datos financieros realistas basados en investigación
    """
    
    def __init__(self):
        # Perfiles de usuario con datos reales
        self.profiles = {
            'joven_profesional': {
                'name': 'Joven Profesional',
                'age_range': (22, 30),
                'income_range': (1800000, 3500000),
                'income_variability': 0.05,  # 5% variación
                'expense_ratio': (0.75, 0.85),
                'savings_discipline': 0.7,  # 70% probabilidad de ahorrar
                'categories': {
                    'Transporte': (0.15, 0.20),
                    'Comida': (0.20, 0.25),
                    'Entretenimiento': (0.15, 0.20),
                    'Vivienda': (0.25, 0.30),
                    'Servicios': (0.10, 0.15),
                    'Salud': (0.03, 0.08),
                    'Educación': (0.02, 0.05),
                    'Otros': (0.05, 0.10)
                },
                'patterns': {
                    'weekend_multiplier': 1.5,
                    'impulse_buying': 0.3,  # 30% de compras son impulsivas
                    'delivery_frequency': 0.4,  # 40% de comidas son delivery
                    'subscriptions': ['Netflix', 'Spotify', 'Gym']
                }
            },
            'familia': {
                'name': 'Familia',
                'age_range': (30, 45),
                'income_range': (3000000, 6000000),
                'income_variability': 0.03,
                'expense_ratio': (0.80, 0.90),
                'savings_discipline': 0.6,
                'categories': {
                    'Vivienda': (0.30, 0.35),
                    'Educación': (0.15, 0.20),
                    'Comida': (0.20, 0.25),
                    'Transporte': (0.10, 0.15),
                    'Salud': (0.10, 0.15),
                    'Servicios': (0.10, 0.15),
                    'Entretenimiento': (0.05, 0.10),
                    'Otros': (0.05, 0.10)
                },
                'patterns': {
                    'weekend_multiplier': 1.2,
                    'impulse_buying': 0.15,
                    'delivery_frequency': 0.15,
                    'subscriptions': ['Netflix', 'Disney+', 'Medicina Prepagada']
                }
            },
            'freelancer': {
                'name': 'Freelancer',
                'age_range': (25, 40),
                'income_range': (2000000, 8000000),
                'income_variability': 0.40,  # 40% variación (ingresos irregulares)
                'expense_ratio': (0.65, 0.80),
                'savings_discipline': 0.8,  # Ahorra más por precaución
                'categories': {
                    'Trabajo': (0.20, 0.30),
                    'Vivienda': (0.20, 0.25),
                    'Comida': (0.15, 0.20),
                    'Transporte': (0.10, 0.15),
                    'Impuestos': (0.15, 0.20),
                    'Servicios': (0.10, 0.15),
                    'Entretenimiento': (0.05, 0.10),
                    'Otros': (0.05, 0.10)
                },
                'patterns': {
                    'weekend_multiplier': 1.3,
                    'impulse_buying': 0.20,
                    'delivery_frequency': 0.30,
                    'subscriptions': ['Adobe', 'Notion', 'Spotify', 'Coworking']
                }
            },
            'estudiante': {
                'name': 'Estudiante',
                'age_range': (18, 25),
                'income_range': (800000, 1500000),
                'income_variability': 0.15,
                'expense_ratio': (0.90, 1.00),
                'savings_discipline': 0.3,
                'categories': {
                    'Educación': (0.30, 0.40),
                    'Comida': (0.20, 0.25),
                    'Transporte': (0.15, 0.20),
                    'Entretenimiento': (0.15, 0.20),
                    'Servicios': (0.05, 0.10),
                    'Otros': (0.05, 0.10)
                },
                'patterns': {
                    'weekend_multiplier': 1.8,
                    'impulse_buying': 0.40,
                    'delivery_frequency': 0.50,
                    'subscriptions': ['Spotify', 'Netflix']
                }
            },
            'profesional_senior': {
                'name': 'Profesional Senior',
                'age_range': (40, 55),
                'income_range': (5000000, 12000000),
                'income_variability': 0.03,
                'expense_ratio': (0.70, 0.80),
                'savings_discipline': 0.9,
                'categories': {
                    'Vivienda': (0.25, 0.30),
                    'Inversiones': (0.15, 0.20),
                    'Educación': (0.15, 0.20),
                    'Salud': (0.10, 0.15),
                    'Transporte': (0.10, 0.15),
                    'Entretenimiento': (0.10, 0.15),
                    'Servicios': (0.08, 0.12),
                    'Otros': (0.05, 0.10)
                },
                'patterns': {
                    'weekend_multiplier': 1.1,
                    'impulse_buying': 0.10,
                    'delivery_frequency': 0.20,
                    'subscriptions': ['Netflix', 'Amazon Prime', 'Medicina Prepagada', 'Seguros']
                }
            }
        }
        
        # Precios realistas por categoría
        self.expense_ranges = {
            'Transporte': {
                'Uber': (5000, 25000),
                'Gasolina': (50000, 150000),
                'Parqueadero': (3000, 15000),
                'Mantenimiento': (150000, 800000),
                'Bus': (2800, 3500)
            },
            'Comida': {
                'Mercado': (300000, 800000),
                'Restaurante': (25000, 60000),
                'Delivery': (20000, 50000),
                'Café': (5000, 15000),
                'Snacks': (2000, 8000)
            },
            'Entretenimiento': {
                'Cine': (15000, 25000),
                'Bar': (50000, 150000),
                'Streaming': (15000, 45000),
                'Gym': (80000, 200000),
                'Hobbies': (50000, 300000)
            },
            'Vivienda': {
                'Arriendo': (800000, 3000000),
                'Hipoteca': (1000000, 4000000),
                'Administración': (150000, 500000)
            },
            'Servicios': {
                'Internet': (50000, 120000),
                'Celular': (30000, 100000),
                'Luz': (80000, 250000),
                'Agua': (40000, 120000),
                'Gas': (30000, 80000)
            },
            'Salud': {
                'Prepagada': (200000, 600000),
                'Consulta': (80000, 200000),
                'Medicamentos': (30000, 150000),
                'Odontología': (100000, 500000)
            },
            'Educación': {
                'Colegio': (800000, 2500000),
                'Universidad': (3000000, 8000000),
                'Cursos': (50000, 300000),
                'Libros': (50000, 200000),
                'Útiles': (100000, 300000)
            },
            'Trabajo': {
                'Software': (50000, 300000),
                'Herramientas': (100000, 500000),
                'Coworking': (300000, 800000)
            },
            'Impuestos': {
                'Renta': (500000, 2000000),
                'IVA': (100000, 500000)
            },
            'Inversiones': {
                'CDT': (1000000, 5000000),
                'Acciones': (500000, 3000000),
                'Fondos': (300000, 2000000)
            },
            'Otros': {
                'Ropa': (50000, 300000),
                'Regalos': (30000, 200000),
                'Varios': (10000, 100000)
            }
        }

    
    def generate_user(self, profile_name, months=12):
        """
        Genera un usuario completo con transacciones realistas
        """
        profile = self.profiles[profile_name]
        
        # Datos básicos del usuario
        user_id = str(uuid.uuid4())
        age = random.randint(*profile['age_range'])
        base_income = random.randint(*profile['income_range'])
        
        # Determinar trayectoria financiera
        trajectory = random.choices(
            ['mejora', 'deterioro', 'estable'],
            weights=[0.20, 0.15, 0.65]
        )[0]
        
        user_data = {
            'id': user_id,
            'profile': profile_name,
            'age': age,
            'base_income': base_income,
            'trajectory': trajectory,
            'incomes': [],
            'expenses': []
        }
        
        # Generar transacciones mes a mes
        for month in range(months):
            month_data = self._generate_month(
                profile, base_income, month, months, trajectory
            )
            
            user_data['incomes'].extend(month_data['incomes'])
            user_data['expenses'].extend(month_data['expenses'])
        
        return user_data
    
    def _generate_month(self, profile, base_income, month_num, total_months, trajectory):
        """
        Genera transacciones de un mes específico
        """
        # Calcular ingreso del mes con variabilidad
        income_variation = random.uniform(
            1 - profile['income_variability'],
            1 + profile['income_variability']
        )
        monthly_income = base_income * income_variation
        
        # Ajustar según trayectoria
        if trajectory == 'mejora':
            # Ingresos aumentan gradualmente
            growth_factor = 1 + (month_num / total_months) * 0.15
            monthly_income *= growth_factor
        elif trajectory == 'deterioro':
            # Ingresos disminuyen gradualmente
            decline_factor = 1 - (month_num / total_months) * 0.10
            monthly_income *= decline_factor
        
        # Fecha base del mes
        base_date = datetime.now() - timedelta(days=30 * (total_months - month_num))
        
        incomes = []
        expenses = []
        
        # Generar ingresos
        # Salario principal (día 1-5)
        salary_date = base_date + timedelta(days=random.randint(1, 5))
        incomes.append({
            'date': salary_date,
            'amount': monthly_income * 0.85,  # 85% del ingreso
            'type': 'Salario',
            'description': 'Salario mensual'
        })
        
        # Ingresos adicionales (freelance, bonos, etc)
        if random.random() < 0.3:  # 30% probabilidad
            extra_date = base_date + timedelta(days=random.randint(10, 25))
            incomes.append({
                'date': extra_date,
                'amount': monthly_income * random.uniform(0.10, 0.30),
                'type': 'Extra',
                'description': random.choice(['Bono', 'Freelance', 'Comisión', 'Venta'])
            })
        
        # Calcular presupuesto de gastos
        expense_ratio = random.uniform(*profile['expense_ratio'])
        
        # Ajustar según trayectoria
        if trajectory == 'mejora':
            # Gastos disminuyen gradualmente
            expense_ratio *= (1 - (month_num / total_months) * 0.15)
        elif trajectory == 'deterioro':
            # Gastos aumentan (lifestyle creep)
            expense_ratio *= (1 + (month_num / total_months) * 0.20)
        
        total_budget = monthly_income * expense_ratio
        
        # Distribuir gastos por categoría
        for category, (min_ratio, max_ratio) in profile['categories'].items():
            category_budget = total_budget * random.uniform(min_ratio, max_ratio)
            
            # Generar transacciones de esta categoría
            category_expenses = self._generate_category_expenses(
                category, category_budget, base_date, profile
            )
            expenses.extend(category_expenses)
        
        # Agregar gastos especiales según el mes
        special_expenses = self._generate_special_expenses(base_date, monthly_income)
        expenses.extend(special_expenses)
        
        return {
            'incomes': incomes,
            'expenses': expenses
        }
    
    def _generate_category_expenses(self, category, budget, base_date, profile):
        """
        Genera gastos realistas para una categoría específica
        """
        expenses = []
        
        if category not in self.expense_ranges:
            # Categoría sin subcategorías definidas
            num_transactions = random.randint(2, 8)
            for _ in range(num_transactions):
                amount = budget / num_transactions * random.uniform(0.7, 1.3)
                date = self._random_date_in_month(base_date, profile)
                expenses.append({
                    'date': date,
                    'amount': amount,
                    'category': category,
                    'description': f'Gasto en {category}'
                })
            return expenses
        
        # Categorías con subcategorías definidas
        subcategories = self.expense_ranges[category]
        remaining_budget = budget
        
        for subcategory, (min_amount, max_amount) in subcategories.items():
            # Decidir si hacer este tipo de gasto
            if random.random() < 0.7:  # 70% probabilidad
                # Número de transacciones de este tipo
                if subcategory in ['Arriendo', 'Hipoteca', 'Prepagada', 'Colegio', 'Universidad']:
                    # Gastos mensuales fijos
                    num_trans = 1
                    amount = random.uniform(min_amount, max_amount)
                    date = base_date + timedelta(days=random.randint(1, 5))
                elif subcategory in ['Streaming', 'Gym', 'Internet', 'Celular']:
                    # Suscripciones
                    num_trans = 1
                    amount = random.uniform(min_amount, max_amount)
                    date = base_date + timedelta(days=random.randint(1, 28))
                else:
                    # Gastos variables
                    num_trans = random.randint(1, 10)
                    amount = min(
                        random.uniform(min_amount, max_amount),
                        remaining_budget / num_trans
                    )
                    date = None
                
                for _ in range(num_trans):
                    if date is None:
                        date = self._random_date_in_month(base_date, profile)
                    
                    if remaining_budget >= amount:
                        expenses.append({
                            'date': date,
                            'amount': amount,
                            'category': category,
                            'description': subcategory,
                            'is_recurring': subcategory in ['Arriendo', 'Hipoteca', 'Streaming', 'Gym']
                        })
                        remaining_budget -= amount
                    
                    date = None  # Reset para próxima iteración
        
        return expenses
    
    def _random_date_in_month(self, base_date, profile):
        """
        Genera fecha aleatoria considerando patrones realistas
        """
        # Más gastos al inicio y fin de semana
        day = random.randint(1, 28)
        
        # Ajustar por patrones de fin de semana
        date = base_date + timedelta(days=day)
        
        # Si es fin de semana, más probabilidad de gastos
        if date.weekday() >= 5:  # Sábado o Domingo
            # Aplicar multiplicador de fin de semana
            pass
        
        # Hora del día (para gastos como Uber, comida)
        hour = random.choices(
            range(24),
            weights=[1]*6 + [2]*3 + [3]*3 + [4]*6 + [3]*3 + [2]*3  # Picos en almuerzo y cena
        )[0]
        
        return date.replace(hour=hour, minute=random.randint(0, 59))
    
    def _generate_special_expenses(self, base_date, monthly_income):
        """
        Genera gastos especiales según fechas importantes
        """
        expenses = []
        month = base_date.month
        
        special_dates = {
            1: ('Útiles Escolares', 0.10),  # Enero
            2: ('San Valentín', 0.05),
            4: ('Semana Santa', 0.08),
            5: ('Día de la Madre', 0.04),
            6: ('Día del Padre', 0.04),
            7: ('Vacaciones', 0.12),
            8: ('Regreso a Clases', 0.08),
            9: ('Amor y Amistad', 0.05),
            12: ('Navidad', 0.15)
        }
        
        if month in special_dates:
            event, ratio = special_dates[month]
            if random.random() < 0.7:  # 70% probabilidad
                amount = monthly_income * ratio * random.uniform(0.8, 1.2)
                date = base_date + timedelta(days=random.randint(10, 25))
                expenses.append({
                    'date': date,
                    'amount': amount,
                    'category': 'Otros',
                    'description': event
                })
        
        return expenses
    
    def generate_dataset(self, n_users=100, db_config=None):
        """
        Genera dataset completo de usuarios
        """
        print(f"🎨 Generando {n_users} usuarios ultra-realistas...")
        print("=" * 70)
        
        # Distribuir perfiles de manera realista
        profile_distribution = {
            'joven_profesional': 0.30,
            'familia': 0.25,
            'freelancer': 0.15,
            'estudiante': 0.15,
            'profesional_senior': 0.15
        }
        
        users_data = []
        
        for i in range(n_users):
            # Seleccionar perfil según distribución
            profile = random.choices(
                list(profile_distribution.keys()),
                weights=list(profile_distribution.values())
            )[0]
            
            # Generar usuario
            months = random.randint(12, 18)  # 12-18 meses de datos
            user = self.generate_user(profile, months)
            users_data.append(user)
            
            if (i + 1) % 10 == 0:
                print(f"  ✅ Generados {i + 1}/{n_users} usuarios...")
        
        print(f"\n📊 Resumen del dataset:")
        for profile, ratio in profile_distribution.items():
            count = int(n_users * ratio)
            print(f"  {self.profiles[profile]['name']}: {count} usuarios")
        
        # Guardar en base de datos si se proporciona config
        if db_config:
            self._save_to_database(users_data, db_config)
        
        return users_data
    
    def _save_to_database(self, users_data, db_config):
        """
        Guarda datos en PostgreSQL
        """
        print(f"\n💾 Guardando en base de datos...")
        
        try:
            conn = psycopg2.connect(**db_config)
            cur = conn.cursor()
            
            for i, user in enumerate(users_data):
                try:
                    # Crear usuario
                    cur.execute("""
                        INSERT INTO "Users" ("Id", "Email", "Name", "PasswordHash", "CreatedAt")
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT ("Id") DO NOTHING
                    """, (
                        user['id'],
                        f"realistic_{i}@test.com",
                        f"{self.profiles[user['profile']]['name']} {i}",
                        'synthetic_user_no_password',  # Password hash placeholder
                        datetime.now()
                    ))
                    conn.commit()
                    
                    # Dar consentimiento (opcional, si la tabla existe)
                    try:
                        cur.execute("""
                            INSERT INTO userconsent (userid, allowdatafortraining, consentdate)
                            VALUES (%s, TRUE, %s)
                            ON CONFLICT (userid) DO UPDATE SET allowdatafortraining = TRUE
                        """, (user['id'], datetime.now()))
                        conn.commit()
                    except Exception:
                        # Si la tabla no existe, hacer rollback y continuar
                        conn.rollback()
                    
                    # Insertar ingresos
                    incomes_data = [
                        (str(uuid.uuid4()), user['id'], inc['amount'], inc['date'], inc['type'], datetime.now())
                        for inc in user['incomes']
                    ]
                    
                    if incomes_data:
                        execute_values(cur, """
                            INSERT INTO "Incomes" ("Id", "UserId", "Amount", "Date", "Type", "CreatedAt")
                            VALUES %s
                        """, incomes_data)
                    
                    # Insertar gastos
                    expenses_data = [
                        (
                            str(uuid.uuid4()),
                            user['id'],
                            exp['amount'],
                            exp['category'],
                            exp['date'],
                            exp.get('description', ''),
                            datetime.now()
                        )
                        for exp in user['expenses']
                    ]
                    
                    if expenses_data:
                        execute_values(cur, """
                            INSERT INTO "Expenses" ("Id", "UserId", "Amount", "Category", "Date", "Description", "CreatedAt")
                            VALUES %s
                        """, expenses_data)
                    
                    conn.commit()
                    
                    if (i + 1) % 10 == 0:
                        print(f"  💾 Guardados {i + 1}/{len(users_data)} usuarios...")
                        
                except Exception as e:
                    conn.rollback()
                    print(f"  ⚠️  Error con usuario {i}: {e}")
                    continue
            
            conn.commit()
            cur.close()
            conn.close()
            
            print(f"\n✅ {len(users_data)} usuarios guardados en base de datos")
            
            # Estadísticas
            total_transactions = sum(len(u['incomes']) + len(u['expenses']) for u in users_data)
            print(f"📈 Total de transacciones: {total_transactions:,}")
            print(f"📊 Promedio por usuario: {total_transactions // len(users_data):,}")
            
        except Exception as e:
            print(f"\n❌ Error guardando en base de datos: {e}")

def main():
    """
    Ejecuta el generador
    """
    import sys
    
    # Configuración de base de datos
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'financialcopilot',
        'user': 'postgres',
        'password': 'postgres'
    }
    
    # Número de usuarios
    n_users = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    
    # Generar datos
    generator = RealisticFinancialDataGenerator()
    users_data = generator.generate_dataset(n_users, db_config)
    
    print(f"\n🎉 ¡Generación completada!")
    print(f"\n📝 Próximos pasos:")
    print(f"  1. Entrenar modelo: python train_professional.py")
    print(f"  2. Iniciar AI Engine: python main.py")

if __name__ == "__main__":
    main()
