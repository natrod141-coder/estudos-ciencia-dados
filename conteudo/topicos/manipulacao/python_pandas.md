---
titulo: "Python e pandas"
modulo: manipulacao
ordem: 2
horas: 16
estado: publicado
resumo: "Ler, limpar, transformar e agrupar dados com pandas, com NumPy e tratamento de dados faltantes."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "NumPy: arrays e operações vetorizadas"
    tipo: leitura
    minutos: 20
  - id: a2
    titulo: "Series e DataFrame: ler, olhar e selecionar"
    tipo: leitura
    minutos: 20
  - id: a3
    titulo: "Tipos de dado e conversões"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "Dados faltantes: encontrar, entender e tratar"
    tipo: leitura
    minutos: 25
  - id: a5
    titulo: "Criar colunas, filtrar e ordenar"
    tipo: leitura
    minutos: 15
  - id: a6
    titulo: "Agrupar e resumir: groupby, agg e pivot_table"
    tipo: leitura
    minutos: 20
  - id: a7
    titulo: "Juntar tabelas: merge e concat"
    tipo: leitura
    minutos: 15
  - id: a8
    titulo: "Boas práticas com pandas"
    tipo: leitura
    minutos: 10
  - id: a9
    titulo: "Vídeo de apoio: NumPy para análise de dados"
    tipo: video
    minutos: 25
    link: ""
  - id: a10
    titulo: "Vídeo de apoio: pandas do zero"
    tipo: video
    minutos: 40
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Dado a = np.array([1, 2, 3]), o que a * 2 devolve?"
    opcoes: ["[1, 2, 3, 1, 2, 3]", "array([2, 4, 6])", "Um erro, porque não dá para multiplicar um array por um número", "6"]
    correta: 1
    explicacao: "No NumPy, as operações são feitas elemento a elemento: cada valor é multiplicado por 2. Com uma lista do Python, [1, 2, 3] * 2 repetiria a lista, dando [1, 2, 3, 1, 2, 3]. Essa diferença é a base da vetorização."
  - pergunta: "O que np.where(x > 0, x, 0) faz com o array x?"
    opcoes: ["Remove os valores negativos, e o array fica menor", "Devolve as posições dos valores positivos", "Devolve um array do mesmo tamanho, com os valores que não são positivos trocados por 0", "Conta quantos valores são positivos"]
    correta: 2
    explicacao: "Com três argumentos, o np.where escolhe elemento a elemento: onde a condição é verdadeira, pega o valor de x, e onde é falsa, pega 0. O tamanho não muda. Com um argumento só, np.where(x > 0), ele devolve as posições, o que é outro uso."
  - pergunta: "Qual é a diferença entre df.loc[5] e df.iloc[5]?"
    opcoes: ["loc busca pelo rótulo do índice, e iloc pela posição, começando em 0", "Nenhuma, são sinônimos", "loc seleciona colunas, e iloc seleciona linhas", "iloc é a versão antiga e não deve ser usada"]
    correta: 0
    explicacao: "O loc usa os rótulos: df.loc[5] é a linha cujo índice vale 5, onde quer que ela esteja. O iloc usa a posição: df.iloc[5] é a sexta linha. Depois de filtrar ou ordenar, os dois costumam apontar para linhas diferentes."
  - pergunta: "O que df[df['canal'] == np.nan] devolve?"
    opcoes: ["As linhas com canal faltante", "Um erro de tipo", "Todas as linhas", "Nenhuma linha, porque NaN não é igual a nada, nem a ele mesmo"]
    correta: 3
    explicacao: "Por definição, NaN == NaN é falso, então a comparação dá falso em todas as linhas. Para encontrar faltantes, use df['canal'].isna(), e para o contrário, .notna()."
  - pergunta: "Um CSV tem a coluna id_cliente com alguns valores faltantes. Ao ler com pd.read_csv, sem nenhuma opção, que tipo a coluna recebe?"
    opcoes: ["int64", "float64, porque o NaN do NumPy é um número de ponto flutuante", "str, porque há células vazias", "category"]
    correta: 1
    explicacao: "O NaN é um float, e uma coluna do NumPy só guarda um tipo. Com um faltante, a coluna inteira vira float64, e o id 42 aparece como 42.0. Para manter inteiros com faltantes, use o tipo Int64, com I maiúsculo: dtype={'id_cliente': 'Int64'}."
  - pergunta: "Uma coluna de idade tem 30% de valores faltantes. Qual deve ser o primeiro passo?"
    opcoes: ["Preencher com a média, para não perder linhas", "Apagar a coluna, porque tem faltantes demais", "Entender por que os valores faltam, porque o motivo muda o tratamento", "Preencher com zero"]
    correta: 2
    explicacao: "Se os faltantes forem ao acaso, preencher ou remover dá resultados parecidos. Se houver um padrão, como um formulário novo que passou a pedir a idade só a partir de março, ou pessoas mais velhas deixando de responder, qualquer tratamento automático distorce a análise. Olhe os faltantes cruzados com outras colunas antes de decidir."
  - pergunta: "Numa coluna de valor de compra, alguns valores faltam porque o sistema não registrou o valor. Por que preencher com 0 é um erro?"
    opcoes: ["Porque o pandas não aceita zero em colunas de valor", "Porque o fillna não funciona com números", "Porque zero deixa a coluna com tipo inteiro", "Porque zero é um valor real, diferente de 'não sei': a soma e a média ficariam mais baixas que a realidade"]
    correta: 3
    explicacao: "Zero significa 'a compra custou zero', o que é falso. A média cairia, e o ticket médio também. Zero só é um bom preenchimento quando faltante significa zero de fato, como 'nenhum desconto aplicado'."
  - pergunta: "Qual comando calcula o faturamento total de cada estado?"
    opcoes: ["df.groupby('estado')['valor'].sum()", "df.sum('estado')", "df['estado'].value_counts()", "df.sort_values('estado').sum()"]
    correta: 0
    explicacao: "O groupby separa as linhas por estado, a seleção ['valor'] escolhe a coluna e o sum soma cada grupo. É o padrão separar, aplicar e combinar. O value_counts conta as linhas de cada estado, mas não soma valores."
  - pergunta: "Um merge de 1.000 pedidos com a tabela de clientes, com how='left', resultou em 1.080 linhas. Qual é a causa mais provável?"
    opcoes: ["O merge sempre acrescenta algumas linhas", "Alguns pedidos não têm cliente", "Há clientes repetidos na tabela de clientes, e os pedidos deles foram duplicados", "O how='left' cria uma linha extra para cada cliente"]
    correta: 2
    explicacao: "Se um id_cliente aparece duas vezes na tabela de clientes, cada pedido desse cliente casa com as duas linhas e é duplicado. Conferir a quantidade de linhas antes e depois do merge, ou usar validate='many_to_one', pega esse erro na hora."
  - pergunta: "Depois de um merge com how='left' entre pedidos e clientes, algumas linhas ficaram com o nome do cliente vazio. O que isso indica?"
    opcoes: ["Um erro do pandas", "Clientes que não fizeram pedidos", "Nomes que tinham acentos", "Pedidos cujo id_cliente não existe na tabela de clientes"]
    correta: 3
    explicacao: "O how='left' mantém todas as linhas da tabela da esquerda, os pedidos. Quando não há cliente correspondente, as colunas vindas da direita ficam faltantes. Com indicator=True, o merge cria uma coluna que mostra de onde veio cada linha."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Uma base de clientes tem a coluna renda com 25% de valores faltantes, e um colega sugere: 'é só preencher com a média'. Explique os riscos dessa sugestão e como você decidiria o tratamento."
  rubrica:
    - "Diz que é preciso entender o motivo dos faltantes antes de tratar, por exemplo verificando se clientes de renda alta ou de algum canal deixam mais a renda em branco."
    - "Explica os efeitos de preencher com a média: ela é puxada por valores extremos, reduz artificialmente a variabilidade e, se os faltantes tiverem um padrão, enviesa as conclusões."
    - "Propõe alternativas, como a mediana por grupo, uma coluna indicando o que foi imputado, comparar a análise com e sem os valores imputados ou tratar 'não informado' como categoria, e documentar a decisão."
  modelo: "Antes de preencher, eu investigaria por que a renda falta. Se os faltantes estiverem concentrados num grupo, como clientes de renda alta que preferem não informar, ou clientes que vieram de um canal cujo cadastro não pede renda, preencher com a média de todos distorce a análise desse grupo. A média também tem problemas próprios: renda é assimétrica, então a média é puxada pelos valores altos, e colocar o mesmo valor em 25% das linhas reduz artificialmente a variabilidade. Eu usaria a mediana, de preferência calculada dentro de grupos parecidos, como região ou faixa etária, e criaria uma coluna indicando quais valores foram imputados. Também rodaria a análise principal com e sem os imputados, para ver se a conclusão muda. Se a renda for usada em faixas, 'não informado' pode ser uma categoria própria. E registraria a decisão, para quem usar a base depois."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Da base crua à análise"
  descricao: "Uma loja online exportou seis meses de pedidos e o cadastro de clientes, com pedidos repetidos, valores escritos como n/d e pedidos sem cliente, sem canal e sem valor. Você vai usar NumPy para cálculos vetorizados, ler os dados com os tipos certos, tratar os faltantes com uma regra para cada coluna, juntar as tabelas e responder às perguntas da diretoria."
  pasta: "desafios/manipulacao/python_pandas"
  testes: 13
  tempo: "3 h"
  ferramentas: "VS Code, Python 3.11 ou superior, NumPy, pandas e pytest"
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
      descricao: "Abra desafios/manipulacao/python_pandas/README.md. Os dados estão em data/pedidos.csv (uma linha por pedido: id, data, cliente, categoria, canal, itens e valor) e data/clientes.csv (id, nome, estado e data de cadastro)."
    - titulo: "Implemente as funções em solucao.py"
      descricao: "O arquivo tem quatro partes: NumPy, leitura, dados faltantes e análise. Siga a ordem, porque cada parte usa as anteriores. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def padronizar(valores):"
        - "def aplicar_desconto(precos, quantidades, minimo=10, desconto=0.10):"
        - "def classificar_valores(valores):"
        - "def ler_pedidos(caminho_csv):"
        - "def resumo_faltantes(tabela):"
        - "def tratar_faltantes(pedidos):"
        - "def juntar_clientes(pedidos, clientes):"
        - "def resumo_por_estado(pedidos):"
        - "def evolucao_mensal(pedidos):"
        - "def top_clientes(pedidos, n=5):"
        - "def analisar(caminho_pedidos, caminho_clientes):"
    - titulo: "Rode os testes a cada função pronta"
      descricao: "O pytest mostra qual teste falhou e por quê. Leia a mensagem antes de mudar o código."
      comandos:
        - "cd desafios/manipulacao/python_pandas"
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/python_pandas"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de Python e pandas"'
        - "git push -u origin desafio/python_pandas"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Arranjo (array)", en: "array, ndarray" }
  - { pt: "Vetorização", en: "vectorization" }
  - { pt: "Difusão", en: "broadcasting" }
  - { pt: "Máscara booleana", en: "boolean mask" }
  - { pt: "Índice", en: "index" }
  - { pt: "Tipo de dado", en: "data type (dtype)" }
  - { pt: "Valor faltante", en: "missing value (NaN, NA)" }
  - { pt: "Imputação", en: "imputation" }
  - { pt: "Agrupar", en: "group by" }
  - { pt: "Agregação", en: "aggregation" }
  - { pt: "Junção", en: "join, merge" }
  - { pt: "Concatenar", en: "concatenate" }
  - { pt: "Encadeamento de métodos", en: "method chaining" }
  - { pt: "Cópia sob demanda", en: "copy-on-write" }
