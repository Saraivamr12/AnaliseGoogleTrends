import time
import random
import pandas as pd
import requests
from pytrends.request import TrendReq as OriginalTrendReq
import plotly.express as px
import streamlit as st

# Configurar Streamlit
st.set_page_config(page_title="Tendências de Produtos e Categorias", layout="wide")

# ✅ Headers personalizados para evitar bloqueios
HEADERS = {
    'accept': '*/*',
    'accept-language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    'priority': 'u=1',
    'referer': 'https://trends.google.com.br/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'script',
    'sec-fetch-mode': 'no-cors',
    'sec-fetch-site': 'cross-site',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-client-data': 'CIa2yQEIpbbJAQipncoBCNfhygEIkqHLAQiJo8sBCPyYzQEIhaDNAQji0M4BCLPTzgEIodTOAQjv1c4BCPHVzgEIzdjOARjO1c4B',
}

# ✅ Subclasse TrendReq para incluir os headers personalizados
class TrendReq(OriginalTrendReq):
    def _get_data(self, url, method="get", trim_chars=0, **kwargs):
        return super()._get_data(url, method=method, trim_chars=trim_chars, headers=HEADERS, **kwargs)

# ⚙️ Configurar PyTrends com headers customizados
pytrends = TrendReq(hl="en-US", tz=360)

# 📦 Dividindo os produtos em grupos menores
groups = [
    [
        {"product": "ventilador WAP", "category": "ventiladores"},
        {"product": "fone bluetooth WAAW", "category": "fone de ouvido"},
        {"product": "parafusadeira WAP", "category": "ferramenta"},
        {"product": "aspirador robô WAP", "category": "aspiradores robô"}
    ],
    [
        {"product": "caixa de som WAAW", "category": "caixas de som"},
        {"product": "fone de ouvido WAAW", "category": "fone de ouvido"},
        {"product": "ventilador potente WAP", "category": "ventiladores"}
    ],
    [
        {"product": "ventilador de parede WAP", "category": "ventiladores"},
        {"product": "lavadora wap", "category": "lavadora de alta pressão"},
        {"product": "aspirador vertical wap", "category": "aspirador"},
        {"product": "extratora wap", "category": "extratora"}
    ],
]

# 🔍 Função para buscar dados com intervalo aleatório
@st.cache_data
def fetch_trends(product, category):
    """
    Busca dados de tendências do Google Trends para um produto e uma categoria com intervalo aleatório.
    """
    try:
        # 🔎 Consultar dados do produto
        pytrends.build_payload([product], cat=0, timeframe="today 12-m", geo="BR")
        product_data = pytrends.interest_over_time()
        time.sleep(random.uniform(60, 120))  # ⏳ Intervalo aleatório de 30 a 90 segundos

        # 🔎 Consultar dados da categoria
        pytrends.build_payload([category], cat=0, timeframe="today 12-m", geo="BR")
        category_data = pytrends.interest_over_time()
        time.sleep(random.uniform(60, 120))

        # 📊 Combinar os dados
        if not product_data.empty and not category_data.empty:
            product_data = product_data.reset_index().rename(columns={product: "Interest"})
            product_data["Keyword"] = product

            category_data = category_data.reset_index().rename(columns={category: "Interest"})
            category_data["Keyword"] = category

            combined_data = pd.concat([product_data, category_data], ignore_index=True)
            return combined_data
        else:
            return None
    except Exception as e:
        st.error(f"Erro ao buscar dados para {product} ou {category}: {e}")
        return None

# 📊 Interface do Streamlit
st.title("Tendências de Produtos e Categorias no Google Trends")

# 📈 Exibir dados por grupo
for idx, group in enumerate(groups, start=1):
    st.header(f"Grupo {idx}")
    for item in group:
        st.subheader(f"{item['product']} vs {item['category']}")
        data = fetch_trends(item["product"], item["category"])

        if isinstance(data, pd.DataFrame):
            # 📉 Criar gráfico com Plotly
            fig = px.line(
                data,
                x="date",
                y="Interest",
                color="Keyword",
                title=f"Tendências: {item['product']} vs {item['category']}",
                labels={"date": "Data", "Interest": "Interesse", "Keyword": "Palavra-chave"},
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"Nenhum dado disponível para {item['product']} ou {item['category']}")
