import streamlit as st
import sqlite3
import os
import re # Para validação de email/telefone
import pandas as pd # Necessário instalar: pip install pandas
from datetime import datetime
from database import criar_conexao

st.set_page_config(page_title="Painel do Psicólogo", page_icon="🧠", layout="wide")

# Verifica se está logado e, se não, redireciona.
if "logado" not in st.session_state or not st.session_state["logado"]:
    # st.warning("Acesso restrito. Por favor, faça login primeiro.")
    st.switch_page("Home.py") # Redireciona para o Home.py se não estiver logado
    st.stop()


# Variáveis de sessão do Psicólogo
PSICOLOGO_ID = st.session_state['psicologo_id']
NOME_PSICOLOGO = st.session_state['nome_psicologo']

#st.title(f"👋 Bem-vindo(a), Dr(a). {NOME_PSICOLOGO}")

# ----------------------------------------------
# 1. FUNÇÕES AUXILIARES DE VALIDAÇÃO E DB
# ----------------------------------------------

def validar_email(email):
    # Regex simples para validar formato de email
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validar_telefone(telefone):
    # Regex para validar telefone com 10 ou 11 dígitos, aceitando ( ) - e espaços
    telefone_limpo = re.sub(r'\D', '', telefone)
    return len(telefone_limpo) >= 10 and len(telefone_limpo) <= 11

def get_pacientes():
    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome FROM pacientes WHERE psicologo_id = ?", (PSICOLOGO_ID,))
    pacientes = cursor.fetchall()
    conn.close()
    return {id: nome for id, nome in pacientes}

# ----------------------------------------------
# 2. FUNCIONALIDADES DO PAINEL
# ----------------------------------------------

def cadastrar_paciente():
    st.subheader("📝 Cadastrar Novo Paciente")
    
    # Campo para a foto removido temporariamente para simplificar o refactoring e evitar erros de permissão de I/O em alguns ambientes.
    # Caso queira reativar, inclua um bloco para salvar o arquivo no disco.

    with st.form("form_paciente"):
        col1, col2 = st.columns(2)
        with col1:
            nome = st.text_input("Nome Completo*")
            telefone = st.text_input("Telefone*")
            carteirinha = st.text_input("Número da Carteirinha (até 20 dígitos)", max_chars=20)
        with col2:
            email = st.text_input("Email*")
            # foto = st.file_uploader("Foto (opcional)", type=["png", "jpg", "jpeg"]) # Removido
        
        observacoes = st.text_area("Observações Iniciais")

        if st.form_submit_button("💾 Salvar Cadastro", use_container_width=True):
            if not nome or not telefone or not email:
                st.error("Preencha todos os campos obrigatórios (*).")
                return
            
            if not validar_email(email):
                st.error("Email inválido.")
                return
            
            if not validar_telefone(telefone):
                st.error("Telefone inválido. Use 10 ou 11 dígitos.")
                return

            foto_path = ""
            # Código para salvar foto foi omitido, use 'foto_path = None'

            try:
                conn = criar_conexao()
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO pacientes (psicologo_id, nome, telefone, email, observacoes, foto_path, carteirinha) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (PSICOLOGO_ID, nome, telefone, email, observacoes, foto_path, carteirinha)
                )
                conn.commit()
                conn.close()
                st.success(f"Paciente **{nome}** cadastrado com sucesso!")
            except Exception as e:
                st.error(f"Erro ao salvar: {e}")

