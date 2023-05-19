# Análise Estatística focada em Apostas utilizando a API-Football

# Sobre o projeto

Análise de futebol com o objetivo de aplicação em apostas esportivas. Este repositório contém um projeto de análise esportiva para futebol. O projeto consome dados de uma API de acordo com as escolhas desejadas (país e campeonato) e os manipula para gerar resultados que podem ser usados para comparação entre times, jogadores e previsão de resultados. Suas saídas foram divididas em vários scripts, incluindo os seguintes notebooks listados abaixo.

#### Next steps: o código de back-end será transformado em um app streamlit de fácil navegação e obtenção dos outputs para o usuário final.

*A API pode ser acessada em  https://dashboard.api-football.com/

![image](https://user-images.githubusercontent.com/87664450/235800116-f1374610-39ad-4dc2-898f-4265021771a3.png)

# Módulos functions.py e visualizations.py
Contêm todas as fórmulas, chaves e bibliotecas necessárias para executar os notebooks abaixo.

# 1. bets_headxhead.ipynb
Análise de futuros jogos entre dois times. Permite selecionar o país, liga e jogo a ser analisado, comparando o desempenho das equipes que se enfrentarão no campeonato e também em seus últimos jogos entre si.

![image](https://github.com/viniciusfjacinto/football_bets/assets/87664450/806e7de9-3509-4758-aeb2-85b0fca348c2)

# 2. bets_jxj.ipynb
Permite comparar o desempenho de 2 jogadores individuais ao longo do campeonato. É uma aplicação muito interessante quando queremos observar o desempenho anterior de 2 estrelas antes de um confronto entre eles ocorrer (ex: Mbappé x Lewandowski).

![image](https://github.com/viniciusfjacinto/football_bets/assets/87664450/44e3674b-351b-430e-9cb0-2006b634d004)

# 3. bets_odds_gatherer.ipynb
Permite baixar todas as odds disponíveis para jogos futuros, a fim de analisar o mercado e visualizar as melhores opções de acordo com os preços oferecidos por diferentes casas de apostas.

![image](https://github.com/viniciusfjacinto/football_bets/assets/87664450/4a61288d-65bb-42d5-b9e6-d1fb3e483932)

# 4. bets_historical_statistics.ipynb

Permite solicitar e baixar todas as estatísticas de uma liga, desde a data atual até quando as informações estão disponíveis (geralmente 2010, com informações mais detalhadas disponíveis a partir de 2015/2016 em diante). Com isso, é possível elaborar estudos, gráficos e observar o comportamento das equipes ao longo da história. Uma verdadeira mina de ouro para os entusiastas do futebol. Além disso, podemos avaliar como as previsões fornecidas pela API têm se saído, se têm sido corretas ou incorretas na maioria dos jogos, e identificar as apostas mais precisas.

![image](https://user-images.githubusercontent.com/87664450/235799789-cfb39f25-e59d-4c3e-a763-c6a8e6a0fc89.png)
![image](https://github.com/viniciusfjacinto/football_bets/assets/87664450/37f1f50b-478d-4b16-b908-57c6ade9439a)

# 5. bets_ml_models.ipynb

Aplicamos modelos de aprendizado de máquina com base nos dados históricos coletados no item 4. Usamos a biblioteca Scikit-Learn para pré-processamento e padronização de dados e, em seguida, executamos e avaliamos diferentes modelos. Os modelos de aprendizado de máquina visam analisar todos os resultados anteriores para prever qual será o resultado de jogos futuros. É uma ferramenta poderosa para análise esportiva.

![image](https://user-images.githubusercontent.com/87664450/235799729-95c9bd8b-dc2e-4f7a-9bde-851f999e2776.png)
