import sqlite3

def criar_conexao():
    # Permite acesso de threads diferentes, essencial para o Streamlit
    return sqlite3.connect("psycontrol.db", check_same_thread=False)

def inicializar_banco():
    conn = criar_conexao()
    cursor = conn.cursor()

    # 1. Tabela Psicologos (Sem alteração)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS psicologos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        usuario TEXT UNIQUE NOT NULL,
        senha TEXT NOT NULL
    );
    """)

    # 2. Tabela Pacientes (Inclui a coluna carteirinha)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pacientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        psicologo_id INTEGER NOT NULL,
        nome TEXT NOT NULL,
        telefone TEXT,
        email TEXT,
        observacoes TEXT,
        foto_path TEXT,
        carteirinha TEXT,
        FOREIGN KEY (psicologo_id) REFERENCES psicologos(id)
    );
    """)

    # 3. Tabela Sessoes (ATUALIZADA: Adicionado a coluna 'valor' REAL)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL,
        tipo_receita TEXT, -- NOVA COLUNA
        qtd_sessoes INTEGER, -- NOVA COLUNA
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
    );
    """)
    
    # *** ATENÇÃO: MIGRAÇÃO DE COLUNAS EXISTENTES ***
    # Se você já usou o app, estas linhas SÃO NECESSÁRIAS para adicionar as novas colunas
    try:
        cursor.execute("ALTER TABLE sessoes ADD COLUMN valor REAL")
    except sqlite3.OperationalError:
        pass # Coluna já existe
        
    try:
        cursor.execute("ALTER TABLE sessoes ADD COLUMN tipo_receita TEXT") # MIGRAÇÃO
    except sqlite3.OperationalError:
        pass # Coluna já existe

    try:
        cursor.execute("ALTER TABLE sessoes ADD COLUMN qtd_sessoes INTEGER") # MIGRAÇÃO
    except sqlite3.OperationalError:
        pass # Coluna já existe
    # **********************************************

# ... (o resto do código do database.py)

    # 4. Tabela Agendamentos (Sem alteração)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS agendamentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        paciente_id INTEGER NOT NULL,
        data TEXT NOT NULL,
        hora TEXT NOT NULL,
        observacoes TEXT,
        FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE CASCADE
    );
    """)
    
    # 5. Tabela de Custos (Sem alteração)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS custos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        psicologo_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        valor REAL NOT NULL,
        data TEXT NOT NULL,
        categoria TEXT NOT NULL,
        FOREIGN KEY (psicologo_id) REFERENCES psicologos(id) ON DELETE CASCADE
    );
    """)

    conn.commit()
    conn.close()