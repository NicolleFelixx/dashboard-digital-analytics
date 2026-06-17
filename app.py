"""
📊 Digital Analytics Dashboard — E-commerce
Dashboard interativo de métricas de aquisição e conversão.

Para rodar localmente:
    streamlit run app.py

⚠️ Dados sintéticos, gerados para fins de demonstração (ver generate_data.py).
"""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# ---- paleta de cores (mesma identidade do perfil) ----
ROSA = "#F72585"
ROXO = "#9D4EDD"
SEQUENCIA = ["#F72585", "#9D4EDD", "#7B2FF7", "#B5179E", "#FF8FAB", "#C792EA"]

# ====================================================================
# CONFIGURAÇÃO DA PÁGINA
# ====================================================================
st.set_page_config(
    page_title="Digital Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)


# ====================================================================
# CARREGAR DADOS (com cache para não reler o arquivo a cada interação)
# ====================================================================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("data/ga4_ecommerce_sample.csv", parse_dates=["data"])
    return df


df = carregar_dados()

# ====================================================================
# SIDEBAR — FILTROS
# ====================================================================
st.sidebar.title("🎛️ Filtros")

data_min, data_max = df["data"].min(), df["data"].max()
periodo = st.sidebar.date_input(
    "Período",
    value=(data_min, data_max),
    min_value=data_min,
    max_value=data_max,
)

canais = st.sidebar.multiselect(
    "Canais",
    options=sorted(df["canal"].unique()),
    default=sorted(df["canal"].unique()),
)

dispositivos = st.sidebar.multiselect(
    "Dispositivos",
    options=sorted(df["dispositivo"].unique()),
    default=sorted(df["dispositivo"].unique()),
)

st.sidebar.markdown("---")
st.sidebar.caption("⚠️ Dados sintéticos para demonstração.")

# aplica os filtros
if len(periodo) == 2:
    inicio, fim = pd.to_datetime(periodo[0]), pd.to_datetime(periodo[1])
    mask = (df["data"] >= inicio) & (df["data"] <= fim)
else:
    mask = pd.Series(True, index=df.index)

dff = df[mask & df["canal"].isin(canais) & df["dispositivo"].isin(dispositivos)]

# ====================================================================
# CABEÇALHO
# ====================================================================
st.title("📊 Digital Analytics Dashboard — E-commerce")
st.markdown("Métricas de **aquisição, comportamento e conversão** por canal e dispositivo.")

if dff.empty:
    st.warning("Nenhum dado para os filtros selecionados. Ajuste os filtros na barra lateral.")
    st.stop()

# ====================================================================
# KPIs PRINCIPAIS
# ====================================================================
total_sessoes = int(dff["sessoes"].sum())
total_usuarios = int(dff["usuarios"].sum())
total_compras = int(dff["compras"].sum())
total_receita = float(dff["receita"].sum())
taxa_conversao = (total_compras / total_sessoes * 100) if total_sessoes else 0
ticket_medio = (total_receita / total_compras) if total_compras else 0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Sessões", f"{total_sessoes:,}".replace(",", "."))
c2.metric("Usuários", f"{total_usuarios:,}".replace(",", "."))
c3.metric("Taxa de Conversão", f"{taxa_conversao:.2f}%")
c4.metric("Receita", f"R$ {total_receita:,.0f}".replace(",", "."))
c5.metric("Ticket Médio", f"R$ {ticket_medio:,.0f}".replace(",", "."))

st.markdown("---")

# ====================================================================
# LINHA 1: sessões ao longo do tempo  +  receita por canal
# ====================================================================
col_a, col_b = st.columns([2, 1])

with col_a:
    st.subheader("Sessões ao longo do tempo")
    serie = dff.groupby("data", as_index=False)["sessoes"].sum()
    fig = px.area(serie, x="data", y="sessoes")
    fig.update_traces(line_color=ROSA, fillcolor="rgba(247,37,133,0.2)")
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), height=320)
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader("Receita por canal")
    por_canal = dff.groupby("canal", as_index=False)["receita"].sum().sort_values("receita")
    fig = px.bar(por_canal, x="receita", y="canal", orientation="h",
                 color="canal", color_discrete_sequence=SEQUENCIA)
    fig.update_layout(showlegend=False, margin=dict(t=10, b=0, l=0, r=0), height=320,
                      yaxis_title=None, xaxis_title="R$")
    st.plotly_chart(fig, use_container_width=True)

# ====================================================================
# LINHA 2: funil de conversão  +  receita por dispositivo
# ====================================================================
col_c, col_d = st.columns(2)

with col_c:
    st.subheader("Funil de conversão")
    etapas = ["Sessões", "Visualizações de produto", "Add ao carrinho", "Compras"]
    valores = [
        dff["sessoes"].sum(),
        dff["product_views"].sum(),
        dff["add_to_cart"].sum(),
        dff["compras"].sum(),
    ]
    fig = go.Figure(go.Funnel(
        y=etapas, x=valores,
        marker={"color": SEQUENCIA[:4]},
        textinfo="value+percent initial",
    ))
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), height=340)
    st.plotly_chart(fig, use_container_width=True)

with col_d:
    st.subheader("Receita por dispositivo")
    por_disp = dff.groupby("dispositivo", as_index=False)["receita"].sum()
    fig = px.pie(por_disp, names="dispositivo", values="receita", hole=0.55,
                 color_discrete_sequence=SEQUENCIA)
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), height=340)
    st.plotly_chart(fig, use_container_width=True)

# ====================================================================
# TABELA: desempenho por canal
# ====================================================================
st.subheader("Desempenho por canal")
resumo = dff.groupby("canal").agg(
    sessoes=("sessoes", "sum"),
    compras=("compras", "sum"),
    receita=("receita", "sum"),
).reset_index()
resumo["taxa_conversao_%"] = (resumo["compras"] / resumo["sessoes"] * 100).round(2)
resumo = resumo.sort_values("receita", ascending=False)
st.dataframe(resumo, use_container_width=True, hide_index=True)

st.caption("Feito com Streamlit por Nicolle Felix • Dados sintéticos para demonstração")
