import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    'postgresql://postgres.pseyjjtoufvhboqnsnsw:4*a26y#W.z.Nx+9@aws-0-us-west-2.pooler.supabase.com:6543/postgres',
    cursor_factory=RealDictCursor
)
c = conn.cursor()
c.execute('SELECT id, description, installments, value_type FROM expenses ORDER BY id DESC LIMIT 5')
rows = c.fetchall()

print('ID | Descrição | Parcelas | Tipo de Valor')
print('-' * 60)
for row in rows:
    print(f"{row['id']} | {row['description']} | {row['installments']} | {row['value_type']}")

conn.close()
