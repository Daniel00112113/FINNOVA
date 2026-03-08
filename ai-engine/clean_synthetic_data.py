"""
Script para limpiar datos sintéticos de la base de datos
"""
import psycopg2

def clean_all_synthetic_data():
    """
    Elimina TODOS los datos sintéticos (synthetic_ y realistic_)
    """
    db_config = {
        'host': 'localhost',
        'port': 5432,
        'database': 'FinancialCopilotDB',
        'user': 'postgres',
        'password': 'postgres'
    }
    
    print("🧹 Limpiando datos sintéticos...")
    print("=" * 60)
    
    try:
        conn = psycopg2.connect(**db_config)
        cur = conn.cursor()
        
        # Contar antes de eliminar
        cur.execute("SELECT COUNT(*) FROM Users WHERE Email LIKE 'synthetic_%' OR Email LIKE 'realistic_%'")
        count_users = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM Expenses WHERE UserId IN (SELECT Id FROM Users WHERE Email LIKE 'synthetic_%' OR Email LIKE 'realistic_%')")
        count_expenses = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM Incomes WHERE UserId IN (SELECT Id FROM Users WHERE Email LIKE 'synthetic_%' OR Email LIKE 'realistic_%')")
        count_incomes = cur.fetchone()[0]
        
        print(f"📊 Datos a eliminar:")
        print(f"  Usuarios: {count_users}")
        print(f"  Gastos: {count_expenses}")
        print(f"  Ingresos: {count_incomes}")
        print(f"  Total transacciones: {count_expenses + count_incomes}")
        
        if count_users == 0:
            print("\n✅ No hay datos sintéticos para eliminar")
            return
        
        response = input("\n¿Confirmar eliminación? (s/n): ")
        
        if response.lower() != 's':
            print("❌ Operación cancelada")
            return
        
        print("\n🗑️ Eliminando...")
        
        # Eliminar en orden correcto (por foreign keys)
        cur.execute("DELETE FROM Expenses WHERE UserId IN (SELECT Id FROM Users WHERE Email LIKE 'synthetic_%' OR Email LIKE 'realistic_%')")
        print(f"  ✅ {cur.rowcount} gastos eliminados")
        
        cur.execute("DELETE FROM Incomes WHERE UserId IN (SELECT Id FROM Users WHERE Email LIKE 'synthetic_%' OR Email LIKE 'realistic_%')")
        print(f"  ✅ {cur.rowcount} ingresos eliminados")
        
        cur.execute("DELETE FROM Debts WHERE UserId IN (SELECT Id FROM Users WHERE Email LIKE 'synthetic_%' OR Email LIKE 'realistic_%')")
        print(f"  ✅ {cur.rowcount} deudas eliminadas")
        
        cur.execute("DELETE FROM UserConsent WHERE UserId IN (SELECT Id FROM Users WHERE Email LIKE 'synthetic_%' OR Email LIKE 'realistic_%')")
        print(f"  ✅ {cur.rowcount} consentimientos eliminados")
        
        cur.execute("DELETE FROM Users WHERE Email LIKE 'synthetic_%' OR Email LIKE 'realistic_%'")
        print(f"  ✅ {cur.rowcount} usuarios eliminados")
        
        conn.commit()
        cur.close()
        conn.close()
        
        print("\n✅ Limpieza completada exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    clean_all_synthetic_data()