# ... (O restante da função listar_pacientes)
def listar_pacientes():
    st.subheader("👥 Listagem de Pacientes")

    conn = criar_conexao()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nome, telefone, email, observacoes, carteirinha FROM pacientes WHERE psicologo_id = ?", (PSICOLOGO_ID,))
    pacientes = cursor.fetchall()
    conn.close()

    if not pacientes:
        st.info("Nenhum paciente cadastrado.")
        return

    st.markdown(f"**Total de pacientes:** **{len(pacientes)}**")
    
    # Prepara um dicionário para facilitar o mapeamento
    pacientes_map = {id: {'nome': nome, 'tel': tel, 'email': email, 'obs': obs, 'cart': cart} 
                     for id, nome, tel, email, obs, cart in pacientes}

    # ----------------------------------------------------
    # Layout de Listagem com Expander para detalhes
    # ----------------------------------------------------
    
    st.markdown("---")

    for id_pac, dados in pacientes_map.items():
        # Usa um container para delimitar cada paciente na lista
        with st.container(border=True):
            col_info, col_acao = st.columns([5, 1])

            # Coluna de Informações (Nome, Telefone, Email)
            with col_info:
                st.markdown(f"**👤 {dados['nome']}** (ID: {id_pac})")
                st.caption(f"📞 {dados['tel']} | 📧 {dados['email']}")
                
                # Expansor para detalhes e observações
                with st.expander("Detalhes e Observações"):
                    st.write(f"**Carteirinha:** {dados['cart'] if dados['cart'] else 'N/A'}")
                    st.write("**Observações Iniciais:**")
                    st.markdown(dados['obs'] if dados['obs'] else "_Nenhuma observação inicial._")

            # Coluna de Ações (Exclusão)
            with col_acao:
                st.write("") # Espaçamento
                if st.button("🗑️ Excluir", key=f"excluir_{id_pac}", use_container_width=True, type="secondary"):
                    
                    # Confirmação antes de excluir
                    if st.session_state.get(f"confirm_excluir_{id_pac}"):
                        conn = criar_conexao()
                        cursor = conn.cursor()
                        # O ON DELETE CASCADE cuida de sessões e agendamentos
                        cursor.execute("DELETE FROM pacientes WHERE id = ?", (id_pac,))
                        conn.commit()
                        conn.close()
                        st.success(f"Paciente **{dados['nome']}** e todos os seus dados excluídos.")
                        st.experimental_rerun()
                    else:
                        st.warning("Clique novamente para confirmar a exclusão TOTAL dos dados do paciente.")
                        st.session_state[f"confirm_excluir_{id_pac}"] = True
                        st.experimental_rerun()
# Substitua a função cadastrar_sessao() COMPLETA

# Substitua a função cadastrar_sessao() COMPLETA

