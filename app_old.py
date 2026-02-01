import streamlit as st
import pandas as pd
import json
import os
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import gspread
from google.oauth2.service_account import Credentials

# Configuração da página
st.set_page_config(
    page_title="Sistema de Avaliação e PDI",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
            st.error("❌ Credenciais do Google não encontradas!")
            st.info("📝 Configure as credenciais em .streamlit/secrets.toml ou service_account.json")
            st.stop()
        
        client = gspread.authorize(credentials)
        return client
    except Exception as e:
        st.error(f"❌ Erro ao conectar ao Google Sheets: {str(e)}")
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
        st.success(f"✅ Conectado à planilha: {sheet_name}")
    except gspread.exceptions.SpreadsheetNotFound:
        # Cria nova planilha se não existir
        spreadsheet = client.create(sheet_name)
        st.success(f"✅ Nova planilha criada: {sheet_name}")
    
    # Obtém ou cria a primeira aba
    try:
        worksheet = spreadsheet.worksheet("Avaliações")
    except:
        worksheet = spreadsheet.add_worksheet(title="Avaliações", rows=1000, cols=20)
        # Adiciona cabeçalhos
        headers = ["ID", "Nome", "Avaliador", "Data", "Scores_JSON", "Observacoes_JSON", 
                   "Total_Pontos", "Classificacao", "Pontos_Fortes_JSON", "Gargalos_JSON", 
                   "Acoes_Melhoria_JSON", "Timestamp"]
        worksheet.update('A1:L1', [headers])
    
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
                    'total_pontos': record.get('Total_Pontos', 0),
                    'classificacao': record.get('Classificacao', ''),
                    'pontos_fortes': json.loads(record.get('Pontos_Fortes_JSON', '[]')),
                    'gargalos': json.loads(record.get('Gargalos_JSON', '[]')),
                    'acoes_melhoria': json.loads(record.get('Acoes_Melhoria_JSON', '[]')),
                    'timestamp': record.get('Timestamp', '')
                }
        
        return dados
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {str(e)}")
        return {}

# Função para salvar dados no Google Sheets
def salvar_dados(dados):
    """Salva dados no Google Sheets"""
    try:
        worksheet = obter_planilha()
        
        # Limpa todos os dados (exceto cabeçalho)
        worksheet.delete_rows(2, worksheet.row_count)
        
        # Prepara dados para inserção
        rows = []
        for id_col, info in dados.items():
            row = [
                id_col,
                info.get('nome', ''),
                info.get('avaliador', ''),
                info.get('data', ''),
                json.dumps(info.get('scores', {}), ensure_ascii=False),
                json.dumps(info.get('observacoes', {}), ensure_ascii=False),
                info.get('total_pontos', 0),
                info.get('classificacao', ''),
                json.dumps(info.get('pontos_fortes', []), ensure_ascii=False),
                json.dumps(info.get('gargalos', []), ensure_ascii=False),
                json.dumps(info.get('acoes_melhoria', []), ensure_ascii=False),
                info.get('timestamp', '')
            ]
            rows.append(row)
        
        # Insere todos os dados de uma vez
        if rows:
            worksheet.update(f'A2:L{len(rows)+1}', rows)
        
        return True
    except Exception as e:
        st.error(f"❌ Erro ao salvar dados: {str(e)}")
        return False

# Função para calcular pontuação total
def calcular_total(scores):
    return sum(scores.values()) if scores else 0

# Função para classificar performance
def classificar_performance(total_pontos):
    if total_pontos >= 31:
        return "🟢 ALTO DESEMPENHO", "#00A86B"
    elif total_pontos >= 16:
        return "🟡 MANUTENÇÃO", "#FFD700"
    else:
        return "🔴 RISCO", "#FF6B6B"

