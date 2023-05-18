import streamlit as st
import pandas as pd
from pandas import json_normalize
import requests
#from ..notebook.functions import *

@st.cache
def main():

    if __name__ == '__main__':
        main()

st.title("Previsão Esportiva - Futebol")

#API KEY

# request API
payload = {}

headers = {
    "x-rapidapi-key": "c58a251d827eeee96ac5cb890e882cc9",
    "x-rapidapi-host": "v3.football.api-sports.io",
}

#API CALL - caminho para as requisicoes
stream_req = 'https://v3.football.api-sports.io/fixtures?date='
fix_req = "https://v3.football.api-sports.io/fixtures?ids="
odds_req = 'https://v3.football.api-sports.io/odds?fixture='
pred_req = 'https://v3.football.api-sports.io/predictions?fixture='
hxh_req = 'https://v3.football.api-sports.io/fixtures/headtohead?h2h='

#cria um range de datas para +- X dias

from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')

#seleciona a range de datas
import datetime
x_dias_inicio = 0
x_dias_fim = 3

#date = hoje, datet0 = hoje - X dias, datet1 = hoje + X dias
datet0 = (datetime.date.today()) + datetime.timedelta(days=-x_dias_inicio)
datet1 = (datetime.date.today()) + datetime.timedelta(days=+x_dias_fim)

date_list = (pd.date_range(start=datet0, end=datet1,
                           freq='D')).strftime('%Y-%m-%d').tolist()

def req_padrao(req, iterador):

    ls_v = []

    fixrange = req + str(iterador)
    fix_d = requests.request("GET", fixrange, headers=headers, data=payload)
    fix_d = fix_d.json()
    fix_d = json_normalize(fix_d["response"])
    ls_v.append(fix_d)

    return pd.concat(ls_v)

df_stream = pd.concat([req_padrao(stream_req,i) for i in date_list])

df_stream['fixture.hxh'] = (df_stream['teams.home.name']) + " x " + (df_stream['teams.away.name'])

# Function to transform the date format
def transform_date(date_string):
    return date_string.split('T')[0]

# Apply the transformation to the 'fixture.date' column
df_stream['fixture.date'] = df_stream['fixture.date'].apply(transform_date)

# Display a selectbox to choose the city
selected_country = st.selectbox('Selecione um país', df_stream['league.country'].sort_values().unique())

selected_league = st.selectbox('Select uma liga', df_stream[df_stream['league.country']==selected_country]['league.name'].sort_values().unique())

# Filter the dataframe based on the selected city
filtered_df = df_stream[(df_stream['league.country'] == selected_country) & (df_stream['league.name'] == selected_league)][['fixture.date','league.name','fixture.hxh']].rename(columns = {"fixture.date":"Data","league.name":"Liga","fixture.hxh":"Casa x Visitante"}).reset_index(drop = True)

# Display the filtered dataframe
st.dataframe(filtered_df)

select_fixture = st.selectbox('Selecione uma partida', filtered_df['Casa x Visitante'].sort_values().unique())

filtered_fixture_df = filtered_df[filtered_df['Casa x Visitante']==select_fixture]

st.dataframe(filtered_fixture_df)