---

## NumPy: arrays e operações vetorizadas

O NumPy é a base do cálculo numérico em Python. O pandas é construído em cima dele, e muito do que parece "mágica" no pandas vem do NumPy. A estrutura central é o **array**: uma sequência de valores, todos do mesmo tipo, guardados lado a lado na memória.

```python
import numpy as np

precos = np.array([10.0, 20.0, 5.0])
quantidades = np.array([2, 10, 12])

precos.shape, precos.dtype   # ((3,), dtype('float64'))
```

A diferença para uma lista do Python está nas operações. Com arrays, elas acontecem **elemento a elemento**, sem precisar de `for`:

```python
totais = precos * quantidades        # array([ 20., 200.,  60.])
precos * 1.1                         # aumento de 10% em todos
[10, 20] * 2                         # lista: [10, 20, 10, 20]
```

Isso se chama **vetorização**. Além de mais curto, é muito mais rápido: o laço acontece dentro do NumPy, em código compilado, e não linha a linha no Python. Com um milhão de valores, a diferença costuma ser de dezenas de vezes.

Três ferramentas aparecem o tempo todo:

- **Máscaras booleanas.** Uma comparação gera um array de verdadeiros e falsos, que serve para filtrar: `totais[totais > 50]` devolve só os totais acima de 50.
- **`np.where`** escolhe entre dois valores, elemento a elemento: `np.where(quantidades >= 10, totais * 0.9, totais)` dá desconto de 10% só nas compras grandes.
- **`np.select`** generaliza para várias faixas: recebe uma lista de condições e uma de resultados, e usa a primeira condição verdadeira.

