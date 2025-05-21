import streamlit as st
import pandas as pd
import altair as alt
from collections import Counter
import re

st.set_page_config(page_title="Dashboard VendaSimples", layout="wide")

st.title("📊 Dashboard de Scraping – ERP & Gestão Empresarial")
st.markdown("Análise das páginas e posições capturadas no Google com base no termo **ERP** e concorrência de mercado.")

# Upload do arquivo JSON
uploaded_file = st.file_uploader("📁 Faça o upload do arquivo JSON gerado pelo scraping", type="json")

if uploaded_file:
    df = pd.read_json(uploaded_file)

    # Domínio do link
    df["domínio"] = df["link"].apply(lambda x: x.split("/")[2] if isinstance(x, str) else "N/A")

    # Layout de colunas
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌐 Top 10 domínios mais frequentes")
        dominios = df["domínio"].value_counts().reset_index()
        dominios.columns = ["Domínio", "Frequência"]
        chart = alt.Chart(dominios.head(10)).mark_bar().encode(
            x="Frequência:Q",
            y=alt.Y("Domínio:N", sort="-x"),
            tooltip=["Domínio", "Frequência"]
        ).properties(height=400)
        st.altair_chart(chart, use_container_width=True)

    with col2:
        st.subheader("📈 Posição Média no Google (quanto menor, melhor)")
        posicao_media = df.groupby("domínio")["positionOverall"].mean().reset_index().sort_values(by="positionOverall")
        posicao_media.columns = ["Domínio", "Posição Média"]
        st.dataframe(posicao_media.head(10))

    st.markdown("---")

    # Palavras mais comuns nos títulos
    st.subheader("🔑 Palavras mais frequentes nos títulos")
    palavras = []
    for titulo in df["title"].dropna():
        palavras.extend(re.findall(r'\b\w{4,}\b', titulo.lower()))
    contagem = Counter(palavras)
    df_palavras = pd.DataFrame(contagem.items(), columns=["Palavra", "Frequência"]).sort_values(by="Frequência", ascending=False)
    st.dataframe(df_palavras.head(20))

    st.markdown("---")

    # Snippets mais extensos (potencial educativo)
    st.subheader("📚 Snippets mais ricos em conteúdo (educativos)")
    df["snippet_len"] = df["snippet"].apply(lambda x: len(x.split()) if isinstance(x, str) else 0)
    top_snippets = df.sort_values(by="snippet_len", ascending=False)[["title", "snippet", "link"]].head(5)

    for _, row in top_snippets.iterrows():
        st.markdown(f"**🔹 {row['title']}**")
        st.markdown(f"`{row['link']}`")
        st.write(row['snippet'])
        st.markdown("---")

    st.success("✅ Análise finalizada com sucesso.")
else:
    st.info("Faça o upload do seu arquivo `.json` gerado pelo scraping para visualizar o dashboard.")
