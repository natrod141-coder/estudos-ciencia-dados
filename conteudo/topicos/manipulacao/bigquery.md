---
titulo: "BigQuery"
modulo: manipulacao
ordem: 5
horas: 5
estado: publicado
resumo: "SQL na nuvem: tabelas particionadas, custos e boas práticas."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "O que é o BigQuery e como ele guarda os dados"
    tipo: leitura
    minutos: 12
  - id: a2
    titulo: "Como a cobrança funciona"
    tipo: leitura
    minutos: 12
  - id: a3
    titulo: "Particionamento e clusterização"
    tipo: leitura
    minutos: 12
  - id: a4
    titulo: "Dados aninhados: STRUCT, ARRAY e UNNEST"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Funções úteis: QUALIFY, SAFE_CAST, COUNTIF e datas"
    tipo: leitura
    minutos: 10
  - id: a6
    titulo: "Vídeo de apoio: primeiros passos no console do BigQuery"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "No BigQuery sob demanda, quanto lê a consulta SELECT * FROM eventos LIMIT 10, numa tabela não particionada de 2 TB?"
    opcoes: ["Só as 10 linhas, quase nada", "A tabela inteira, cerca de 2 TB: o LIMIT só corta o resultado, e não o que é lido", "Metade da tabela", "Só o primeiro dia de dados"]
    correta: 1
    explicacao: "O BigQuery cobra pelos dados lidos das colunas referenciadas, e o LIMIT é aplicado depois da leitura. Para explorar uma tabela, use a aba de visualização do console, que não cobra, ou filtre por uma partição."
  - pergunta: "Por que escolher só as colunas necessárias reduz o custo de uma consulta no BigQuery?"
    opcoes: ["Porque o BigQuery guarda os dados por coluna e cobra apenas pelas colunas lidas", "Porque o resultado fica menor e mais rápido de baixar", "Porque colunas não selecionadas são apagadas", "Não reduz, o custo é por linha"]
    correta: 0
    explicacao: "O armazenamento é colunar: cada coluna fica guardada separadamente. Uma consulta que usa 3 de 50 colunas lê só essas 3. Por isso SELECT * é o hábito mais caro no BigQuery."
  - pergunta: "Uma tabela está particionada pela coluna data_evento. Qual filtro permite ao BigQuery ler só as partições necessárias?"
    opcoes: ["WHERE CAST(momento AS STRING) LIKE '2026-03%'", "ORDER BY data_evento DESC LIMIT 100", "WHERE data_evento BETWEEN '2026-03-01' AND '2026-03-07'", "WHERE id_usuario = 'U0001'"]
    correta: 2
    explicacao: "A poda de partições acontece quando o filtro é feito diretamente na coluna de partição, com valores constantes. Filtrar por outra coluna, ordenar ou limitar não evita a leitura das outras partições."
  - pergunta: "Para que serve clusterizar uma tabela pela coluna id_cliente?"
    opcoes: ["Criar uma tabela separada para cada cliente", "Deixar a tabela pública para outros projetos", "Remover as linhas duplicadas de cada cliente", "Guardar as linhas do mesmo cliente próximas umas das outras, para que filtros por id_cliente leiam menos blocos"]
    correta: 3
    explicacao: "A clusterização ordena os dados dentro de cada partição pelas colunas escolhidas, até quatro. Filtros e agrupamentos por essas colunas passam a ler menos blocos. Ela complementa o particionamento, que costuma ser por data."
  - pergunta: "Uma tabela tem um pedido por linha, com os itens num array. Depois de FROM pedidos, UNNEST(itens) AS item, o que COUNT(*) conta?"
    opcoes: ["O número de pedidos", "O número de itens, porque cada pedido vira uma linha por item", "O número de categorias", "Nada, porque o UNNEST não pode ser usado com COUNT"]
    correta: 1
    explicacao: "O UNNEST abre o array, e cada item vira uma linha, repetindo os dados do pedido. É a mesma multiplicação de linhas de um JOIN. Para contar pedidos depois do UNNEST, use COUNT(DISTINCT id_pedido)."
  - pergunta: "O que faz QUALIFY ROW_NUMBER() OVER (PARTITION BY id_evento ORDER BY ingerido_em DESC) = 1?"
    opcoes: ["Ordena os eventos pela data de ingestão", "Conta quantas vezes cada evento aparece", "Mantém só a versão gravada por último de cada evento, removendo duplicatas", "Filtra a primeira partição da tabela"]
    correta: 2
    explicacao: "O ROW_NUMBER numera as cópias de cada id_evento, da mais recente para a mais antiga, e o QUALIFY mantém só a de número 1. É o jeito mais comum de remover duplicatas no BigQuery, sem precisar de subconsulta."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Um painel roda, toda vez que alguém o abre, SELECT * FROM eventos_app numa tabela de 3 TB não particionada, e depois filtra os últimos 7 dias no próprio painel. A conta do BigQuery disparou. Explique por quê e proponha três mudanças."
  rubrica:
    - "Explica que o BigQuery sob demanda cobra pelos bytes lidos, que SELECT * sem filtro lê todas as colunas da tabela inteira a cada execução, e que filtrar depois, no painel, não reduz o que foi lido."
    - "Propõe ler só as colunas usadas e filtrar a data na própria consulta, com a tabela particionada por data e, se fizer sentido, clusterizada pelas colunas mais filtradas."
    - "Propõe uma terceira medida, como uma tabela agregada ou visão materializada para o painel, atualização agendada em vez de consulta a cada abertura, limite de bytes faturados ou estimativa antes de rodar."
  modelo: "No modelo sob demanda, cada consulta é cobrada pelos bytes que lê. O SELECT * lê todas as colunas da tabela inteira, cerca de 3 TB, toda vez que o painel é aberto. Filtrar os 7 dias depois, no painel, não ajuda: a leitura já aconteceu. Com dezenas de aberturas por dia, a conta cresce rápido. Eu faria três mudanças. Primeiro, particionaria a tabela pela data do evento e colocaria o filtro dos 7 dias na própria consulta, para o BigQuery ler só essas partições. Segundo, trocaria o SELECT * pelas poucas colunas que o painel usa, e clusterizaria a tabela pelas colunas mais filtradas. Terceiro, criaria uma tabela agregada, atualizada uma vez por dia por uma consulta agendada, com os números que o painel mostra: o painel passaria a ler alguns megabytes em vez de terabytes. Também configuraria um limite de bytes faturados por consulta, para um erro futuro não passar despercebido."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Consultas que cabem no orçamento"
  descricao: "Você vai calcular quanto uma consulta custaria no BigQuery, comparando SELECT * com consultas que leem só as colunas e partições necessárias, e escrever consultas no estilo BigQuery com UNNEST, QUALIFY, contagem condicional, conversão segura e agregação por semana, rodando no DuckDB, sem precisar de conta na nuvem."
  pasta: "desafios/manipulacao/bigquery"
  testes: 10
  tempo: "2 h"
  ferramentas: "VS Code, Python 3.11 ou superior, pandas, DuckDB e pytest"
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
      descricao: "Abra o terminal do VS Code com Ctrl+` (acento grave). Depois use Ctrl+Shift+P, Python: Select Interpreter, e escolha o .venv. Se o ambiente já existia, rode de novo o pip install: este desafio usa o DuckDB."
      comandos:
        - "# Linux ou macOS"
        - "python3 -m venv .venv"
        - "source .venv/bin/activate"
        - "# Windows (PowerShell)"
        - "python -m venv .venv"
        - '.venv\Scripts\Activate.ps1'
        - "pip install -r desafios/requirements.txt"
    - titulo: "Leia o enunciado e conheça os dados"
      descricao: "Abra desafios/manipulacao/bigquery/README.md. Ele descreve os três arquivos de dados e traz a tabela com as diferenças de sintaxe entre o BigQuery e o DuckDB."
    - titulo: "Implemente as funções e escreva as consultas em solucao.py"
      descricao: "Na parte 1, implemente as funções de custo. Na parte 2, escreva cada consulta dentro das aspas triplas. Não altere a pasta tests."
      codigo: true
      comandos:
        - "def bytes_faturados(tamanhos, colunas, particoes=None):"
        - "def custo_dolares(bytes_, preco_por_tib=6.25):"
        - "def comparar_consultas(caminho_csv, preco_por_tib=6.25):"
        - "CONSULTA_1 = \"\"\" SELECT ... UNNEST(itens) ... \"\"\""
        - "..."
        - "CONSULTA_6 = \"\"\" ... \"\"\""
    - titulo: "Teste cada parte"
      descricao: "Veja o resultado de uma consulta com o primeiro comando e rode os testes com o segundo."
      comandos:
        - "cd desafios/manipulacao/bigquery"
        - "python -c \"import solucao; print(solucao.executar(solucao.CONSULTA_1))\""
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/bigquery"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de BigQuery"'
        - "git push -u origin desafio/bigquery"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Projeto", en: "project" }
  - { pt: "Conjunto de dados", en: "dataset" }
  - { pt: "Armazenamento colunar", en: "columnar storage" }
  - { pt: "Bytes processados", en: "bytes processed, bytes billed" }
  - { pt: "Preço sob demanda", en: "on-demand pricing" }
  - { pt: "Capacidade (slots)", en: "capacity pricing, slots" }
  - { pt: "Partição", en: "partition" }
  - { pt: "Poda de partições", en: "partition pruning" }
  - { pt: "Clusterização", en: "clustering" }
  - { pt: "Registro aninhado", en: "STRUCT, record" }
  - { pt: "Campo repetido", en: "ARRAY, repeated field" }
  - { pt: "Execução de teste", en: "dry run" }
  - { pt: "Visão materializada", en: "materialized view" }
