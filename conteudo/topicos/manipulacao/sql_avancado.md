---
titulo: "SQL avançado"
modulo: manipulacao
ordem: 4
horas: 8
estado: publicado
resumo: "JOINs, subconsultas, CTEs e funções de janela."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "JOIN: juntar tabelas pela chave"
    tipo: leitura
    minutos: 20
  - id: a2
    titulo: "LEFT JOIN e o que não tem par"
    tipo: leitura
    minutos: 15
  - id: a3
    titulo: "Subconsultas e EXISTS"
    tipo: leitura
    minutos: 15
  - id: a4
    titulo: "CTEs: consultas em etapas"
    tipo: leitura
    minutos: 12
  - id: a5
    titulo: "Funções de janela"
    tipo: leitura
    minutos: 25
  - id: a6
    titulo: "Armadilhas e desempenho"
    tipo: leitura
    minutos: 10
  - id: a7
    titulo: "Vídeo de apoio: JOINs explicados"
    tipo: video
    minutos: 20
    link: ""
  - id: a8
    titulo: "Vídeo de apoio: funções de janela na prática"
    tipo: video
    minutos: 20
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "O que um INNER JOIN entre clientes e pedidos, pela coluna id_cliente, devolve?"
    opcoes: ["Todos os clientes, com ou sem pedido", "Só as combinações de cliente e pedido que casam pela chave: clientes sem pedido ficam de fora", "Todos os clientes e todos os pedidos, combinados de todas as formas", "Só os clientes com mais de um pedido"]
    correta: 1
    explicacao: "O INNER JOIN mantém só as linhas que têm par nas duas tabelas. Um cliente com três pedidos aparece em três linhas, e um cliente sem pedido não aparece. Para manter todos os clientes, use LEFT JOIN."
  - pergunta: "Numa consulta com clientes LEFT JOIN pedidos, você acrescenta WHERE p.status = 'entregue'. O que acontece com os clientes sem pedido?"
    opcoes: ["Somem: nas linhas deles, status é NULL, o WHERE as descarta, e o LEFT JOIN vira, na prática, um INNER JOIN", "Continuam no resultado, com status NULL", "Aparecem com status 'entregue'", "A consulta dá erro"]
    correta: 0
    explicacao: "O WHERE roda depois do JOIN e descarta as linhas em que a condição não é verdadeira, inclusive as com NULL. Para filtrar os pedidos sem perder os clientes, coloque a condição no ON: LEFT JOIN pedidos p ON p.id_cliente = c.id_cliente AND p.status = 'entregue'."
  - pergunta: "Depois de um LEFT JOIN de clientes com pedidos, por que usar COUNT(p.id_pedido), e não COUNT(*), para contar os pedidos de cada cliente?"
    opcoes: ["Porque COUNT(*) é mais lento", "Porque COUNT(*) não funciona com GROUP BY", "Porque o cliente sem pedido gera uma linha com as colunas de pedidos em NULL: COUNT(*) conta essa linha como 1, e COUNT(p.id_pedido) conta 0", "Não há diferença nesse caso"]
    correta: 2
    explicacao: "O LEFT JOIN cria uma linha para o cliente sem pedido, com as colunas da direita em NULL. O COUNT(*) conta linhas, então dá 1. O COUNT(coluna) ignora NULL, então dá 0, que é a resposta certa."
  - pergunta: "Você junta pedidos, que têm a coluna frete, com itens_pedido e soma o frete. O total sai bem maior que o frete real. Por quê?"
    opcoes: ["Porque o SUM arredonda os valores", "Porque o JOIN remove os pedidos sem itens", "Porque o frete está guardado em outra moeda", "Porque, depois do JOIN, cada pedido aparece uma vez por item, e o frete é somado repetido"]
    correta: 3
    explicacao: "Um pedido com três itens vira três linhas no JOIN, e o frete dele aparece três vezes. É a multiplicação de linhas (fan-out). Some o frete a partir da tabela pedidos, antes de juntar com os itens, ou em CTEs separadas."
  - pergunta: "Por que WHERE id NOT IN (SELECT id_cliente FROM pedidos) pode devolver zero linhas quando a subconsulta tem algum NULL?"
    opcoes: ["Porque x NOT IN (1, 2, NULL) nunca é verdadeiro: a comparação com NULL é desconhecida, e o NOT EXISTS não tem esse problema", "Porque NOT IN não aceita subconsultas", "Porque a subconsulta precisa de DISTINCT", "Porque NOT IN só funciona com texto"]
    correta: 0
    explicacao: "NOT IN equivale a 'diferente de cada valor da lista'. Comparar com NULL dá desconhecido, e desconhecido nunca é verdadeiro, então nenhuma linha passa. O NOT EXISTS verifica se existe alguma linha que satisfaça a condição e lida bem com NULL."
  - pergunta: "Qual é a principal vantagem de usar CTEs (WITH) numa consulta longa?"
    opcoes: ["Deixam a consulta sempre mais rápida", "Criam tabelas permanentes no banco", "Dão nome a etapas intermediárias, e a consulta passa a ser lida de cima para baixo, em partes que podem ser testadas uma a uma", "Substituem o GROUP BY"]
    correta: 2
    explicacao: "Uma CTE é uma consulta com nome, que só existe durante a execução da consulta principal. Ela troca subconsultas aninhadas, lidas de dentro para fora, por uma sequência de etapas nomeadas. Em geral não muda o desempenho: o ganho é de legibilidade."
  - pergunta: "Qual é a diferença entre SUM(valor) com GROUP BY cliente e SUM(valor) OVER (PARTITION BY cliente)?"
    opcoes: ["Nenhuma, as duas devolvem o mesmo resultado", "O GROUP BY junta as linhas em uma por cliente; a função de janela mantém todas as linhas e acrescenta, em cada uma, o total do cliente", "A função de janela só funciona com datas", "O GROUP BY é mais recente e substitui o OVER"]
    correta: 1
    explicacao: "Funções de janela calculam sobre um grupo de linhas sem colapsar o resultado. Isso permite, por exemplo, mostrar cada pedido ao lado do total do cliente e calcular a participação: valor / SUM(valor) OVER (PARTITION BY cliente)."
  - pergunta: "Três produtos venderam 50, 50 e 40 unidades. Ordenando do maior para o menor, que posições a função RANK() dá?"
    opcoes: ["1, 2, 3", "1, 1, 2", "1, 2, 2", "1, 1, 3"]
    correta: 3
    explicacao: "O RANK dá a mesma posição aos empatados e pula as posições seguintes: 1, 1, 3. O DENSE_RANK não pula: 1, 1, 2. O ROW_NUMBER nunca repete: 1, 2, 3, e desempata de forma arbitrária se o ORDER BY não definir um critério."
  - pergunta: "Numa tabela com uma linha por mês, o que LAG(faturamento) OVER (ORDER BY mes) devolve na linha de março?"
    opcoes: ["O faturamento de abril", "O faturamento de fevereiro", "A soma de janeiro a março", "A diferença entre março e fevereiro"]
    correta: 1
    explicacao: "O LAG devolve o valor da linha anterior, na ordem definida pelo OVER. O LEAD devolve o da linha seguinte. Com o LAG, a variação mensal fica (faturamento - LAG(faturamento)) / LAG(faturamento)."
  - pergunta: "Por que WHERE ROW_NUMBER() OVER (PARTITION BY categoria ORDER BY quantidade DESC) = 1 dá erro?"
    opcoes: ["Porque ROW_NUMBER precisa de um apelido", "Porque PARTITION BY não aceita texto", "Porque só se pode usar uma função de janela por consulta", "Porque as funções de janela são calculadas depois do WHERE, junto com o SELECT; é preciso calcular numa CTE e filtrar na consulta de fora"]
    correta: 3
    explicacao: "Na ordem de execução, o WHERE vem antes das funções de janela. A solução é calcular a posição numa CTE ou subconsulta e filtrar fora. Alguns bancos, como BigQuery, Snowflake e DuckDB, têm a cláusula QUALIFY, que filtra pelo resultado de uma função de janela diretamente."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Um relatório calcula, por cliente, o frete total e o valor dos produtos com esta estrutura: clientes JOIN pedidos JOIN itens_pedido, com SUM(p.frete) e SUM(i.quantidade * i.preco_unitario) na mesma consulta. O frete total do relatório não bate com o do financeiro. Explique a causa e como corrigir."
  rubrica:
    - "Identifica a multiplicação de linhas: depois do JOIN com itens_pedido, cada pedido aparece uma vez por item, e o frete, que é do pedido, é somado várias vezes."
    - "Explica que a soma dos itens está certa nesse nível, e que o problema é somar na mesma linha medidas de níveis diferentes (pedido e item)."
    - "Propõe calcular cada medida no seu nível antes de juntar, por exemplo com duas CTEs agregadas por cliente, uma a partir de pedidos e outra a partir dos itens, e sugere conferir contagens ou totais contra a tabela de origem."
  modelo: "O frete é uma informação do pedido, mas o JOIN com itens_pedido cria uma linha por item. Um pedido com quatro itens aparece quatro vezes, e o SUM(frete) conta o frete dele quatro vezes. O valor dos produtos está certo, porque ele é do nível do item, e cada item aparece uma vez só. O erro está em somar, na mesma tabela juntada, medidas de níveis diferentes. A correção é agregar cada medida no seu próprio nível antes de juntar: uma CTE soma o frete por cliente a partir da tabela pedidos, outra soma o valor dos itens por cliente juntando pedidos e itens, e a consulta final junta as duas pelo id do cliente. Para conferir, eu compararia o frete total do relatório com SELECT SUM(frete) FROM pedidos: os dois precisam bater."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Análises com várias tabelas"
  descricao: "Com o banco completo da loja, com clientes, pedidos, itens e produtos, você vai responder dez perguntas que exigem JOIN, LEFT JOIN, subconsultas, NOT EXISTS, CTEs e funções de janela: rankings por categoria, faturamento acumulado e variação mensal."
  pasta: "desafios/manipulacao/sql_avancado"
  testes: 10
  tempo: "2 h 30 min"
  ferramentas: "VS Code, Python 3.11 ou superior (o SQLite já vem junto), pandas e pytest"
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
    - titulo: "Leia o enunciado e conheça o banco"
      descricao: "Abra desafios/manipulacao/sql_avancado/README.md: ele mostra como as quatro tabelas se ligam e define o faturamento usado nas perguntas."
    - titulo: "Escreva as consultas em solucao.py"
      descricao: "Cada pergunta tem uma variável. Escreva a consulta dentro das aspas triplas, com as colunas, os nomes e a ordem pedidos. Não altere a pasta tests."
      codigo: true
      comandos:
        - "CONSULTA_1 = \"\"\" SELECT ... JOIN ... \"\"\""
        - "..."
        - "CONSULTA_7 = \"\"\" WITH ... SELECT ... \"\"\""
        - "..."
        - "CONSULTA_10 = \"\"\" ... LAG(...) OVER (...) ... \"\"\""
    - titulo: "Teste cada consulta"
      descricao: "Veja o resultado de uma consulta com o primeiro comando e rode os testes com o segundo."
      comandos:
        - "cd desafios/manipulacao/sql_avancado"
        - "python -c \"import solucao; print(solucao.executar(solucao.CONSULTA_1))\""
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/sql_avancado"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de SQL avançado"'
        - "git push -u origin desafio/sql_avancado"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Junção interna", en: "inner join" }
  - { pt: "Junção à esquerda", en: "left (outer) join" }
  - { pt: "Junção completa", en: "full outer join" }
  - { pt: "Chave de junção", en: "join key" }
  - { pt: "Subconsulta", en: "subquery" }
  - { pt: "Subconsulta correlacionada", en: "correlated subquery" }
  - { pt: "Expressão de tabela comum", en: "common table expression (CTE)" }
  - { pt: "Função de janela", en: "window function" }
  - { pt: "Partição", en: "partition" }
  - { pt: "Total acumulado", en: "running total" }
  - { pt: "Multiplicação de linhas", en: "fan-out, row explosion" }
  - { pt: "Índice", en: "index" }
