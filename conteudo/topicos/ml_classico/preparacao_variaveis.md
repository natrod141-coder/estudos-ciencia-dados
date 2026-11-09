---
titulo: "Preparação de variáveis"
modulo: ml_classico
ordem: 6
horas: 6
estado: publicado
resumo: "Tratar faltantes, categorias e escalas, e evitar vazamento de dados, antes de treinar o modelo."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Criar variáveis a partir dos dados"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "Valores faltantes"
    tipo: leitura
    minutos: 10
  - id: a3
    titulo: "Variáveis categóricas e escalas"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Vazamento de dados"
    tipo: leitura
    minutos: 15
  - id: a5
    titulo: "Pipelines no scikit-learn"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Vídeo de apoio: pipelines e pré-processamento"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Qual destas colunas vaza o alvo num modelo que prevê se o cliente vai cancelar?"
    opcoes: ["A quantidade de acessos no último mês", "O motivo do cancelamento, informado pelo cliente ao sair", "O plano contratado", "A idade do cliente"]
    correta: 1
    explicacao: "O motivo só existe depois que o cliente cancelou. No momento da previsão, essa informação ainda não está disponível. Com ela, o modelo parece ótimo no teste e não serve para nada na prática."
  - pergunta: "Na hora de preencher as idades vazias com a mediana, de onde deve vir essa mediana?"
    opcoes: ["De toda a base, treino e teste juntos", "Do conjunto de teste", "De uma base externa", "Só do conjunto de treino; a mesma mediana é usada depois para preencher o teste e os dados novos"]
    correta: 3
    explicacao: "Tudo o que o pré-processamento aprende, como medianas, médias, desvios e categorias, precisa vir só do treino. Senão, informação do teste entra no modelo, e o resultado fica otimista. Um pipeline do scikit-learn garante isso."
  - pergunta: "A coluna cidade tem 47 valores, e 40 deles têm menos de 1% dos clientes cada. O que costuma funcionar melhor?"
    opcoes: ["Agrupar as cidades raras numa categoria de 'outras', e só então criar as colunas de 0 e 1", "Criar uma coluna de 0 e 1 para cada uma das 47 cidades", "Apagar os clientes das cidades raras", "Numerar as cidades de 1 a 47 e usar o número como variável"]
    correta: 0
    explicacao: "Categorias com poucos exemplos geram colunas que o modelo não consegue aprender e que podem nem aparecer no teste. Agrupar as raras reduz o ruído e resolve as cidades novas. Numerar de 1 a 47 cria uma ordem que não existe."
  - pergunta: "Para qual destes modelos é importante padronizar as variáveis, colocando todas na mesma escala?"
    opcoes: ["Árvore de decisão", "Random forest", "Regressão logística com regularização", "Gradient boosting com árvores"]
    correta: 2
    explicacao: "A regularização penaliza o tamanho dos coeficientes, e o tamanho de um coeficiente depende da escala da variável. Sem padronizar, variáveis em escalas grandes são penalizadas de um jeito diferente das outras. Modelos de árvore não dependem da escala."
  - pergunta: "O primeiro modelo do projeto deu AUC de 0,99 no teste. Qual é a reação certa?"
    opcoes: ["Comemorar e colocar em produção", "Aumentar o conjunto de teste", "Trocar de modelo para ver se chega a 1,00", "Desconfiar: procurar vazamento, olhando quais variáveis mais pesam e se cada uma estaria disponível no momento da previsão"]
    correta: 3
    explicacao: "Em problemas reais de negócio, resultados quase perfeitos são raros. Antes de comemorar, confira as variáveis mais importantes, a data em que cada uma é preenchida e se há linhas repetidas entre treino e teste."
  - pergunta: "Qual é a principal vantagem de colocar o pré-processamento e o modelo num Pipeline do scikit-learn?"
    opcoes: ["O modelo fica mais preciso", "O pipeline aprende as transformações só com os dados de fit e aplica as mesmas a qualquer dado novo, o que evita vazamento e simplifica o uso em produção", "O treino fica mais rápido", "O pipeline escolhe o melhor modelo sozinho"]
    correta: 1
    explicacao: "Com o pipeline, fit aprende tudo com o treino, e predict aplica as mesmas etapas, na mesma ordem, ao teste e aos dados de produção. Na validação cruzada, o pipeline inteiro é refeito em cada parte, o que evita um vazamento sutil."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Você vai montar um modelo de cancelamento com uma base que tem datas, valores faltantes, categorias com muitos valores e uma coluna de data de cancelamento. Descreva, passo a passo, como prepararia as variáveis e como evitaria o vazamento."
  rubrica:
    - "Identifica e remove as variáveis que não estariam disponíveis no momento da previsão, como a data de cancelamento, e explica o critério."
    - "Descreve o tratamento de cada tipo de variável: criação de variáveis a partir de datas, preenchimento dos faltantes, possivelmente com um indicador, agrupamento das categorias raras e padronização quando o modelo precisa."
    - "Explica que tudo o que o pré-processamento aprende vem só do treino, de preferência com um pipeline, separando treino e teste antes de qualquer cálculo."
  modelo: "Primeiro, eu olharia cada coluna e perguntaria: no dia em que o modelo vai prever, essa informação já existe? A data de cancelamento só existe para quem já cancelou, então sai. Um teste rápido ajuda: colunas preenchidas só para uma das classes são suspeitas. Depois, separaria treino e teste antes de calcular qualquer coisa. Com o treino, criaria as variáveis: os meses de assinatura, a partir da data de início e da data de referência da base, e um indicador de se o cliente respondeu à pesquisa de satisfação, porque não responder também pode dizer algo. Os vazios numéricos seriam preenchidos com a mediana do treino. As cidades com poucos clientes seriam agrupadas numa categoria de raras, e as categorias virariam colunas de 0 e 1, com a regra de mandar para as raras qualquer cidade nova. Para a regressão logística, padronizaria as variáveis numéricas; para modelos de árvore, não precisaria. Tudo isso ficaria num Pipeline do scikit-learn, para que medianas, escalas e categorias sejam aprendidas só com o treino e aplicadas iguais no teste e em produção. Por fim, desconfiaria de qualquer resultado bom demais: com a data de cancelamento, o modelo chegaria a uma AUC perto de 1, o que é sinal de vazamento, e não de um modelo excelente."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Do dado cru ao modelo, sem vazamento"
  descricao: "A base de assinaturas chegou crua: datas no lugar de meses de assinatura, idades e notas faltando, dezenas de cidades com poucos clientes e uma coluna que entrega a resposta. Você vai encontrar o vazamento, criar as variáveis, montar um pipeline que aprende o pré-processamento só com o treino e medir o estrago que o vazamento faria."
  pasta: "desafios/ml_classico/preparacao_variaveis"
  testes: 8
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
      descricao: "Abra desafios/ml_classico/preparacao_variaveis/README.md. A base crua está em data/assinaturas_brutas.csv."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def colunas_suspeitas(df, alvo='cancelou', limite=0.9):"
        - "def criar_variaveis(df, referencia=REFERENCIA):"
        - "def separar(df, colunas_a_remover, alvo='cancelou', semente=42):"
        - "def montar_preprocessamento(numericas, categoricas):"
        - "def montar_pipeline(numericas=NUMERICAS, categoricas=CATEGORICAS):"
        - "def auc(modelo, X, y):"
        - "def auc_com_vazamento(df, semente=42):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ml_classico/preparacao_variaveis"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/preparacao_variaveis"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de preparação de variáveis"'
        - "git push -u origin desafio/preparacao_variaveis"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Engenharia de variáveis", en: "feature engineering" }
  - { pt: "Preenchimento de faltantes", en: "imputation" }
  - { pt: "Indicador de faltante", en: "missing indicator" }
  - { pt: "Codificação one-hot", en: "one-hot encoding" }
  - { pt: "Alta cardinalidade", en: "high cardinality" }
  - { pt: "Categorias raras", en: "infrequent categories" }
  - { pt: "Codificação pela média do alvo", en: "target encoding" }
  - { pt: "Padronização", en: "standardization" }
  - { pt: "Vazamento de dados", en: "data leakage" }
  - { pt: "Vazamento do alvo", en: "target leakage" }
  - { pt: "Contaminação entre treino e teste", en: "train-test contamination" }
  - { pt: "Pipeline", en: "pipeline" }
  - { pt: "Transformador de colunas", en: "column transformer" }
