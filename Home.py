import streamlit as st
import sqlite3
import bcrypt # Necessário instalar: pip install bcrypt
from database import criar_conexao, inicializar_banco

# Configuração da página principal.
# Esconde o menu de navegação padrão do Streamlit (Pages) quando o usuário não está logado.
st.set_page_config(
    page_title="PsyControl - Login", 
    layout="centered",
    initial_sidebar_state="collapsed" # Colapsa a sidebar
) 
# Estilo CSS para esconder completamente o menu Pages.
# O Streamlit ainda mostra o menu se você não fizer isso.
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {
        display: none
    }
    </style>
""", unsafe_allow_html=True)


inicializar_banco()

# Estado inicial
if "logado" not in st.session_state:
    st.session_state["logado"] = False

def autenticar(usuario, senha):
    conn = criar_conexao()
    cursor = conn.cursor()
    # 1. Busca o usuário e o hash da senha
    cursor.execute("SELECT id, nome, senha FROM psicologos WHERE usuario = ?", (usuario,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        psicologo_id, nome_psicologo, senha_hash = resultado
        # 2. Verifica a senha usando bcrypt
        # ATENÇÃO: Se a senha foi cadastrada antes da criptografia (seu código antigo),
        # esta verificação falhará! Você pode precisar recadastrar seu psicólogo.
        try:
            if bcrypt.checkpw(senha.encode('utf-8'), senha_hash.encode('utf-8')):
                return (psicologo_id, nome_psicologo)
        except ValueError:
             # Trata o caso de senhas antigas não criptografadas.
             # Você PODE querer remover esta linha após migrar todos os usuários.
             st.error("Erro na verificação. Tente recadastrar-se.")
             return None
    
    return None

def tela_login():
    st.title("🔐 Login do Psicólogo")
    
    # O código antigo usava st.sidebar.radio, que mostrava o menu, mas você quer
    # gerenciar isso na tela principal quando não está logado.
    st.markdown("---")
    
    usuario = st.text_input("Usuário")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Entrar", use_container_width=True):
        resultado = autenticar(usuario, senha)
        if resultado:
            st.session_state["logado"] = True
            st.session_state["psicologo_id"] = resultado[0]
            st.session_state["nome_psicologo"] = resultado[1]
            st.success(f"Bem-vindo, {resultado[1]}!")
            
            # **REDIRECIONA CORRETAMENTE** para a página na subpasta 'pages/'
            st.switch_page("pages/painel_psicologo.py")
        else:
            st.error("Usuário ou senha incorretos")

def tela_registro():
    st.title("📝 Cadastro de Psicólogo")
    
    st.markdown("---")
    
    nome = st.text_input("Nome Completo")
    usuario = st.text_input("Usuário desejado")
    senha = st.text_input("Senha", type="password")
    
    if st.button("Registrar", use_container_width=True):
        if nome and usuario and senha:
            try:
                # Criptografa a senha antes de salvar
                senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                conn = criar_conexao()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO psicologos (nome, usuario, senha) VALUES (?, ?, ?)", (nome, usuario, senha_hash))
                conn.commit()
                conn.close()
                st.success("Cadastro realizado com sucesso! Faça login para continuar.")
            except sqlite3.IntegrityError:
                st.error("Usuário já existe. Escolha outro.")
        else:
            st.warning("Preencha todos os campos.")

# -------------------------------------------------------------
# Interface principal
# -------------------------------------------------------------
if st.session_state["logado"]:
    # Se logado, redireciona para o painel (página pages/painel_psicologo.py)
    st.switch_page("pages/painel_psicologo.py")
else:
    # Se não logado, exibe a opção de Login ou Registro (na sidebar)
    menu = st.sidebar.radio("Menu de Acesso", ["Login", "Cadastrar Psicólogo"])
    
    if menu == "Login":
        tela_login()
    else:
        tela_registro()