import pandas as pd

def viz_radar(df_predictions):
    
    '''
    utilizado para visualizacao das previsões geradas pela API para uma partida em questão
    
    args:
        df (DataFrame): dataframe de previsoes
    
    returns:
        radar: gráficos de diferença percentual entre variáveis do time 
        'form, att, def, poisson, h2h' e previsão sugerida
        gráfico em formato radar/teia-de-aranha
    '''
    import matplotlib.pyplot as plt
    from math import pi
    
    df_predictions[['fixture.id','teams.home.id','teams.home.name','teams.away.name','teams.away.id','predictions.advice']]

    comp = pd.concat([df_predictions[['teams.home.name','teams.away.name']],df_predictions[['comparison.form.home',
     'comparison.form.away',
     'comparison.att.home',
     'comparison.att.away',
     'comparison.def.home',
     'comparison.def.away',
     'comparison.poisson_distribution.home',
     'comparison.poisson_distribution.away',
     'comparison.h2h.home',
     'comparison.h2h.away',
     'comparison.goals.home',
     'comparison.goals.away',
     'comparison.total.home',
     'comparison.total.away']]], axis = 1)

    X = comp.filter(regex='.home')
    X.columns = X.columns.str.replace('.home','')
    Y = comp.filter(regex='.away')
    Y.columns = Y.columns.str.replace('.away','')

    compxy = pd.concat([X,Y])
    for i in compxy.iloc[:,1:].columns:
        compxy[i] = compxy[i].str.replace('%','').astype(float)

    compxy.columns = compxy.columns.str.replace('comparison.','')

    df = compxy

    fig,ax = plt.subplots(figsize = (6,6))
    # number of variable
    categories=list(df)[1:]
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
    plt.yticks([10,20,30,40,50,60,70,80,90,100], ["10","20","30","40","50","60","70","80","90","100"], color="grey", size=10)
    plt.ylim(0,100)

    # Ind1

    values=df.iloc[0,1:].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1.2, linestyle='solid', label=compxy.iloc[0,0])
    ax.fill(angles, values, 'b', alpha=0.1)

    # Ind2
    values=df.iloc[1,1:].values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1.2, linestyle='solid', label=compxy.iloc[1,0])
    ax.fill(angles, values, 'r', alpha=0.1)

    # Add legend
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # observation
    plt.figtext(.97, 0.5, str(list(df_predictions['predictions.advice'])).replace('[','').replace(']','').replace("'",""))


    # Show the graph
    radar = plt.show
    
    return radar

def viz_stacked(viz):
    
     '''
    utilizado para visualizacao das estatísticas de confrontos anteriores entre 2 times
    
    args:
        viz (DataFrame): dataframe final com todas as informações do conflito
    
    returns:
        stacked: gráfico de barras empilhadas que vão de 0 à 100%, comparando alguns destaques dos times em seus últimos confrontos
    '''
        
    import seaborn as sns
    sns.set(style = 'white')
    sns.set_palette("Set2")

    viz = viz[['teams.name','statistics.games.rating.pergame',\
                    'Total Shots.pergols','Total Shots.pergame',\
                    'Ball Possession.pergame','D','L','W','gols']].\
    set_index('teams.name').rename(columns = {'gols':'Gols feitos', 'W':'Vitórias','D':'Empates','L':'Derrotas','statistics.games.rating.pergame':'Rating por Jogo','Ball Possession.pergame':'Posse de Bola por Jogo','Total Shots.pergame':'Chutes ao Gol por Jogo','Total Shots.pergols':'Chutes ao Gol por Gol'}).T

    # Add a small value to all the values in the dataframe to avoid zero values
    viz = viz + 0.00001

    # Convert the values to percentages
    viz_pct = viz / viz.sum(axis=1).values.reshape(-1, 1)

    # Create a stacked bar graph
    fig, ax = plt.subplots()
    viz_pct.plot(kind='barh', stacked=True, ax=ax)

    # Set the x-axis limits and ticks
    ax.set_xlim([0, 1])
    ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1])
    ax.set_xticklabels(['0%', '20%', '40%', '60%', '80%', '100%'])

    # Add the values to the graph
    for i, (idx, row) in enumerate(viz_pct.iterrows()):
        cum_sum = 0
        for j, val in enumerate(row):
            if val != 0:
                ax.text(cum_sum + val / 2, i, f'{float(viz.values[i][j]):.0f}', ha='center', va='center')
            cum_sum += val

    # Set the y-axis label and legend
    ax.set_ylabel('')
    ax.legend(title='Results', loc='center left', bbox_to_anchor=(1, 0.5))

    # Set the title of the plot
    ax.set_title('Results by Team')

       # Show the graph
    stacked = plt.show
    
    return stacked