Funções de resumo como `sum`, `mean`, `std`, `min` e `max` funcionam sobre o array inteiro ou, num array de duas dimensões, por linha ou coluna, com o argumento `axis`. Atenção a um detalhe já visto em estatística: `np.std` divide por n. Para o desvio padrão amostral, use `np.std(x, ddof=1)`.

O valor faltante do NumPy é o `np.nan`, que é um número de ponto flutuante. Qualquer conta com ele dá `nan`: `np.mean([1, np.nan, 3])` devolve `nan`. As versões `np.nanmean`, `np.nansum` e parecidas ignoram os faltantes.

## Series e DataFrame: ler, olhar e selecionar

O pandas tem duas estruturas. A **Series** é uma coluna: um array do NumPy com um **índice**, que dá um rótulo a cada valor. O **DataFrame** é uma tabela: várias Series que compartilham o mesmo índice.

Quase toda análise começa lendo um arquivo. O `read_csv` tem opções para os problemas mais comuns:

```python
import pandas as pd

pedidos = pd.read_csv(
    "data/pedidos.csv",
    sep=",",                   # num CSV brasileiro, ";"
    decimal=".",               # e, nesse caso, ","
    parse_dates=["data"],      # converte a coluna para data
    na_values=["n/d"],         # textos que significam faltante
    dtype={"id_cliente": "Int64"},
)
```

