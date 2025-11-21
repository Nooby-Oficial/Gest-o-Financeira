import psycopg2

conn = psycopg2.connect(
    'postgresql://postgres.pseyjjtoufvhboqnsnsw:4*a26y#W.z.Nx+9@aws-0-us-west-2.pooler.supabase.com:6543/postgres'
)
c = conn.cursor()

# Atualizar despesas existentes sem value_type
c.execute("""
    UPDATE expenses 
    SET value_type = 'total' 
    WHERE value_type IS NULL
""")

rows_updated = c.rowcount
conn.commit()
conn.close()

print(f"✅ {rows_updated} despesas atualizadas com value_type = 'total'")
print("Agora todas as despesas parceladas aparecerão como 'Parcelado por Mês'")