---

## JOIN: juntar tabelas pela chave

Num banco relacional, a informação fica espalhada: o pedido sabe o `id_cliente`, mas o nome do cliente está na tabela `clientes`. O `JOIN` junta as tabelas pela coluna em comum:

```sql
SELECT p.id_pedido, p.data_pedido, c.nome, c.estado
FROM pedidos AS p
JOIN clientes AS c ON c.id_cliente = p.id_cliente;
```

- `AS p` e `AS c` são **apelidos de tabela**. Com eles, `p.id_pedido` deixa claro de qual tabela vem cada coluna. Quando as duas tabelas têm uma coluna com o mesmo nome, como `nome` em `clientes` e em `produtos`, o apelido é obrigatório.
- O `ON` diz como casar as linhas: aqui, cada pedido com o cliente de mesmo `id_cliente`.
- `JOIN` sozinho é o mesmo que `INNER JOIN`: só entram as linhas que têm par nas duas tabelas.

Para chegar ao faturamento por categoria, é preciso atravessar três tabelas: o item diz a quantidade e o preço cobrado, o pedido diz o status, e o produto diz a categoria.

```sql
SELECT pr.categoria,
       SUM(i.quantidade * i.preco_unitario) AS faturamento
FROM itens_pedido AS i
JOIN pedidos  AS p  ON p.id_pedido  = i.id_pedido
JOIN produtos AS pr ON pr.id_produto = i.id_produto
WHERE p.status = 'entregue'
GROUP BY pr.categoria
ORDER BY faturamento DESC;
```

