import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from string import Template
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

# Configuração da página
st.set_page_config(
    page_title="Sistema de Avaliação e PDI",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Ajuste de cores para Light/Dark do Streamlit
_theme_base = st.get_option("theme.base") or "dark"
_header_bg = "linear-gradient(135deg, #FFFFFF 0%, #1a1a1a 100%)" if _theme_base == "dark" else "linear-gradient(135deg, #000000 0%, #F5F5F5 100%)"
_header_text = "#FFFFFF" if _theme_base == "dark" else "#000000"
_header_subtext = "#FFFFFF" if _theme_base == "dark" else "#4c4c4c"
_text_primary = "#BBBBBB" if _theme_base == "dark" else "#000000"
_text_secondary = "#BDBDBD" if _theme_base == "dark" else "#4c4c4c"

# Configuração do Google Sheets
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Função para conectar ao Google Sheets
@st.cache_resource
def conectar_google_sheets():
    """Conecta ao Google Sheets usando credenciais do Streamlit Secrets"""
    try:
        # Tenta carregar credenciais do Streamlit Secrets (para Streamlit Cloud)
        if "gcp_service_account" in st.secrets:
            credentials_dict = dict(st.secrets["gcp_service_account"])
            credentials = Credentials.from_service_account_info(
                credentials_dict,
                scopes=SCOPES
            )
        # Fallback para arquivo local (desenvolvimento)
        elif os.path.exists("service_account.json"):
            credentials = Credentials.from_service_account_file(
                "service_account.json",
                scopes=SCOPES
            )
        else:
            st.error("Credenciais do Google não encontradas!")
            st.info("Configure as credenciais em .streamlit/secrets.toml ou service_account.json")
            st.stop()
        
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"Erro ao conectar ao Google Sheets: {str(e)}")
        st.stop()

# Função para obter ou criar planilha
@st.cache_resource
def obter_planilha():
    """Obtém ou cria a planilha de avaliações"""
    client = conectar_google_sheets()
    
    # Nome da planilha (pode ser configurado)
    sheet_name = st.secrets.get("sheet_name", "Avaliações PDI - SATTE ALAM")
    
    try:
        # Tenta abrir planilha existente
        spreadsheet = client.open(sheet_name)
        st.success(f"Conectado à planilha: {sheet_name}")
    except gspread.exceptions.SpreadsheetNotFound:
        # Cria nova planilha se não existir
        spreadsheet = client.create(sheet_name)
        st.success(f"Nova planilha criada: {sheet_name}")
    
    # Obtém ou cria a primeira aba
    headers = [
        "ID", "Nome", "Avaliador", "Data", "Scores_JSON", "Observacoes_JSON",
        "Opiniao", "Total_Pontos", "Classificacao", "Pontos_Fortes_JSON",
        "Gargalos_JSON", "Acoes_Melhoria_JSON", "Timestamp"
    ]

    try:
        worksheet = spreadsheet.worksheet("Avaliações")
        current_headers = worksheet.row_values(1)
        if "Opiniao" not in current_headers:
            worksheet.update('A1:M1', [headers])
    except:
        worksheet = spreadsheet.add_worksheet(title="Avaliações", rows=1000, cols=20)
        # Adiciona cabeçalhos
        worksheet.update('A1:M1', [headers])
    
    return worksheet

# Função para obter ou criar planilha de feedbacks
@st.cache_resource
def obter_planilha_feedbacks():
    """Obtém ou cria a planilha de feedbacks"""
    client = conectar_google_sheets()
    sheet_name = st.secrets.get("sheet_name", "Avaliações PDI - SATTE ALAM")

    try:
        spreadsheet = client.open(sheet_name)
    except gspread.exceptions.SpreadsheetNotFound:
        spreadsheet = client.create(sheet_name)

    headers = ["ID", "Nome", "DataHora", "Motivo", "Feedback", "Timestamp"]

    try:
        worksheet = spreadsheet.worksheet("Feedbacks")
        current_headers = worksheet.row_values(1)
        if current_headers != headers:
            worksheet.update('A1:F1', [headers])
    except:
        worksheet = spreadsheet.add_worksheet(title="Feedbacks", rows=1000, cols=10)
        worksheet.update('A1:F1', [headers])

    return worksheet

# Função para carregar dados do Google Sheets
def carregar_dados():
    """Carrega dados do Google Sheets e converte para formato dict"""
    try:
        worksheet = obter_planilha()
        records = worksheet.get_all_records()
        
        # Converter para formato dict
        dados = {}
        for record in records:
            if record.get('ID'):
                id_col = record['ID']
                dados[id_col] = {
                    'nome': record.get('Nome', ''),
                    'avaliador': record.get('Avaliador', ''),
                    'data': record.get('Data', ''),
                    'scores': json.loads(record.get('Scores_JSON', '{}')),
                    'observacoes': json.loads(record.get('Observacoes_JSON', '{}')),
                    'opiniao': record.get('Opiniao', ''),
                    'total_pontos': record.get('Total_Pontos', 0),
                    'classificacao': record.get('Classificacao', ''),
                    'pontos_fortes': json.loads(record.get('Pontos_Fortes_JSON', '[]')),
                    'gargalos': json.loads(record.get('Gargalos_JSON', '[]')),
                    'acoes_melhoria': json.loads(record.get('Acoes_Melhoria_JSON', '[]')),
                    'timestamp': record.get('Timestamp', '')
                }
        
        return dados
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return {}

