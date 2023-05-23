# manipular dados
import pandas as pd
from pandas import json_normalize
import numpy as np
from ast import literal_eval

# requisicoes de API
import requests
import json

# manipular datas
import time
import datetime

# manipular strings
from unidecode import unidecode

# remover warnings
import warnings

warnings.simplefilter("ignore")

# request API
payload = {}

headers = {
    "x-rapidapi-key": "c58a251d827eeee96ac5cb890e882cc9",
    "x-rapidapi-host": "v3.football.api-sports.io",
}

def req_padrao(req, iterador):
    """
    tanto as funções req_padrao, req_alt e req_odds agilizam o processo de fazer as requisições à API, já entregando os dados de forma estruturada para manipulação

    args: req - caminho para o endpoint da requisição
    iterador: coluna onde está o id necessário para a validade da requisição (normalmente, o fixture.id)


    returns:

    """
    ls_v = []

    fixrange = req + str(iterador)
    fix_d = requests.request("GET", fixrange, headers=headers, data=payload)
    fix_d = fix_d.json()
    fix_d = json_normalize(fix_d["response"])
    ls_v.append(fix_d)

    return pd.concat(ls_v)

def req_alt(req, iterador):
    ls_v = []

    fixrange = req + str(iterador)
    fix_d = requests.request("GET", fixrange, headers=headers, data=payload)
    fix_d = fix_d.json()
    fix_d = json_normalize(fix_d["response"])
    fix_d["fixture.id"] = iterador
    ls_v.append(fix_d)

    return pd.concat(ls_v)

def req_hxh(req, iterador1, iterador2):
    ls_v = []

    fixrange = req + str(iterador1)
    fix_d = requests.request("GET", fixrange, headers=headers, data=payload)
    fix_d = fix_d.json()
    fix_d = json_normalize(fix_d["response"])
    fix_d["fixture.id.ns"] = iterador2
    ls_v.append(fix_d)

    return pd.concat(ls_v)

def flatten_nested_json_df(df):
    """
    abre um Json até o último nível, trazendo todas as colunas para o nível mais alto,
    no processo, repete alguns valores para as linhas
    args:
        df (DataFrame): dataframe contendo colunas em Json
    returns:
        df (DataFrame): dataframe contendo todas as informacoes do Json

    notes:
        em certos Json com muitas informações, pode ocorrer um MemoryError. Recomenda combinar a função com
        .explode() e json_normalize(record_path = [], meta = []) para melhores resultados
    """

    df = df.reset_index()
    s = (df.applymap(type) == list).all()
    list_columns = s[s].index.tolist()
    s = (df.applymap(type) == dict).all()
    dict_columns = s[s].index.tolist()
    while len(list_columns) > 0 or len(dict_columns) > 0:
        new_columns = []
        for col in dict_columns:
            horiz_exploded = pd.json_normalize(df[col]).add_prefix(f"{col}.")
            horiz_exploded.index = df.index
            df = pd.concat([df, horiz_exploded], axis=1).drop(columns=[col])
            new_columns.extend(horiz_exploded.columns)
        for col in list_columns:
            df = df.drop(columns=[col]).join(df[col].explode().to_frame())
            new_columns.append(col)
        s = (df[new_columns].applymap(type) == list).all()
        list_columns = s[s].index.tolist()
        s = (df[new_columns].applymap(type) == dict).all()
        dict_columns = s[s].index.tolist()
    return df

