---
titulo: "Regressão logística"
modulo: ml_classico
ordem: 2
horas: 9
estado: publicado
resumo: "Prever a probabilidade de uma classe, como comprou ou não comprou."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Classificação e probabilidade"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "A função logística e a chance"
    tipo: leitura
    minutos: 15
  - id: a3
    titulo: "Treinar e prever probabilidades"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Do risco à decisão: o limiar"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Acertos, erros e a armadilha da acurácia"
    tipo: leitura
    minutos: 15
  - id: a6
    titulo: "Razões de chance e cuidados"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Vídeo de apoio: regressão logística"
    tipo: video
    minutos: 30
    link: ""
  - id: a8
    titulo: "Vídeo de apoio: matriz de confusão"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Por que não usar uma regressão linear comum para prever se um cliente vai cancelar (1) ou não (0)?"
    opcoes: ["Porque a regressão linear não aceita variáveis categóricas", "Porque a reta pode prever valores abaixo de 0 e acima de 1, que não fazem sentido como probabilidade", "Porque a regressão linear é lenta demais", "Porque a regressão linear só funciona com uma variável"]
    correta: 1
    explicacao: "A regressão logística passa a soma ponderada das variáveis pela função logística, que leva qualquer número para o intervalo entre 0 e 1. O resultado pode ser lido como probabilidade."
  - pergunta: "O que o modelo de regressão logística devolve com predict_proba?"
    opcoes: ["Só a classe prevista, 0 ou 1", "O erro de cada previsão", "A probabilidade de cada classe para cada exemplo", "A importância de cada variável"]
    correta: 2
    explicacao: "predict_proba devolve uma coluna por classe; a segunda é a probabilidade de cancelar. O predict devolve a classe, usando o limiar de 0,5. Na maioria dos problemas de negócio, a probabilidade é mais útil que a classe."
  - pergunta: "Numa base em que 27% dos clientes cancelam, um modelo tem 75% de acurácia. O que dá para concluir?"
    opcoes: ["Pouca coisa: prever que ninguém cancela já acerta 73%. É preciso olhar quantos cancelamentos o modelo encontra", "Que o modelo é excelente", "Que o modelo acerta 75% dos cancelamentos", "Que o modelo é pior que o acaso"]
    correta: 0
    explicacao: "Com classes desbalanceadas, a acurácia é dominada pela classe maior. No desafio, o modelo com limiar 0,5 tem 75% de acurácia, mas encontra só 20% dos clientes que cancelaram. A matriz de confusão mostra isso; a acurácia sozinha esconde."
  - pergunta: "Na matriz de confusão, o que é um falso negativo, neste problema?"
    opcoes: ["Um cliente que não cancelou e o modelo previu que não cancelaria", "Um cliente que não cancelou, mas o modelo previu cancelamento", "Um erro de digitação na base", "Um cliente que cancelou, mas o modelo previu que ele ficaria"]
    correta: 3
    explicacao: "Negativo é o que o modelo previu (não cancela), e falso diz que a previsão errou (o cliente cancelou). Aqui, é o cliente que o time de retenção deixou de ligar e perdeu."
  - pergunta: "O que acontece ao baixar o limiar de 0,5 para 0,3?"
    opcoes: ["O modelo é treinado de novo", "O modelo passa a marcar mais clientes como risco: encontra mais cancelamentos, mas também dá mais alarmes falsos", "A acurácia sempre aumenta", "As probabilidades mudam"]
    correta: 1
    explicacao: "O limiar não muda o modelo nem as probabilidades: muda só a decisão. No desafio, com 0,3 o modelo passa a encontrar 55% dos cancelamentos em vez de 20%, mas a lista cresce de 115 para 412 clientes, e mais deles não iam cancelar."
  - pergunta: "Como escolher o limiar certo?"
    opcoes: ["Usar sempre 0,5", "Escolher o que dá a maior acurácia", "Pelos custos e capacidades do negócio: quanto custa um alarme falso, quanto custa perder um cancelamento e quantos clientes o time consegue atender", "Escolher ao acaso e ajustar com o tempo"]
    correta: 2
    explicacao: "Se uma ligação custa pouco e um cliente perdido custa muito, vale um limiar baixo. Se o time só consegue ligar para 300 clientes, o limiar é o que gera uma lista desse tamanho. O 0,5 é só o padrão, e raramente é o melhor."
  - pergunta: "A razão de chance de atrasos_pagamento é 1,85. O que isso significa?"
    opcoes: ["Que cada atraso de pagamento a mais multiplica a chance de cancelar por cerca de 1,85, mantidas as outras variáveis", "Que 85% dos clientes com atraso cancelam", "Que a probabilidade de cancelar aumenta 1,85 ponto percentual por atraso", "Que clientes com atraso cancelam 1,85 vez mais rápido"]
    correta: 0
    explicacao: "Na regressão logística, os coeficientes atuam sobre o logaritmo da chance. Exponenciando, cada coeficiente vira um multiplicador da chance, que é a probabilidade de cancelar dividida pela de ficar. Não é um aumento fixo na probabilidade."
  - pergunta: "Por que estratificar a divisão entre treino e teste num problema de classificação?"
    opcoes: ["Para o treino ficar maior", "Para embaralhar melhor as linhas", "Porque o scikit-learn exige", "Para manter a mesma proporção de cada classe no treino e no teste, e o teste representar bem a base"]
    correta: 3
    explicacao: "Sem estratificar, o sorteio pode deixar o teste com uma proporção de cancelamentos diferente da real, principalmente com classes raras ou bases pequenas. O stratify=y mantém as proporções."
  - pergunta: "O que a regressão logística não consegue captar sozinha?"
    opcoes: ["Variáveis numéricas", "Interações e relações não lineares, como um risco que só é alto quando o cliente é novo e quase não usa o serviço", "Variáveis de sim ou não", "Mais de dez variáveis"]
    correta: 1
    explicacao: "O modelo soma os efeitos de cada variável. Um padrão que depende da combinação de duas variáveis só aparece se você criar uma variável para ela. Os modelos de árvore, nos próximos tópicos, captam esse tipo de padrão sozinhos."
  - pergunta: "O modelo deu probabilidade de 0,8 a um cliente. Como usar esse número com segurança?"
    opcoes: ["Como certeza de que ele vai cancelar", "Como um número sem significado, só para ordenar", "Como uma estimativa de risco, que só deve ser lida como probabilidade se o modelo estiver calibrado: entre os clientes com 0,8, cerca de 80% deveriam cancelar", "Como o percentual de clientes parecidos com ele na base"]
    correta: 2
    explicacao: "A regressão logística costuma dar probabilidades razoavelmente calibradas, mas isso deve ser conferido: agrupe os clientes por faixa de probabilidade e compare com a taxa real de cancelamento de cada faixa. O tópico de métricas volta a esse assunto."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "O time de retenção pediu 'o modelo que prevê quem vai cancelar'. Explique como você transformaria as probabilidades do modelo numa lista de clientes para ligar, e como mostraria ao time quão bom é o modelo, sem usar a acurácia como medida principal."
  rubrica:
    - "Explica que o modelo dá uma probabilidade para cada cliente e que a lista sai de um limiar, ou dos N clientes de maior risco, escolhido pela capacidade e pelos custos do time, e não pelo 0,5 padrão."
    - "Mostra o desempenho com a matriz de confusão: quantos dos que cancelaram a lista pega e quantos da lista realmente iam cancelar, em linguagem do negócio."
    - "Explica por que a acurácia engana com classes desbalanceadas, comparando com a acurácia de prever que ninguém cancela."
  modelo: "O modelo dá, para cada cliente, a probabilidade de cancelar no próximo trimestre. Em vez de usar o corte padrão de 50%, eu ordenaria os clientes do maior risco para o menor e pegaria o tamanho de lista que o time consegue atender, por exemplo 300 clientes. Se o custo de uma ligação for baixo e o de perder um cliente for alto, vale até uma lista maior. Para mostrar a qualidade, eu usaria dois números, medidos em clientes que o modelo não viu no treino. Primeiro: dos clientes que de fato cancelaram, quantos estão na lista. Segundo: dos clientes da lista, quantos de fato iam cancelar. Com um corte em 30%, por exemplo, a lista pega 55% dos cancelamentos, e 44% da lista ia mesmo cancelar, contra 27% se o time ligasse para clientes ao acaso. Eu evitaria a acurácia, porque ela engana aqui: como só 27% cancelam, um 'modelo' que diz que ninguém cancela acerta 73% das vezes e não ajuda em nada. O modelo com corte em 50% tem 75% de acurácia, quase o mesmo, mas só encontra 20% dos cancelamentos."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Quem vai cancelar a assinatura"
  descricao: "Com 5 mil clientes de uma plataforma por assinatura, você vai treinar uma regressão logística, transformar probabilidades em decisões com um limiar, montar a matriz de confusão, ver a acurácia enganar numa base desbalanceada, ler as razões de chance e gerar a lista dos clientes de maior risco."
  pasta: "desafios/ml_classico/regressao_logistica"
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
      descricao: "Abra desafios/ml_classico/regressao_logistica/README.md. Os clientes estão em data/assinaturas.csv."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def preparar(df):"
        - "def dividir(X, y, semente=42):"
        - "def ajustar(X, y):"
        - "def probabilidades(modelo, X):"
        - "def classificar(probs, limiar=0.5):"
        - "def matriz_confusao(y_real, y_previsto):"
        - "def acuracia_ingenua(y):"
        - "def razoes_de_chance(modelo, colunas):"
        - "def clientes_mais_arriscados(df, probs, n=10):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ml_classico/regressao_logistica"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/regressao_logistica"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de regressão logística"'
        - "git push -u origin desafio/regressao_logistica"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Classificação", en: "classification" }
  - { pt: "Regressão logística", en: "logistic regression" }
  - { pt: "Função logística", en: "logistic function, sigmoid" }
  - { pt: "Chance", en: "odds" }
  - { pt: "Logaritmo da chance", en: "log-odds, logit" }
  - { pt: "Razão de chance", en: "odds ratio" }
  - { pt: "Limiar de decisão", en: "decision threshold" }
  - { pt: "Matriz de confusão", en: "confusion matrix" }
  - { pt: "Verdadeiro positivo", en: "true positive (TP)" }
  - { pt: "Falso positivo", en: "false positive (FP)" }
  - { pt: "Falso negativo", en: "false negative (FN)" }
  - { pt: "Acurácia", en: "accuracy" }
  - { pt: "Classes desbalanceadas", en: "imbalanced classes" }
  - { pt: "Divisão estratificada", en: "stratified split" }
  - { pt: "Regularização", en: "regularization" }
  - { pt: "Calibração", en: "calibration" }
