import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
import plotly.express as px
import streamlit as st
import streamlit_folium
from PIL import Image
from datetime import datetime

pd.options.display.float_format = '{:.2f}'.format
pd.set_option('display.max_columns', None)


data = pd.read_csv('kc_house_data.csv')
df = data.copy()

#FUNÇÕES---------------------------------------------------------------------------

def preco_ano_construcao(df):
    df_aux = np.round(df.loc[:, ['price', 'yr_built']].groupby('yr_built').mean().reset_index())
    fig = px.line(df_aux, x='yr_built', y='price')
    return fig

def top5_maior(df):
    df_aux = df.loc[:, ['id', 'price', 'bedrooms', 'bathrooms','waterfront', 'view', 'condition', 'ratings', 'm2_living']].sort_values(by='price', ascending=False).head(5)
    return df_aux

def top5_menor(df):
    df_aux = df.loc[:, ['id', 'price', 'bedrooms', 'bathrooms','waterfront', 'view', 'condition', 'ratings', 'm2_living']].sort_values(by='price', ascending=False).head(5)
    return df_aux

def maiores_notas(df):
    df_aux = df[['ratings', 'price']].groupby('ratings').mean().reset_index()
    fig = px.line(df_aux, x='ratings', y='price')
    return fig

def preco_por_dia(df):
    df['day'] = pd.to_datetime(df['date'])
    df_aux = df[['price', 'day']].groupby('day').mean().reset_index()
    fig = px.line(df_aux, x='day', y='price')
    return fig

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


#LAYOUT STREAMLIT (GRÁFICOS)-------------------------------------------------------------------

#1 linha
with st.container():
    col1, col2, col3, col4 = st.columns(4)

    col1.metric('Total de imóveis', df['id'].count())
    col2.metric('Imóveis reformados', len(df[df['yr_renovated'] != 0]))
    col3.metric('Maior preço', df['price'].max())
    col4.metric('Menor preço', df['price'].min())

st.markdown("""___""")

#2 linha
st.header('Preço por ano de construção')
fig = preco_ano_construcao(df)
st.plotly_chart(fig, use_container_width=True)

st.markdown("""___""")


#3 linha
st.markdown('## Top 5')

#3.1 top 5 mais caros
st.markdown('### Maiores Preços')
df_aux = top5_maior(df)
st.dataframe(data=df_aux, use_container_width=True)


#3.2
st.markdown('### Menores Preços')
df_aux = top5_menor(df)
st.dataframe(data=df_aux, use_container_width=True)


st.markdown("""___""")

#4 casa com maiores notas são mais caras
st.markdown('## Relação preço/nota')
fig = maiores_notas(df)
st.plotly_chart(fig, use_container_width=True)


#5 preço(imóvel) por dia
st.markdown('## Preço por dia')
fig = preco_por_dia(df)
st.plotly_chart(fig, use_container_width=True)