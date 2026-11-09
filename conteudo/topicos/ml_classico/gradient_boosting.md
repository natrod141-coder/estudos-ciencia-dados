---
titulo: "Gradient Boosting"
modulo: ml_classico
ordem: 5
horas: 7
estado: publicado
resumo: "XGBoost e LightGBM: árvores que corrigem os erros das anteriores."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "A ideia: cada árvore corrige as anteriores"
    tipo: leitura
    minutos: 12
  - id: a2
    titulo: "Os hiperparâmetros que importam"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Boosting sobreajusta: curva de validação e parada antecipada"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "XGBoost, LightGBM, CatBoost e o scikit-learn"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Boosting ou floresta?"
    tipo: leitura
    minutos: 8
  - id: a6
    titulo: "Vídeo de apoio: gradient boosting"
    tipo: video
    minutos: 30
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Qual é a diferença principal entre gradient boosting e random forest?"
    opcoes: ["O boosting usa regressão logística, e a floresta usa árvores", "O boosting só funciona com variáveis numéricas", "O boosting treina árvores em sequência, cada uma corrigindo os erros que as anteriores ainda cometem; a floresta treina árvores independentes e tira a média", "Não há diferença: são nomes diferentes para o mesmo modelo"]
    correta: 2
    explicacao: "Na floresta, as árvores são fundas e independentes, e a média reduz a variância. No boosting, as árvores são pequenas e dependentes: cada uma é ajustada ao que as anteriores erraram, e a soma delas reduz o viés."
  - pergunta: "O que faz a taxa de aprendizado (learning_rate) no boosting?"
    opcoes: ["Diminui a contribuição de cada árvore: com taxa menor, cada passo corrige menos, e são precisas mais árvores, mas o resultado costuma generalizar melhor", "Controla a profundidade das árvores", "Define quantos clientes cada árvore vê", "Acelera o treino sem mudar o resultado"]
    correta: 0
    explicacao: "Cada árvore nova entra multiplicada pela taxa. Passos pequenos corrigem os erros aos poucos, e o modelo tem mais chance de parar no ponto certo. No desafio, a taxa 0,3 chega ao melhor resultado em 9 iterações; a 0,03, em 91."
  - pergunta: "Com taxa 0,3 e 300 árvores, a AUC na validação foi máxima na 9ª árvore e caiu depois, enquanto a AUC no treino chegou a 1,0. O que aconteceu?"
    opcoes: ["As árvores ficaram pequenas demais", "Faltou padronizar as variáveis", "A validação está errada", "Sobreajuste: depois de corrigir os padrões reais, as árvores seguintes passaram a corrigir ruído do treino"]
    correta: 3
    explicacao: "Ao contrário da random forest, mais árvores no boosting podem piorar o modelo. Cada árvore nova reduz o erro no treino, mesmo quando não há mais padrão a aprender. Por isso o número de árvores precisa ser escolhido com validação."
  - pergunta: "Como funciona a parada antecipada (early stopping)?"
    opcoes: ["O modelo para quando o treino atinge AUC de 1,0", "Uma parte dos dados de treino fica separada como validação, e o treino para quando o desempenho nela não melhora por um número de iterações seguidas", "O modelo para depois de um tempo fixo", "O modelo para quando acaba a memória"]
    correta: 1
    explicacao: "Com early_stopping=True, o HistGradientBoostingClassifier separa uma fração do treino, acompanha o desempenho nela a cada iteração e para quando ele não melhora por n_iter_no_change iterações. No desafio, o modelo parou sozinho em 69 iterações, de um limite de 2.000."
  - pergunta: "O que o HistGradientBoostingClassifier faz com uma coluna que tem valores vazios?"
    opcoes: ["Dá erro, como a maioria dos modelos", "Apaga as linhas com valor vazio", "Trata o vazio como uma informação: em cada divisão, aprende para qual lado mandar os exemplos com valor faltante", "Troca os vazios pela média da coluna"]
    correta: 2
    explicacao: "Os boostings baseados em histograma, como este, o LightGBM e o XGBoost, aceitam valores faltantes sem pré-processamento. Às vezes, o próprio fato de faltar é informativo: um cliente que não respondeu à pesquisa de satisfação pode ter um risco diferente."
  - pergunta: "Nos dados do desafio, o boosting com parada antecipada e a random forest ficaram com AUC parecida no teste. Como decidir entre os dois?"
    opcoes: ["Escolher sempre o boosting, porque vence competições", "Comparar na validação, com a mesma divisão, e considerar também o custo de ajuste, o tempo de treino e de previsão, e a facilidade de manter; em empate, o mais simples de operar", "Escolher sempre a floresta, porque não sobreajusta", "Escolher pelo que deu a maior AUC no treino"]
    correta: 1
    explicacao: "Não existe um vencedor universal. Em muitos dados tabulares, um boosting bem ajustado fica à frente; em outros, como os do desafio, empata. A floresta funciona bem com os valores padrão; o boosting costuma pedir mais ajuste. A comparação certa é na validação, e a decisão leva em conta mais que a métrica."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Explique como o gradient boosting monta as previsões, por que ele pode sobreajustar quando ganha árvores demais, ao contrário da random forest, e como você escolheria o número de árvores."
  rubrica:
    - "Explica que o boosting soma árvores pequenas treinadas em sequência, cada uma ajustada aos erros que o conjunto das anteriores ainda comete, com a contribuição de cada uma reduzida pela taxa de aprendizado."
    - "Explica o sobreajuste: depois que os padrões reais foram corrigidos, as árvores novas continuam reduzindo o erro do treino corrigindo ruído, o que piora o desempenho em dados novos; na floresta, mais árvores só estabilizam a média."
    - "Descreve a escolha do número de árvores com validação: acompanhar a curva de validação a cada iteração ou usar a parada antecipada, e combinar com uma taxa de aprendizado menor."
  modelo: "O boosting começa com uma previsão simples, como a taxa média de cancelamento, e vai acrescentando árvores pequenas, uma de cada vez. Cada árvore nova é treinada para corrigir o que o conjunto das anteriores ainda erra: onde o modelo subestima o risco, ela puxa para cima; onde superestima, para baixo. A contribuição de cada árvore é reduzida pela taxa de aprendizado, para o modelo avançar em passos pequenos. O problema é que esse processo não tem um fim natural: sempre há algum erro no treino para corrigir. Depois que os padrões reais foram aprendidos, as árvores seguintes passam a corrigir ruído, coisas que só valem para os clientes do treino, e o desempenho em clientes novos piora. Na random forest é diferente: as árvores são independentes, e mais árvores só deixam a média mais estável. Para escolher o número de árvores, eu separo uma validação e acompanho a AUC a cada iteração, ou uso a parada antecipada, que faz isso sozinha e para quando a validação passa algumas iterações sem melhorar. Com uma taxa de aprendizado menor, o pico vem mais tarde e costuma ser um pouco melhor, ao custo de mais tempo de treino."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Árvores que corrigem os erros das anteriores"
  descricao: "Com os mesmos clientes dos tópicos anteriores, você vai treinar um gradient boosting, ver na curva de validação que ele sobreajusta com árvores demais, comparar taxas de aprendizado, usar a parada antecipada, comparar com a random forest e treinar com categorias e valores faltantes, sem pré-processamento."
  pasta: "desafios/ml_classico/gradient_boosting"
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
      descricao: "Abra desafios/ml_classico/gradient_boosting/README.md. Os clientes estão em data/assinaturas.csv."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "Cada função tem uma docstring com o que recebe e o que devolve. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def preparar(df):"
        - "def dividir_em_tres(X, y, semente=42):"
        - "def treinar_boosting(X, y, taxa=0.1, iteracoes=300, semente=42):"
        - "def auc(modelo, X, y):"
        - "def curva_de_validacao(modelo, X_val, y_val):"
        - "def melhor_iteracao(curva):"
        - "def treinar_com_parada_antecipada(X, y, taxa=0.05, semente=42):"
        - "def com_faltantes(X, coluna, fracao, semente=42):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/ml_classico/gradient_boosting"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/gradient_boosting"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de gradient boosting"'
        - "git push -u origin desafio/gradient_boosting"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Reforço de gradiente", en: "gradient boosting" }
  - { pt: "Taxa de aprendizado", en: "learning rate, shrinkage" }
  - { pt: "Função de perda", en: "loss function" }
  - { pt: "Perda logarítmica", en: "log loss" }
  - { pt: "Iteração", en: "iteration, boosting round" }
  - { pt: "Parada antecipada", en: "early stopping" }
  - { pt: "Curva de validação", en: "validation curve" }
  - { pt: "Boosting por histogramas", en: "histogram-based gradient boosting" }
  - { pt: "Categoria nativa", en: "native categorical support" }
  - { pt: "Valor faltante", en: "missing value" }
