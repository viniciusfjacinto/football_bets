import streamlit as st
import pandas as pd
from pandas import json_normalize
import requests
st.set_option('deprecation.showPyplotGlobalUse', False)
import matplotlib.pyplot as plt
# from ..notebook.functions import req_c
# from ..notebook.functions import req_padrao


@st.cache
def main():

    if __name__ == '__main__':
        main()

st.title("Previsão Esportiva - Futebol")

#API KEY

# request API
payload = {}

headers = {
    "x-rapidapi-key": "#####################",
    "x-rapidapi-host": "v3.football.api-sports.io",
}

#API CALL - caminho para as requisicoes
stream_req = 'https://v3.football.api-sports.io/fixtures?date='
fix_req = "https://v3.football.api-sports.io/fixtures?ids="
odds_req = 'https://v3.football.api-sports.io/odds?fixture='
pred_req = 'https://v3.football.api-sports.io/predictions?fixture='
hxh_req = 'https://v3.football.api-sports.io/fixtures/headtohead?h2h='


#CSS Style
#working on

#cria um range de datas para +- X dias

from datetime import datetime
date = datetime.today().strftime('%Y-%m-%d')

#seleciona a range de datas
import datetime
x_dias_inicio = 0
x_dias_fim = 8

#date = hoje, datet0 = hoje - X dias, datet1 = hoje + X dias
datet0 = (datetime.date.today()) + datetime.timedelta(days=-x_dias_inicio)
datet1 = (datetime.date.today()) + datetime.timedelta(days=+x_dias_fim)

date_list = (pd.date_range(start=datet0, end=datet1,
                           freq='D')).strftime('%Y-%m-%d').tolist()


#select boxes
def req_padrao(req, iterador):
    ls_v = []

    fixrange = req + str(iterador)
    fix_d = requests.request("GET", fixrange, headers=headers, data=payload)
    fix_d = fix_d.json()
    fix_d = json_normalize(fix_d["response"])
    ls_v.append(fix_d)

    return pd.concat(ls_v)

def req_c():
    countries = []
    fixrange = "https://v3.football.api-sports.io/countries"
    fix_c = requests.request("GET", fixrange, headers=headers, data=payload)
    fix_c = fix_c.json()
    fix_c = json_normalize(fix_c["response"])
    countries.append(fix_c)

    df_countries = pd.concat(countries)

    return list(df_countries['name'])

def req_l_by_c(country):
    leagues = []
    fixrange = "https://v3.football.api-sports.io/leagues?country=" + str(country)
    fix_l = requests.request("GET", fixrange, headers=headers, data=payload)
    fix_l = fix_l.json()
    fix_l = json_normalize(fix_l["response"])
    leagues.append(fix_l)

    df_leagues = pd.concat(leagues)

    return df_leagues

def req_padrao_byc_byl(league,date):
    ls_v = []

    fixrange =  "https://v3.football.api-sports.io/fixtures?league="+str(league) +"&season="+ str(date)[:4] + "&date=" + str(date)
    fix_d = requests.request("GET", fixrange, headers=headers, data=payload)
    fix_d = fix_d.json()
    fix_d = json_normalize(fix_d["response"])
    ls_v.append(fix_d)

    return pd.concat(ls_v)


country = list(req_c())
#
index_country = country.index('Brazil')
selected_country = st.sidebar.selectbox('País', country, index=index_country)
#

league= req_l_by_c(selected_country)
#
index_league = league.index[0]


selected_league = st.sidebar.selectbox('Liga',list(league['league.name']), index = 0)
#

selected_dates = st.sidebar.selectbox("Selecione uma data",date_list)
#

