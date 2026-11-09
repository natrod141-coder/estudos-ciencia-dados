---
titulo: "Árvores de decisão"
modulo: ml_classico
ordem: 3
horas: 7
estado: publicado
resumo: "Modelos que dividem os dados por perguntas sucessivas."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Como uma árvore decide"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "Como a árvore escolhe as perguntas"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "A árvore que decora"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Treino, validação e teste"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Ler a árvore, e os limites dela"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Vídeo de apoio: árvores de decisão"
    tipo: video
    minutos: 25
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Como uma árvore de decisão calcula a probabilidade de cancelar para um cliente novo?"
    opcoes: ["Somando o efeito de cada variável, como a regressão logística", "Procurando o cliente mais parecido na base", "Levando o cliente pelas perguntas até uma folha e usando a proporção de cancelamentos entre os clientes de treino daquela folha", "Fazendo a média de todas as folhas"]
    correta: 2
    explicacao: "Cada folha guarda os clientes de treino que responderam às perguntas do mesmo jeito. A probabilidade prevista é a proporção de cancelamentos entre eles. Por isso a árvore dá a mesma probabilidade a todos os clientes de uma mesma folha."
  - pergunta: "Uma árvore sem limite de profundidade teve AUC de 1,00 no treino e de 0,61 na validação. O que aconteceu?"
    opcoes: ["Sobreajuste: a árvore cresceu até separar cada cliente do treino e decorou casos particulares, que não se repetem em clientes novos", "O modelo é ótimo, a validação é que está errada", "Faltaram dados de treino", "A AUC não serve para árvores"]
    correta: 0
    explicacao: "Sem limite, a árvore continua dividindo até cada folha ter clientes de uma classe só. As últimas divisões capturam ruído, e não padrão. A distância grande entre o treino e a validação é o sinal clássico de sobreajuste."
  - pergunta: "Por que escolher a profundidade da árvore num conjunto de validação, e não no de teste?"
    opcoes: ["Porque o conjunto de teste é menor", "Porque a validação tem mais cancelamentos", "Porque o scikit-learn não aceita escolher pelo teste", "Porque, se o teste for usado para escolher, ele deixa de ser uma medida imparcial: o resultado fica otimista, como se tivesse sido ajustado a ele"]
    correta: 3
    explicacao: "Testar vinte profundidades e ficar com a melhor no teste é, na prática, ajustar o modelo ao teste. A validação serve para as escolhas; o teste é usado uma vez só, no fim, para medir o resultado. O tópico de validação cruzada mostra como fazer isso sem perder dados."
  - pergunta: "Quais parâmetros controlam o quanto uma árvore pode crescer?"
    opcoes: ["random_state e n_jobs", "max_depth, a profundidade máxima, e min_samples_leaf, o mínimo de exemplos por folha", "test_size e stratify", "C e max_iter"]
    correta: 1
    explicacao: "Limitar a profundidade, exigir um mínimo de exemplos por folha ou limitar o número de folhas impede a árvore de criar regras para grupos minúsculos. Esses são os hiperparâmetros a escolher na validação."
  - pergunta: "É preciso padronizar as variáveis, colocando todas na mesma escala, antes de treinar uma árvore?"
    opcoes: ["Sim, sempre", "Sim, mas só as variáveis em reais", "Não: cada pergunta compara uma variável com um valor de corte, e mudar a escala da variável só muda o valor do corte", "Não, porque árvores só aceitam variáveis de 0 e 1"]
    correta: 2
    explicacao: "Uma pergunta como 'valor mensal menor que 56,91?' funciona igual com o valor em reais ou em centavos. Por isso árvores não precisam de padronização, ao contrário da regressão logística regularizada."
  - pergunta: "Treinando a mesma árvore com uma amostra um pouco diferente dos dados, as regras mudam bastante. Que característica das árvores é essa, e o que fazer?"
    opcoes: ["É um erro de programação: as regras deviam ser sempre iguais", "É sinal de que faltam variáveis", "É a calibração das probabilidades", "É a instabilidade: pequenas mudanças nos dados mudam as primeiras perguntas, e a árvore inteira muda junto. Juntar muitas árvores, como faz a random forest, reduz esse problema"]
    correta: 3
    explicacao: "Como cada pergunta depende das anteriores, uma mudança no topo se propaga. A média de muitas árvores, cada uma treinada numa amostra diferente, é bem mais estável que qualquer árvore sozinha. É a ideia do próximo tópico."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Explique, para alguém do time de retenção, como funciona uma árvore de decisão, por que ela pode 'decorar' os clientes do treino e como você escolheu o tamanho da árvore do seu modelo."
  rubrica:
    - "Explica a árvore como uma sequência de perguntas sobre o cliente, que termina numa folha, e a previsão como a proporção de cancelamentos entre os clientes de treino da folha, com um exemplo de caminho."
    - "Explica o sobreajuste: sem limite, a árvore cria perguntas até separar cada cliente, e essas regras não valem para clientes novos, o que aparece na diferença entre o desempenho no treino e na validação."
    - "Descreve a escolha do tamanho com três conjuntos: várias profundidades comparadas na validação, a mais simples entre as melhores escolhida, e o teste usado uma vez só, no fim."
  modelo: "A árvore faz perguntas sobre o cliente, uma depois da outra, como num fluxograma. A primeira pergunta do nosso modelo é se a nota de satisfação é 2 ou menos. Se sim, a próxima é se ele abriu mais de um chamado no suporte. Cada caminho termina num grupo de clientes do histórico que responderam igual, e a chance de cancelar é a proporção de cancelamentos nesse grupo. Os insatisfeitos com vários chamados, por exemplo, cancelam bem mais que a média. O risco de decorar vem de a árvore poder continuar perguntando até cada grupo ter um cliente só. Aí ela acerta tudo no histórico, mas as últimas perguntas descrevem detalhes daqueles clientes específicos, que não se repetem. Para escolher o tamanho, separei os clientes em três partes. Treinei árvores de vários tamanhos com a primeira parte e comparei o desempenho na segunda, que o modelo não viu. A árvore sem limite acertava 100% do histórico e ia muito mal na segunda parte. O desempenho na segunda parte melhorava até umas seis perguntas em sequência e depois piorava, então fiquei com seis. A terceira parte foi usada uma vez só, no fim, para medir o resultado de forma honesta."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Uma árvore que se explica, e que decora"
  descricao: "Com os mesmos clientes do tópico anterior, você vai ver uma árvore sem limite decorar o treino, escolher a profundidade num conjunto de validação, ler as regras que a árvore aprendeu, encontrar o grupo de risco que ela descobriu sozinha e medir o resultado final no teste."
  pasta: "desafios/ml_classico/arvores_decisao"
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
      descricao: "Abra desafios/ml_classico/arvores_decisao/README.md. Os clientes estão em data/assinaturas.csv."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def preparar(df):"
        - "def dividir_em_tres(X, y, semente=42):"
        - "def treinar_arvore(X, y, profundidade=None, semente=42):"
        - "def auc(modelo, X, y):"
        - "def curva_de_profundidade(X_treino, y_treino, X_val, y_val, profundidades):"
        - "def melhor_profundidade(curva):"
        - "def regras(modelo, colunas):"
        - "def importancias(modelo, colunas):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ml_classico/arvores_decisao"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/arvores_decisao"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de árvores de decisão"'
        - "git push -u origin desafio/arvores_decisao"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Árvore de decisão", en: "decision tree" }
  - { pt: "Nó", en: "node" }
  - { pt: "Folha", en: "leaf" }
  - { pt: "Divisão", en: "split" }
  - { pt: "Impureza de Gini", en: "Gini impurity" }
  - { pt: "Profundidade máxima", en: "max depth" }
  - { pt: "Mínimo de exemplos por folha", en: "min samples leaf" }
  - { pt: "Hiperparâmetro", en: "hyperparameter" }
  - { pt: "Sobreajuste", en: "overfitting" }
  - { pt: "Conjunto de validação", en: "validation set" }
  - { pt: "Importância das variáveis", en: "feature importance" }
  - { pt: "Interação entre variáveis", en: "feature interaction" }