Antes de qualquer cálculo, olhe os dados:

| Comando                        | Mostra                                                   |
| ------------------------------ | -------------------------------------------------------- |
| `df.head()`, `df.sample(5)`    | Algumas linhas                                           |
| `df.shape`                     | Quantidade de linhas e colunas                           |
| `df.info()`                    | Tipo de cada coluna e quantos valores não faltantes tem  |
| `df.describe()`                | Resumo estatístico das colunas numéricas                 |
| `df["canal"].value_counts()`   | Frequência de cada valor                                 |
| `df["id_pedido"].is_unique`    | Se a coluna tem valores repetidos                        |

Para selecionar:

- uma coluna: `df["valor"]`, que devolve uma Series;
- várias colunas: `df[["data", "valor"]]`, que devolve um DataFrame (repare nos colchetes duplos);
- linhas por condição: `df[df["valor"] > 100]`;
- linhas e colunas por rótulo: `df.loc[df["canal"] == "app", ["data", "valor"]]`;
- linhas e colunas por posição: `df.iloc[0:5, 0:3]`.

O `loc` usa os rótulos do índice, e o `iloc` usa a posição, começando em 0. Depois de filtrar ou ordenar, o rótulo 5 e a posição 5 raramente são a mesma linha.

## Tipos de dado e conversões

Cada coluna tem um tipo, o **dtype**, e metade dos erros de análise vem de uma coluna no tipo errado. Os principais:

| dtype            | Guarda                       | Observação                                                     |
| ---------------- | ---------------------------- | -------------------------------------------------------------- |
| `int64`          | Inteiros                     | Não aceita faltantes: com um faltante, a coluna vira `float64` |
| `Int64`          | Inteiros com faltantes       | Com I maiúsculo, usa `pd.NA` como faltante                     |
| `float64`        | Números com casas decimais   | Faltante é `NaN`                                               |
| `bool`           | Verdadeiro ou falso          |                                                                |
| `datetime64`     | Datas e horas                | Faltante é `NaT`                                               |
| `str` ou `object`| Texto                        | No pandas 3, texto tem o tipo `str`; em versões anteriores, `object` |
| `category`       | Poucos valores repetidos     | Economiza memória e aceita ordem, como visto em tipos de variáveis |

As conversões mais usadas:

```python
# texto para número; o que não for número vira faltante
df["valor"] = pd.to_numeric(df["valor"], errors="coerce")

# texto para data, com o formato explícito
df["data"] = pd.to_datetime(df["data"], format="%d/%m/%Y")

# limpeza de texto: os métodos .str valem para a coluna inteira
df["nome"] = df["nome"].str.strip().str.title()
```