def cadastrar_sessao():
    st.subheader("✍️ Registrar Nova Sessão")
    pacientes_dict = get_pacientes()

    if not pacientes_dict:
        st.warning("Cadastre um paciente primeiro para registrar uma sessão.")
        return
        
    paciente_selecionado = st.selectbox("Paciente*", [""] + list(pacientes_dict.values()))
    
    if paciente_selecionado:
        paciente_id = list(pacientes_dict.keys())[list(pacientes_dict.values()).index(paciente_selecionado)]
        
        # LINHA 1: Data e Tipo de Receita
        col_data, col_tipo_receita = st.columns(2)
        with col_data:
            data_sessao = st.date_input("Data da Sessão*", max_value=datetime.today().date())
        with col_tipo_receita:
            # NOVO CAMPO 1: Classificação da Receita
            tipo_receita = st.selectbox(
                "Tipo de Receita*", 
                ["Particular", "Convênio - Plano A", "Convênio - Plano B", "Outros"]
            )
            
        # LINHA 2: Valor Unitário e Quantidade de Sessões
        col_valor_unitario, col_quantidade = st.columns(2)
        with col_valor_unitario:
            # NOVO CAMPO 2: Valor Unitário (será multiplicado)
            valor_unitario = st.number_input("Valor Unitário (R$)*", min_value=0.00, format="%.2f", step=10.00) 
        with col_quantidade:
            # NOVO CAMPO 3: Quantidade de Sessões
            qtd_sessoes = st.number_input("Qtd. de Sessões (paga agora)*", min_value=1, step=1)
            
        # CÁLCULO DA RECEITA TOTAL
        valor_total_recebido = valor_unitario * qtd_sessoes
        
        # Exibe o total calculado de forma clara
        st.info(f"💰 **Receita Total Registrada:** **R$ {valor_total_recebido:,.2f}** ({qtd_sessoes} x R$ {valor_unitario:,.2f})".replace(",", "X").replace(".", ",").replace("X", "."))
        
        descricao = st.text_area("Descrição/Notas da Sessão*", height=250)

        if st.button("Salvar Sessão e Receita", use_container_width=True, type="primary"):
            if descricao and valor_unitario >= 0 and qtd_sessoes >= 1:
                conn = None
                try:
                    conn = criar_conexao()
                    cursor = conn.cursor()
                    data_str = data_sessao.strftime("%Y-%m-%d")
                    
                    # Salva a RECEITA TOTAL CALCULADA no campo 'valor' da tabela sessoes
                    cursor.execute(
                        "INSERT INTO sessoes (paciente_id, data, descricao, valor, tipo_receita, qtd_sessoes) VALUES (?, ?, ?, ?, ?, ?)",
                        (paciente_id, data_str, descricao, valor_total_recebido, tipo_receita, qtd_sessoes)
                    )
                    conn.commit()
                    st.success(f"Receita de R$ {valor_total_recebido:.2f} registrada! Tipo: {tipo_receita}.")
                    st.rerun() # <--- CORREÇÃO APLICADA AQUI
                except sqlite3.OperationalError as e:
                    # Este erro ocorrerá se as colunas 'tipo_receita' e 'qtd_sessoes' não existirem
                    if "no such column" in str(e):
                        st.error("ERRO CRÍTICO: As colunas 'tipo_receita' e 'qtd_sessoes' não foram adicionadas à tabela 'sessoes'. Por favor, execute a migração manual (Passo 2).")
                    else:
                        st.error(f"Erro ao salvar a sessão: {e}")
                except Exception as e:
                    st.error(f"Erro ao salvar a sessão: {e}")
                finally:
                    if conn:
                        conn.close()
            else:
                st.error("Preencha a descrição, o valor unitário e a quantidade de sessões.")

# Certifique-se de que get_pacientes() está definida e retorna {id: nome}

# Substitua a função listar_sessoes() COMPLETA

