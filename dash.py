import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout='wide') #Realiza a mudança de layout do streamlit para página toda

df = pd.read_csv('dados_vendas.csv', delimiter=';', encoding='ISO-8859-1')#leitura do arquivo CSV com a biblioteca pandas

df["DATA_VENDA"] = pd.to_datetime(df["DATA_VENDA"]) #conversão da coluna DATA_VENDA para uma coluna com valor de data/hora
df  = df.sort_values("DATA_VENDA") #ordenando a coluna DATA_VENDA para ordem crescente

#verificando quantos meses tem no DataFrame

df["MES"] = df["DATA_VENDA"].apply(lambda x: str(x.month) + "-" + str(x.year))
#criando uma coluna mês no df, aplicando uma função que busque o mês e o ano

#inserindo a select box na lateral

mes = st.sidebar.selectbox("Mês", df["MES"].unique()) 
#variavel mÊs irá buscar no streamlit, uma barra lateral
#que possibilita que você possa realizar buscas por meio do mês

#FILTRO DE MÊS

df_filtro = df[df["MES"] == mes]
df_filtro

#criação de colunas no dashboard

col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

fig_date = px.bar(df_filtro, x = "DATA_VENDA", y = "VALOR_TOTAL", color = "LOJA", title="Faturamento por Dia")
col1.plotly_chart(fig_date)

fig_prod = px.bar(df_filtro, x = "VALOR_TOTAL", y = "PRODUTO", color="LOJA", title="faturamento por Produto")
col2.plotly_chart(fig_prod)

loja_total = df_filtro.groupby("LOJA")[["VALOR_TOTAL"]].sum().reset_index()
fig_loja = px.bar(loja_total, x= "LOJA", y = "VALOR_TOTAL", color="LOJA", title="Faturamento por Loja" )
col3.plotly_chart(fig_loja)

fig_pagto = px.pie(df_filtro, values="VALOR_TOTAL", names="FORMA_PAGAMENTO", title="Faturamento por tipo de pagamento")
col4.plotly_chart(fig_pagto)


