---

## A ideia: cada árvore corrige as anteriores

A random forest junta árvores **independentes**: cada uma é treinada sozinha, e a floresta tira a média. O **gradient boosting** junta árvores **em sequência**:

1. Começa com uma previsão simples, como a taxa média de cancelamento, a mesma para todos.
2. Olha onde essa previsão erra: os clientes que cancelaram com risco previsto baixo, os que ficaram com risco previsto alto.
3. Treina uma árvore pequena para corrigir esses erros, e soma a correção à previsão, multiplicada pela **taxa de aprendizado**.
4. Repete os passos 2 e 3 centenas de vezes.

Cada árvore nova se concentra no que o conjunto das anteriores ainda erra. Enquanto a floresta reduz a variância com a média de árvores fundas, o boosting reduz o viés somando árvores rasas, cada uma acrescentando um pouco do padrão que faltava.

O "gradiente" do nome vem da forma de medir o erro. O modelo tem uma **função de perda**, que, na classificação, costuma ser a perda logarítmica: ela pune mais as previsões confiantes e erradas. O gradiente dessa perda diz, para cada cliente, em que direção e com que força a previsão precisa mudar, e cada árvore nova é treinada para seguir essa direção. Não é preciso fazer a conta à mão: o importante é a ideia de corrigir aos poucos o que ainda está errado.