def listar_sessoes():
    st.subheader("📚 Histórico de Sessões e Receita")
    
    # 1. Busca Segura dos Dados
    conn = None
    df_sessoes = pd.DataFrame()
    
    try:
        conn = criar_conexao()
        df_sessoes = pd.read_sql_query(
            """
            SELECT 
                s.id, s.data, s.descricao, s.valor, s.tipo_receita, s.qtd_sessoes, 
                p.nome as paciente_nome, s.paciente_id 
            FROM sessoes s
            JOIN pacientes p ON s.paciente_id = p.id
            WHERE p.psicologo_id = ? 
            ORDER BY s.data DESC
            """, 
            conn, 
            params=(PSICOLOGO_ID,)
        )
    except Exception as e:
        st.error(f"Erro ao carregar histórico de sessões. Detalhe: {e}")
        return
    finally:
        if conn:
            conn.close()

    if df_sessoes.empty:
        st.info("Nenhuma sessão registrada. Use a aba 'Registrar Sessão' para começar.")
        return

    # ----------------------------------------------------
    # 2. FILTROS NA BARRA LATERAL (UX PROFISSIONAL)
    # ----------------------------------------------------
    st.sidebar.markdown("### 🔎 Filtros do Histórico")

    # Filtro por Paciente
    pacientes_list = df_sessoes['paciente_nome'].unique().tolist()
    paciente_filter = st.sidebar.selectbox("Filtrar por Paciente", ["Todos"] + sorted(pacientes_list))

    # Filtro por Tipo de Receita
    tipos_receita_list = df_sessoes['tipo_receita'].unique().tolist()
    
    # *** CORREÇÃO AQUI: Removemos os valores None antes de ordenar ***
    tipos_receita_validos = [t for t in tipos_receita_list if t is not None]
    tipo_receita_filter = st.sidebar.selectbox("Filtrar por Tipo de Receita", ["Todos"] + sorted(tipos_receita_validos))
    
    # Filtro de Data
    col_start, col_end = st.sidebar.columns(2)
    with col_start:
        data_min = datetime.strptime(df_sessoes['data'].min(), "%Y-%m-%d").date()
        data_inicio_filter = st.date_input("De", value=data_min, min_value=data_min)
    with col_end:
        data_fim_filter = st.date_input("Até", value=datetime.today().date(), max_value=datetime.today().date())


    # Aplicar os Filtros
    df_filtrado = df_sessoes.copy()
    
    if paciente_filter != "Todos":
        df_filtrado = df_filtrado[df_filtrado['paciente_nome'] == paciente_filter]
        
    if tipo_receita_filter != "Todos":
        # Se o tipo de receita for None para registros antigos, eles serão ignorados pelo filtro.
        df_filtrado = df_filtrado[df_filtrado['tipo_receita'] == tipo_receita_filter]
        
    # Filtro de Data
    df_filtrado['data_dt'] = pd.to_datetime(df_filtrado['data'])
    df_filtrado = df_filtrado[
        (df_filtrado['data_dt'].dt.date >= data_inicio_filter) & 
        (df_filtrado['data_dt'].dt.date <= data_fim_filter)
    ]
    
    # ----------------------------------------------------
    # 3. EXIBIÇÃO E AÇÕES
    # ----------------------------------------------------
    st.markdown(f"**Sessões Encontradas:** **{len(df_filtrado)}**")
    
    if df_filtrado.empty:
        st.warning("Nenhuma sessão corresponde aos filtros selecionados.")
        return

    st.markdown("---")
    
    for _, row in df_filtrado.iterrows():
        id_sessao = row['id']
        data_exibicao = datetime.strptime(row['data'], "%Y-%m-%d").strftime("%d/%m/%Y")
        
        # Cria um container por sessão para melhor visualização
        with st.container(border=True):
            col_info, col_valor, col_acao = st.columns([3, 2, 1])
            
            # Coluna de Informações Principais
            with col_info:
                st.markdown(f"**📅 {data_exibicao}** | **👤 {row['paciente_nome']}**")
                # Usa 'N/A' se o campo tipo_receita for None em registros antigos
                tipo_receita_exibicao = row['tipo_receita'] if row['tipo_receita'] else "N/A (Antigo)"
                qtd_sessoes_exibicao = int(row['qtd_sessoes']) if row['qtd_sessoes'] else 1
                st.caption(f"Tipo: {tipo_receita_exibicao} | Qtd: {qtd_sessoes_exibicao}")
            
            # Coluna de Valor/Receita
            with col_valor:
                # Formatação de moeda
                valor_formatado = f"R$ {row['valor']:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                st.markdown(f"**💰 Receita:** **{valor_formatado}**")
            
            # Coluna de Ações
            with col_acao:
                # Chave Única garantida com 'sessao_excluir_'
                if st.button("🗑️ Excluir", key=f"sessao_excluir_{id_sessao}", use_container_width=True, type="secondary"):
                    
                    conn_del = None
                    try:
                        conn_del = criar_conexao()
                        cursor_del = conn_del.cursor()
                        cursor_del.execute("DELETE FROM sessoes WHERE id = ?", (id_sessao,))
                        conn_del.commit()
                        st.success(f"Sessão de {data_exibicao} excluída.")
                        st.rerun() 
                    except Exception as e:
                        st.error(f"Erro ao excluir: {e}")
                    finally:
                        if conn_del:
                            conn_del.close()
            
            # Expansor para a descrição
            with st.expander("Ver Notas da Sessão"):
                st.markdown(row['descricao'])

