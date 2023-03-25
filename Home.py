import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
import plotly.express as px
import streamlit as st
import streamlit_folium
from streamlit_folium import folium_static
from PIL import Image
from datetime import datetime

pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.max_columns', None)


data = pd.read_csv('kc_house_data.csv')
df = data.copy()

#FUNÇÕES---------------------------------------------------------------------------

def mapa_imoveis(df):
    map = folium.Map([ 47.608013 ,-122.335167],
                tiles='OpenStreetMap',
                zoom_start=9,
                width="%100",height="%100")

    #adc coordenadas
    coordenadas = df[['lat','long']]
    folium.plugins.MarkerCluster(locations=coordenadas).add_to(map)
    return map


#TRATAMENTO DE DADOS---------------------------------------------------------------

#renomeando coluna de notas
df.rename(columns={'grade': 'ratings'}, inplace=True)

#convertendo obj em data
df['date'] = pd.to_datetime(df['date'], format='%Y%m%dT000000')

#convertendo sqft - M²
df['m2_living'] = np.round(df['sqft_living'].apply(lambda x: x * 0.0929))
df['m2_lot'] = np.round(df['sqft_lot'].apply(lambda x: x * 0.0929))

#arredondando quantidade de banheiros
df['bathrooms'] = np.round(df['bathrooms'])

#criando colunas para codificar
#preço
df['price_code'] = df['price'].apply(lambda x: 0 if x < 321950 else
                                            1 if x < 450000 else
                                            2 if x < 645000 else 3)

#area útil 
df['m2_code'] = df['m2_living'].apply(lambda x: 0 if x < 132 else
                                            1 if x < 177 else
                                            2 if x < 236 else 3)

#vista para a agua
df['waterfront'] = df['waterfront'].apply(lambda x: 'Sim' if x == 1 else 'Nao')
#vista
df['view'] = df['view'].apply(lambda x: 'Sim' if x == 1 else 'Nao')

#transformando colunas em int
df['bathrooms'] = df['bathrooms'].astype(int)
df['floors'] = df['floors'].astype(int)


#TITULO DA PÁGINA-------------------------------------------------------------------
st.markdown('#  🏢Visão Geral')
st.markdown("""___""")

#BARRA LATERAL----------------------------------------------------------------------
#anexando imagem
image = Image.open('logo.png')
st.sidebar.image(image, width=120)

#criando barra lateral
#title
st.sidebar.markdown('# House Rocket')
#subtitle
st.sidebar.markdown('## Os melhores imóveis de Seattle!')
#barra separadora
st.sidebar.markdown("""___""")


#subtitle
st.sidebar.markdown('### Filtros')


#multseleção PAISES
water_options = st.sidebar.multiselect(
    'Visão para a água',
    ['Sim','Nao'],
    default=['Sim','Nao'])

#barra separadora
st.sidebar.markdown("""___""")

#multseleção Culinaria
view_options = st.sidebar.multiselect(
    'Visão ampla',
    ['Sim','Nao'],
    default=['Sim','Nao'])

#barra separadora
st.sidebar.markdown("""___""")
#assinatura
st.sidebar.markdown('### Powered by Juan Zimmermann')


#INTERAÇÃO NO FILTRO---------------------------------------------------------------------------

#filtro pais
linhas_selecionadas = df['waterfront'].isin(water_options)
df = df.loc[linhas_selecionadas, :]

# filtro comida
linhas_selecionadas = df['view'].isin(view_options)
df = df.loc[linhas_selecionadas, :]


#LAYOUT PAGINA---------------------------------------------------------------------------------
#title
st.markdown('# House Rocket')
#subtitle
st.markdown('## Melhores Análises Imobiliárias')
#barra separadora
st.markdown("""___""")

#1. linha
st.markdown('## Mapa Imóveis')
map = mapa_imoveis(df)
folium_static(map, width=1024, height=600)



st.write("# House Rocket Dashboard")
st.markdown(
    """
    House Rocket Dashboards foi construído para acompanhar as métricas imobiliarias da região de Seattle.
    ### Como utilizar esse Growth Dashboard?
    - Visão Geral
        - Principais métricas de analise
        - Gráfico da variação do preço por ano de construção
        - Top 5
            - Imóveis com valor de compra mais alto
            - Imóveis com valor de compra mais baixo
        - Relação direta entre valor de venda do imóvel e sua nota de avaliação
        - Variação de preço por dia


    ### Ask for Help
        - LinkedIn: Juan Zimmermann
        - Git Hub: juanzimmer
        - Discord: Juan Zimmermann
""")