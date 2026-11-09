---
titulo: "Random Forest"
modulo: ml_classico
ordem: 4
horas: 7
estado: publicado
resumo: "Várias árvores votando juntas para errar menos."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Por que muitas árvores erram menos que uma"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "Bagging e o sorteio de variáveis"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Quantas árvores, e de que tamanho"
    tipo: leitura
    minutos: 10
  - id: a4
    titulo: "A estimativa fora da sacola"
    tipo: leitura
    minutos: 8
  - id: a5
    titulo: "Importância das variáveis: duas medidas, uma armadilha"
    tipo: leitura
    minutos: 12
  - id: a6
    titulo: "Vídeo de apoio: random forest"
    tipo: video
    minutos: 25
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Por que a média de muitas árvores costuma errar menos que uma árvore só?"
    opcoes: ["Porque cada árvore da floresta é mais profunda", "Porque árvores diferentes erram de jeitos diferentes, e na média parte desses erros se cancela", "Porque a floresta usa mais variáveis que a árvore", "Porque a floresta é treinada por mais tempo"]
    correta: 1
    explicacao: "Uma árvore funda tem pouco viés, mas muita variância: muda muito com os dados. A média de muitas árvores diferentes mantém o pouco viés e reduz a variância. Isso só funciona se as árvores forem diferentes entre si."
  - pergunta: "O que é a amostragem bootstrap, usada no bagging?"
    opcoes: ["Separar os dados em treino e teste", "Escolher as melhores variáveis antes do treino", "Treinar a mesma árvore várias vezes", "Sortear, com reposição, uma amostra do mesmo tamanho dos dados de treino para cada árvore, de modo que cada uma vê um conjunto um pouco diferente de exemplos"]
    correta: 3
    explicacao: "Com reposição, alguns clientes aparecem duas ou três vezes na amostra de uma árvore, e cerca de 37% não aparecem. Cada árvore aprende com uma versão diferente dos dados, e por isso elas erram de jeitos diferentes."
  - pergunta: "Para que serve o parâmetro max_features, que limita as variáveis consideradas em cada divisão?"
    opcoes: ["Para deixar as árvores mais diferentes entre si: sem ele, todas começariam pelas mesmas variáveis fortes e errariam parecido", "Para reduzir o número de colunas da tabela", "Para escolher a variável alvo", "Para impedir que a floresta use variáveis categóricas"]
    correta: 0
    explicacao: "Se uma variável é muito forte, todas as árvores a usariam na primeira pergunta e ficariam parecidas. Sorteando um subconjunto de variáveis em cada divisão, outras variáveis ganham espaço. No desafio, a raiz quadrada do número de colunas, o padrão, foi a melhor opção."
  - pergunta: "O que acontece ao aumentar o número de árvores de 300 para 3.000?"
    opcoes: ["O modelo sobreajusta", "A AUC sempre melhora bastante", "Quase nada muda na qualidade, porque o ganho estabiliza, mas o treino e a previsão ficam mais lentos", "A floresta passa a decorar o treino"]
    correta: 2
    explicacao: "Mais árvores não causam sobreajuste numa random forest: a média só fica mais estável. Mas o ganho estabiliza: no desafio, de 200 para 500 árvores a AUC não muda. O limite prático é o tempo e a memória."
  - pergunta: "O que é a estimativa fora da sacola (OOB)?"
    opcoes: ["A AUC no conjunto de teste", "A avaliação de cada cliente de treino feita só pelas árvores que não o viram, o que dá uma estimativa do desempenho sem separar um conjunto de validação", "Uma forma de treinar mais rápido", "O erro das árvores que foram descartadas"]
    correta: 1
    explicacao: "Como cada árvore deixa de fora uns 37% dos clientes, todo cliente de treino tem um grupo de árvores que nunca o viu. A média delas é uma previsão honesta para ele. No desafio, a AUC fora da sacola, 0,757, ficou quase igual à do teste, 0,756."
  - pergunta: "Pela importância por impureza, a idade é a variável mais importante da floresta. Pela importância por permutação, os atrasos de pagamento são. Em qual confiar mais?"
    opcoes: ["Na de impureza, porque é calculada pelo próprio modelo", "Nas duas igualmente", "Na de permutação, porque mede quanto o desempenho cai em dados de teste quando a variável é embaralhada. A de impureza favorece variáveis com muitos valores diferentes, como a idade", "Em nenhuma, a importância de variáveis não faz sentido em florestas"]
    correta: 2
    explicacao: "Variáveis com muitos valores oferecem muitos pontos de corte e acabam usadas em divisões que só descrevem ruído do treino, o que infla a importância por impureza. A permutação mede o efeito real no desempenho, em dados que o modelo não viu."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Um colega diz: 'se uma árvore sobreajusta, uma floresta de 500 árvores deve sobreajustar 500 vezes mais'. Explique por que isso não acontece e o que, então, controla a qualidade de uma random forest."
  rubrica:
    - "Explica que a floresta faz a média de árvores treinadas com amostras bootstrap e sorteios de variáveis diferentes, cujos erros se cancelam em parte, o que reduz a variância."
    - "Diz que aumentar o número de árvores não causa sobreajuste: a média só fica mais estável, e o ganho estabiliza a partir de algumas centenas."
    - "Aponta o que de fato controla a qualidade: o tamanho das árvores, como min_samples_leaf, e o sorteio de variáveis, max_features, escolhidos com a estimativa fora da sacola ou com validação."
  modelo: "Cada árvore da floresta sobreajusta, sim: é funda e decora parte do seu treino. Mas cada uma é treinada com uma amostra diferente dos clientes, sorteada com reposição, e em cada divisão só pode escolher entre algumas variáveis sorteadas. Por isso, cada árvore decora coisas diferentes. Quando a floresta tira a média das 500, os erros particulares de cada árvore se cancelam em boa parte, e o que sobra é o padrão que aparece em muitas delas. Aumentar o número de árvores não piora nada: só deixa a média mais estável. No nosso caso, a partir de umas 200 árvores a AUC parou de mudar. O que controla a qualidade é o tamanho de cada árvore, como o mínimo de clientes por folha, que no nosso caso funcionou melhor em 5 do que em 1, e o número de variáveis sorteadas em cada divisão. Esses parâmetros eu escolho comparando a AUC fora da sacola, que avalia cada cliente só com as árvores que não o viram, ou numa validação separada."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Muitas árvores votando juntas"
  descricao: "Com os mesmos clientes dos tópicos anteriores, você vai treinar uma random forest, compará-la com uma árvore sozinha, medir quanto ela melhora com mais árvores, usar a estimativa fora da sacola no lugar da validação, comparar a estabilidade das duas e descobrir por que a importância por impureza engana."
  pasta: "desafios/ml_classico/random_forest"
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
      descricao: "Abra desafios/ml_classico/random_forest/README.md. Os clientes estão em data/assinaturas.csv."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def preparar(df):"
        - "def dividir(X, y, semente=42):"
        - "def treinar_floresta(X, y, n_arvores=300, semente=42):"
        - "def auc_teste(modelo, X, y):"
        - "def auc_oob(floresta, y_treino):"
        - "def curva_de_arvores(X_treino, y_treino, X_teste, y_teste, quantidades, semente=42):"
        - "def concordancia(modelo_a, modelo_b, X):"
        - "def importancia_por_impureza(modelo, colunas):"
        - "def importancia_por_permutacao(modelo, X, y, semente=42):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ml_classico/random_forest"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/random_forest"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de random forest"'
        - "git push -u origin desafio/random_forest"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Floresta aleatória", en: "random forest" }
  - { pt: "Combinação de modelos", en: "ensemble" }
  - { pt: "Amostragem com reposição", en: "bootstrap" }
  - { pt: "Agregação por bootstrap", en: "bagging (bootstrap aggregating)" }
  - { pt: "Variância do modelo", en: "variance" }
  - { pt: "Viés do modelo", en: "bias" }
  - { pt: "Estimativa fora da sacola", en: "out-of-bag (OOB) estimate" }
  - { pt: "Importância por impureza", en: "impurity-based feature importance (MDI)" }
  - { pt: "Importância por permutação", en: "permutation importance" }