## Os hiperparâmetros que importam

O boosting tem mais botões que a floresta, e eles interagem entre si. Os principais:

- **Taxa de aprendizado** (`learning_rate`): o tamanho de cada passo de correção. Taxas menores, como 0,05 ou 0,03, pedem mais árvores, mas costumam generalizar melhor.
- **Número de árvores** (`max_iter` no scikit-learn, `n_estimators` em outras bibliotecas): quantos passos de correção. Diferente da floresta, aqui árvores demais pioram o modelo, como você vai ver.
- **Tamanho de cada árvore** (`max_depth`, `max_leaf_nodes`, `min_samples_leaf`): no boosting, as árvores são pequenas, de poucas folhas. Árvores maiores captam interações mais complexas, mas sobreajustam mais rápido.
- **Regularização** (`l2_regularization` no scikit-learn) e **subamostragem** de linhas e colunas, comum no XGBoost e no LightGBM: freios extras contra o sobreajuste.

A regra prática: fixe uma taxa de aprendizado pequena, escolha o número de árvores com validação ou parada antecipada, e só então ajuste o tamanho das árvores.

## Boosting sobreajusta: curva de validação e parada antecipada

Como cada árvore nova reduz o erro no treino, o treino sempre melhora. Mas, depois que os padrões reais foram aprendidos, as árvores seguintes passam a corrigir **ruído**, e o desempenho em dados novos piora. Nos dados do desafio, com 300 árvores:

| Taxa | Melhor iteração | AUC no pico | AUC com todas as árvores | AUC no treino |
| ---- | --------------- | ----------- | ------------------------ | ------------- |
| 0,3  | 9               | 0,780       | 0,727                    | 1,000         |
| 0,1  | 28              | 0,787       | 0,755                    | 1,000         |
| 0,03 | 91              | 0,785       | 0,771 (com 400)          | 0,979         |

A **curva de validação**, a AUC na validação depois de cada árvore, mostra o pico e a queda. O `staged_predict_proba` devolve as previsões depois de cada iteração, o que permite desenhar essa curva com um modelo só.

Na prática, o número de árvores é escolhido pela **parada antecipada**: o modelo separa uma parte do treino como validação interna, acompanha o desempenho a cada iteração e para quando ele passa um número de iterações seguidas sem melhorar.

```python
from sklearn.ensemble import HistGradientBoostingClassifier

X = assinaturas.drop(columns=["cliente_id", "cancelou"]).astype(
    {"plano": "category", "canal": "category"}
)
# depois de separar X_treino e y_treino, como nos tópicos anteriores
modelo = HistGradientBoostingClassifier(
    learning_rate=0.05,
    max_iter=2000,
    early_stopping=True,
    validation_fraction=0.2,
    n_iter_no_change=20,
    categorical_features="from_dtype",
    random_state=42,
)
modelo.fit(X_treino, y_treino)
print(modelo.n_iter_)  # parou sozinho, bem antes das 2.000
```

## XGBoost, LightGBM, CatBoost e o scikit-learn

O gradient boosting é tão usado em dados tabulares que ganhou bibliotecas próprias, muito otimizadas:

- **XGBoost**: popularizou o boosting em competições, com regularização e subamostragem embutidas.
- **LightGBM**: agrupa os valores de cada variável em faixas, os histogramas, o que acelera muito o treino em bases grandes.
- **CatBoost**: tem um tratamento cuidadoso de variáveis categóricas.

As três têm uma interface parecida com a do scikit-learn, com `fit` e `predict_proba`. O próprio scikit-learn tem o `HistGradientBoostingClassifier`, inspirado no LightGBM, que usamos no desafio por não exigir instalar nada além do scikit-learn. Ele tem dois recursos muito práticos:

- **Categorias nativas.** Com `categorical_features="from_dtype"`, as colunas do tipo `category` do pandas são tratadas como categorias, sem criar colunas de 0 e 1.
- **Valores faltantes.** Ele aceita colunas com vazios: em cada divisão, aprende para qual lado mandar os exemplos com valor faltante. No desafio, mesmo com 15% das notas de satisfação apagadas, o modelo treina e mantém uma AUC acima de 0,70, sem nenhum preenchimento.

## Boosting ou floresta?

Nos dados do desafio, o boosting com parada antecipada e a random forest ficaram no mesmo nível, com AUC em torno de 0,74 a 0,75 no teste. Isso surpreende quem ouviu que o boosting "sempre ganha", mas é comum: o resultado depende dos dados. Algumas orientações para escolher:

- **Compare na mesma validação**, com a mesma divisão, e inclua a regressão logística como referência. Se o modelo complexo não vence a logística com folga, a logística pode ser a melhor escolha, por ser simples de explicar e de manter.
- **A floresta funciona bem com os valores padrão** e quase não sobreajusta com mais árvores. É uma boa primeira tentativa.
- **O boosting costuma chegar mais longe com ajuste**, principalmente em bases grandes, mas exige cuidado com a taxa, o número de árvores e o tamanho delas.
- **Pense na operação**: tempo de treino, tempo de previsão, tamanho do modelo e facilidade de explicar o resultado para quem vai usar.

Os dois próximos tópicos tratam das duas peças que faltam para comparar modelos com segurança: preparar as variáveis sem vazar informação do teste e usar validação cruzada para escolher hiperparâmetros com mais confiança.