---

## O que é o BigQuery e como ele guarda os dados

O **BigQuery** é o data warehouse do Google Cloud: um banco de dados feito para análise, que consulta bilhões de linhas em segundos. Ele é *serverless*: não há servidor para configurar nem capacidade para dimensionar. Você carrega os dados e escreve SQL. É muito usado por empresas que já estão no Google Cloud e por quem analisa dados do Google Analytics 4, que exporta os eventos direto para o BigQuery.

Os dados ficam organizados em três níveis, que aparecem no nome completo de cada tabela:

```sql
-- projeto.conjunto_de_dados.tabela
SELECT id_pedido, data_pedido
FROM `minha-empresa.vendas.pedidos`
WHERE data_pedido = '2026-03-01';
```

- O **projeto** é a unidade de cobrança e de permissões.
- O **conjunto de dados** (*dataset*) agrupa tabelas e define a região onde os dados ficam.
- A **tabela** guarda os dados.

A linguagem é o **GoogleSQL**, um SQL padrão com algumas extensões. Tudo o que você viu em SQL básico e avançado funciona: JOIN, GROUP BY, CTE, funções de janela.

A diferença mais importante está por baixo: o BigQuery usa **armazenamento colunar**. Num banco tradicional, cada linha fica guardada inteira. No BigQuery, cada **coluna** fica guardada separadamente. Para uma consulta que soma o valor dos pedidos, basta ler a coluna de valor, sem tocar nas outras. É isso que torna as consultas analíticas rápidas, e é isso que define o custo.

