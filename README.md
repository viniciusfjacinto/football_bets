# Statistics Analysis for Betting using Football-API

# About the Project

Dense data-driven notebooks focuseds on football analysis aimed at applications in sports betting.
This repository contains a sports analysis project for soccer. The project consumes data from an API and manipulates it in order to generate results that can be used for comparison between teams, players, and prediction of outcomes. Its outputs were divided into several scripts, including the following notebooks.

*The API can be acessed through https://dashboard.api-football.com/

![image](https://user-images.githubusercontent.com/87664450/235800116-f1374610-39ad-4dc2-898f-4265021771a3.png)

# modules functions.py and visualizations.py
Contain all the necessary formulas, keys and libraries for running the notebooks below

# 1. bets_headxhead.ipynb
Analysis of future matches between two teams. It allows selecting the country, league, and match to be analyzed, comparing the performance of the teams that will face each other in the championship and also in their last matches against each other.

![image](https://user-images.githubusercontent.com/87664450/235794080-56355ccc-21ac-452d-bd2d-76ca595fd0da.png)

# 2. bets_jxj.ipynb
Allows comparing the performance of 2 individual players throughout the championship. It is a very interesting application when we want to observe the past performance of 2 stars before a match between them occurs (ex: Mbappe x Lewandowski).

![image](https://github.com/viniciusfjacinto/football_bets/assets/87664450/44e3674b-351b-430e-9cb0-2006b634d004)

# 3. bets_odds_gatherer.ipynb
Allows downloading all available odds for upcoming matches, in order to analyze the market and visualize the best entries according to the prices offered by different bookmakers.

![image](https://github.com/viniciusfjacinto/football_bets/assets/87664450/4a61288d-65bb-42d5-b9e6-d1fb3e483932)

# 4. bets_historical_statistics.ipynb

Allows requesting and downloading all statistics of a league, from today's date to when information is available (usually 2010, with more detailed information available from 2015/2016 onwards). With this, it is possible to elaborate studies, graphs and observe the behavior of teams throughout history. A real gold mine for football enthusiasts.
Aditionally we can evaluate how the predictions provided by the API have performed, whether they have been correct or incorrect in the majority of games, and identify the most accurate bets.

![image](https://user-images.githubusercontent.com/87664450/235799789-cfb39f25-e59d-4c3e-a763-c6a8e6a0fc89.png)
![image](https://github.com/viniciusfjacinto/football_bets/assets/87664450/79f58dfe-2d96-4a90-a2ef-b4e0f0f973fa)


# 5. bets_ml_models.ipynb

We apply machine learning models on top of the historical data collected in item 4. We use the Scikit-Learn library for data preprocessing and normalization, and then run and evaluate different models. The machine learning models aim to analyze all previous results to predict what the outcome of future matches will be. It is a powerful tool for sports analysis.

![image](https://user-images.githubusercontent.com/87664450/235799729-95c9bd8b-dc2e-4f7a-9bde-851f999e2776.png)