---

## Como uma árvore decide

Uma **árvore de decisão** prevê fazendo perguntas, uma depois da outra, como num fluxograma. Esta é a árvore de profundidade 3 treinada com os clientes do desafio:

```text
|--- nota_satisfacao <= 2.50
|   |--- chamados_suporte <= 1.50
|   |   |--- atrasos_pagamento <= 0.50
|   |   |   |--- class: 0
|   |   |--- atrasos_pagamento >  0.50
|   |   |   |--- class: 0
|   |--- chamados_suporte >  1.50
|   |   |--- valor_mensal <= 56.91
|   |   |   |--- class: 1
|   |   |--- valor_mensal >  56.91
|   |   |   |--- class: 1
|--- nota_satisfacao >  2.50
|   |--- atrasos_pagamento <= 1.50
|   |   |--- idade <= 24.50
|   |   |   |--- class: 0
|   |   |--- idade >  24.50
|   |   |   |--- class: 0
|   |--- atrasos_pagamento >  1.50
|   |   |--- meses_assinatura <= 13.50
|   |   |   |--- class: 1
|   |   |--- meses_assinatura >  13.50
|   |   |   |--- class: 0
```

Cada pergunta é um **nó**. Cada ponto final do caminho é uma **folha**. Um cliente novo desce pela árvore respondendo às perguntas até chegar a uma folha, e a previsão é tirada dos clientes de treino que chegaram àquela mesma folha: a probabilidade de cancelar é a proporção de cancelamentos entre eles, e a classe é a mais comum.

Repare no que a árvore encontrou sozinha: clientes com nota de satisfação baixa **e** com mais de um chamado ao suporte formam um grupo de alto risco. É uma **interação**: o risco depende da combinação, e não de cada variável isolada. A regressão logística, que soma os efeitos, não enxerga esse padrão a menos que alguém crie uma variável para ele.