Para praticar de graça, o BigQuery tem um modo *sandbox*, que não pede cartão de crédito, com limites de armazenamento e de consulta, e um catálogo de conjuntos de dados públicos em `bigquery-public-data`, com dados de exemplo do Google Analytics, de censos e de muitos outros assuntos.

## Como a cobrança funciona

No modelo **sob demanda**, o padrão, a cobrança é pelo **volume de dados lidos** por cada consulta, e não pelo tempo nem pelo tamanho do resultado. Pela documentação do Google:

- o primeiro 1 TiB processado por mês é gratuito;
- a cobrança é arredondada para cima, por MB;
- cada consulta é cobrada por no mínimo 10 MB, e cada tabela referenciada também.

Acima da franquia, paga-se um valor por TiB lido. Na região multirregional dos EUA, era de US$ 6,25 por TiB quando este texto foi escrito. Confira sempre a página de preços, porque o valor muda com o tempo e com a região. O armazenamento é cobrado à parte, e costuma ser bem mais barato que as consultas. Empresas grandes costumam trocar o sob demanda pelo **modelo de capacidade**, em que se paga por uma quantidade de processamento reservada (os *slots*), e não por bytes lidos.

O que isso significa na prática:

| Na consulta                          | O que é lido                                        |
| ------------------------------------ | --------------------------------------------------- |
| `SELECT *`                           | Todas as colunas                                    |
| `SELECT a, b`                        | Só as colunas a e b                                 |
| `... LIMIT 10`                       | **O mesmo que sem LIMIT**: ele só corta o resultado |
| `WHERE` numa coluna comum            | Todas as linhas das colunas usadas                  |
| `WHERE` na coluna de partição        | Só as partições que passam no filtro                |

Hábitos que evitam sustos:

- **Olhe a estimativa antes de rodar.** O editor do console mostra quantos bytes a consulta vai processar, calculados por uma execução de teste (*dry run*), que não cobra nada.
- **Nunca use `SELECT *` para explorar.** Use a aba de visualização da tabela, que mostra algumas linhas sem custo.
- **Configure um limite de bytes faturados** por consulta. Se a consulta passar do limite, ela falha em vez de cobrar.
- **Para painéis, crie tabelas agregadas.** Um painel que lê uma tabela bruta a cada abertura multiplica o custo pelo número de acessos.

## Particionamento e clusterização

Uma tabela **particionada** é dividida em partes, em geral por data: uma partição por dia, por exemplo. Quando a consulta filtra a coluna de partição, o BigQuery lê só as partições necessárias, o que se chama **poda de partições**. Numa tabela com três anos de eventos, analisar uma semana passa a ler 7 partições em vez de mais de mil.

