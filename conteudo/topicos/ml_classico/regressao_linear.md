---
titulo: "Regressão linear"
modulo: ml_classico
ordem: 1
horas: 9
estado: publicado
resumo: "Prever um valor numérico a partir de outras variáveis."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Aprendizado supervisionado e regressão"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "A reta de mínimos quadrados"
    tipo: leitura
    minutos: 15
  - id: a3
    titulo: "Várias variáveis e variáveis categóricas"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Treino, teste e as medidas de erro"
    tipo: leitura
    minutos: 15
  - id: a5
    titulo: "Ler os coeficientes"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Olhar os erros e conhecer os limites"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Vídeo de apoio: regressão linear do zero"
    tipo: video
    minutos: 30
    link: ""
  - id: a8
    titulo: "Vídeo de apoio: regressão linear com scikit-learn"
    tipo: video
    minutos: 25
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Qual destes problemas é de regressão?"
    opcoes: ["Decidir se um cliente vai cancelar a assinatura", "Separar e-mails em spam e não spam", "Prever em quantos minutos uma entrega vai chegar", "Agrupar clientes parecidos sem saber os grupos de antemão"]
    correta: 2
    explicacao: "Regressão prevê um valor numérico contínuo, como tempo, preço ou quantidade. Cancelar ou não e spam ou não são classificação. Agrupar sem rótulos é aprendizado não supervisionado."
  - pergunta: "No modelo de entregas, o coeficiente de chuva é 8,9. O que isso quer dizer?"
    opcoes: ["Que, mantidas as outras variáveis iguais, uma entrega com chuva leva em média 8,9 minutos a mais", "Que chove em 8,9% das entregas", "Que a chuva explica 8,9% do tempo de entrega", "Que toda entrega com chuva leva exatamente 8,9 minutos"]
    correta: 0
    explicacao: "Cada coeficiente é a variação média do alvo quando aquela variável aumenta uma unidade, com as demais fixas. Como chuva vale 0 ou 1, o coeficiente é a diferença média entre entregas com e sem chuva, comparando entregas parecidas no resto."
  - pergunta: "Por que, ao transformar a região em colunas de 0 e 1, se deixa uma região sem coluna?"
    opcoes: ["Para economizar memória", "Porque o scikit-learn não aceita mais de duas colunas", "Porque uma região tem poucos dados", "Porque com uma coluna para cada região e o intercepto, as colunas ficam redundantes; a região sem coluna vira a referência, e os coeficientes das outras medem a diferença em relação a ela"]
    correta: 3
    explicacao: "Se todas as regiões tivessem coluna, a soma delas seria sempre 1, igual ao intercepto: há infinitas combinações de coeficientes com o mesmo resultado. Tirando uma, cada coeficiente passa a ser lido como a diferença em relação à região de referência."
  - pergunta: "Por que medir o erro num conjunto de teste, separado antes do treino?"
    opcoes: ["Porque o treino fica mais rápido", "Porque o erro nos dados de treino é otimista: o modelo já viu aquelas respostas. O que importa é o erro em dados novos", "Porque o scikit-learn exige", "Para ter mais dados de treino"]
    correta: 1
    explicacao: "O modelo foi ajustado para errar pouco justamente nos dados de treino. O teste simula o uso real: entregas que o modelo nunca viu. A diferença entre os dois erros é o primeiro sinal de sobreajuste."
  - pergunta: "Qual é a diferença entre o MAE e o RMSE?"
    opcoes: ["O MAE é sempre maior que o RMSE", "Não há diferença, são nomes diferentes da mesma medida", "Os dois medem o erro na unidade do alvo, mas o RMSE eleva os erros ao quadrado antes da média e, por isso, pesa mais os erros grandes", "O RMSE só serve para classificação"]
    correta: 2
    explicacao: "Com erros de 1, 1 e 10 minutos, o MAE é 4 e o RMSE é cerca de 5,8. Se um atraso grande é muito pior que vários pequenos, o RMSE reflete melhor o problema. O MAE é mais fácil de explicar: o erro típico, em minutos."
  - pergunta: "O modelo teve R² de 0,92 no teste. O que isso significa?"
    opcoes: ["Que o modelo explica 92% da variação do tempo de entrega, em comparação com prever sempre a média", "Que o modelo acerta 92% das entregas em cheio", "Que 92% das entregas chegam no prazo", "Que o erro médio é de 0,92 minuto"]
    correta: 0
    explicacao: "O R² compara o erro do modelo com o erro de prever sempre a média. 1 é perfeito, 0 é o mesmo que a média, e pode até ficar negativo, se o modelo for pior que ela. Ele não diz o tamanho do erro em minutos: para isso, use o MAE ou o RMSE."
  - pergunta: "Para que serve comparar o modelo com uma previsão ingênua, como prever sempre a média?"
    opcoes: ["Para treinar o modelo mais rápido", "Para escolher a semente aleatória", "Para descobrir quais variáveis usar", "Para saber se o modelo acrescenta algo: um erro de 10 minutos só é bom se a alternativa simples errar bem mais"]
    correta: 3
    explicacao: "Sem uma referência, um número de erro não diz nada. No desafio, prever a média erra uns 15,7 minutos, e o modelo, uns 4,3. Se a diferença fosse pequena, o modelo não valeria a complexidade."
  - pergunta: "O modelo foi treinado com entregas de 1 a 25 km. Quanto confiar na previsão para uma entrega de 80 km?"
    opcoes: ["Totalmente, a reta continua valendo", "Pouco: é uma extrapolação, e nada garante que a relação continue linear fora do intervalo dos dados", "Nada, o modelo dá erro", "Totalmente, desde que o R² seja alto"]
    correta: 1
    explicacao: "Dentro do intervalo dos dados, o modelo foi testado. Fora dele, a entrega pode envolver outra rota, uma estrada, outra equipe. Previsões fora do intervalo de treino merecem desconfiança, por melhor que seja o R²."
  - pergunta: "No gráfico dos resíduos contra o valor previsto, os pontos formam uma curva, em vez de uma nuvem sem forma. O que isso indica?"
    opcoes: ["Que o modelo está perfeito", "Que há poucos dados", "Que a relação entre as variáveis e o alvo não é linear, e o modelo está deixando um padrão para trás", "Que o conjunto de teste é pequeno"]
    correta: 2
    explicacao: "Os resíduos de um bom modelo não têm padrão. Uma curva mostra uma relação que a reta não captura. Transformar uma variável, como usar o logaritmo, ou acrescentar um termo ao quadrado costuma resolver."
  - pergunta: "Num modelo de vendas, o coeficiente do investimento em anúncios é positivo. Isso prova que anunciar mais aumenta as vendas?"
    opcoes: ["Sim, o coeficiente positivo prova a causa", "Sim, desde que o R² seja maior que 0,5", "Não, porque coeficientes de regressão não podem ser positivos", "Não: o coeficiente mede associação nos dados. Outras causas, como a sazonalidade, podem mover as duas coisas juntas. Para medir causa, é preciso um experimento, como um teste A/B"]
    correta: 3
    explicacao: "A empresa pode anunciar mais justamente nos meses em que já venderia mais. A regressão descreve o padrão dos dados que você tem. Conclusões de causa e efeito precisam de um desenho de experimento, ou de muito cuidado com as variáveis que ficaram de fora."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "O gerente de operações quer usar o seu modelo de tempo de entrega no site. Explique a ele, sem jargão, o que o modelo faz, quão bem ele funciona e quais são os cuidados no uso."
  rubrica:
    - "Explica que o modelo aprende, com entregas passadas, quanto cada fator, como distância, chuva e horário de pico, soma ao tempo, e dá exemplos concretos dos coeficientes."
    - "Mostra o desempenho com números compreensíveis, medidos em entregas que o modelo não viu, como o erro típico em minutos, e compara com a alternativa simples."
    - "Aponta cuidados: o modelo não vale para situações fora do que viu, como distâncias muito maiores, erra mais em alguns casos, precisa ser reavaliado com o tempo, e mostra associação, e não causa."
  modelo: "O modelo olhou 600 entregas passadas e aprendeu quanto cada fator costuma somar ao tempo. Cada quilômetro acrescenta uns 2,4 minutos, chuva acrescenta uns 9 minutos, e o horário de pico, uns 7. A região norte costuma demorar uns 4 minutos a mais que o centro. Com isso, ele estima o tempo de uma entrega nova a partir dos dados do pedido. Para saber se funciona, testei em 120 entregas que ficaram de fora do aprendizado: o erro típico foi de uns 4 minutos. Se o site mostrasse sempre o tempo médio, o erro seria de uns 16 minutos, então o modelo é bem melhor que o que temos hoje. Os cuidados: ele só conhece entregas de até 25 km, e não deve ser usado para distâncias muito maiores. Algumas entregas fogem do padrão, com erros de mais de 15 minutos, então vale mostrar uma faixa, como 'entre 45 e 55 minutos', em vez de um número exato. O comportamento das entregas muda com o tempo, com novas rotas e entregadores, então o modelo precisa ser conferido todo mês com as entregas novas. E os números mostram associação: dizem quanto a chuva costuma atrasar, mas não explicam por quê."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Quanto tempo leva uma entrega"
  descricao: "Com 600 entregas passadas, você vai treinar uma regressão linear para prever o tempo de entrega, medir o erro em entregas que o modelo não viu, comparar com prever sempre a média, interpretar os coeficientes e encontrar as previsões que mais erraram."
  pasta: "desafios/ml_classico/regressao_linear"
  testes: 9
  tempo: "2 h"
  ferramentas: "VS Code, Python 3.11 ou superior, pandas, scikit-learn e pytest"
  entrega: "Pull Request no GitHub"
  passos:
    - titulo: "Clone o repositório"
      descricao: "Só na primeira vez. Se já clonou, pule para o passo 2."
      comandos:
        - "git clone https://github.com/[seu_usuario]/[repositorio].git"
        - "cd [repositorio]"
    - titulo: "Abra o repositório no VS Code"
      descricao: "Se o VS Code oferecer Reopen in Container, aceite: o ambiente já vem pronto e você pode pular o passo 3."
      comandos:
        - "code ."
    - titulo: "Crie e ative o ambiente virtual"
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado e conheça os dados"
      descricao: "Abra desafios/ml_classico/regressao_linear/README.md. As entregas estão em data/entregas.csv."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def codificar(df):"
        - "def dividir(X, y, proporcao_teste=0.2, semente=42):"
        - "def ajustar(X, y):"
        - "def coeficientes(modelo, colunas):"
        - "def avaliar(y_real, y_previsto):"
        - "def avaliar_baseline(y_treino, y_teste):"
        - "def prever_tempo(modelo, distancia_km, peso_kg, itens, chuva, horario_pico, regiao):"
        - "def piores_previsoes(df_teste, y_previsto, n=5):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ml_classico/regressao_linear"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/regressao_linear"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de regressão linear"'
        - "git push -u origin desafio/regressao_linear"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Aprendizado supervisionado", en: "supervised learning" }
  - { pt: "Variável alvo", en: "target" }
  - { pt: "Variáveis explicativas", en: "features" }
  - { pt: "Regressão linear", en: "linear regression" }
  - { pt: "Mínimos quadrados", en: "ordinary least squares (OLS)" }
  - { pt: "Intercepto", en: "intercept" }
  - { pt: "Coeficiente", en: "coefficient" }
  - { pt: "Codificação one-hot", en: "one-hot encoding" }
  - { pt: "Categoria de referência", en: "reference category" }
  - { pt: "Resíduo", en: "residual" }
  - { pt: "Erro absoluto médio", en: "mean absolute error (MAE)" }
  - { pt: "Raiz do erro quadrático médio", en: "root mean squared error (RMSE)" }
  - { pt: "Coeficiente de determinação", en: "R², coefficient of determination" }
  - { pt: "Modelo de referência", en: "baseline" }
  - { pt: "Extrapolação", en: "extrapolation" }
  - { pt: "Multicolinearidade", en: "multicollinearity" }
