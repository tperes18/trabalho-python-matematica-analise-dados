# No terminal, caso ainda não possua as seguintes dependências, execute:
# > pip install -r requirements.txt
# OU
# > pip install xlrd
# > pip install streamlit
# > pip install plotly

# Instale a extensão "Streamlit Runner" no VSCode
# Para rodar o arquivo, clique com o botão direito e selecione "Run with Streamlit" OU execute no terminal "python -m streamlit run app.py"

import streamlit as st
import pandas as pd 
import plotly.express as px

path = "CD2022_Populacao_2010_Compatibilizada_20231222.xlsx"

# Linha 0 vazia, linha 1 título, linha 2 cabeçalho (header=2)
df = pd.read_excel(path, header=2)

# ============================================================
# População nos anos 2010 e 2022
# ============================================================
st.header("Comparação de população nos anos 2010 e 2022:")
df = df.iloc[:, 1:8].copy()
df.columns = [
    "UF",
    "COD_UF",
    "COD_MUNIC",
    "Município",
    "pop_2010_sinopse",
    "2010",  # população 2010 compatibilizada
    "2022",  # Censo 2022
]
df.head()


st.dataframe(df)

# ============================================================
# População agregada por estado
# ============================================================
st.subheader("População agregada por estado")
pop_estado = (
    df.groupby("UF")[["2010", "2022"]]
    .sum()
    .reset_index()
)

pop_estado["Crescimento"] = pop_estado["2022"] - pop_estado["2010"]
pop_estado["Crescimento_pct"] = (pop_estado["Crescimento"] / pop_estado["2010"] * 100).round(2)

pop_estado = (
    pop_estado
    .sort_values(by="Crescimento", ascending=False)
    .reset_index(drop=True)
)


st.dataframe(pop_estado)

# ============================================================
# População por município
# ============================================================
st.subheader("População por município")
pop_municipio = (
    df.groupby(["UF", "Município"])[["2010", "2022"]]
    .sum()
    .reset_index()
)

pop_municipio["Crescimento"] = pop_municipio["2022"] - pop_municipio["2010"]
pop_municipio = (
    pop_municipio
    .sort_values(by="Crescimento", ascending=False)
    .reset_index(drop=True)
)

print("População por município:")

pop_municipio.to_csv("populacao_por_municipio.csv", index=False, encoding="utf-8-sig")
print("Arquivo populacao_por_municipio.csv salvo.")