---

## Criar variáveis a partir dos dados

Nos tópicos anteriores, a base de assinaturas vinha pronta. Na prática, preparar os dados costuma tomar mais tempo que treinar o modelo, e pesar mais no resultado. A regra geral é que o modelo só aprende o que está nas colunas: se uma informação útil está escondida numa data ou espalhada numa tabela de eventos, alguém precisa transformá-la numa variável.

Algumas transformações aparecem em quase todo projeto:

- **Datas viram durações e calendário.** A data de início da assinatura sozinha não diz muito; os meses de assinatura, sim. Do mesmo jeito, uma data pode virar o mês, o dia da semana ou "dias desde a última compra".
- **Tabelas de eventos viram contagens e somas por cliente**, sempre numa janela de tempo: pedidos nos últimos 90 dias, valor gasto no último mês, chamados abertos no trimestre. É um trabalho de SQL ou de `groupby`.
- **Razões e diferenças** entre colunas: valor por item, variação do uso em relação ao mês anterior.

```python
referencia = pd.Timestamp("2026-09-30")  # o dia em que a base foi extraída
dias = (referencia - pd.to_datetime(dados["data_inicio"])).dt.days
dados["meses_assinatura"] = (dias / 30.44).astype(int)
```

Repare na **data de referência**. Toda variável é calculada "como era naquele dia". Se o modelo vai prever cancelamentos do próximo trimestre, as variáveis precisam usar só o que se sabia antes dele. É a primeira defesa contra o vazamento, que vem logo adiante.