---

## Aprendizado supervisionado e regressão

Até aqui, você descreveu dados: médias, distribuições, gráficos, testes de hipóteses. Com **machine learning**, o objetivo muda: usar os dados do passado para **prever** algo que ainda não se sabe.

No **aprendizado supervisionado**, você tem exemplos com a resposta conhecida. Cada exemplo tem as **variáveis explicativas**, chamadas de *features*, e o **alvo**, o que se quer prever. No desafio deste tópico, cada entrega passada tem a distância, o peso, a quantidade de itens, se chovia, se era horário de pico, a região e o tempo que levou. O tempo é o alvo. O modelo aprende, com essas entregas, a relação entre as variáveis e o alvo, e depois usa essa relação para prever o tempo de entregas novas, em que o tempo ainda não é conhecido.

Quando o alvo é um **número**, como tempo, preço ou quantidade vendida, o problema é de **regressão**. Quando é uma **categoria**, como cancelou ou não cancelou, é de **classificação**, o assunto do próximo tópico.

A **regressão linear** é o modelo mais simples de regressão, e por isso o melhor ponto de partida: é rápida, fácil de interpretar e serve de referência para qualquer modelo mais complexo.

## A reta de mínimos quadrados

Com uma variável só, a regressão linear procura a reta que melhor descreve a relação entre ela e o alvo:

