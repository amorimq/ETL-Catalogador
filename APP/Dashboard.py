import streamlit as st
import pandas as pd
from sqlalchemy import create_engine

# Configuração inicial da página
st.set_page_config(page_title="Base peças", page_icon="", layout="wide")

st.title("Base de peças")

@st.cache_data 
def carregar_dados():
    engine = create_engine('postgresql+psycopg2://usuario_catalogo:pecas@localhost:5433/catalogo_jd')
    query = "SELECT codigo_peca, descricao_curta, descricao_longa, sistema, subsistema FROM fato_pecas_colhedora;"
    df = pd.read_sql(query, engine)
    return df

try:
    df_pecas = carregar_dados()
    st.metric(label="Total de Peças Extraídas", value=len(df_pecas))
    st.dataframe(df_pecas, width='stretch', hide_index=True)
    csv_data = df_pecas.to_csv(index=False, sep=';', encoding='utf-8-sig')
    st.markdown("---")
    st.download_button(
        label="Download base em CSV",
        data=csv_data,
        file_name="catalogo_pecas_colhedora.csv",
        mime="text/csv"
    )
    
except Exception as e:
    st.error(f"Erro ao conectar com o banco de dados: {e}")