# Função para salvar dados no Google Sheets (SEGURA - sem deletar)
def salvar_dados(dados):
    """Salva dados no Google Sheets de forma segura - APENAS ADICIONA NOVOS REGISTROS"""
    try:
        worksheet = obter_planilha()
        records = worksheet.get_all_records()
        
        # IDs existentes na planilha
        ids_existentes = set(r.get('ID', '') for r in records if r.get('ID'))
        
        # Encontra novos registros para adicionar
        for id_col, info in dados.items():
            if id_col not in ids_existentes:
                # Novo registro - adiciona como nova linha
                row = [
                    id_col,
                    info.get('nome', ''),
                    info.get('avaliador', ''),
                    info.get('data', ''),
                    json.dumps(info.get('scores', {}), ensure_ascii=False),
                    json.dumps(info.get('observacoes', {}), ensure_ascii=False),
                    info.get('opiniao', ''),
                    info.get('total_pontos', 0),
                    info.get('classificacao', ''),
                    json.dumps(info.get('pontos_fortes', []), ensure_ascii=False),
                    json.dumps(info.get('gargalos', []), ensure_ascii=False),
                    json.dumps(info.get('acoes_melhoria', []), ensure_ascii=False),
                    info.get('timestamp', '')
                ]
                worksheet.append_row(row)
        
        return True
    except Exception as e:
        st.error(f"Erro ao salvar dados: {str(e)}")
        st.warning("⚠️ **Aviso:** Houve um problema ao salvar. Verifique o Google Sheets manualmente e faça backup dos dados se necessário.")
        return False

# Função para atualizar um registro individual (mais seguro)
def atualizar_avaliacao(id_colaborador, dados_atualizados):
    """Atualiza uma avaliação individual sem deletar outras"""
    try:
        worksheet = obter_planilha()
        records = worksheet.get_all_records()
        
        # Encontra a linha do colaborador
        linha_encontrada = None
        for idx, record in enumerate(records, start=2):  # Começa de 2 porque 1 é cabeçalho
            if record.get('ID') == id_colaborador:
                linha_encontrada = idx
                break
        
        if linha_encontrada is None:
            # Se não encontrou, adiciona como nova linha
            row = [
                id_colaborador,
                dados_atualizados.get('nome', ''),
                dados_atualizados.get('avaliador', ''),
                dados_atualizados.get('data', ''),
                json.dumps(dados_atualizados.get('scores', {}), ensure_ascii=False),
                json.dumps(dados_atualizados.get('observacoes', {}), ensure_ascii=False),
                dados_atualizados.get('opiniao', ''),
                dados_atualizados.get('total_pontos', 0),
                dados_atualizados.get('classificacao', ''),
                json.dumps(dados_atualizados.get('pontos_fortes', []), ensure_ascii=False),
                json.dumps(dados_atualizados.get('gargalos', []), ensure_ascii=False),
                json.dumps(dados_atualizados.get('acoes_melhoria', []), ensure_ascii=False),
                dados_atualizados.get('timestamp', '')
            ]
            worksheet.append_row(row)
        else:
            # Atualiza a linha encontrada
            row = [
                id_colaborador,
                dados_atualizados.get('nome', ''),
                dados_atualizados.get('avaliador', ''),
                dados_atualizados.get('data', ''),
                json.dumps(dados_atualizados.get('scores', {}), ensure_ascii=False),
                json.dumps(dados_atualizados.get('observacoes', {}), ensure_ascii=False),
                dados_atualizados.get('opiniao', ''),
                dados_atualizados.get('total_pontos', 0),
                dados_atualizados.get('classificacao', ''),
                json.dumps(dados_atualizados.get('pontos_fortes', []), ensure_ascii=False),
                json.dumps(dados_atualizados.get('gargalos', []), ensure_ascii=False),
                json.dumps(dados_atualizados.get('acoes_melhoria', []), ensure_ascii=False),
                dados_atualizados.get('timestamp', '')
            ]
            worksheet.update(f'A{linha_encontrada}:M{linha_encontrada}', [row])
        
        return True
    except Exception as e:
        st.error(f"Erro ao atualizar avaliação: {str(e)}")
        return False

# Funções de feedbacks
def carregar_feedbacks():
    """Carrega feedbacks do Google Sheets"""
    try:
        worksheet = obter_planilha_feedbacks()
        records = worksheet.get_all_records()
        feedbacks = []
        for record in records:
            if record.get('ID'):
                feedbacks.append({
                    'id': record.get('ID', ''),
                    'nome': record.get('Nome', ''),
                    'datahora': record.get('DataHora', ''),
                    'motivo': record.get('Motivo', ''),
                    'feedback': record.get('Feedback', ''),
                    'timestamp': record.get('Timestamp', '')
                })
        return feedbacks
    except Exception as e:
        st.error(f"Erro ao carregar feedbacks: {str(e)}")
        return []

