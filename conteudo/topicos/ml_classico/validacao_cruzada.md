---
titulo: "Validação cruzada"
modulo: ml_classico
ordem: 7
horas: 8
estado: publicado
resumo: "Como estimar o desempenho real de um modelo e evitar overfitting."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Uma nota que depende da sorte"
    tipo: leitura
    minutos: 8
  - id: a2
    titulo: "Validação cruzada em k partes"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Escolher hiperparâmetros com busca em grade"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "O teste continua guardado"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Vazamento dentro da validação"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Quando as linhas não são independentes"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Vídeo de apoio: validação cruzada"
    tipo: video
    minutos: 20
    link: ""
  - id: a8
    titulo: "Vídeo de apoio: busca de hiperparâmetros"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Por que medir um modelo numa única divisão entre treino e teste pode enganar?"
    opcoes: ["Porque o conjunto de teste é sempre pequeno demais", "Porque o modelo vê o teste durante o treino", "Porque a divisão é um sorteio: com outro sorteio, a nota muda, e uma diferença entre modelos pode ser só sorte", "Porque a AUC só funciona com validação cruzada"]
    correta: 2
    explicacao: "No desafio, a mesma regressão logística teve AUC entre 0,707 e 0,745 em dez divisões diferentes. Se dois modelos diferem em 0,02 numa divisão só, não dá para saber se um é melhor ou se o sorteio favoreceu um deles."
  - pergunta: "Como funciona a validação cruzada em 5 partes?"
    opcoes: ["Os dados são divididos em 5 partes; cada parte serve de teste uma vez, com o modelo treinado nas outras 4, e o resultado é a média das 5 notas", "O modelo é treinado 5 vezes com os mesmos dados", "Os dados de teste são divididos em 5 partes", "Cinco modelos diferentes são comparados no mesmo teste"]
    correta: 0
    explicacao: "Cada linha é usada para teste exatamente uma vez e para treino quatro vezes. A média das cinco notas é uma estimativa bem mais estável que uma divisão só, e o desvio padrão mostra o quanto ela varia."
  - pergunta: "O que a validação cruzada estratificada (StratifiedKFold) garante?"
    opcoes: ["Que o modelo não sobreajusta", "Que as partes têm tamanhos diferentes", "Que o teste final fica separado", "Que cada parte tem a mesma proporção de cada classe que a base inteira"]
    correta: 3
    explicacao: "Com 27% de cancelamentos, uma parte sorteada sem estratificar poderia ter 22% ou 32%, e as notas variariam mais. Em classificação, a estratificação é o padrão recomendado."
  - pergunta: "A validação cruzada deu AUC média de 0,727, com desvio padrão de 0,018 entre as partes. Um segundo modelo deu 0,733. O que dá para concluir?"
    opcoes: ["Que o segundo modelo é claramente melhor", "Que a diferença é menor que a variação entre as partes, e os dois modelos estão, na prática, empatados", "Que o primeiro modelo é melhor, por ter desvio menor", "Que é preciso trocar a métrica"]
    correta: 1
    explicacao: "Uma diferença de 0,006 é bem menor que o quanto a nota oscila de uma parte para outra. Num empate assim, outros critérios decidem: simplicidade, tempo de treino, facilidade de explicar."
  - pergunta: "O que o GridSearchCV faz?"
    opcoes: ["Escolhe o melhor modelo pelo conjunto de teste", "Treina um modelo só, com os valores padrão", "Testa cada combinação de hiperparâmetros da grade com validação cruzada, escolhe a de melhor média e, por padrão, treina de novo o modelo escolhido com todos os dados recebidos", "Divide os dados em treino e teste"]
    correta: 2
    explicacao: "No desafio, a grade de 4 profundidades vezes 3 tamanhos de folha gera 12 combinações, cada uma avaliada em 5 partes: 60 árvores. A melhor combinação é treinada de novo com todo o treino, pronta para o teste final."
  - pergunta: "Depois da busca em grade, a melhor combinação teve AUC média de 0,724 na validação cruzada. Que número reportar como desempenho esperado do modelo?"
    opcoes: ["A AUC no conjunto de teste, separado antes da busca e usado uma vez só", "Os 0,724 da validação cruzada", "A AUC no treino", "A maior AUC entre as partes da validação"]
    correta: 0
    explicacao: "Escolher a melhor entre muitas combinações favorece a que teve sorte nas partes, então a melhor nota da busca é um pouco otimista. O teste, que não participou de nenhuma escolha, dá a estimativa honesta. No desafio, ela foi de 0,71."
  - pergunta: "Com um alvo sorteado ao acaso e 2 mil colunas de ruído, escolher as 20 colunas mais relacionadas ao alvo antes da validação cruzada deu AUC de 0,81. Por quê?"
    opcoes: ["Porque algumas colunas de ruído realmente preveem o alvo", "Porque a validação cruzada estava estratificada", "Porque 20 colunas é pouco", "Porque a seleção olhou o alvo de todas as linhas, inclusive as que depois serviram de teste em cada parte: o modelo foi avaliado em dados que ajudaram a escolhê-lo"]
    correta: 3
    explicacao: "Entre 2 mil colunas sorteadas, algumas parecem relacionadas ao alvo só por acaso, e a seleção as encontra usando todas as linhas. Com a seleção dentro do pipeline, refeita em cada parte só com o treino daquela parte, a AUC volta para 0,50, o valor honesto."
  - pergunta: "A base tem várias linhas por cliente, uma para cada mês. Que validação cruzada usar?"
    opcoes: ["A estratificada comum, sorteando as linhas", "A por grupos (GroupKFold), com o cliente como grupo, para que o mesmo cliente nunca esteja no treino e no teste ao mesmo tempo", "Nenhuma: com várias linhas por cliente, não dá para validar", "Uma divisão só, sem sorteio"]
    correta: 1
    explicacao: "Se meses do mesmo cliente caem dos dois lados, o modelo reconhece o cliente, e não o padrão, e a nota fica otimista. Com GroupKFold, todas as linhas de um cliente ficam na mesma parte."
  - pergunta: "Você quer prever as vendas do mês que vem a partir do histórico. Como validar?"
    opcoes: ["Sorteando os meses entre treino e teste", "Usando a validação estratificada", "Respeitando o tempo: treinar com os meses anteriores e testar com os seguintes, como faz o TimeSeriesSplit", "Validando só com o último mês do treino"]
    correta: 2
    explicacao: "Sorteando os meses, o modelo aprenderia com dados posteriores aos que precisa prever, o que é impossível na prática. A validação no tempo imita o uso real: só o passado prevê o futuro."
  - pergunta: "A validação cruzada escolheu a melhor configuração. Que modelo vai para produção?"
    opcoes: ["O modelo de uma das partes da validação, escolhido ao acaso", "A média dos cinco modelos da validação", "O modelo que teve a maior nota numa parte", "O modelo com a configuração escolhida, treinado de novo com todos os dados de treino"]
    correta: 3
    explicacao: "A validação cruzada serve para avaliar e escolher a configuração; os modelos de cada parte são descartados. O modelo final usa todos os dados disponíveis. O GridSearchCV faz isso sozinho, com refit=True, o padrão."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Descreva, passo a passo, como você compararia três modelos de cancelamento, uma regressão logística, uma random forest e um gradient boosting, para escolher um e informar o desempenho esperado. Diga onde entram a validação cruzada, a busca de hiperparâmetros e o conjunto de teste."
  rubrica:
    - "Separa o teste antes de tudo e só o usa uma vez, no fim, com o modelo escolhido."
    - "Usa validação cruzada estratificada no treino para ajustar os hiperparâmetros de cada modelo e para comparar os três, olhando a média e a variação, e com o pré-processamento dentro de um pipeline."
    - "Explica o critério de escolha: considera a variação entre as partes, prefere o mais simples em caso de empate e treina o escolhido de novo com todo o treino antes do teste final."
  modelo: "Primeiro, separo 25% dos clientes como teste, estratificando pelo cancelamento, e não olho mais para eles até o fim. Com os 75% restantes, monto um pipeline para cada modelo, com o pré-processamento dentro, para que tudo seja aprendido só com o treino de cada parte. Para a logística, busco a força da regularização; para a floresta, o mínimo de clientes por folha e o número de variáveis sorteadas; para o boosting, a taxa de aprendizado e o tamanho das árvores, com parada antecipada. Cada busca usa validação cruzada estratificada em 5 partes, com a AUC como métrica. Depois, comparo a melhor configuração de cada modelo pela média e pelo desvio padrão das partes. Se as diferenças forem menores que a variação entre as partes, considero empate e fico com o mais simples de explicar e de operar, que costuma ser a logística ou a floresta. O modelo escolhido é treinado de novo com todo o treino, e só então meço a AUC no teste, uma vez. Esse é o número que informo como desempenho esperado, sabendo que a melhor nota da validação cruzada tende a ser um pouco otimista."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Uma nota que não depende da sorte"
  descricao: "Você vai medir quanto a nota de um modelo muda só trocando o sorteio da divisão, usar a validação cruzada para ter uma estimativa mais firme, ver um vazamento transformar colunas sorteadas num modelo de AUC 0,81, corrigi-lo com um pipeline e escolher os hiperparâmetros de uma árvore com busca em grade, guardando o teste para o fim."
  pasta: "desafios/ml_classico/validacao_cruzada"
  testes: 9
  tempo: "1 h 30 min"
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
      descricao: "Abra desafios/ml_classico/validacao_cruzada/README.md. Os clientes estão em data/assinaturas.csv."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "As funções preparar e dados_de_ruido já estão prontas. Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def auc_em_divisoes(X, y, sementes):"
        - "def validacao_cruzada(modelo, X, y, k=5, semente=42):"
        - "def resumo(notas):"
        - "def selecao_antes_de_dividir(X, y, k=20, semente=0):"
        - "def selecao_dentro_do_pipeline(X, y, k=20, semente=0):"
        - "def busca_em_grade(X, y, semente=42):"
        - "def auc_final(grade, X_teste, y_teste):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ml_classico/validacao_cruzada"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/validacao_cruzada"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de validação cruzada"'
        - "git push -u origin desafio/validacao_cruzada"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Validação cruzada", en: "cross-validation" }
  - { pt: "Validação cruzada em k partes", en: "k-fold cross-validation" }
  - { pt: "Validação estratificada", en: "stratified k-fold" }
  - { pt: "Parte", en: "fold" }
  - { pt: "Busca em grade", en: "grid search" }
  - { pt: "Busca aleatória", en: "random search" }
  - { pt: "Hiperparâmetro", en: "hyperparameter" }
  - { pt: "Validação cruzada aninhada", en: "nested cross-validation" }
  - { pt: "Validação por grupos", en: "group k-fold" }
  - { pt: "Validação no tempo", en: "time series split" }
  - { pt: "Seleção de variáveis", en: "feature selection" }
  - { pt: "Sobreajuste", en: "overfitting" }
  - { pt: "Subajuste", en: "underfitting" }