```sql
CREATE TABLE `minha-empresa.app.eventos`
PARTITION BY data_evento
CLUSTER BY id_usuario, evento
AS
SELECT *, DATE(momento) AS data_evento
FROM `minha-empresa.app.eventos_brutos`;
```

Para a poda funcionar, o filtro precisa ser feito **diretamente na coluna de partição**, com valores conhecidos: `WHERE data_evento BETWEEN '2026-03-01' AND '2026-03-07'`. Transformar a coluna, como em `WHERE CAST(data_evento AS STRING) LIKE '2026-03%'`, pode fazer o BigQuery ler tudo. Uma tabela pode ser criada com a opção que **exige** filtro de partição em toda consulta, o que protege contra acidentes.

A **clusterização** ordena os dados, dentro de cada partição, por até quatro colunas. Filtros e agrupamentos por essas colunas passam a ler menos blocos. Particione pela data, que quase toda consulta filtra, e clusterize pelas colunas mais usadas em filtros, como cliente ou tipo de evento.

## Dados aninhados: STRUCT, ARRAY e UNNEST

Em bancos tradicionais, um pedido e seus itens ficam em duas tabelas, ligadas por JOIN. No BigQuery, é comum guardar os itens **dentro** do pedido, numa coluna do tipo array de registros:

```
id_pedido:   P00001
data_pedido: 2026-03-01
itens:
  - {sku: SKU-401, categoria: Beleza, quantidade: 3, preco: 49.9}
  - {sku: SKU-302, categoria: Eletrônicos, quantidade: 2, preco: 249.0}
```

- Um **STRUCT** é um registro com campos nomeados, acessados com ponto: `item.categoria`.
- Um **ARRAY** é uma lista de valores do mesmo tipo. `ARRAY_LENGTH(itens)` dá o tamanho.

Isso evita JOINs caros em tabelas enormes. A exportação do Google Analytics 4 usa esse formato: cada evento tem um array `event_params` com os parâmetros.

Para analisar os itens, o **UNNEST** abre o array em linhas:

```sql
SELECT item.categoria,
       SUM(item.quantidade * item.preco) AS faturamento
FROM `minha-empresa.vendas.pedidos`,
     UNNEST(itens) AS item
WHERE data_pedido BETWEEN '2026-03-01' AND '2026-03-31'
GROUP BY item.categoria;
```

A vírgula antes do `UNNEST` é um JOIN de cada pedido com os seus próprios itens. Depois dela, cada pedido aparece uma vez por item, a mesma multiplicação de linhas vista em SQL avançado. Para contar pedidos, use `COUNT(DISTINCT id_pedido)`. Para manter pedidos com array vazio, use `LEFT JOIN UNNEST(itens) AS item`.

## Funções úteis: QUALIFY, SAFE_CAST, COUNTIF e datas

**QUALIFY** filtra pelo resultado de uma função de janela, sem subconsulta. O uso mais comum é remover duplicatas, frequentes em dados que chegam por ingestão contínua:

```sql
SELECT *
FROM `minha-empresa.app.eventos`
WHERE data_evento >= '2026-03-01'
QUALIFY ROW_NUMBER() OVER (PARTITION BY id_evento
                           ORDER BY ingerido_em DESC) = 1;
```

**SAFE_CAST** converte tipos e devolve NULL, em vez de erro, quando a conversão falha. Outras funções têm a versão `SAFE.`, como `SAFE.PARSE_DATE` e `SAFE_DIVIDE`, que devolve NULL na divisão por zero:

```sql
SELECT SAFE_CAST(cupom AS INT64)                      AS desconto,
       SAFE_DIVIDE(compraram, visualizaram) * 100     AS conversao
FROM ...
```

**COUNTIF** e **IF** fazem contagens condicionais, ótimas para funis:

```sql
SELECT versao_app,
       COUNT(DISTINCT IF(evento = 'visualizou_produto',
                         id_usuario, NULL)) AS visualizaram,
       COUNT(DISTINCT IF(evento = 'comprou',
                         id_usuario, NULL)) AS compraram,
       COUNTIF(evento = 'comprou')          AS compras
FROM `minha-empresa.app.eventos`
WHERE data_evento BETWEEN '2026-03-01' AND '2026-03-31'
GROUP BY versao_app;
```

**Datas.** As funções mais usadas são `DATE_TRUNC(data, MONTH)` para agrupar por mês, `DATE_DIFF(fim, inicio, DAY)` para a diferença em dias, `DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY)` para janelas móveis e `FORMAT_DATE('%Y-%m', data)` para texto. Atenção: em `DATE_TRUNC(data, WEEK)`, a semana começa no **domingo**. Para começar na segunda-feira, use `WEEK(MONDAY)` ou `ISOWEEK`.