# ----------------------------------------------
# 3. FUNCIONALIDADES DE AGENDAMENTO (NOVA)
# ----------------------------------------------

def cadastrar_agendamento():
    st.subheader("📅 Agendar Sessão")
    pacientes_dict = get_pacientes()
    
    if not pacientes_dict:
        st.warning("Cadastre um paciente primeiro para agendar uma sessão.")
        return

    with st.form("form_agendamento"):
        paciente_selecionado = st.selectbox("Paciente*", [""] + list(pacientes_dict.values()))
        
        col_data, col_hora = st.columns(2)
        with col_data:
            data_agendamento = st.date_input("Data do Agendamento*", min_value=datetime.today().date())
        with col_hora:
            hora_agendamento = st.time_input("Hora do Agendamento*", value=datetime.now().time())
        
        observacoes = st.text_area("Observações do Agendamento")

        if st.form_submit_button("Agendar", use_container_width=True):
            if paciente_selecionado:
                paciente_id = list(pacientes_dict.keys())[list(pacientes_dict.values()).index(paciente_selecionado)]
                
                try:
                    conn = criar_conexao()
                    cursor = conn.cursor()
                    # Formato da data YYYY-MM-DD
                    data_str = data_agendamento.strftime("%Y-%m-%d")
                    hora_str = hora_agendamento.strftime("%H:%M")
                    
                    cursor.execute(
                        "INSERT INTO agendamentos (paciente_id, data, hora, observacoes) VALUES (?, ?, ?, ?)",
                        (paciente_id, data_str, hora_str, observacoes)
                    )
                    conn.commit()
                    conn.close()
                    st.success(f"Sessão agendada com sucesso para **{paciente_selecionado}** em {data_agendamento.strftime('%d/%m/%Y')} às {hora_str}.")
                except Exception as e:
                    st.error(f"Erro ao agendar: {e}")
            else:
                st.error("Selecione um paciente.")

# Substitua esta função COMPLETA em pages/painel_psicologo.py

def listar_agendamentos():
    st.subheader("🗓️ Próximos Agendamentos")

    # Inicializa conn e agendamentos fora do bloco try para garantir escopo e valores padrão
    conn = None 
    agendamentos = [] 

    try:
        conn = criar_conexao()
        cursor = conn.cursor()
        
        # Busca agendamentos do psicólogo, com o nome do paciente, ordenado por data e hora
        cursor.execute("""
            SELECT a.id, p.nome, a.data, a.hora, a.observacoes, a.paciente_id
            FROM agendamentos a
            JOIN pacientes p ON a.paciente_id = p.id
            WHERE p.psicologo_id = ? AND a.data >= date('now', 'localtime')
            ORDER BY a.data ASC, a.hora ASC
        """, (PSICOLOGO_ID,))
        agendamentos = cursor.fetchall()
        
    except Exception as e:
        # Exibe um erro amigável caso haja problemas de conexão ou SQL
        st.error(f"Erro ao carregar agendamentos do banco de dados. Tente novamente. Detalhe: {e}")
        return # Sai da função em caso de erro

    finally:
        # ESSENCIAL: Garante que a conexão seja fechada, mesmo se houver erro
        if conn:
            conn.close() 

    if not agendamentos:
        st.info("Nenhum agendamento futuro encontrado.")
        return

    # Usar um container para a lista
    st.markdown(f"**Total de Agendamentos Futuros:** **{len(agendamentos)}**")
    st.markdown("---")
    
    # O loop de exibição permanece o mesmo, usando as variáveis corretamente
    for id_agend, nome_paciente, data_str, hora_str, obs, paciente_id in agendamentos:
        # Formata a data para exibição
        data_exibicao = datetime.strptime(data_str, "%Y-%m-%d").strftime("%d/%m/%Y")
        
        with st.container(border=True):
            col_info, col_acao = st.columns([4, 2])
            
            with col_info:
                st.markdown(f"**👤 Paciente:** {nome_paciente}")
                st.markdown(f"**⏰ Data e Hora:** **{data_exibicao}** às **{hora_str}**")
                
                with st.expander("Observações do Agendamento"):
                    st.markdown(obs if obs else "_Nenhuma observação._")

            with col_acao:
                st.write("") # Espaçamento para alinhar o botão
                # Botão Excluir - Usa sua própria conexão segura
                if st.button("❌ Excluir", key=f"excluir_agend_{id_agend}", use_container_width=True, type="secondary"):
                    
                    conn_del = None
                    try:
                        conn_del = criar_conexao()
                        cursor_del = conn_del.cursor()
                        cursor_del.execute("DELETE FROM agendamentos WHERE id = ?", (id_agend,))
                        conn_del.commit()
                        st.success(f"Agendamento com {nome_paciente} excluído.")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Erro ao excluir: {e}")
                    finally:
                        if conn_del:
                            conn_del.close()