Antes de escrever um JOIN, pergunte **qual é o nível de cada tabela**, ou seja, o que uma linha representa: um cliente, um pedido, um item. Ao juntar uma tabela de nível mais alto (pedidos) com uma de nível mais baixo (itens), o resultado fica no nível mais baixo: uma linha por item.

## LEFT JOIN e o que não tem par

| Tipo              | Mantém                                                       |
| ----------------- | ------------------------------------------------------------ |
| `INNER JOIN`      | Só as linhas com par nas duas tabelas                        |
| `LEFT JOIN`       | Todas as linhas da esquerda; sem par, as colunas da direita ficam NULL |
| `RIGHT JOIN`      | Todas as linhas da direita (é um LEFT JOIN com as tabelas trocadas) |
| `FULL OUTER JOIN` | Todas as linhas das duas                                     |
| `CROSS JOIN`      | Todas as combinações possíveis, sem condição                 |

O `LEFT JOIN` serve para perguntas que precisam incluir quem não tem par. Clientes que nunca compraram:

```sql
SELECT c.nome
FROM clientes AS c
LEFT JOIN pedidos AS p ON p.id_cliente = c.id_cliente
WHERE p.id_pedido IS NULL;
```

Três armadilhas do `LEFT JOIN`:

- **Contagem.** Um cliente sem pedido gera uma linha com as colunas de `pedidos` em NULL. `COUNT(*)` conta essa linha e dá 1. Use `COUNT(p.id_pedido)`, que ignora NULL e dá 0.
- **Filtro no WHERE.** Uma condição sobre a tabela da direita no `WHERE`, como `p.status = 'entregue'`, descarta as linhas NULL e transforma o LEFT JOIN num INNER JOIN. Para filtrar a tabela da direita e manter todos da esquerda, coloque a condição no `ON`: `LEFT JOIN pedidos p ON p.id_cliente = c.id_cliente AND p.status = 'entregue'`.
- **Soma de NULL.** A soma de um cliente sem pedido dá NULL, e não 0. Use `COALESCE(SUM(...), 0)`.