---

## Uma nota que depende da sorte

Até aqui, todo modelo do módulo foi avaliado numa única divisão entre treino e teste. Mas essa divisão é um **sorteio**. No desafio deste tópico, a mesma regressão logística, nos mesmos dados, foi treinada e testada em dez divisões diferentes, mudando só a semente do sorteio. A AUC no teste variou de **0,707 a 0,745**.

Isso tem uma consequência séria. Se a random forest teve 0,75 numa divisão e a logística, 0,73, a diferença pode ser só o sorteio. E, quando você testa vinte configurações e fica com a melhor numa divisão só, está escolhendo, em parte, a que teve mais sorte.

## Validação cruzada em k partes

A **validação cruzada** usa todos os dados para avaliar, sem abrir mão de nenhum para treinar:

1. Divida os dados em k partes, geralmente 5 ou 10.
2. Para cada parte: treine o modelo com as outras k-1 e meça o desempenho nela.
3. Resuma as k notas pela **média** e pelo **desvio padrão**.

Cada linha é usada para teste exatamente uma vez. A média é uma estimativa muito mais estável que uma divisão só, e o desvio mostra o quanto ela varia. Em classificação, use a versão **estratificada**, que mantém a proporção de cada classe em todas as partes.

```python
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

partes = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
notas = cross_val_score(
    LogisticRegression(max_iter=5000), X, y,
    cv=partes, scoring="roc_auc",
)
print(notas.round(3))  # [0.693 0.73  0.74  0.742 0.731]
print(notas.mean(), notas.std())  # 0.727 e 0.018
```