try:
    df_stream = req_padrao_byc_byl(league[league['league.name']==str(selected_league)]['league.id'][0],str(selected_dates))


    # #transformations
    df_stream['fixture.hxh'] = (df_stream['teams.home.name']) + " x " + (df_stream['teams.away.name'])

    # # Function to transform the date format
    def transform_date(date_string):
        return date_string.split('T')[0]

    # # Apply the transformation to the 'fixture.date' column
    df_stream['fixture.date'] = df_stream['fixture.date'].apply(transform_date)

    df_stream = df_stream.rename(columns = {'fixture.hxh':'Casa x Visitante', 'fixture.date': 'Data da Partida'})


    select_fixture = st.sidebar.selectbox('Partida', df_stream['Casa x Visitante'].sort_values().unique())



    filtered_fixture_df = df_stream[df_stream['Casa x Visitante']==select_fixture]

    selected_id = st.sidebar.selectbox('ID da partida', df_stream[df_stream['Casa x Visitante']==select_fixture]['fixture.id'].sort_values().unique(), disabled=True)

    def req_pred(id):
        fixrange = f'https://v3.football.api-sports.io/predictions?fixture={id}'
        fix_d = requests.request("GET", fixrange, headers=headers, data=payload)
        fix_d = fix_d.json()
        fix_d = json_normalize(fix_d["response"])
        fix_d['fixture.id'] = selected_id
        return fix_d

    predictions= (req_pred(selected_id))
    #st.write(predictions.iloc[:,1:].T)


    def viz_radar(df_predictions):
        """
        utilizado para visualizacao das previsões geradas pela API para uma partida em questão

        args:
            df (DataFrame): dataframe de previsoes

        returns:
            radar: gráficos de diferença percentual entre variáveis do time
            'form, att, def, poisson, h2h' e previsão sugerida
            gráfico em formato radar/teia-de-aranha
        """

        from math import pi

        # df_predictions[
        #     [
        #         "fixture.id",
        #         "teams.home.name",
        #         "teams.away.name",
        #         "predictions.advice",
        #     ]
        # ]

        comp = pd.concat(
            [
                df_predictions[["teams.home.name", "teams.away.name"]],
                df_predictions[
                    [
                        "comparison.form.home",
                        "comparison.form.away",
                        "comparison.att.home",
                        "comparison.att.away",
                        "comparison.def.home",
                        "comparison.def.away",
                        "comparison.poisson_distribution.home",
                        "comparison.poisson_distribution.away",
                        "comparison.h2h.home",
                        "comparison.h2h.away",
                        "comparison.goals.home",
                        "comparison.goals.away",
                        "comparison.total.home",
                        "comparison.total.away",
                    ]
                ],
            ],
            axis=1,
        )

        X = comp.filter(regex=".home")
        X.columns = X.columns.str.replace(".home", "")
        Y = comp.filter(regex=".away")
        Y.columns = Y.columns.str.replace(".away", "")

        compxy = pd.concat([X, Y])
        for i in compxy.iloc[:, 1:].columns:
            compxy[i] = compxy[i].str.replace("%", "").astype(float)

        compxy.columns = compxy.columns.str.replace("comparison.", "")

        df = compxy

        fig, ax = plt.subplots(figsize=(6, 6))
        # number of variable
        categories = list(df)[1:]
        N = len(categories)

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        ax = plt.subplot(111, polar=True)

        # If you want the first axis to be on top:
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)

        # Draw one axe per variable + add labels
        plt.xticks(angles[:-1], categories)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks(
            [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
            ["10", "20", "30", "40", "50", "60", "70", "80", "90", "100"],
            color="grey",
            size=10,
        )
        plt.ylim(0, 100)

        # Ind1

        values = df.iloc[0, 1:].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1.2, linestyle="solid", label=compxy.iloc[0, 0])
        ax.fill(angles, values, "b", alpha=0.1)

        # Ind2
        values = df.iloc[1, 1:].values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1.2, linestyle="solid", label=compxy.iloc[1, 0])
        ax.fill(angles, values, "r", alpha=0.1)

        # Add legend
        plt.legend(loc="upper right", bbox_to_anchor=(0.1, 0.1))

        # observation
        plt.figtext(
            0.97,
            0.5,
            str(list(df_predictions["predictions.advice"]))
            .replace("[", "")
            .replace("]", "")
            .replace("'", ""),
        )

        # Show the graph
        radar = plt.show
        radar_st = st.pyplot()
        return radar_st

    viz_radar(predictions)

except Exception:
    st.write(f"Não haverão partidas para a {selected_league} no dia {selected_dates[-2:]}, por favor selecione outra data")