# ----------------------------------------------
# 4. GESTÃO DE CUSTOS/FINANCEIRO (NOVA E MELHORADA)
# ----------------------------------------------

# Substitua a função get_dados_financeiros()
def get_dados_financeiros():
    """Busca todos os custos e receita do psicólogo de forma segura."""
    conn = None
    df_custos = pd.DataFrame()
    df_receita = pd.DataFrame()
    
    try:
        conn = criar_conexao()
        
        # 1. Busca Custos
        df_custos = pd.read_sql_query(
            "SELECT * FROM custos WHERE psicologo_id = ? ORDER BY data DESC", 
            conn, 
            params=(PSICOLOGO_ID,)
        )
        
        # 2. Busca Receita (Sessões)
        # Junta com o nome do paciente para possível análise futura
        df_receita = pd.read_sql_query(
            """
            SELECT s.data, s.valor, p.nome as paciente_nome
            FROM sessoes s
            JOIN pacientes p ON s.paciente_id = p.id
            WHERE p.psicologo_id = ? AND s.valor IS NOT NULL
            """, 
            conn, 
            params=(PSICOLOGO_ID,)
        )
        
    except Exception as e:
        st.error(f"Erro ao carregar dados financeiros: {e}")
        df_custos = pd.DataFrame()
        df_receita = pd.DataFrame()
    finally:
        if conn:
            conn.close()
    
    return df_custos, df_receita


