import psycopg2
import pandas as pd

db_config = {
    'host': 'localhost',
    'port': 5432,
    'database': 'financialcopilot',
    'user': 'postgres',
    'password': 'postgres'
}

conn = psycopg2.connect(**db_config)

query = """
SELECT "Date", "Amount", "Category"
FROM "Expenses"
LIMIT 5
"""

df = pd.read_sql(query, conn)

print("Columnas del DataFrame:")
print(df.columns.tolist())
print("\nPrimeras filas:")
print(df.head())
print("\nTipos de datos:")
print(df.dtypes)

conn.close()
