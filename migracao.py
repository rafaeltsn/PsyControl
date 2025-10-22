import sqlite3

# Conectar ao banco de dados
conn = sqlite3.connect("psycontrol.db")
cursor = conn.cursor()

# Adicionar coluna 'carteirinha' se ainda não existir
try:
    cursor.execute("ALTER TABLE pacientes ADD COLUMN carteirinha TEXT")
    print("Coluna 'carteirinha' adicionada com sucesso.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("A coluna 'carteirinha' já existe.")
    else:
        raise

conn.commit()
conn.close()