# CSS customizado com identidade visual SATTE ALAM MOTORS
st.markdown("""
<style>
    /* Cores corporativas */
    :root {
        --primary-color: #D32F2F;
        --secondary-color: #1976D2;
        --accent-color: #F57C00;
        --success-color: #00796B;
        --warning-color: #F57F17;
        --danger-color: #C62828;
        --text-primary: #212121;
        --text-secondary: #757575;
        --bg-light: #FAFAFA;
        --border-color: #E0E0E0;
    }
    
    /* Fonte personalizada */
    body {
        font-family: 'Roboto', 'Segoe UI', sans-serif;
    }
    
    /* Header section */
    .header-section {
        background: linear-gradient(135deg, #D32F2F 0%, #1976D2 100%);
        padding: 30px;
        border-radius: 12px;
        color: white;
        margin-bottom: 30px;
        box-shadow: 0 4px 12px rgba(211, 47, 47, 0.3);
    }
    
    .header-section h1 {
        margin: 0;
        font-weight: 700;
        font-size: 2rem;
        letter-spacing: -0.5px;
    }
    
    .header-section p {
        margin: 10px 0 0 0;
        font-size: 1rem;
        opacity: 0.95;
    }
    
    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #F5F5F5 0%, #FFFFFF 100%);
        padding: 20px;
        border-radius: 10px;
        border-left: 4px solid #D32F2F;
        margin: 10px 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }
    
    /* Section headers */
    .section-header {
        color: #D32F2F;
        border-bottom: 3px solid #D32F2F;
        padding-bottom: 10px;
        margin-bottom: 20px;
        font-weight: 700;
    }
    
    /* Status badges */
    .status-high {
        background-color: #C8E6C9;
        color: #00796B;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-medium {
        background-color: #FFE0B2;
        color: #E65100;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    .status-low {
        background-color: #FFCDD2;
        color: #C62828;
        padding: 8px 16px;
        border-radius: 20px;
        font-weight: 600;
        display: inline-block;
    }
    
    /* Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #D32F2F 0%, #B71C1C 100%);
        color: white;
        border: none;
        font-weight: 600;
        padding: 10px 20px;
        border-radius: 6px;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        box-shadow: 0 4px 12px rgba(211, 47, 47, 0.4);
        transform: translateY(-2px);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        border: 2px solid #E0E0E0;
        border-radius: 6px;
    }
    
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #D32F2F !important;
        box-shadow: 0 0 0 3px rgba(211, 47, 47, 0.1);
    }
    
    /* Divider */
    hr {
        border-color: #E0E0E0;
        margin: 30px 0;
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown("""
<div class="header-section">
    <h1>SISTEMA DE AVALIAÇÃO E PDI</h1>
    <p>Gestão de Performance e Desenvolvimento Individual | SATTE ALAM MOTORS</p>
</div>
""", unsafe_allow_html=True)

# Sidebar para gerenciar colaboradores
st.sidebar.title("GERENCIAMENTO")
modo = st.sidebar.radio(
    "Selecione a ação:",
    ["Nova Avaliação", "Visualizar Colaboradores", "Relatório"]
)

dados = carregar_dados()

if modo == "📝 Nova Avaliação":
    st.header("Formulário de Avaliação")
    
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
    st.subheader("🎯 Matriz de Competências")
    st.caption("Escala: 1=Insatisfatório, 2=Abaixo da Expectativa, 3=Atende, 4=Supera, 5=Excepcional")
    
    # Critérios de avaliação
    criterios = {
        "Organização": "Manutenção do box e zelo com ferramentas",
        "Trabalho em Equipe": "Colaboração e clima organizacional",
        "Comunicação e Regras": "Postura e adesão às normas internas",
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
    st.subheader(f"Total de Pontos: {total_pontos}/35 - {classificacao}")
    
    st.divider()
    st.subheader("📋 Plano de Desenvolvimento Individual (PDI)")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("✅ O que CONTINUAR fazendo (Pontos Fortes)")
        ponto_forte_1 = st.text_area("Ponto Forte 1", key="pf1", height=80)
        ponto_forte_2 = st.text_area("Ponto Forte 2", key="pf2", height=80)
    
    with col2:
        st.subheader("❌ O que PARAR de fazer (Gargalos)")
        gargalo_1 = st.text_area("Gargalo 1", key="g1", height=80)
        gargalo_2 = st.text_area("Gargalo 2", key="g2", height=80)
    
    st.subheader("🚀 O que COMEÇAR a desenvolver (Ações de Melhoria)")
    
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
    if st.button("💾 Salvar Avaliação", use_container_width=True):
        if nome_colaborador.strip() and avaliador.strip():
            id_colaborador = f"{nome_colaborador}_{data_avaliacao}"
            
            dados[id_colaborador] = {
                "nome": nome_colaborador,
                "avaliador": avaliador,
                "data": str(data_avaliacao),
                "scores": scores,
                "observacoes": observacoes,
                "total_pontos": total_pontos,
                "classificacao": classificacao,
                "pontos_fortes": [ponto_forte_1, ponto_forte_2],
                "gargalos": [gargalo_1, gargalo_2],
                "acoes_melhoria": acoes_melhoria,
                "timestamp": datetime.now().isoformat()
            }
            
            salvar_dados(dados)
            st.success(f"✅ Avaliação de {nome_colaborador} salva com sucesso!")
            st.balloons()
        else:
            st.error("❌ Por favor, preencha Nome do Colaborador e Avaliador")

elif modo == "👥 Visualizar Colaboradores":
    st.header("Colaboradores Registrados")
    
    if not dados:
        st.info("📭 Nenhuma avaliação registrada ainda.")
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
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            st.subheader(f"📋 Avaliação de {colaborador_selecionado}")
        
        with col2:
            if st.button("🗑️ Deletar Colaborador", key="btn_delete"):
                del dados[id_selecionado]
                salvar_dados(dados)
                st.success(f"✅ {colaborador_selecionado} foi deletado!")
                st.rerun()
        
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
        st.subheader("🎯 Notas por Critério")
        
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
        st.subheader("📋 Plano de Desenvolvimento Individual")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Pontos Fortes")
            for i, ponto in enumerate(dados_colaborador["pontos_fortes"], 1):
                if ponto:
                    st.write(f"• {ponto}")
        
        with col2:
            st.markdown("### ❌ Gargalos")
            for i, gargalo in enumerate(dados_colaborador["gargalos"], 1):
                if gargalo:
                    st.write(f"• {gargalo}")
        
        st.markdown("### 🚀 Ações de Melhoria")
        for i, acao in enumerate(dados_colaborador["acoes_melhoria"], 1):
            with st.expander(f"Ação {i}: {acao['acao'][:50]}..."):
                st.write(f"**Ação:** {acao['acao']}")
                st.write(f"**Como e Prazos:** {acao['prazo']}")

elif modo == "📊 Relatório":
    st.header("📊 Relatório Geral de Performance")
    
    if not dados:
        st.info("📭 Nenhuma avaliação registrada ainda.")
    else:
        # Preparar dados para visualização
        nomes = []
        totais = []
        classificacoes = []
        cores_map = {"🟢 ALTO DESEMPENHO": "#00A86B", "🟡 MANUTENÇÃO": "#FFD700", "🔴 RISCO": "#FF6B6B"}
        cores = []
        
        for id_col, dados_col in dados.items():
            nomes.append(dados_col["nome"])
            totais.append(dados_col["total_pontos"])
            classificacao = dados_col["classificacao"]
            classificacoes.append(classificacao)
            cores.append(cores_map.get(classificacao, "#667eea"))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total de Colaboradores", len(dados))
        with col2:
            st.metric("Média de Pontos", f"{sum(totais) / len(totais):.1f}/35")
        with col3:
            alto_desempenho = sum(1 for c in classificacoes if "ALTO" in c)
            st.metric("Alto Desempenho", alto_desempenho)
        
        st.divider()
        
        # Gráfico de distribuição de scores
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Distribuição de Pontuações")
            
            fig1 = px.bar(
                x=nomes,
                y=totais,
                color=totais,
                color_continuous_scale=["#FF6B6B", "#FFD700", "#00A86B"],
                labels={"y": "Pontos", "x": "Colaborador"},
                height=400
            )
            fig1.update_layout(showlegend=False)
            st.plotly_chart(fig1, use_container_width=True)
        
        with col2:
            st.subheader("📈 Curva de Vitalidade (Distribuição Normal)")
            
            # Criar histograma dos scores
            fig2 = px.histogram(
                x=totais,
                nbins=10,
                labels={"x": "Pontos", "count": "Quantidade"},
                color_discrete_sequence=["#667eea"],
                height=400
            )
            
            # Adicionar linhas de referência
            fig2.add_vline(x=15, line_dash="dash", line_color="red", annotation_text="Risco")
            fig2.add_vline(x=30, line_dash="dash", line_color="orange", annotation_text="Limite Manutenção")
            fig2.add_vline(x=31, line_dash="dash", line_color="green", annotation_text="Alto Desempenho")
            
            st.plotly_chart(fig2, use_container_width=True)
        
        st.divider()
        
        # Tabela resumida
        st.subheader("📋 Resumo de Todos os Colaboradores")
        
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
        st.subheader("🎯 Análise por Critério")
        
        criterios_medias = {}
        for criterio in ["Organização", "Trabalho em Equipe", "Comunicação e Regras", 
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
            color_discrete_sequence=["#667eea"],
            height=400
        )
        st.plotly_chart(fig3, use_container_width=True)

# Footer
st.divider()
st.caption("☁️ Todos os dados são salvos automaticamente no Google Sheets")