def transform_fixture(df):
    """
    utilizado no output das requisições de partidas/fixtures
    realiza a abertura e manipulação para o formato desejado para as colunas
    statistics, players, lineups e events

    args:
        df (DataFrame): dataframe de partidas contendo as colunas 'statistics', 'players', 'lineups' e 'events'

    returns:
        {nome_desejado} (List): list com 4 dataframes contendo em
        [0] = events
        [1] = lineups
        [2] = players
        [3] = statistics
    """

    # abre o json da coluna 'statistics'
    statistics = []

    for i, j in zip(range(df.shape[0]), df["fixture.id"]):
        try:
            st = json_normalize(
                df["statistics"].iloc[i],
                record_path=["statistics"],
                meta=[["team", "id"], ["team", "name"], ["team", "logo"]],
            )

            st = pd.pivot(
                st,
                index=["team.name", "team.id", "team.logo"],
                columns=["type"],
                values=["value"],
            ).reset_index()

            # st.index = st.reset_index()['index']

            st["fixture.id"] = j

            statistics.append(st)

        except Exception:
            pass

    try:
        sts = pd.concat(statistics)
    except Exception:
        pass

    # renomeia as colunas removendo o multi_index 'value'
    cols = sts.columns
    cols = [col[1] if col[0] == "value" else col[0] for col in cols]
    sts.columns = cols

    # transformar as variáveis BP e P% em numéricas
    sts["Ball Possession"] = sts["Ball Possession"].str.strip("%").astype(float)
    sts["Passes %"] = sts["Passes %"].str.strip("%").astype(float)

    # transforma as demais colunas em numéricas
    for i in sts.iloc[:, 3:].columns:
        sts[i].astype(float)

    sts.iloc[:, 3:] = sts.iloc[:, 3:].astype(float)

    # abre o json da coluna 'players'
    players = []

    for i, j in zip(range(df.shape[0]), df["fixture.id"]):
        try:
            pl = flatten_nested_json_df(
                json_normalize(
                    df["players"].iloc[i],
                    ["players"],
                    [["team", "name"], ["team", "id"], ["team", "logo"]],
                )
            )

            pl["fixture.id"] = j

            players.append(pl)

        except Exception:
            pass

    try:
        pls = pd.concat(players)
    except Exception:
        pass

    # ajustes nos dados de players
    # passes accuracy - transforma em variável numérica
    pls["statistics.passes.accuracy"] = [
        str(value).replace("%", "") if value != "None" else value
        for value in pls["statistics.passes.accuracy"]
    ]
    pls["statistics.passes.accuracy"] = (
        pls["statistics.passes.accuracy"].replace("None", np.nan).astype(float)
    )

    # passes accuracy - calcula a média por time
    pls_pa = (
        pls[["statistics.passes.accuracy", "fixture.id", "team.name", "team.id"]]
        .groupby(["fixture.id", "team.name", "team.id"], as_index=False)
        .mean()
        .iloc[:, 3]
    )

    # games rating - transforma em variável numérica - agrupa Goleiro dentro de Defesa
    pls["statistics.games.rating"] = (
        pls["statistics.games.rating"].replace("-", np.nan).replace("–", np.nan)
    )
    pls["statistics.games.rating"] = pls["statistics.games.rating"].astype(float)
    pls["statistics.games.position"] = pls["statistics.games.position"].str.replace(
        "G", "D"
    )

    # games rating - calcula a média por time e por grupo (F, D, M)
    plrt = (
        pls.groupby(
            ["fixture.id", "team.id", "statistics.games.position"], as_index=False
        )[["statistics.games.rating"]]
        .mean()
        .sort_values(by=["fixture.id", "team.id"])
    )
    plrt = plrt.pivot(
        values="statistics.games.rating",
        index=["fixture.id", "team.id"],
        columns="statistics.games.position",
    )
    plrt.columns = [f"statistics.games.rating.{col}" for col in plrt.columns]
    try:
        plrt = plrt.drop(columns="statistics.games.rating.SUB").reset_index()
    except Exception:
        pass

    # games rating - calcula a média geral por time
    pls_gr = (
        pls[["statistics.games.rating", "fixture.id", "team.name", "team.id"]]
        .groupby(["fixture.id", "team.name", "team.id"], as_index=False)
        .mean()
        .iloc[:, 3]
    )

    # filtra as variáveis de interesse
    pls = pls.filter(
        [
            "team.id",
            "team.name",
            "team.logo",
            "fixture.id",
            "league_round",
            "statistics.offsides",
            "statistics.shots.total",
            "statistics.shots.on",
            "statistics.goals.total",
            "statistics.goals.conceded",
            "statistics.goals.assists",
            "statistics.goals.saves",
            "statistics.passes.total",
            "statistics.passes.key",
            "statistics.passes.accuracy",
            "statistics.tackles.total",
            "statistics.tackles.blocks",
            "statistics.tackles.interceptions",
            "statistics.duels.total",
            "statistics.duels.won",
            "statistics.dribbles.attempts",
            "statistics.dribbles.success",
            "statistics.dribbles.past",
            "statistics.fouls.drawn",
            "statistics.fouls.committed",
            "statistics.cards.yellow",
            "statistics.cards.red",
            "statistics.penalty.won",
            "statistics.penalty.commited",
            "statistics.penalty.scored",
            "statistics.penalty.missed",
            "statistics.penalty.saved",
            "statistics.games.rating",
        ]
    )

    # transforma as variáveis filtradas em float
    for i in pls.iloc[:, 3:].columns:
        pls[i] = pls[i].astype(float)

    # realiza a soma por time
    pls = pls.groupby(["fixture.id", "team.name", "team.id"], as_index=False).sum()

    # substitui a variável passes accuracy e games rating
    pls["statistics.passes.accuracy"] = pls_pa
    pls["statistics.games.rating"] = pls_gr

    # faz um merge dos ratings por time/grupo
    pls = pls.merge(plrt, on=["fixture.id", "team.id"])

    # abre o json da coluna 'lineups'
    lineups = []

    for i, j in zip(range(df.shape[0]), df["fixture.id"]):
        try:
            lp = json_normalize(df["lineups"].iloc[i])
            lp["fixture.id"] = j
            lineups.append(lp)

        except Exception:
            pass

    lps = pd.concat(lineups)
    lps = lps.iloc[:, :]

    # ver o time inteiro
    # titulares #flatten_nested_json_df(json_normalize(df['lineups'].iloc[3]).drop(columns = 'substitutes'))
    # substitutos #flatten_nested_json_df(json_normalize(df['lineups'].iloc[3]).drop(columns = 'startXI'))

    # abre o json da coluna 'events'
    events = []

    for i, j in zip(range(df.shape[0]), df["fixture.id"]):
        try:
            ev = json_normalize(df["events"].iloc[i])

            ev = ev.groupby(["team.id", "detail"], as_index=False).count()

            ev = ev.pivot_table(
                index=["team.id"], columns="detail", values="type"
            ).reset_index()

            ev["fixture.id"] = j

            events.append(ev)

        except Exception:
            pass

    evts = pd.concat(events)

    return evts, lps, pls, sts