---

## Por que muitas árvores erram menos que uma

No tópico anterior, você viu os dois problemas de uma árvore funda: ela decora o treino e muda muito com pequenas mudanças nos dados. Em termos técnicos, ela tem pouco **viés**, porque consegue representar padrões complicados, e muita **variância**, porque o que ela aprende depende demais da amostra.

A ideia da **random forest** é simples: em vez de uma árvore, treinar centenas e tirar a média das probabilidades. Se cada árvore erra de um jeito diferente, na média parte dos erros se cancela, e o que sobra é o padrão que aparece em muitas delas. A média mantém o pouco viés de cada árvore e corta a variância.

Mas há uma condição: as árvores precisam ser **diferentes entre si**. Cem cópias da mesma árvore erram igual, e a média delas é a própria árvore. A random forest usa dois sorteios para garantir essa diversidade.

## Bagging e o sorteio de variáveis

O primeiro sorteio é o **bootstrap**: cada árvore é treinada com uma amostra do mesmo tamanho dos dados de treino, sorteada **com reposição**. Alguns clientes aparecem duas ou três vezes na amostra de uma árvore, e cerca de 37% nem aparecem. Treinar vários modelos em amostras bootstrap e fazer a média se chama **bagging**.

O segundo sorteio é o das variáveis: em cada divisão, a árvore só pode escolher entre um subconjunto sorteado de colunas, controlado pelo `max_features`. Sem isso, todas as árvores começariam pelas mesmas variáveis fortes e ficariam parecidas. No scikit-learn, o padrão para classificação é a raiz quadrada do número de colunas. Nos dados do desafio, ele foi a melhor opção: AUC de 0,756 no teste, contra 0,746 com metade das colunas e 0,741 com todas.