A média de 0,727 fica praticamente igual à média das dez divisões sorteadas, 0,728. E o desvio de 0,018 dá uma régua: duas configurações cuja diferença é menor que isso estão, na prática, empatadas.

O custo é de tempo: k treinos em vez de um. Para bases muito grandes ou modelos muito lentos, uma divisão só, com um teste grande, pode bastar.

## Escolher hiperparâmetros com busca em grade

A validação cruzada é a ferramenta certa para escolher **hiperparâmetros**: em vez de comparar profundidades de árvore numa validação de 20%, como no tópico de árvores, compare pela média das partes. O `GridSearchCV` faz isso para todas as combinações de uma grade:

```python
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

grade = GridSearchCV(
    DecisionTreeClassifier(random_state=42),
    {"max_depth": [4, 5, 6, 8], "min_samples_leaf": [1, 20, 50]},
    cv=StratifiedKFold(5, shuffle=True, random_state=42),
    scoring="roc_auc",
)
grade.fit(X_treino, y_treino)
print(grade.best_params_)  # {'max_depth': 8, 'min_samples_leaf': 50}
print(grade.best_score_)  # 0.724
```

São 12 combinações, cada uma avaliada em 5 partes: 60 árvores. A melhor combinou uma profundidade maior com folhas de pelo menos 50 clientes, e chegou a 0,724 na validação cruzada, bem acima dos 0,696 da melhor árvore limitada só pela profundidade. Depois da busca, o `GridSearchCV` treina de novo a melhor combinação com todos os dados recebidos, e o objeto `grade` pode ser usado direto para prever.