## Subconsultas e EXISTS

Uma **subconsulta** é uma consulta dentro de outra. A forma mais simples devolve um único valor:

```sql
SELECT nome, preco
FROM produtos
WHERE preco > (SELECT AVG(preco) FROM produtos);
```

Uma subconsulta também pode devolver uma lista, usada com `IN`, ou uma tabela inteira, usada no `FROM` como se fosse uma tabela.

Para perguntas do tipo "existe algum...?", o `EXISTS` é o mais claro. Produtos que nunca foram vendidos:

```sql
SELECT pr.nome
FROM produtos AS pr
WHERE NOT EXISTS (
    SELECT 1
    FROM itens_pedido AS i
    WHERE i.id_produto = pr.id_produto
);
```

Essa é uma **subconsulta correlacionada**: ela usa uma coluna da consulta de fora (`pr.id_produto`) e é avaliada para cada produto. O `SELECT 1` é uma convenção, porque o `EXISTS` só verifica se alguma linha existe.

Prefira `NOT EXISTS` a `NOT IN` com subconsulta. Se a subconsulta devolver algum NULL, `x NOT IN (...)` nunca é verdadeiro, e a consulta devolve zero linhas sem nenhum aviso.

## CTEs: consultas em etapas

Uma **CTE** (*common table expression*) dá nome a uma consulta intermediária, com `WITH`. Consultas longas deixam de ser lidas de dentro para fora e passam a ser lidas de cima para baixo, em etapas:

```sql
WITH valor_por_pedido AS (
    SELECT p.id_pedido, p.id_cliente,
           SUM(i.quantidade * i.preco_unitario) AS valor
    FROM pedidos AS p
    JOIN itens_pedido AS i ON i.id_pedido = p.id_pedido
    WHERE p.status = 'entregue'
    GROUP BY p.id_pedido, p.id_cliente
),
ticket_por_cliente AS (
    SELECT id_cliente, AVG(valor) AS ticket_medio
    FROM valor_por_pedido
    GROUP BY id_cliente
)
SELECT c.nome, ROUND(t.ticket_medio, 2) AS ticket_medio
FROM ticket_por_cliente AS t
JOIN clientes AS c ON c.id_cliente = t.id_cliente
ORDER BY t.ticket_medio DESC;
```