```text
tempo previsto = intercepto + coeficiente x distância
```

"Melhor" tem um sentido preciso: a reta que deixa a menor soma dos erros ao quadrado, os **mínimos quadrados**. Cada erro, chamado de **resíduo**, é a diferença entre o tempo real e o previsto. Elevar ao quadrado faz os erros para cima e para baixo não se anularem e pesa mais os erros grandes.

No scikit-learn, todo modelo segue o mesmo roteiro: criar, ajustar com `fit` e prever com `predict`.

```python
import pandas as pd
from sklearn.linear_model import LinearRegression

entregas = pd.read_csv("entregas.csv")

modelo = LinearRegression()
modelo.fit(entregas[["distancia_km"]], entregas["tempo_min"])
print(modelo.intercept_, modelo.coef_)  # 26.9 e [2.39]
```

A leitura: uma entrega leva uns 26,9 minutos mais 2,39 minutos por quilômetro. Repare nos colchetes duplos em `entregas[["distancia_km"]]`: o scikit-learn espera uma tabela de variáveis, mesmo quando é uma só.

## Várias variáveis e variáveis categóricas

Com várias variáveis, a ideia é a mesma: cada uma ganha um coeficiente, e a previsão é a soma.

```text
tempo = intercepto + b1 x distância + b2 x peso
        + b3 x itens + b4 x chuva + ...
```

