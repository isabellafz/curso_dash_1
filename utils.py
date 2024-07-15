from dataset import df
import pandas as pd
import streamlit as st
import time

def format_number(value, prefix= ''):
    for unit in ['', 'mil']:
        if value < 1000:
            return f'{prefix} {value:.2f} {unit}'
        value /= 1000
    return f'{prefix} {value:.2f} milhões'


#  DataFrame Receita por estado
df_rec_estado = df.groupby('Local da compra')[['Preço']].sum()
df_rec_estado = df.drop_duplicates(subset='Local da compra')[['Local da compra', 'lat', 'lon']].merge(df_rec_estado, left_on='Local da compra', right_index=True).sort_values('Preço', ascending=False)


# DataFrame receita mensal
df_rec_mensal = df.set_index('Data da Compra').groupby(pd.Grouper(freq='M'))['Preço'].sum().reset_index()
df_rec_mensal['Ano'] = df_rec_mensal['Data da Compra'].dt.year
df_rec_mensal['Mes'] = df_rec_mensal['Data da Compra'].dt.month_name()


#DataFrame receita por categoria

df_rec_categoria = df.groupby('Categoria do Produto')[['Preço']].sum().sort_values('Preço', ascending=False)


#DataFrame vendedor

df_vendedores = pd.DataFrame(df.groupby('Vendedor')['Preço'].agg(['sum', 'count']))


# agg e um metodo de agregação, e usamos o .gg para somar todos os valores
# de cada vendedor e contar as vendas de cada um


#função para converter em arquivo csv

@st.cache_data
def convert_csv(df):
    return df.to_csv(index=False).encode('utf-8')


def mensagem_sucesso():
    sucess = st.sucess(
        'Arquivo baixado com sucesso',
        ico="✅",
        
        )
    time.sleep(4)
    sucess.empty()