def salvar_feedback(nome, motivo, feedback_texto):
    """Salva feedback individual no Google Sheets"""
    try:
        worksheet = obter_planilha_feedbacks()
        datahora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        feedback_id = f"{nome}_{datahora}"
        row = [
            feedback_id,
            nome,
            datahora,
            motivo,
            feedback_texto,
            datetime.now().isoformat()
        ]
        worksheet.append_row(row)
        return True
    except Exception as e:
        st.error(f"Erro ao salvar feedback: {str(e)}")
        return False

# Função para calcular pontuação total
def calcular_total(scores):
    return sum(scores.values()) if scores else 0

# Função para classificar performance
def classificar_performance(total_pontos):
    if total_pontos >= 40:
        return "ALTO DESEMPENHO", "#00796B"
    elif total_pontos >= 21:
        return "MANUTENÇÃO", "#E65100"
    else:
        return "RISCO", "#C62828"

_css_base = """
<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
    /* Cores corporativas SATTE ALAM */
    :root {
        --primary-color: #000000;
        --secondary-color: #FFFFFF;
        --accent-color: #FF6600;
        --support-color: #4c4c4c;
        --text-primary: $text_primary;
        --text-secondary: $text_secondary;
        --bg-light: #FAFAFA;
        --border-color: #E0E0E0;
        --header-bg: $header_bg;
        --header-text: $header_text;
        --header-subtext: $header_subtext;
    }
    
    /* Forçar cor de texto no modo dark */
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] *:not(.stButton):not(.status-high):not(.status-medium):not(.status-low) {
        color: $text_primary !important;
    }
    
    /* Fonte personalizada - Montserrat */
    * {
        font-family: 'Montserrat', 'Segoe UI', sans-serif;
    }
    
    body {
        font-family: 'Montserrat', 'Segoe UI', sans-serif;
    }
    
    /* Header section */
    .header-section {
        background: var(--header-bg);
        padding: 40px;
        border-radius: 12px;
        color: var(--header-text);
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
        display: flex;
        align-items: center;
        gap: 30px;
    }
    
    /* Metric labels: respeitar tema light/dark */
    [data-testid="stMetricLabel"] {
        background-color: transparent;
        color: var(--text-primary);
    }

    [data-testid="stMetricValue"] {
        color: var(--text-primary);
    }
    
    /* Estilo para o container da logo */
    .logo-container {
        background: var(--header-bg);
        padding: 20px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .header-container {
        background: var(--header-bg);
        padding: 20px 30px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #F5F5F5 0%, #FFFFFF 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #FF6600;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        color: var(--text-primary);
    }
    
    /* Section headers */
    .section-header {
        color: var(--text-primary) !important;
        border-bottom: 3px solid #FF6600;
        padding-bottom: 12px;
        margin-bottom: 20px;
        margin-top: 20px;
        font-weight: 700;
        font-size: 1.3rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Títulos sub-seção - respeitam tema */
    .subtitle-green,
    .subtitle-red,
    .subtitle-blue,
    .subtitle-dark {
        color: var(--text-primary) !important;
        font-weight: 700 !important;
    }

    .subtitle-blue {
        margin-top: 20px !important;
    }

    .subtitle-green,
    .subtitle-red,
    .subtitle-dark {
        margin-top: 0 !important;
    }

    /* Forçar cor de texto GLOBALMENTE */
    * {
        color: $text_primary !important;
    }
    
    /* Exceções para manter cores específicas */
    .stButton button {
        color: white !important;
    }
    
    .status-high {
        color: #1B5E20 !important;
    }
    
    .status-medium {
        color: #E65100 !important;
    }
    
    .status-low {
        color: #C62828 !important;
    }

    /* Labels e valores de métricas */
    [data-testid="stMetricLabel"],
    [data-testid="stMetricValue"] {
        color: var(--text-primary) !important;
    }
    
    /* Status badges */
    .status-high {
        background-color: #E8F5E9;
        color: #1B5E20;
        padding: 10px 18px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        border: 2px solid #4CAF50;
    }
    
    .status-medium {
        background-color: #FFF3E0;
        color: #E65100;
        padding: 10px 18px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        border: 2px solid #FF6600;
    }
    
    .status-low {
        background-color: #FFEBEE;
        color: #C62828;
        padding: 10px 18px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
        border: 2px solid #D32F2F;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #FF6600 0%, #E65100 100%);
        color: white;
        border: none;
        font-weight: 600;
        padding: 12px 24px;
        border-radius: 6px;
        transition: all 0.3s ease;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        font-family: 'Montserrat', sans-serif;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(255, 102, 0, 0.4);
        transform: translateY(-2px);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border: 2px solid #E0E0E0 !important;
        border-radius: 6px;
        font-family: 'Montserrat', sans-serif;
        color: var(--text-primary) !important;
        background-color: transparent !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #FF6600 !important;
        box-shadow: 0 0 0 3px rgba(255, 102, 0, 0.1) !important;
    }
    
    /* Divider */
    hr {
        border-color: #E0E0E0;
        margin: 30px 0;
    }
    
    /* Sidebar - removido para manter tema padrão do Streamlit */
    
    /* DataFrame styling */
    .dataframe {
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Info/Success/Error boxes */
    .stAlert {
        border-radius: 6px;
        margin: 10px 0;
    }
</style>
"""