```python
from sklearn.ensemble import RandomForestClassifier

floresta = RandomForestClassifier(
    n_estimators=300, min_samples_leaf=5,
    oob_score=True, random_state=42, n_jobs=-1,
)
floresta.fit(X_treino, y_treino)
probs = floresta.predict_proba(X_teste)[:, 1]
```

O `n_jobs=-1` treina as árvores em paralelo, usando todos os núcleos do computador. O resultado, no conjunto de teste do desafio: uma árvore sozinha, com a profundidade 6 escolhida no tópico anterior, chega a 0,70 de AUC; a floresta, a 0,76. E fica mais estável: treinando duas árvores com amostras um pouco diferentes dos dados, a correlação entre as probabilidades que elas dão aos mesmos clientes é de 0,76; entre duas florestas, de 0,97.

## Quantas árvores, e de que tamanho

Mais árvores **não causam sobreajuste** numa random forest: a média só fica mais estável. Mas o ganho estabiliza. Nos dados do desafio:

| Árvores | AUC no teste |
| ------- | ------------ |
| 1       | 0,63         |
| 10      | 0,74         |
| 50      | 0,75         |
| 200     | 0,76         |
| 500     | 0,76         |

O limite prático é o tempo e a memória. Algumas centenas de árvores costumam bastar.

O que mais influencia a qualidade é o **tamanho de cada árvore**. Por padrão, o scikit-learn deixa as árvores crescerem até o fim, com `min_samples_leaf=1`. Nos dados do desafio, exigir pelo menos 5 clientes por folha melhorou a AUC de 0,736 para 0,756: árvores um pouco menos fundas decoram menos ruído.

Uma vantagem prática das florestas é que os valores padrão já funcionam bem. Elas exigem bem menos ajuste que o modelo do próximo tópico, o gradient boosting.

## A estimativa fora da sacola

Como cada árvore deixou de fora uns 37% dos clientes de treino, todo cliente de treino tem um grupo de árvores que nunca o viu. A média das previsões dessas árvores é uma previsão honesta para ele: é a **estimativa fora da sacola**, ou OOB, do inglês *out-of-bag*.

```python
from sklearn.metrics import roc_auc_score

oob = floresta.oob_decision_function_[:, 1]
print(roc_auc_score(y_treino, oob))  # 0.757
```

No desafio, a AUC fora da sacola foi de 0,757, e a AUC no teste, de 0,756. A estimativa OOB permite comparar configurações de floresta sem separar um conjunto de validação, aproveitando todos os dados de treino.

## Importância das variáveis: duas medidas, uma armadilha

A floresta herda das árvores a **importância por impureza**: o quanto as divisões com cada variável reduziram a impureza, na média das árvores. Ela é rápida, porque sai do próprio treino, mas tem um viés conhecido: favorece variáveis com **muitos valores diferentes**. Uma variável como a idade, com dezenas de valores, oferece muitos pontos de corte, e acaba usada em divisões profundas que só descrevem ruído do treino.

A **importância por permutação** mede outra coisa: quanto o desempenho do modelo cai, em dados que ele não viu, quando os valores de uma coluna são embaralhados. Se embaralhar uma variável derruba a AUC, o modelo depende dela de verdade.

```python
from sklearn.inspection import permutation_importance

resultado = permutation_importance(
    floresta, X_teste, y_teste, scoring="roc_auc",
    n_repeats=5, random_state=42, n_jobs=-1,
)
importancia = pd.Series(resultado.importances_mean, index=X_teste.columns)
print(importancia.sort_values(ascending=False).head(4).round(3))
```

Nos dados do desafio, as duas medidas discordam. Pela impureza, a idade é a variável mais importante. Pela permutação, os atrasos de pagamento, os chamados ao suporte e a nota de satisfação vêm na frente, e a idade aparece em quarto. Os dados foram gerados com efeitos conhecidos, e a permutação acerta: os atrasos, os chamados e a satisfação são os que mais mexem no risco.

Dois cuidados com a permutação: calcule em dados de teste ou de validação, e não no treino; e, quando duas variáveis carregam a mesma informação, embaralhar uma delas derruba pouco o desempenho, porque o modelo usa a outra. Importância baixa não quer dizer, necessariamente, que a variável não tem relação com o alvo.

Por fim, os limites da floresta: ela é bem menos interpretável que uma árvore só, ocupa mais memória, é mais lenta para prever e, como as árvores, não extrapola: para valores fora do intervalo do treino, ela repete o que viu nas pontas.