## Valores faltantes

A maioria dos modelos do scikit-learn não aceita valores vazios. As saídas mais comuns:

- **Apagar as linhas com vazio.** Simples, mas joga dados fora e pode distorcer a base, se os vazios não forem aleatórios: talvez os clientes insatisfeitos sejam justamente os que não respondem à pesquisa.
- **Preencher**, com a mediana para variáveis numéricas ou com a categoria mais comum para categóricas. É o que faz o `SimpleImputer`.
- **Preencher e marcar.** Uma coluna extra, como `nota_respondida`, guarda o fato de o valor ter faltado, para o modelo usar se isso for informativo. O `SimpleImputer` faz isso com `add_indicator=True`; no desafio, você cria a coluna à mão.
- **Usar um modelo que aceita vazios**, como o `HistGradientBoostingClassifier` do tópico anterior.

Em todos os casos, o valor de preenchimento, como a mediana, é calculado **só com o treino**, e o mesmo valor é usado depois para o teste e para os dados novos.

## Variáveis categóricas e escalas

As categorias viram colunas de 0 e 1 com a **codificação one-hot**. Três cuidados:

- **Categorias raras.** A base do desafio tem 47 cidades, quarenta delas com menos de 1% dos clientes cada. Uma coluna para cada uma geraria dezenas de colunas quase vazias, que o modelo não consegue aprender. O `OneHotEncoder` agrupa as raras numa categoria só, com `min_frequency`.
- **Categorias novas.** Em produção, vai aparecer uma cidade que não estava no treino. Com `handle_unknown="infrequent_if_exist"`, ela cai na categoria das raras, em vez de quebrar o modelo.
- **Nunca numere as categorias** de 1 a N para usar o número como variável: isso cria uma ordem que não existe, como se Curitiba fosse "maior" que Belo Horizonte.