---

## Classificação e probabilidade

No tópico anterior, o alvo era um número: o tempo de uma entrega. Em muitos problemas de negócio, o alvo é uma **categoria**: o cliente vai cancelar ou não, a transação é fraude ou não, o e-mail é spam ou não. Esses são problemas de **classificação**. Quando há duas categorias, a classificação é **binária**, e as classes costumam ser codificadas como 1, o evento de interesse, e 0.

Mais útil do que dizer "este cliente vai cancelar" é dizer "este cliente tem 62% de chance de cancelar". A probabilidade permite ordenar os clientes por risco, escolher quantos atender e medir a confiança de cada previsão. A **regressão logística** é o modelo mais simples que faz isso, e, como a regressão linear, serve de referência para qualquer modelo mais complexo.

Por que não usar a regressão linear comum, prevendo 0 ou 1? Porque uma reta não tem limites: para alguns clientes, ela preveria 1,3 ou -0,2, que não fazem sentido como probabilidade.

## A função logística e a chance

A regressão logística começa igual à linear, com uma soma ponderada das variáveis:

```text
z = b0 + b1 x atrasos + b2 x chamados + ... + bk x usa_app
```

Depois, passa essa soma pela **função logística**, que transforma qualquer número num valor entre 0 e 1:

```text
probabilidade = 1 / (1 + e^(-z))
```