# Substitua a função gestao_custos()
def gestao_custos():
    st.subheader("💵 Visão Financeira Completa")

    # ----------------------------------------------------
    # 1. VISUALIZAÇÃO DE KPIs (RECEITA, CUSTO E LUCRO)
    # ----------------------------------------------------
    df_custos, df_receita = get_dados_financeiros()
    
    total_custos = df_custos['valor'].sum() if not df_custos.empty else 0.0
    total_receita = df_receita['valor'].sum() if not df_receita.empty else 0.0
    lucro = total_receita - total_custos
    
    # Função auxiliar para formatar em moeda brasileira
    def formatar_moeda(valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    col_receita, col_custo, col_lucro = st.columns(3)
    
    # Cartão 1: Receita
    with col_receita:
        st.metric(
            label="RECEITA TOTAL (Sessões)", 
            value=formatar_moeda(total_receita),
            delta=f"Último mês: +R$ 0,00", # Placeholder para futura análise de delta
            delta_color="normal"
        )

    # Cartão 2: Custos
    with col_custo:
        st.metric(
            label="CUSTOS TOTAIS", 
            value=formatar_moeda(total_custos),
            delta_color="inverse" # Usa cor inversa para indicar que é uma saída
        )

    # Cartão 3: Lucro
    with col_lucro:
        st.metric(
            label="LUCRO LÍQUIDO", 
            value=formatar_moeda(lucro),
            delta=f"{(lucro / total_receita * 100):.1f}% de Margem" if total_receita > 0 else "Sem Receita",
            delta_color="normal" if lucro >= 0 else "inverse"
        )
    
    st.markdown("---")
    
    col_add, col_cat = st.columns([1, 1])
    
    # ----------------------------------------------------
    # 2. ADICIONAR NOVA DESPESA (Permanece no lado esquerdo)
    # ----------------------------------------------------
    with col_add:
        st.markdown("##### ➕ Registrar Nova Despesa")
        with st.form("form_custo"):
            data_custo = st.date_input("Data da Despesa*", max_value=datetime.today().date())
            descricao = st.text_input("Descrição (Ex: Aluguel de Sala, Licença Software)")
            valor = st.number_input("Valor (R$)*", min_value=0.01, format="%.2f", step=5.00) 
            
            categorias = ["Aluguel", "Material de Escritório", "Software/Licenças", "Treinamento/Cursos", "Marketing", "Outros"]
            categoria = st.selectbox("Categoria", categorias)

            if st.form_submit_button("💾 Salvar Despesa", use_container_width=True):
                if descricao and valor:
                    conn = None
                    try:
                        conn = criar_conexao()
                        cursor = conn.cursor()
                        data_str = data_custo.strftime("%Y-%m-%d")
                        cursor.execute(
                            "INSERT INTO custos (psicologo_id, descricao, valor, data, categoria) VALUES (?, ?, ?, ?, ?)",
                            (PSICOLOGO_ID, descricao, valor, data_str, categoria)
                        )
                        conn.commit()
                        st.success(f"Despesa de R$ {valor:.2f} salva com sucesso!")
                        st.experimental_rerun()
                    except Exception as e:
                        st.error(f"Erro ao salvar despesa: {e}")
                    finally:
                        if conn:
                            conn.close()
                else:
                    st.error("Preencha a descrição e o valor.")
    
    # ----------------------------------------------------
    # 3. ANÁLISE GRÁFICA E TABELA
    # ----------------------------------------------------
    with col_cat:
        visualizar_custos(df_custos, df_receita)
    

# Substitua a função visualizar_custos()
def visualizar_custos(df_custos, df_receita):
    st.markdown("##### 📈 Análise Gráfica Detalhada")

    if df_custos.empty and df_receita.empty:
        st.info("Sem dados para análise. Registre receitas (sessões) e despesas (custos).")
        return

    # Gráfico de Receita vs Custo por Mês
    st.markdown("###### Receita e Custos ao Longo do Tempo")
    
    # Prepara dados de custo por mês
    if not df_custos.empty:
        df_custos['Ano/Mês'] = df_custos['data'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%Y-%m"))
        custos_por_mes = df_custos.groupby('Ano/Mês')['valor'].sum().reset_index().rename(columns={'valor': 'Custos'})
    else:
        custos_por_mes = pd.DataFrame({'Ano/Mês': [], 'Custos': []})
        
    # Prepara dados de receita por mês
    if not df_receita.empty:
        df_receita['Ano/Mês'] = df_receita['data'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%Y-%m"))
        receita_por_mes = df_receita.groupby('Ano/Mês')['valor'].sum().reset_index().rename(columns={'valor': 'Receita'})
    else:
        receita_por_mes = pd.DataFrame({'Ano/Mês': [], 'Receita': []})
        
    # Combina os dois dataframes
    df_mensal = pd.merge(custos_por_mes, receita_por_mes, on='Ano/Mês', how='outer').fillna(0)
    df_mensal = df_mensal.sort_values('Ano/Mês').set_index('Ano/Mês')
    
    st.line_chart(df_mensal[['Receita', 'Custos']])

    # 1. Gráfico de Distribuição de Custos por Categoria
    st.markdown("###### Distribuição de Custos por Categoria")
    if not df_custos.empty:
        custos_por_categoria = df_custos.groupby('categoria')['valor'].sum().sort_values(ascending=False).reset_index()
        st.bar_chart(custos_por_categoria.set_index('categoria'))
    else:
        st.info("Nenhum custo registrado para análise de categoria.")


    st.markdown("---")
    st.markdown("###### Histórico de Transações")
    
    # Tabela de Histórico de Custos
    if not df_custos.empty:
        st.markdown("**Despesas (Custos)**")
        df_custos_table = df_custos[['data', 'descricao', 'categoria', 'valor']].copy()
        df_custos_table.columns = ['Data', 'Descrição', 'Categoria', 'Valor (R$)']
        df_custos_table['Valor (R$)'] = df_custos_table['Valor (R$)'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_custos_table['Data'] = df_custos_table['Data'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%d/%m/%Y"))
        st.dataframe(df_custos_table, use_container_width=True, hide_index=True)

    # Tabela de Histórico de Receitas
    if not df_receita.empty:
        st.markdown("**Receitas (Sessões)**")
        df_receita_table = df_receita[['data', 'paciente_nome', 'valor']].copy()
        df_receita_table.columns = ['Data', 'Paciente', 'Valor (R$)']
        df_receita_table['Valor (R$)'] = df_receita_table['Valor (R$)'].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        df_receita_table['Data'] = df_receita_table['Data'].apply(lambda x: datetime.strptime(x, "%Y-%m-%d").strftime("%d/%m/%Y"))
        st.dataframe(df_receita_table, use_container_width=True, hide_index=True)

# Lembre-se de adicionar 'from datetime import datetime' e 'import pandas as pd' no topo do arquivo se já não estiverem!
# ... (todas as funções)

# ----------------------------------------------
# 5. INTERFACE PRINCIPAL
# ----------------------------------------------

# ----------------------------------------------
# 5. INTERFACE PRINCIPAL
# ----------------------------------------------

# Movendo o título para um container de cabeçalho
with st.container():
    col_titulo, col_sair = st.columns([5, 1])
    with col_titulo:
        # UNIFICADO: O título principal agora contém a saudação e o nome
        st.title(f"👋 Painel de Gestão: Dr(a). {st.session_state['nome_psicologo']}")
        # st.subheader(f"Dr(a). {NOME_PSICOLOGO}") # REMOVA esta subheader se já usou a linha acima
    with col_sair:
        st.markdown("<br>", unsafe_allow_html=True) # Espaço para alinhar
        if st.button("🔒 Sair", type="primary", use_container_width=True):
            st.session_state["logado"] = False
            st.session_state["psicologo_id"] = None
            st.session_state["nome_psicologo"] = None
            st.switch_page("Home.py")

st.markdown("---") # Divisor visual

# ... (o resto do código com as abas)

st.markdown("---") # Divisor visual

# Otimização da Interface com abas
abas = st.tabs([
    "Cadastrar Paciente", 
    "Pacientes & Detalhes", 
    "Agendamentos",
    "Registrar Sessão", 
    "Histórico de Sessões", 
    "Gestão Financeira"
])

# Remanejando as funções nas abas para melhor fluxo (Cadastro -> Lista -> Agendamento -> Sessão)

with abas[0]:
    cadastrar_paciente()

with abas[1]:
    listar_pacientes()

with abas[2]:
    cadastrar_agendamento()
    st.markdown("---")
    listar_agendamentos()

with abas[3]:
    cadastrar_sessao()

with abas[4]:
    listar_sessoes()

with abas[5]:
    gestao_custos()


# Botão de Sair no final da página
st.markdown("---")
if st.button("🔒 Sair do Painel", type="primary"):
    st.session_state["logado"] = False
    st.session_state["psicologo_id"] = None
    st.session_state["nome_psicologo"] = None
    st.switch_page("Home.py")