# CSS customizado com identidade visual SATTE ALAM MOTORS
st.markdown(
    Template(_css_base).substitute(
        header_bg=_header_bg,
        header_text=_header_text,
        header_subtext=_header_subtext,
        text_primary=_text_primary,
        text_secondary=_text_secondary,
    ),
    unsafe_allow_html=True,
)

# Título principal
st.markdown("""
<style>
.header-wrapper {
    background: var(--header-bg);
    padding: 20px 30px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 20px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
.header-text h1 {
    color: var(--header-text);
    margin: 0;
    font-weight: 700;
    font-size: 2rem;
    letter-spacing: 0.5px;
}
.header-text p {
    color: var(--header-subtext);
    margin: 8px 0 0 0;
    font-size: 0.95rem;
    opacity: 0.95;
    font-weight: 400;
}
</style>
<div class="header-wrapper">
    <div style="flex: 1;">
""", unsafe_allow_html=True)

try:
    col_logo, col_text = st.columns([0.8, 3])
    with col_logo:
        st.image("logo.png", width=180)
    with col_text:
        st.markdown("""
        <div class="header-text">
            <h1>SISTEMA DE AVALIAÇÃO E PDI</h1>
            <p>Gestão de Performance e Desenvolvimento Individual | SATTE ALAM MOTORS</p>
        </div>
        """, unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("""
    <div class="header-text">
        <h1>SISTEMA DE AVALIAÇÃO E PDI</h1>
        <p>Gestão de Performance e Desenvolvimento Individual | SATTE ALAM MOTORS</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar para gerenciar colaboradores
st.sidebar.title("GERENCIAMENTO")
modo = st.sidebar.radio(
    "Selecione a ação:",
    ["Nova Avaliação", "Visualizar Colaboradores", "Relatório", "Feedbacks"]
)

dados = carregar_dados()

if modo == "Nova Avaliação":
    st.markdown('<h2 class="section-header">FORMULÁRIO DE AVALIAÇÃO</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        nome_colaborador = st.text_input(
            "Nome do Colaborador",
            key="nome_col"
        )
        avaliador = st.text_input(
            "Nome do Avaliador (Gestor)",
            key="avaliador"
        )
    
    with col2:
        data_avaliacao = st.date_input(
            "Data da Avaliação",
            value=datetime.now()
        )
    
    st.divider()
    st.markdown('<h3 class="section-header">MATRIZ DE COMPETÊNCIAS</h3>', unsafe_allow_html=True)
    st.caption("Escala: 1=Insatisfatório, 2=Abaixo da Expectativa, 3=Atende, 4=Supera, 5=Excepcional")
    
    # Critérios de avaliação
    criterios = {
        "Organização": "Manutenção do box e zelo com ferramentas",
        "Trabalho em Equipe": "Colaboração e clima organizacional",
        "Comunicação e Regras": "Postura e adesão às normas internas",
        "Segurança e EPIs": "Cumprimento de regras de segurança e uso correto de EPIs",
        "Conduta e Respeito": "Boas práticas de conduta e prevenção ao assédio moral",
        "Eficiência Técnica": "Entrega dentro do tempo padrão (produtividade)",
        "Qualidade (Retorno)": "Execução correta na 1ª vez (sem retrabalho)",
        "Adesão aos Processos": "Uso de checklists e registros no sistema",
        "Capacitação": "Busca por cursos e novos conhecimentos técnicos"
    }
    
    scores = {}
    observacoes = {}
    
    for idx, (criterio, descricao) in enumerate(criterios.items()):
        col1, col2, col3 = st.columns([2, 1, 2])
        
        with col1:
            st.caption(f"**{criterio}**")
            st.text(descricao)
        
        with col2:
            scores[criterio] = st.selectbox(
                label="Nota",
                options=[1, 2, 3, 4, 5],
                key=f"score_{idx}"
            )
        
        with col3:
            observacoes[criterio] = st.text_input(
                "Observações",
                key=f"obs_{idx}",
                placeholder="Evidências/Justificativa"
            )
    
    total_pontos = calcular_total(scores)
    classificacao, cor = classificar_performance(total_pontos)
    
    st.divider()
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f'<h3 class="section-header">Total de Pontos: {total_pontos}/45</h3>', unsafe_allow_html=True)
    with col2:
        if "ALTO" in classificacao:
            st.markdown(f'<div class="status-high">{classificacao}</div>', unsafe_allow_html=True)
        elif "MANUTENÇÃO" in classificacao:
            st.markdown(f'<div class="status-medium">{classificacao}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="status-low">{classificacao}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown('<h3 class="section-header">OPINIÃO DO COLABORADOR</h3>', unsafe_allow_html=True)
    opiniao_colaborador = st.text_area(
        "Opinião sobre riscos ocupacionais e problemas no processo",
        key="opiniao_colaborador",
        height=120,
        placeholder="Relate riscos observados, gargalos do processo e sugestões de melhoria"
    )

    st.divider()
    st.markdown('<h3 class="section-header">PLANO DE DESENVOLVIMENTO INDIVIDUAL (PDI)</h3>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4 class="subtitle-green">O que CONTINUAR fazendo (Pontos Fortes)</h4>', unsafe_allow_html=True)
        ponto_forte_1 = st.text_area("Ponto Forte 1", key="pf1", height=80)
        ponto_forte_2 = st.text_area("Ponto Forte 2", key="pf2", height=80)
    
    with col2:
        st.markdown('<h4 class="subtitle-red">O que PARAR de fazer (Gargalos)</h4>', unsafe_allow_html=True)
        gargalo_1 = st.text_area("Gargalo 1", key="g1", height=80)
        gargalo_2 = st.text_area("Gargalo 2", key="g2", height=80)
    
    st.markdown('<h4 class="subtitle-blue">O que COMEÇAR a desenvolver (Ações de Melhoria)</h4>', unsafe_allow_html=True)
    
    num_acoes = st.number_input("Quantas ações de melhoria?", min_value=1, max_value=5, value=3)
    
    acoes_melhoria = []
    for i in range(num_acoes):
        col1, col2 = st.columns(2)
        with col1:
            acao = st.text_area(f"Ação de Melhoria {i+1}", key=f"acao_{i}", height=80)
        with col2:
            prazo = st.text_input(f"Como e Prazos? {i+1}", key=f"prazo_{i}")
        if acao:
            acoes_melhoria.append({"acao": acao, "prazo": prazo})
    
    # Botão para salvar
    if st.button("SALVAR AVALIAÇÃO", use_container_width=True):
        if nome_colaborador.strip() and avaliador.strip():
            id_colaborador = f"{nome_colaborador}_{data_avaliacao}"
            
            dados[id_colaborador] = {
                "nome": nome_colaborador,
                "avaliador": avaliador,
                "data": str(data_avaliacao),
                "scores": scores,
                "observacoes": observacoes,
                "opiniao": opiniao_colaborador,
                "total_pontos": total_pontos,
                "classificacao": classificacao,
                "pontos_fortes": [ponto_forte_1, ponto_forte_2],
                "gargalos": [gargalo_1, gargalo_2],
                "acoes_melhoria": acoes_melhoria,
                "timestamp": datetime.now().isoformat()
            }
            
            salvar_dados(dados)
            st.success(f"Avaliação de {nome_colaborador} salva com sucesso!")
            st.balloons()
        else:
            st.error("Por favor, preencha Nome do Colaborador e Avaliador")

elif modo == "Visualizar Colaboradores":
    st.markdown('<h2 class="section-header">COLABORADORES REGISTRADOS</h2>', unsafe_allow_html=True)
    
    if not dados:
        st.info("Nenhuma avaliação registrada ainda.")
    else:
        # Criar DataFrame com os dados
        dados_lista = []
        for id_col, dados_col in dados.items():
            dados_lista.append({
                "Nome": dados_col["nome"],
                "Avaliador": dados_col["avaliador"],
                "Data": dados_col["data"],
                "Total Pontos": dados_col["total_pontos"],
                "Classificação": dados_col["classificacao"],
                "ID": id_col
            })
        
        df = pd.DataFrame(dados_lista)
        
        # Seletor de colaborador
        colaborador_selecionado = st.selectbox(
            "Selecione um colaborador para visualizar/editar:",
            [d["Nome"] for d in dados_lista]
        )
        
        # Filtrar dados do colaborador selecionado
        id_selecionado = next(d["ID"] for d in dados_lista if d["Nome"] == colaborador_selecionado)
        dados_colaborador = dados[id_selecionado]
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown(f'<h3 class="section-header">AVALIAÇÃO DE {colaborador_selecionado.upper()}</h3>', unsafe_allow_html=True)
        
        with col2:
            modo_editar = st.button("✏️ EDITAR", key="btn_edit", use_container_width=True)
        
        with col3:
            if st.button("🗑️ DELETAR", key="btn_delete", use_container_width=True):
                del dados[id_selecionado]
                salvar_dados(dados)
                st.success(f"{colaborador_selecionado} foi deletado!")
                st.rerun()
        
        if modo_editar:
            st.session_state.editando = id_selecionado
        
        # Informações básicas
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Avaliador", dados_colaborador["avaliador"])
        with col2:
            st.metric("Data", dados_colaborador["data"])
        with col3:
            classificacao_texto = dados_colaborador["classificacao"]
            st.metric("Classificação", classificacao_texto)
        
        # Scores
        st.markdown('<h3 class="section-header">NOTAS POR CRITÉRIO</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Tabela de scores
            scores_data = []
            for criterio, score in dados_colaborador["scores"].items():
                obs = dados_colaborador["observacoes"].get(criterio, "")
                scores_data.append({
                    "Critério": criterio,
                    "Nota": score,
                    "Observações": obs
                })
            
            df_scores = pd.DataFrame(scores_data)
            st.dataframe(df_scores, use_container_width=True, hide_index=True)
        
        with col2:
            # Gráfico de radar
            fig = go.Figure(data=go.Scatterpolar(
                r=list(dados_colaborador["scores"].values()),
                theta=list(dados_colaborador["scores"].keys()),
                fill='toself',
                name='Score'
            ))
            
            fig.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 5])),
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # PDI
        st.markdown('<h3 class="section-header">PLANO DE DESENVOLVIMENTO INDIVIDUAL</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h4 class="subtitle-dark">Pontos Fortes</h4>', unsafe_allow_html=True)
            for i, ponto in enumerate(dados_colaborador["pontos_fortes"], 1):
                if ponto:
                    st.write(f"• {ponto}")
        
        with col2:
            st.markdown('<h4 class="subtitle-dark">Gargalos</h4>', unsafe_allow_html=True)
            for i, gargalo in enumerate(dados_colaborador["gargalos"], 1):
                if gargalo:
                    st.write(f"• {gargalo}")
        
        st.markdown('<h4 class="subtitle-dark">Ações de Melhoria</h4>', unsafe_allow_html=True)
        for i, acao in enumerate(dados_colaborador["acoes_melhoria"], 1):
            with st.expander(f"Ação {i}: {acao['acao'][:50]}..."):
                st.write(f"**Ação:** {acao['acao']}")
                st.write(f"**Como e Prazos:** {acao['prazo']}")

        # Opinião do colaborador
        st.markdown('<h3 class="section-header">OPINIÃO DO COLABORADOR</h3>', unsafe_allow_html=True)
        opiniao = dados_colaborador.get("opiniao", "")
        if opiniao:
            st.write(opiniao)
        else:
            st.info("Sem opinião registrada.")

        # Modo de edição
        if 'editando' in st.session_state and st.session_state.editando == id_selecionado:
            st.divider()
            st.markdown('<h2 class="section-header">MODO DE EDIÇÃO</h2>', unsafe_allow_html=True)
            
            st.info("Edite os campos abaixo e clique em 'SALVAR ALTERAÇÕES' para atualizar a avaliação.")
            
            col1, col2 = st.columns(2)
            with col1:
                avaliador_edit = st.text_input(
                    "Avaliador",
                    value=dados_colaborador.get("avaliador", ""),
                    key="edit_avaliador"
                )
            with col2:
                data_edit = st.date_input(
                    "Data",
                    value=datetime.strptime(dados_colaborador.get("data", "2000-01-01"), "%Y-%m-%d"),
                    key="edit_data"
                )
            
            st.markdown('<h3 class="section-header">EDITAR MATRIZ DE COMPETÊNCIAS</h3>', unsafe_allow_html=True)
            st.caption("Escala: 1=Insatisfatório, 2=Abaixo da Expectativa, 3=Atende, 4=Supera, 5=Excepcional")
            
            scores_edit = {}
            observacoes_edit = {}
            
            for idx, criterio in enumerate(dados_colaborador["scores"].keys()):
                col1, col2, col3 = st.columns([2, 1, 2])
                
                with col1:
                    st.caption(f"**{criterio}**")
                
                with col2:
                    scores_edit[criterio] = st.selectbox(
                        label="Nota",
                        options=[1, 2, 3, 4, 5],
                        index=int(dados_colaborador["scores"][criterio]) - 1,
                        key=f"edit_score_{idx}"
                    )
                
                with col3:
                    observacoes_edit[criterio] = st.text_input(
                        "Observações",
                        value=dados_colaborador["observacoes"].get(criterio, ""),
                        key=f"edit_obs_{idx}"
                    )
            
            total_pontos_edit = calcular_total(scores_edit)
            classificacao_edit, _ = classificar_performance(total_pontos_edit)
            
            st.divider()
            st.markdown(f'<h3 class="section-header">Total de Pontos: {total_pontos_edit}/45</h3>', unsafe_allow_html=True)
            
            st.divider()
            st.markdown('<h3 class="section-header">EDITAR PDI</h3>', unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown('<h4 style="color: #00796B; margin-top: 0;">Pontos Fortes</h4>', unsafe_allow_html=True)
                pf1_edit = st.text_area("Ponto Forte 1", 
                    value=dados_colaborador["pontos_fortes"][0] if len(dados_colaborador["pontos_fortes"]) > 0 else "",
                    key="edit_pf1", height=80)
                pf2_edit = st.text_area("Ponto Forte 2",
                    value=dados_colaborador["pontos_fortes"][1] if len(dados_colaborador["pontos_fortes"]) > 1 else "",
                    key="edit_pf2", height=80)
            
            with col2:
                st.markdown('<h4 style="color: #C62828; margin-top: 0;">Gargalos</h4>', unsafe_allow_html=True)
                g1_edit = st.text_area("Gargalo 1",
                    value=dados_colaborador["gargalos"][0] if len(dados_colaborador["gargalos"]) > 0 else "",
                    key="edit_g1", height=80)
                g2_edit = st.text_area("Gargalo 2",
                    value=dados_colaborador["gargalos"][1] if len(dados_colaborador["gargalos"]) > 1 else "",
                    key="edit_g2", height=80)
            
            st.markdown('<h4 style="color: #1976D2; margin-top: 20px;">Ações de Melhoria</h4>', unsafe_allow_html=True)
            
            num_acoes_edit = st.number_input("Quantas ações de melhoria?", 
                min_value=1, max_value=5, 
                value=len(dados_colaborador["acoes_melhoria"]) or 3,
                key="edit_num_acoes")
            
            acoes_melhoria_edit = []
            for i in range(num_acoes_edit):
                col1, col2 = st.columns(2)
                with col1:
                    acao_valor = ""
                    if i < len(dados_colaborador["acoes_melhoria"]):
                        acao_valor = dados_colaborador["acoes_melhoria"][i].get("acao", "")
                    acao = st.text_area(f"Ação de Melhoria {i+1}", value=acao_valor, key=f"edit_acao_{i}", height=80)
                with col2:
                    prazo_valor = ""
                    if i < len(dados_colaborador["acoes_melhoria"]):
                        prazo_valor = dados_colaborador["acoes_melhoria"][i].get("prazo", "")
                    prazo = st.text_input(f"Como e Prazos? {i+1}", value=prazo_valor, key=f"edit_prazo_{i}")
                if acao:
                    acoes_melhoria_edit.append({"acao": acao, "prazo": prazo})
            
            st.divider()
            st.markdown('<h3 class="section-header">EDITAR OPINIÃO DO COLABORADOR</h3>', unsafe_allow_html=True)
            opiniao_edit = st.text_area(
                "Opinião sobre riscos ocupacionais e problemas no processo",
                value=dados_colaborador.get("opiniao", ""),
                key="edit_opiniao",
                height=120,
                placeholder="Relate riscos observados, gargalos do processo e sugestões de melhoria"
            )
            
            st.divider()
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("SALVAR ALTERAÇÕES", use_container_width=True, key="btn_save_edit"):
                    dados_atualizados = {
                        "nome": dados_colaborador["nome"],
                        "avaliador": avaliador_edit,
                        "data": str(data_edit),
                        "scores": scores_edit,
                        "observacoes": observacoes_edit,
                        "opiniao": opiniao_edit,
                        "total_pontos": total_pontos_edit,
                        "classificacao": classificacao_edit,
                        "pontos_fortes": [pf1_edit, pf2_edit],
                        "gargalos": [g1_edit, g2_edit],
                        "acoes_melhoria": acoes_melhoria_edit,
                        "timestamp": datetime.now().isoformat()
                    }
                    
                    if atualizar_avaliacao(id_selecionado, dados_atualizados):
                        st.success("Avaliação atualizada com sucesso!")
                        del st.session_state.editando
                        st.rerun()
                    else:
                        st.error("Erro ao atualizar avaliação!")
            
            with col2:
                if st.button("CANCELAR", use_container_width=True, key="btn_cancel_edit"):
                    del st.session_state.editando
                    st.rerun()

elif modo == "Relatório":
    st.markdown('<h2 class="section-header">RELATÓRIO GERAL DE PERFORMANCE</h2>', unsafe_allow_html=True)
    
    if not dados:
        st.info("Nenhuma avaliação registrada ainda.")
    else:
        # Preparar dados para visualização
        nomes = []
        totais = []
        classificacoes = []
        cores_map = {"ALTO DESEMPENHO": "#4CAF50", "MANUTENÇÃO": "#FF6600", "RISCO": "#D32F2F"}
        cores = []
        
        for id_col, dados_col in dados.items():
            nomes.append(dados_col["nome"])
            totais.append(dados_col["total_pontos"])
            classificacao = dados_col["classificacao"]
            classificacoes.append(classificacao)
            cores.append(cores_map.get(classificacao, "#FF6600"))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Colaboradores", len(dados))
        with col2:
            st.metric("Média de Pontos", f"{sum(totais) / len(totais):.1f}/45")
        with col3:
            alto_desempenho = sum(1 for c in classificacoes if "ALTO" in c)
            st.metric("Alto Desempenho", alto_desempenho, delta="Excelente")
        
        st.divider()
        
        # Gráfico de distribuição de scores
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h4 style="color: #000000; font-weight: 700;">DISTRIBUIÇÃO DE PONTUAÇÕES</h4>', unsafe_allow_html=True)
            
            fig1 = px.bar(
                x=nomes,
                y=totais,
                color=totais,
                color_continuous_scale=["#D32F2F", "#FF6600", "#4CAF50"],
                labels={"y": "Pontos", "x": "Colaborador"},
                height=400
            )
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.markdown('<h4 style="color: #D32F2F;">CURVA DE VITALIDADE (DISTRIBUIÇÃO NORMAL)</h4>', unsafe_allow_html=True)
            
            # Criar histograma dos scores
            fig2 = px.histogram(
                x=totais,
                nbins=10,
                labels={"x": "Pontos", "count": "Quantidade"},
                color_discrete_sequence=["#1976D2"],
                height=400
            )
            
            # Adicionar linhas de referência
            fig2.add_vline(x=20, line_dash="dash", line_color="#C62828", annotation_text="Risco")
            fig2.add_vline(x=21, line_dash="dash", line_color="#E65100", annotation_text="Limite Manutenção")
            fig2.add_vline(x=40, line_dash="dash", line_color="#00796B", annotation_text="Alto Desempenho")
            
            st.plotly_chart(fig2, use_container_width=True)
        
        st.divider()
        
        # Tabela resumida
        st.markdown('<h3 class="section-header">RESUMO DE TODOS OS COLABORADORES</h3>', unsafe_allow_html=True)
        
        resumo_data = []
        for id_col, dados_col in dados.items():
            resumo_data.append({
                "Nome": dados_col["nome"],
                "Avaliador": dados_col["avaliador"],
                "Data": dados_col["data"],
                "Total Pontos": dados_col["total_pontos"],
                "Classificação": dados_col["classificacao"]
            })
        
        df_resumo = pd.DataFrame(resumo_data).sort_values("Total Pontos", ascending=False)
        st.dataframe(df_resumo, use_container_width=True, hide_index=True)
        
        st.divider()
        
        # Análise por critério
        st.markdown('<h3 class="section-header">ANÁLISE POR CRITÉRIO</h3>', unsafe_allow_html=True)
        
        criterios_medias = {}
        for criterio in ["Organização", "Trabalho em Equipe", "Comunicação e Regras",
                "Segurança e EPIs", "Conduta e Respeito",
                "Eficiência Técnica", "Qualidade (Retorno)", "Adesão aos Processos",
                "Capacitação"]:
            notas = []
            for id_col, dados_col in dados.items():
                if criterio in dados_col["scores"]:
                    notas.append(dados_col["scores"][criterio])
            if notas:
                criterios_medias[criterio] = sum(notas) / len(notas)
        
        fig3 = px.bar(
            x=list(criterios_medias.keys()),
            y=list(criterios_medias.values()),
            labels={"x": "Critério", "y": "Média de Notas"},
            color_discrete_sequence=["#FF6600"],
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)

elif modo == "Feedbacks":
    st.markdown('<h2 class="section-header">FEEDBACKS SOB DEMANDA</h2>', unsafe_allow_html=True)

    if not dados:
        st.info("Nenhum colaborador registrado ainda.")
    else:
        feedbacks = carregar_feedbacks()

        colaboradores = sorted({d["nome"] for d in dados.values()})
        col1, col2 = st.columns(2)

        with col1:
            colaborador_feedback = st.selectbox(
                "Selecione o colaborador",
                colaboradores
            )
        with col2:
            motivo_feedback = st.text_input(
                "Motivo do feedback",
                placeholder="Ex.: Segurança, processo, conduta, desempenho"
            )

        feedback_texto = st.text_area(
            "Feedback (direcionamento)",
            height=120,
            placeholder="Descreva o direcionamento e expectativas"
        )

        if st.button("SALVAR FEEDBACK", use_container_width=True):
            if colaborador_feedback and motivo_feedback.strip() and feedback_texto.strip():
                if salvar_feedback(colaborador_feedback, motivo_feedback, feedback_texto):
                    st.success("Feedback salvo com sucesso!")
                    st.rerun()
            else:
                st.error("Preencha colaborador, motivo e feedback.")

        st.divider()
        st.markdown('<h3 class="section-header">HISTÓRICO DE FEEDBACKS</h3>', unsafe_allow_html=True)

        filtro_nome = st.selectbox(
            "Filtrar por colaborador",
            ["Todos"] + colaboradores
        )

        feedbacks_filtrados = [
            f for f in feedbacks
            if filtro_nome == "Todos" or f["nome"] == filtro_nome
        ]

        if not feedbacks_filtrados:
            st.info("Nenhum feedback registrado para o filtro selecionado.")
        else:
            df_feedbacks = pd.DataFrame([
                {
                    "Nome": f["nome"],
                    "Data/Hora": f["datahora"],
                    "Motivo": f["motivo"],
                    "Feedback": f["feedback"]
                }
                for f in feedbacks_filtrados
            ]).sort_values("Data/Hora", ascending=False)

            st.dataframe(df_feedbacks, use_container_width=True, hide_index=True)

# Footer
st.divider()
st.markdown("""
<div style="text-align: center; color: #4c4c4c; margin-top: 30px; font-family: 'Montserrat', sans-serif;">
    <p style="margin: 5px 0; font-weight: 700; font-size: 1.1rem;">SATTE ALAM MOTORS</p>
    <p style="margin: 5px 0; font-size: 0.9rem; color: #000000;">Todos os dados são salvos automaticamente no Google Sheets</p>
    <p style="margin: 5px 0; font-size: 0.85rem; color: #4c4c4c;">Sistema de Avaliação e PDI v2.0 | Desenvolvido com Streamlit</p>
</div>
""", unsafe_allow_html=True)