## Como a árvore escolhe as perguntas

Para escolher a primeira pergunta, a árvore testa, para cada variável, vários pontos de corte, e fica com a divisão que deixa os grupos resultantes mais "puros": cada grupo com uma proporção de cancelamentos bem diferente da do outro. A medida de pureza mais usada é a **impureza de Gini**, que é zero quando um grupo tem clientes de uma classe só.

Depois, a árvore repete o processo dentro de cada grupo, e assim por diante. É uma escolha **gulosa**: cada pergunta é a melhor naquele momento, sem olhar para as perguntas que virão.

Algumas consequências práticas:

- **Não precisa padronizar as variáveis.** Uma pergunta como "valor mensal menor que 56,91?" funciona igual em reais ou em centavos: só muda o valor do corte.
- **Variáveis categóricas viram colunas de 0 e 1**, como na regressão, mas sem categoria de referência: a árvore pergunta sobre cada categoria separadamente.
- **A previsão é em degraus.** Todos os clientes de uma folha recebem a mesma probabilidade. Numa regressão com árvore, o valor previsto também muda em saltos, e não de forma contínua.

No scikit-learn, o roteiro é o de sempre:

```python
from sklearn.tree import DecisionTreeClassifier, export_text

arvore = DecisionTreeClassifier(max_depth=3, random_state=42)
arvore.fit(X_treino, y_treino)
print(export_text(arvore, feature_names=list(X_treino.columns)))
```

## A árvore que decora

Sem limite, a árvore continua dividindo até cada folha ter clientes de uma classe só. Nos dados do desafio, a árvore livre chega a 27 níveis de profundidade e 721 folhas, para 3 mil clientes de treino. No treino, ela acerta tudo. Em clientes que não viu, vai mal:

| Profundidade | AUC no treino | AUC na validação |
| ------------ | ------------- | ---------------- |
| 2            | 0,65          | 0,64             |
| 4            | 0,72          | 0,71             |
| 6            | 0,78          | 0,71             |
| 8            | 0,84          | 0,67             |
| 10           | 0,91          | 0,60             |
| sem limite   | 1,00          | 0,61             |

Até a profundidade 6, o desempenho na validação melhora junto com o do treino. Depois, o treino continua subindo, e a validação cai. As perguntas mais profundas já não descrevem padrões, e sim detalhes de clientes específicos, que não se repetem. Isso é **sobreajuste**: o modelo decorou o treino, em vez de aprender com ele.

O tamanho da árvore é controlado por **hiperparâmetros**, que você escolhe antes do treino:

- `max_depth`: o número máximo de perguntas em sequência.
- `min_samples_leaf`: o mínimo de clientes de treino em cada folha. Impede regras para grupos minúsculos.
- `max_leaf_nodes`: o número máximo de folhas.

## Treino, validação e teste

Para escolher a profundidade, é preciso comparar várias árvores em dados que elas não viram. Mas, se a comparação for feita no conjunto de teste, ele deixa de ser imparcial: escolher a melhor entre vinte árvores pelo teste é, na prática, ajustar o modelo a ele, e o resultado final fica otimista.

A saída é separar os dados em três partes:

- **Treino**, para ajustar cada candidato.
- **Validação**, para comparar os candidatos e fazer as escolhas.
- **Teste**, guardado até o fim, usado **uma vez só** para medir o modelo escolhido.

No desafio, a divisão é de 60%, 20% e 20%, sempre estratificada. Entre profundidades com desempenho parecido na validação, fique com a mais simples: ela tende a se comportar melhor em dados novos. O tópico de validação cruzada mostra como fazer essas escolhas sem abrir mão de 20% dos dados para a validação.

## Ler a árvore, e os limites dela

Uma árvore pequena é um dos modelos mais fáceis de explicar: cada caminho até uma folha vira uma frase. "Clientes com nota até 2 e mais de um chamado ao suporte cancelam muito mais que a média" é uma regra que o time de retenção entende e pode usar.

O scikit-learn também calcula a **importância** de cada variável: o quanto as divisões com aquela variável reduziram a impureza, somado na árvore toda. Na árvore de profundidade 5 do desafio, os chamados ao suporte e os atrasos de pagamento aparecem no topo. Dois cuidados com essa medida: ela favorece variáveis numéricas com muitos valores possíveis, que oferecem mais pontos de corte, e, quando duas variáveis são parecidas, a importância se divide entre elas. O próximo tópico mostra uma medida mais confiável, a importância por permutação.

Os limites de uma árvore sozinha:

- **Instabilidade.** Uma pequena mudança nos dados pode trocar a primeira pergunta, e a árvore inteira muda junto.
- **Sobreajuste fácil**, como você viu.
- **Desempenho limitado.** Nos dados do desafio, a melhor árvore fica em torno de 0,71 de AUC na validação, no mesmo patamar da regressão logística, apesar de achar as interações.

A solução mais usada para os três problemas é não confiar numa árvore só, e sim juntar muitas. É o assunto dos dois próximos tópicos: random forest e gradient boosting.