Cada CTE pode usar as anteriores. Uma vantagem prática: dá para testar cada etapa sozinha, rodando só o que está dentro dos parênteses. A CTE existe apenas durante a consulta e não cria nada no banco.

## Funções de janela

As **funções de janela** calculam sobre um grupo de linhas **sem juntar as linhas numa só**, como faria o `GROUP BY`. A sintaxe é `função() OVER (PARTITION BY ... ORDER BY ...)`:

- `PARTITION BY` define os grupos, como uma categoria ou um cliente. Sem ele, a janela é a tabela inteira.
- `ORDER BY` define a ordem dentro de cada grupo, necessária para rankings, acumulados e LAG.

**Rankings.** Qual é o produto mais vendido de cada categoria?

```sql
WITH vendas AS (
    SELECT pr.categoria, pr.nome, SUM(i.quantidade) AS quantidade
    FROM itens_pedido AS i
    JOIN produtos AS pr ON pr.id_produto = i.id_produto
    GROUP BY pr.categoria, pr.nome
),
ranking AS (
    SELECT categoria, nome, quantidade,
           ROW_NUMBER() OVER (PARTITION BY categoria
                              ORDER BY quantidade DESC) AS posicao
    FROM vendas
)
SELECT categoria, nome, quantidade
FROM ranking
WHERE posicao = 1;
```

| Função          | Com os valores 50, 50 e 40 | Uso                                     |
| --------------- | -------------------------- | --------------------------------------- |
| `ROW_NUMBER()`  | 1, 2, 3                    | Escolher exatamente uma linha por grupo |
| `RANK()`        | 1, 1, 3                    | Classificação com empates, como num campeonato |
| `DENSE_RANK()`  | 1, 1, 2                    | Classificação sem pular posições        |

Repare que o filtro `posicao = 1` fica numa consulta de fora. As funções de janela são calculadas depois do `WHERE`, junto com o `SELECT`, então não podem ser filtradas no mesmo nível. BigQuery, Snowflake e DuckDB têm a cláusula `QUALIFY`, que faz esse filtro direto.

**Acumulados e médias móveis.** Com `ORDER BY` dentro do `OVER`, o `SUM` vira um total acumulado:

```sql
SELECT mes, faturamento,
       SUM(faturamento) OVER (ORDER BY mes) AS acumulado,
       AVG(faturamento) OVER (
           ORDER BY mes
           ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
       ) AS media_3_meses
FROM faturamento_mensal;
```

O trecho `ROWS BETWEEN 2 PRECEDING AND CURRENT ROW` define a moldura da janela: a linha atual e as duas anteriores.

**Comparar com a linha anterior.** O `LAG` devolve o valor da linha anterior, e o `LEAD`, o da seguinte:

```sql
SELECT mes, faturamento,
       faturamento - LAG(faturamento) OVER (ORDER BY mes) AS diferenca
FROM faturamento_mensal;
```

**Participação no total.** Sem `ORDER BY`, a janela é o grupo inteiro: `valor / SUM(valor) OVER (PARTITION BY categoria)` dá a participação de cada produto na sua categoria, sem precisar de outra consulta.

## Armadilhas e desempenho

**Multiplicação de linhas.** É o erro mais comum e mais silencioso em SQL. Ao juntar `pedidos` com `itens_pedido`, cada pedido aparece uma vez por item. Somar o `frete`, que é do pedido, depois desse JOIN, conta o frete várias vezes. A regra: **agregue cada medida no nível dela antes de juntar**. Some o frete a partir de `pedidos` e o valor dos itens a partir de `itens_pedido`, em CTEs separadas, e só então junte os resultados.

**Confira os números.** Depois de cada JOIN, compare a quantidade de linhas com a esperada (`SELECT COUNT(*)`). Compare também um total conhecido, como a soma do frete, com a tabela de origem.

**Desempenho.** Em bancos grandes, alguns hábitos fazem diferença:

- Filtre cedo: condições no `WHERE` reduzem as linhas antes dos JOINs e agregações.
- Leia só as colunas necessárias, em vez de `SELECT *`.
- Colunas usadas em JOINs e filtros frequentes costumam ter **índices**, estruturas que permitem ao banco achar as linhas sem ler a tabela inteira. Quem cria índices é, em geral, quem administra o banco.
- O comando `EXPLAIN` (no SQLite, `EXPLAIN QUERY PLAN`) mostra como o banco pretende executar a consulta.