O `errors="coerce"` transforma em faltante tudo o que não conseguir converter, em vez de parar com erro. É prático, mas silencioso: compare a quantidade de faltantes antes e depois da conversão para saber quantos valores foram perdidos.

Colunas de data ganham o acessor `.dt`: `df["data"].dt.month`, `.dt.day_name()`, `.dt.to_period("M")` (o mês, bom para agrupar). Subtrair duas datas dá um intervalo de tempo, e `(fim - inicio).dt.days` dá o número de dias.

## Dados faltantes: encontrar, entender e tratar

Dados reais têm buracos: um campo opcional do cadastro, um sensor que falhou, um sistema que não registrou o valor. Tratar faltantes é uma decisão de análise, e não um detalhe técnico.

**1. Encontrar.** Faltantes aparecem como `NaN`, `None`, `pd.NA` ou `NaT`, e também disfarçados: "n/d", "-", "sem informação", 0 ou 9999 em colunas em que esses valores não fazem sentido. Os disfarçados precisam ser convertidos primeiro, com `na_values` na leitura ou `replace` depois. Então:

```python
df.isna().sum()                    # faltantes por coluna
df.isna().mean() * 100             # porcentagem por coluna
df[df["valor"].isna()]             # as linhas com valor faltante
```

**2. Entender.** Pergunte **por que** o valor falta. Há três situações típicas:

- **Ao acaso:** a falta não tem relação com nada. Um erro de gravação que atingiu linhas aleatórias.
- **Ligada a outra coluna:** a falta depende de algo que você observa. O canal só começou a ser registrado em março, ou o app não pede a renda.
- **Ligada ao próprio valor:** a falta depende do valor que falta. Pessoas de renda muito alta deixam a renda em branco com mais frequência.

Para investigar, cruze a falta com outras colunas: `df.groupby("canal")["renda"].apply(lambda s: s.isna().mean())`. No primeiro caso, quase qualquer tratamento funciona. No terceiro, qualquer preenchimento automático distorce a análise, e o melhor é registrar a limitação.

**3. Tratar.** As opções, cada uma com seu uso:

| Tratamento                                      | Em pandas                                           | Quando usar                                                  |
| ----------------------------------------------- | --------------------------------------------------- | ------------------------------------------------------------ |
| Remover as linhas                               | `df.dropna(subset=["id_cliente"])`                  | Poucas linhas, ou sem o valor a linha não tem uso            |
| Remover a coluna                                | `df.drop(columns=["campo"])`                        | A coluna quase toda vazia e sem importância                  |
| Preencher com uma categoria                     | `df["canal"].fillna("não informado")`               | Variáveis qualitativas: admitir que não se sabe              |
| Preencher com zero                              | `df["desconto"].fillna(0)`                          | Só quando faltante significa zero de fato                    |
| Preencher com a mediana do grupo                | `df.groupby("categoria")["valor"].transform("median")` | Quantitativas, quando os grupos diferem entre si          |
| Repetir o último valor conhecido                | `df["estoque"].ffill()`                             | Séries no tempo que mudam pouco                              |

Três regras valem para qualquer escolha:

- **Crie uma coluna que marque o que foi imputado**, como `df["valor_imputado"] = df["valor"].isna()` antes de preencher. Um valor estimado nunca deve passar por um valor real.
- **Prefira a mediana à média** em variáveis assimétricas, e calcule dentro de grupos parecidos quando os grupos têm faixas diferentes.
- **Rode a análise com e sem os imputados.** Se a conclusão mudar, ela depende da imputação, e isso precisa ser dito.

Por fim, saiba como o pandas lida com faltantes nas contas. `sum`, `mean` e parecidas **ignoram** os faltantes. `count` conta só os não faltantes, enquanto `len` conta todas as linhas. E nenhuma comparação encontra um `NaN`: `df["canal"] == np.nan` é falso em todas as linhas. Use sempre `.isna()` e `.notna()`.

## Criar colunas, filtrar e ordenar