Os modelos só trabalham com números. Variáveis de sim ou não viram 0 e 1, como `chuva`. Variáveis com categorias, como a região, viram uma coluna de 0 e 1 para cada categoria, a **codificação one-hot**, com um detalhe: uma das categorias fica sem coluna. Ela vira a **categoria de referência**, e o coeficiente de cada outra categoria mede a diferença em relação a ela.

```python
X = pd.get_dummies(
    entregas.drop(columns=["pedido_id", "tempo_min"]),
    columns=["regiao"], drop_first=True, dtype=int,
)
y = entregas["tempo_min"]
```

Com `drop_first=True`, o centro, primeira região em ordem alfabética, fica como referência, e surgem as colunas `regiao_norte` e `regiao_sul`. Se as três regiões tivessem coluna, a soma delas seria sempre 1, e o modelo não teria como separar o efeito das regiões do intercepto.

## Treino, teste e as medidas de erro

Um modelo sempre parece bom nos dados em que foi ajustado: ele foi feito para errar pouco justamente ali. A pergunta que interessa é como ele se sai em **dados novos**. Por isso, antes de treinar, separe uma parte dos dados para o **teste**, que o modelo não vai ver:

```python
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42
)
modelo = LinearRegression().fit(X_treino, y_treino)
previsto = modelo.predict(X_teste)

print(mean_absolute_error(y_teste, previsto))  # 4.28 minutos
print(r2_score(y_teste, previsto))  # 0.92
```

O `random_state` fixa o sorteio da divisão, para que o resultado se repita. Três medidas de erro aparecem o tempo todo:

- **MAE**, o erro absoluto médio: a média dos erros, sem sinal, na unidade do alvo. "O modelo erra, em média, 4,3 minutos." É a mais fácil de explicar.
- **RMSE**, a raiz do erro quadrático médio: também na unidade do alvo, mas pesa mais os erros grandes. Aqui, 5,2 minutos. Se um atraso de 30 minutos é muito pior que três de 10, ela reflete melhor o problema.
- **R²**: quanto da variação do alvo o modelo explica, comparado a prever sempre a média. Vai até 1, que seria perfeito. Zero é o mesmo que a média, e pode ficar negativo.

Um número de erro sozinho não diz se o modelo é bom. Compare sempre com um **modelo de referência**, o *baseline*: a previsão mais simples possível.

```python
from sklearn.dummy import DummyRegressor

base = DummyRegressor(strategy="mean").fit(X_treino, y_treino)
print(mean_absolute_error(y_teste, base.predict(X_teste)))  # 15.7
```

Prever sempre o tempo médio erra uns 15,7 minutos. O modelo, uns 4,3. Agora sim, dá para dizer que ele acrescenta algo.

## Ler os coeficientes

A grande vantagem da regressão linear é que ela se explica:

```python
print(pd.Series(modelo.coef_, index=X.columns).round(2))
```

```text
distancia_km    2.39
peso_kg         0.66
itens           1.30
chuva           8.90
horario_pico    7.01
regiao_norte    3.73
regiao_sul     -2.87
```

Cada coeficiente é a variação média do tempo quando aquela variável aumenta uma unidade, **mantidas as outras iguais**. Cada quilômetro soma uns 2,4 minutos. Chuva soma uns 9 minutos. Comparada ao centro, uma entrega no norte leva uns 3,7 minutos a mais, e no sul, uns 2,9 a menos.

Três cuidados na leitura:

- **A unidade importa.** Um coeficiente de 0,66 por quilo e um de 2,39 por quilômetro não dizem qual variável "pesa mais": elas estão em unidades diferentes. Para comparar a importância, compare o efeito de variações típicas de cada uma.
- **Variáveis muito correlacionadas confundem os coeficientes.** Se peso e quantidade de itens andassem sempre juntos, o modelo não teria como separar o efeito de cada um, e os coeficientes ficariam instáveis. É a **multicolinearidade**. A previsão continua boa, mas a leitura de cada coeficiente perde o sentido.
- **Coeficiente é associação, e não causa.** O modelo descreve o padrão dos dados. Se a empresa anuncia mais nos meses em que já venderia mais, o coeficiente do anúncio sai positivo mesmo que o anúncio não faça diferença. Para medir causa, é preciso um experimento, como o teste A/B que você já estudou.

## Olhar os erros e conhecer os limites

Depois das medidas de erro, olhe os **resíduos**: o erro de cada previsão. Num bom modelo, eles parecem uma nuvem sem forma em volta do zero. Padrões são pistas:

- **Uma curva** nos resíduos contra o valor previsto indica que a relação não é linear. Transformar uma variável, como usar o logaritmo do preço, ou acrescentar um termo ao quadrado costuma ajudar.
- **Um funil**, com erros que crescem junto com o valor previsto, indica que o modelo é mais impreciso para valores grandes. Vale informar uma faixa de erro maior nesses casos.
- **Pontos muito distantes** podem ser erros de registro ou casos especiais. Olhar as piores previsões, uma por uma, como você vai fazer no desafio, costuma ensinar mais que qualquer medida.

E os limites do modelo:

- **Extrapolação.** O modelo foi treinado com entregas de 1 a 25 km. Para 80 km, ele simplesmente continua a reta, mas nada garante que a relação seja a mesma. Desconfie de previsões fora do intervalo dos dados de treino.
- **Interações.** A regressão linear soma os efeitos. Se a chuva atrasasse muito mais no horário de pico do que fora dele, o modelo não perceberia, a não ser que você criasse uma variável para essa combinação. Os modelos de árvore, que vêm mais adiante neste módulo, captam interações sozinhos.
- **Mudanças no tempo.** Um modelo treinado com as entregas do ano passado pode envelhecer: rotas mudam, a frota muda. Modelos em produção precisam ser reavaliados com dados novos.