Com grades grandes, o número de combinações explode. O `RandomizedSearchCV` sorteia um número fixo de combinações, e costuma achar configurações tão boas quanto em bem menos tempo.

## O teste continua guardado

A validação cruzada não substitui o conjunto de teste. O fluxo completo:

1. Separe o **teste** antes de tudo.
2. No treino, use a validação cruzada para **escolher**: o modelo, os hiperparâmetros, as variáveis.
3. Treine o modelo escolhido com todo o treino.
4. Meça no teste, **uma vez**, e informe esse número.

Por que não informar o `best_score_` da busca? Porque escolher a melhor entre muitas combinações favorece a que teve sorte nas partes, e a melhor nota da busca tende a ser um pouco otimista. No desafio, a busca deu 0,724 e o teste, 0,71. Quando é preciso uma estimativa honesta sem um teste separado, por exemplo com poucos dados, existe a **validação cruzada aninhada**: uma validação cruzada por fora, para avaliar, e outra por dentro, para escolher.

## Vazamento dentro da validação

A validação cruzada só é honesta se **tudo o que o modelo aprende** com os dados for refeito em cada parte, só com o treino daquela parte. Isso inclui o pré-processamento e, principalmente, a **seleção de variáveis**.

O desafio mostra o tamanho do problema com um caso extremo: 300 linhas, 2 mil colunas de números sorteados e um alvo também sorteado. Nenhuma coluna tem relação com o alvo, e nenhum modelo honesto pode passar de uma AUC de 0,5. Mas, se você escolher as 20 colunas mais relacionadas ao alvo usando **todas** as linhas e só depois fizer a validação cruzada, a AUC sai em **0,81**. Entre 2 mil colunas sorteadas, algumas parecem relacionadas ao alvo por acaso, e a seleção as encontrou olhando inclusive as linhas que depois serviram de teste.

Com a seleção dentro de um pipeline, refeita em cada parte, a AUC volta para **0,50**:

```python
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.pipeline import make_pipeline

pipeline = make_pipeline(
    SelectKBest(f_classif, k=20),
    LogisticRegression(max_iter=2000),
)
cross_val_score(pipeline, X_ruido, y_ruido, cv=partes, scoring="roc_auc")
```

A regra é a do tópico anterior: tudo o que aprende com dados vai dentro do pipeline, e o pipeline vai inteiro para a validação cruzada.

## Quando as linhas não são independentes

A validação cruzada comum supõe que as linhas são independentes umas das outras. Dois casos frequentes quebram essa suposição:

- **Várias linhas da mesma pessoa, loja ou produto.** Se os meses de um mesmo cliente caem no treino e no teste, o modelo reconhece o cliente, e a nota fica otimista. Use a validação **por grupos**, que mantém todas as linhas de um grupo na mesma parte.
- **Dados no tempo.** Para prever o mês que vem, o modelo só pode aprender com o passado. Sortear os meses entre treino e teste deixa o modelo ver o futuro. Use a validação **no tempo**, que sempre treina com períodos anteriores e testa com os seguintes.

```python
from sklearn.model_selection import GroupKFold, TimeSeriesSplit

# várias linhas por cliente: o mesmo cliente nunca fica dos dois lados
cross_val_score(modelo, X, y, cv=GroupKFold(5), groups=clientes)

# linhas em ordem de tempo: treina com o passado, testa com o futuro
cross_val_score(modelo, X, y, cv=TimeSeriesSplit(5))
```

A pergunta a fazer, antes de escolher a validação, é sempre a mesma: como o modelo vai ser usado na prática? A validação precisa imitar esse uso. Se o modelo vai prever clientes novos, nenhum cliente pode estar dos dois lados. Se vai prever o futuro, o teste precisa estar depois do treino.