```python
# nova coluna: a operação vale para a coluna inteira
df["ticket_por_item"] = df["valor"] / df["itens"]
df["faixa"] = np.where(df["valor"] >= 500, "alto", "normal")

# filtros: condições entre parênteses, com & (e), | (ou), ~ (não)
grandes_do_app = df[(df["valor"] > 500) & (df["canal"] == "app")]
sudeste = df[df["estado"].isin(["SP", "RJ", "MG", "ES"])]
marco = df[df["data"].between("2026-03-01", "2026-03-31")]

# ordenar e tirar repetidos
df.sort_values(["data", "valor"], ascending=[True, False])
df.drop_duplicates(subset="id_pedido")
```

Nos filtros, use `&` e `|`, e não `and` e `or`, que não funcionam com Series. Os parênteses em cada condição são obrigatórios.

## Agrupar e resumir: groupby, agg e pivot_table

O `groupby` segue o padrão **separar, aplicar e combinar**: separa as linhas em grupos, aplica um cálculo a cada grupo e junta os resultados numa tabela.

```python
# um cálculo
df.groupby("estado")["valor"].sum()

# vários cálculos, com nomes escolhidos por você
resumo = df.groupby("estado").agg(
    pedidos=("id_pedido", "count"),
    faturamento=("valor", "sum"),
    ticket_medio=("valor", "mean"),
).sort_values("faturamento", ascending=False)

# dois níveis de grupo, virando tabela com pivot_table
pd.pivot_table(df, index="estado", columns="canal",
               values="valor", aggfunc="sum", fill_value=0)
```

A diferença entre `agg` e `transform` confunde no começo. O `agg` devolve **uma linha por grupo**. O `transform` devolve **um valor por linha original**, com o resultado do grupo daquela linha. Por isso o `transform` serve para comparar cada linha com o seu grupo, como `df["valor"] / df.groupby("estado")["valor"].transform("mean")`, e para preencher faltantes com a mediana do grupo.

Para séries no tempo, agrupe pelo período e compare com o anterior:

```python
mensal = df.groupby(df["data"].dt.to_period("M"))["valor"].sum()
# variação % em relação ao mês anterior
mensal.pct_change() * 100
```

## Juntar tabelas: merge e concat

O `merge` junta duas tabelas por uma coluna em comum, como o PROCX do Excel ou o JOIN do SQL:

```python
completo = pedidos.merge(
    clientes[["id_cliente", "nome", "estado"]],
    on="id_cliente",
    how="left",
    validate="many_to_one",
)
```

| `how`     | Mantém                                                      |
| --------- | ----------------------------------------------------------- |
| `"inner"` | Só as linhas com correspondência nas duas tabelas (padrão)  |
| `"left"`  | Todas as linhas da esquerda; sem correspondência, faltante  |
| `"right"` | Todas as linhas da direita                                  |
| `"outer"` | Todas as linhas das duas                                    |

O erro mais comum em merge é a **duplicação silenciosa**: se a chave se repete na tabela da direita, cada linha da esquerda casa com todas as repetições e é duplicada. Três proteções: conferir `len` antes e depois, usar `validate="many_to_one"` (o pandas para com erro se a direita tiver chaves repetidas) e usar `indicator=True` para ver quais linhas não encontraram par.

Para empilhar tabelas com as mesmas colunas, como os arquivos de janeiro, fevereiro e março, use `pd.concat([jan, fev, mar], ignore_index=True)`.

## Boas práticas com pandas

- **Não modifique o que recebeu.** Uma função que limpa dados deve devolver uma tabela nova. A partir do pandas 3.0, o modo de cópia sob demanda (*copy-on-write*) é o padrão: cada operação se comporta como se devolvesse uma cópia, e atribuições encadeadas como `df[df["a"] > 0]["b"] = 1` não alteram mais o `df`. Para alterar parte de uma tabela, use `df.loc[condição, "b"] = 1`.
- **Encadeie as etapas** quando elas formam uma sequência. O código fica legível de cima para baixo:

  ```python
  resumo = (
      pd.read_csv("data/pedidos.csv", na_values=["n/d"])
      .drop_duplicates(subset="id_pedido")
      .query("valor > 0")
      .groupby("categoria")["valor"]
      .agg(["count", "sum", "mean"])
  )
  ```

- **Evite `for` sobre as linhas** (`iterrows`, `apply` com funções de linha). Quase sempre existe uma operação vetorizada que faz o mesmo muito mais rápido.
- **Confira o tamanho a cada etapa.** Uma linha que some num filtro ou se duplica num merge só aparece no resultado final, quando já é difícil de rastrear.