Para categorias com muitos valores e muitos exemplos, como o CEP, existe a **codificação pela média do alvo**: cada categoria vira a taxa de cancelamento dos clientes dela. Ela é poderosa e perigosa, porque usa o próprio alvo, e precisa ser calculada com cuidado para não vazar. O `TargetEncoder` do scikit-learn já faz esse cuidado internamente.

Quanto à **escala**: modelos que comparam coeficientes ou distâncias, como a regressão logística com regularização, o k-vizinhos e o SVM, precisam de variáveis padronizadas, com média 0 e desvio 1, o que faz o `StandardScaler`. Modelos de árvore não precisam.

## Vazamento de dados

**Vazamento** é quando o modelo tem acesso, no treino, a informação que não teria no momento real da previsão. O resultado no teste fica ótimo, e o modelo não funciona em produção. É um dos erros mais caros em machine learning, porque só aparece tarde. Os tipos mais comuns:

- **Vazamento do alvo**: uma variável que só existe depois do evento, ou por causa dele. A data de cancelamento, o motivo do cancelamento, o número de ligações do time de retenção, que só liga para quem já pediu para sair. No desafio, um modelo com a data de cancelamento chega a uma AUC de 1,00. Sem ela, fica em 0,70, um resultado realista.
- **Contaminação entre treino e teste**: aprender o pré-processamento com a base inteira, como calcular a mediana ou escolher as variáveis antes de separar o teste. O efeito costuma ser menor, mas o resultado fica otimista.
- **Linhas repetidas**: o mesmo cliente, ou a mesma transação, no treino e no teste.
- **Vazamento no tempo**: num problema em que o futuro é previsto a partir do passado, sortear treino e teste ao acaso deixa o modelo aprender com dados posteriores aos que ele vai prever. O próximo tópico mostra como dividir respeitando o tempo.

Dois hábitos protegem contra quase todos: perguntar, para cada coluna, **"no dia da previsão, essa informação já existe?"**; e desconfiar de resultados bons demais. Uma coluna preenchida só para uma das classes, como a data de cancelamento, é um alerta fácil de automatizar, como você vai fazer no desafio.

## Pipelines no scikit-learn

O jeito mais seguro de garantir que o pré-processamento aprenda só com o treino é juntar tudo num **pipeline**:

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

numerico = Pipeline([
    ("imputar", SimpleImputer(strategy="median")),
    ("padronizar", StandardScaler()),
])
categorico = OneHotEncoder(
    handle_unknown="infrequent_if_exist",
    min_frequency=0.02, sparse_output=False,
)
preparo = ColumnTransformer([
    ("numericas", numerico, numericas),
    ("categoricas", categorico, categoricas),
])
modelo = Pipeline([
    ("preparo", preparo),
    ("modelo", LogisticRegression(max_iter=2000)),
])

modelo.fit(X_treino, y_treino)
probs = modelo.predict_proba(X_teste)[:, 1]
```

O `ColumnTransformer` aplica um tratamento diferente a cada grupo de colunas. O `Pipeline` encadeia as etapas. No `fit`, cada etapa aprende com os dados de treino: as medianas, as médias e os desvios, as categorias frequentes. No `predict_proba`, as mesmas etapas são aplicadas ao teste, com o que foi aprendido no treino.

Além de evitar a contaminação, o pipeline tem duas vantagens práticas. Ele é **um objeto só**, que pode ser salvo e usado em produção sem reescrever o pré-processamento. E ele funciona dentro da **validação cruzada**, o assunto do próximo tópico: em cada rodada, o pipeline inteiro é treinado de novo, só com a parte de treino daquela rodada.
