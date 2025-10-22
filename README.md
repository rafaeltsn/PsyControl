# 🧠 PsyControl: Sistema de Gestão para Clínicas de Psicologia

![Streamlit Logo](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
[![Licença MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)

## ✨ Visão Geral do Projeto

O **PsyControl** é um sistema de gerenciamento de consultórios de psicologia desenvolvido em **Python** utilizando o framework **Streamlit** para a interface web.

O projeto demonstra a capacidade de construir soluções de gestão completas, seguras e com foco em visualização de dados (Data-Driven), utilizando recursos como:

* **Persistência de Dados:** Banco de dados **SQLite** para armazenar informações críticas de forma segura.
* **Autenticação Robusta:** Implementação de login com criptografia de senha (**`bcrypt`**) para segurança.
* **Análise Financeira:** Utilização da biblioteca **Pandas** para processar e visualizar dados de receita, custos e lucro em tempo real.

## 🚀 Funcionalidades Chave (Diferenciais)

Este projeto oferece ao profissional de psicologia um painel completo com foco em otimização de tempo e saúde financeira:

| Categoria | Funcionalidade | Destaque para o Recrutador |
| :--- | :--- | :--- |
| **Clientes** | Cadastro e Listagem de Pacientes | Validação de `Email` e `Telefone` (Regex), e listagem detalhada. |
| **Sessões** | Registro de Sessão e Receita | Registro de **Receita Total** com cálculo baseado em **Valor Unitário** e **Quantidade de Sessões**. |
| **Agenda** | Agendamentos Futuros | Gestão de agenda com visualização e exclusão de compromissos. |
| **Finanças** | Gestão de Custos e Receita | **Dashboard Financeiro** com cálculo de **Receita Total, Custos e Lucro Líquido** em tempo real. |
| **Data Viz** | Análise Gráfica | Gráficos de linha de **Receita vs. Custos por Mês** e **Distribuição de Custos por Categoria** usando Pandas e Streamlit. |

## 🛠️ Tecnologias Utilizadas

| Categoria | Tecnologia | Uso |
| :--- | :--- | :--- |
| **Linguagem** | **Python** | Lógica de *backend* e *frontend* (aplicação Streamlit) |
| **Framework** | **Streamlit** | Interface do usuário (UI) e Componentes interativos |
| **Banco de Dados** | **SQLite3** | Persistência de dados local |
| **Segurança** | **Bcrypt** | Criptografia segura de senhas de usuário |
| **Análise** | **Pandas** | Manipulação e agregação de dados para visualização financeira |
| **Utilidades** | `sqlite3`, `re`, `datetime` | Conexão com o banco, validação de formato de dados |

## ⚙️ Como Executar o Projeto Localmente

Para testar o **PsyControl** em sua máquina, siga os passos abaixo:

### Pré-requisitos
Certifique-se de ter o **Python 3.x** e o **`pip`** instalados.

### Execução

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/rafaeltsn/PsyControl.git](https://github.com/rafaeltsn/PsyControl.git)
    ```

2.  **Entre na pasta do projeto:**
    ```bash
    cd PsyControl
    ```

3.  **Instale as dependências:**
    O projeto depende das bibliotecas `streamlit`, `pandas` e `bcrypt`.
    ```bash
    pip install streamlit pandas bcrypt
    ```

4.  **Inicialize o Streamlit:**
    O Streamlit usará o arquivo `Home.py` como ponto de entrada.

    ```bash
    streamlit run Home.py
    ```

5.  **Acesse e Cadastre-se:**
    O aplicativo abrirá no seu navegador, geralmente em `http://localhost:8501`. Na primeira tela, use a opção **"Cadastrar Psicólogo"** na barra lateral para criar sua conta de acesso.

## 🧑‍💻 Desenvolvedor

| [**Rafael S.N.**](https://www.linkedin.com/in/rafanasc/) |
| :--- |
| **Foco:** Desenvolvimento Python, Streamlit, Análise de Dados |
| [![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/SEULINKEDIN) |
| [![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/rafaeltsn) |


