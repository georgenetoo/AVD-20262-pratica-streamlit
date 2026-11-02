import pandas as pd
import streamlit as st  # [IA] Claude Code – import necessário para usar o @st.cache_data


# [IA] Claude Code – @st.cache_data guarda o resultado na memória: o CSV (~213 mil linhas)
# é lido só na primeira vez, e não a cada clique num widget
@st.cache_data
def load_data(path="data/clean/dataset.csv"):
    """Lê o dataset já tratado (exportado ao final do notebook de EDA)."""
    df = pd.read_csv(path)
    # [IA] Claude Code – converte a coluna Data (texto "AAAA-MM-DD") para o tipo datetime
    df["Data"] = pd.to_datetime(df["Data"], format="%Y-%m-%d")
    return df
