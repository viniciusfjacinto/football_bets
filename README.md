# Statistics Analysis for Betting using Football-API

![image](https://user-images.githubusercontent.com/87664450/235793112-17bbbe2f-8af5-475d-9ef2-59db266521e5.png)

# About the Project
Data-driven code focused on football analysis, aimed at applications in sports betting.
This repository that contains a sports analysis project for soccer. The project consumes data from an API and manipulates it in order to generate results that can be used for comparison between teams, players, and prediction of outcomes. Its outputs were divided into several scripts, including:

# 1. bets_headxhead.ipynb
Analysis of future matches between two teams. It allows selecting the country, league, and match to be analyzed, comparing the performance of the teams that will face each other in the championship and also in their last matches against each other.

![image](https://user-images.githubusercontent.com/87664450/235794080-56355ccc-21ac-452d-bd2d-76ca595fd0da.png)

# 2. bets_jxj.ipynb
Allows comparing the performance of 2 individual players throughout the championship. It is a very interesting application when we want to observe the past performance of 2 stars before a match between them occurs (ex: Mbappe x Lewandowski).

# 3. bets_odds_gatherer.ipynb
Allows downloading all available odds for upcoming matches, in order to analyze the market and visualize the best entries according to the prices offered by different bookmakers.

# 4. bets_historical_statistics.ipynb

![image](https://user-images.githubusercontent.com/87664450/235799789-cfb39f25-e59d-4c3e-a763-c6a8e6a0fc89.png)

Allows requesting and downloading all statistics of a league, from today's date to when information is available (usually 2010, with more detailed information available from 2015/2016 onwards). With this, it is possible to elaborate studies, graphs and observe the behavior of teams throughout history. A real gold mine for football enthusiasts.

# 5. bets_ml_models.ipynb

![image](https://user-images.githubusercontent.com/87664450/235799729-95c9bd8b-dc2e-4f7a-9bde-851f999e2776.png)

Realiza a aplicação de modelos de machine learning em cima das bases históricas coletadas no item 4. Os modelos buscam analisar todos os resultados anteriores para prever qual será o resultado das partidas futuras