Com z igual a 0, a probabilidade é 0,5. Com z muito positivo, ela se aproxima de 1; com z muito negativo, de 0.

Há uma forma equivalente de ler o modelo, pela **chance**, em inglês *odds*: a probabilidade de o evento acontecer dividida pela probabilidade de não acontecer. Uma probabilidade de 0,8 é uma chance de 4 para 1. A soma ponderada `z` é exatamente o **logaritmo da chance**. Por isso a regressão logística é linear no logaritmo da chance, e não na probabilidade. Essa é a chave para interpretar os coeficientes, mais adiante.

## Treinar e prever probabilidades

O roteiro no scikit-learn é o mesmo do tópico anterior, com dois detalhes novos:

```python
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

assinaturas = pd.read_csv("assinaturas.csv")
X = pd.get_dummies(
    assinaturas.drop(columns=["cliente_id", "cancelou"]),
    columns=["plano", "canal"], drop_first=True, dtype=int,
)
y = assinaturas["cancelou"]

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)
modelo = LogisticRegression(max_iter=5000).fit(X_treino, y_treino)
probs = modelo.predict_proba(X_teste)[:, 1]
print(probs[:5].round(2))  # [0.41 0.07 0.34 0.54 0.48]
```

O primeiro detalhe é o `stratify=y`. Ele mantém a mesma proporção de cancelamentos no treino e no teste. Sem ele, o sorteio poderia deixar o teste com uma proporção diferente da real, o que importa principalmente com classes raras.

O segundo é o `predict_proba`, que devolve uma coluna para cada classe. A segunda coluna, `[:, 1]`, é a probabilidade de cancelar. O `max_iter=5000` dá ao algoritmo de ajuste iterações suficientes para convergir.

Um detalhe que costuma passar despercebido: a `LogisticRegression` do scikit-learn usa **regularização** por padrão. Ela penaliza coeficientes muito grandes, o que reduz o sobreajuste. O parâmetro `C` controla a força: quanto menor, mais forte. A regularização é sensível à escala das variáveis, por isso, em modelos de produção, é comum padronizar as variáveis antes, como você vai ver no tópico de preparação de variáveis.

## Do risco à decisão: o limiar

Para virar decisão, a probabilidade precisa de um **limiar**: acima dele, o cliente entra na lista de risco. O `predict` usa 0,5, mas esse valor raramente é o melhor. Nos dados do desafio, com 1.250 clientes de teste, dos quais 332 cancelaram:

| Limiar | Clientes na lista | Cancelamentos encontrados | Da lista, quantos cancelaram |
| ------ | ----------------- | ------------------------- | ---------------------------- |
| 0,5    | 115               | 67 de 332 (20%)           | 58%                          |
| 0,3    | 412               | 183 de 332 (55%)          | 44%                          |
| 0,2    | 700               | 251 de 332 (76%)          | 36%                          |

Baixar o limiar encontra mais cancelamentos, mas a lista cresce e passa a ter mais clientes que não iam cancelar. Não existe limiar certo em abstrato: ele depende do **negócio**. Quanto custa uma ligação de retenção? Quanto vale um cliente que fica? Quantos clientes o time consegue atender? Se o time só consegue ligar para 300 clientes, o limiar é o que gera uma lista desse tamanho.

Repare que mudar o limiar não muda o modelo nem as probabilidades: muda só a decisão tomada a partir delas.

## Acertos, erros e a armadilha da acurácia

A **matriz de confusão** conta os quatro tipos de resultado:

```python
from sklearn.metrics import confusion_matrix

previsto = (probs >= 0.5).astype(int)
print(confusion_matrix(y_teste, previsto))
```

```text
[[870  48]
 [265  67]]
```

As linhas são o que aconteceu e as colunas, o que o modelo previu. Na primeira linha, os 918 clientes que ficaram: 870 **verdadeiros negativos** e 48 **falsos positivos**, alarmes falsos. Na segunda, os 332 que cancelaram: 265 **falsos negativos**, cancelamentos que o modelo deixou passar, e 67 **verdadeiros positivos**.

A **acurácia**, a proporção de acertos, é (870 + 67) / 1.250 = 75%. Parece bom, até a comparação com o "modelo" mais preguiçoso possível: prever que ninguém cancela. Ele acerta todos os 918 que ficaram, ou seja, 73%. O modelo com limiar 0,5 é só dois pontos melhor, e encontra apenas 20% dos cancelamentos. Com **classes desbalanceadas**, a acurácia é dominada pela classe maior e esconde o que importa.

Duas medidas olham para o que importa aqui. O **recall**: dos clientes que cancelaram, quantos o modelo encontrou. A **precisão**: dos clientes que o modelo apontou, quantos cancelaram. São as duas últimas colunas da tabela do limiar. E, para avaliar o modelo independentemente do limiar, a **AUC** mede o quanto ele ordena bem: a chance de um cliente que cancelou receber uma probabilidade maior que um que ficou. Aqui, ela é de 0,71. O tópico de métricas aprofunda cada uma dessas medidas.

## Razões de chance e cuidados

Como o modelo é linear no logaritmo da chance, cada coeficiente, exponenciado, vira uma **razão de chance**: o fator pelo qual a chance de cancelar é multiplicada quando a variável aumenta uma unidade, mantidas as outras.

```python
razoes = pd.Series(np.exp(modelo.coef_[0]), index=X.columns)
print(razoes.round(2).sort_values())
```

Alguns valores do modelo do desafio:

- `atrasos_pagamento`: 1,85. Cada atraso de pagamento multiplica a chance de cancelar por 1,85.
- `chamados_suporte`: 1,60. Cada chamado ao suporte multiplica a chance por 1,6.
- `usa_app`: 0,73. Quem usa o aplicativo tem uma chance de cancelar 27% menor.
- `plano_premium`: 0,58. Comparado ao plano básico, a referência, a chance no premium é 42% menor.

Os mesmos cuidados da regressão linear valem aqui: os coeficientes mostram associação, e não causa; variáveis muito correlacionadas confundem a leitura; e a razão de chance de uma variável medida em reais ou em meses depende da unidade.

Dois cuidados são próprios da classificação:

- **Razão de chance não é aumento de probabilidade.** Multiplicar a chance por 1,85 é um aumento grande para quem tinha 30% de probabilidade, e pequeno para quem tinha 2%.
- **Probabilidade calibrada.** Para ler 0,8 como "80% de chance", é preciso que, entre os clientes com probabilidade perto de 0,8, cerca de 80% de fato cancelem. A regressão logística costuma ser razoavelmente calibrada, mas vale conferir, agrupando os clientes por faixa de probabilidade.

Por fim, o limite principal do modelo: ele **soma efeitos**. Nos dados do desafio, há um grupo de alto risco formado por clientes novos que quase não usam o serviço, e um pico de cancelamentos na renovação anual. A regressão logística capta esses padrões só em parte. Os modelos de árvore, nos próximos tópicos, encontram esse tipo de combinação sozinhos.
