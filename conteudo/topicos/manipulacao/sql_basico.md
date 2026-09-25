---
titulo: "SQL básico"
modulo: manipulacao
ordem: 3
horas: 8
estado: publicado
resumo: "SELECT, WHERE, ORDER BY, GROUP BY e funções de agregação."

# Checklist de aulas. O texto de leitura está abaixo, depois deste cabeçalho.
# Para uma aula em vídeo, cole o endereço em "link".
aulas:
  - id: a1
    titulo: "Bancos relacionais, tabelas e chaves"
    tipo: leitura
    minutos: 10
  - id: a2
    titulo: "SELECT, FROM e WHERE"
    tipo: leitura
    minutos: 20
  - id: a3
    titulo: "Ordenar, limitar e remover repetidos"
    tipo: leitura
    minutos: 10
  - id: a4
    titulo: "NULL: o valor desconhecido"
    tipo: leitura
    minutos: 10
  - id: a5
    titulo: "Agregar: COUNT, SUM, AVG, GROUP BY e HAVING"
    tipo: leitura
    minutos: 20
  - id: a6
    titulo: "CASE WHEN e a ordem de execução de uma consulta"
    tipo: leitura
    minutos: 12
  - id: a7
    titulo: "Vídeo de apoio: SQL do zero"
    tipo: video
    minutos: 30
    link: ""
  - id: a8
    titulo: "Vídeo de apoio: GROUP BY e HAVING"
    tipo: video
    minutos: 15
    link: ""

# Questões fechadas. "correta" é a posição da resposta certa, começando em 0.
quiz:
  - pergunta: "Qual consulta devolve os clientes do estado de SP?"
    opcoes: ["SELECT * FROM clientes WHERE estado = 'SP';", "SELECT clientes WHERE estado = SP;", "SELECT * FROM clientes HAVING estado = 'SP';", "SELECT estado = 'SP' FROM clientes;"]
    correta: 0
    explicacao: "A estrutura é SELECT colunas FROM tabela WHERE condição. Texto vai entre aspas simples: sem elas, SP seria lido como o nome de uma coluna. O HAVING filtra grupos, e não linhas."
  - pergunta: "Qual condição encontra os clientes sem e-mail cadastrado (email vazio, NULL)?"
    opcoes: ["WHERE email = NULL", "WHERE email = ''", "WHERE email IS NULL", "WHERE NOT email"]
    correta: 2
    explicacao: "NULL significa 'valor desconhecido', e qualquer comparação com ele, inclusive = NULL, dá desconhecido, e não verdadeiro. Por isso existe o IS NULL. O texto vazio '' é um valor diferente de NULL."
  - pergunta: "Qual é a diferença entre WHERE e HAVING?"
    opcoes: ["Nenhuma, são sinônimos", "WHERE filtra as linhas antes do agrupamento, e HAVING filtra os grupos depois das agregações", "HAVING só funciona com texto", "WHERE só pode ser usado sem GROUP BY"]
    correta: 1
    explicacao: "O WHERE decide quais linhas entram no cálculo. O HAVING decide quais grupos aparecem no resultado, e por isso pode usar agregações, como HAVING COUNT(*) >= 5. Uma condição sobre a linha, como status = 'entregue', vai no WHERE."
  - pergunta: "Numa tabela de 100 clientes, 20 não têm e-mail (NULL). O que devolvem COUNT(*) e COUNT(email)?"
    opcoes: ["100 e 100", "80 e 100", "100 e 80", "80 e 80"]
    correta: 2
    explicacao: "COUNT(*) conta linhas, então dá 100. COUNT(coluna) conta só os valores que não são NULL, então dá 80. As outras agregações, como SUM e AVG, também ignoram os NULL."
  - pergunta: "O que a condição WHERE estado = 'SP' OR estado = 'RJ' AND frete > 50 seleciona?"
    opcoes: ["Pedidos de SP ou RJ com frete acima de 50", "Nada, porque a sintaxe está errada", "Só pedidos com frete acima de 50", "Todos os pedidos de SP e só os pedidos do RJ com frete acima de 50"]
    correta: 3
    explicacao: "O AND é avaliado antes do OR, como a multiplicação antes da soma. A condição é lida como estado = 'SP' OR (estado = 'RJ' AND frete > 50). Para o sentido esperado, use parênteses: (estado = 'SP' OR estado = 'RJ') AND frete > 50, ou estado IN ('SP', 'RJ') AND frete > 50."
  - pergunta: "Qual padrão encontra os nomes que terminam com 'Silva'?"
    opcoes: ["LIKE 'Silva%'", "LIKE '%Silva'", "LIKE '_Silva'", "= '*Silva'"]
    correta: 1
    explicacao: "No LIKE, o % representa qualquer sequência de caracteres, inclusive nenhuma, e o _ representa exatamente um caractere. '%Silva' é 'qualquer coisa seguida de Silva'. 'Silva%' seria 'começa com Silva'."
  - pergunta: "Qual consulta traz os 3 pedidos de maior frete?"
    opcoes: ["SELECT * FROM pedidos LIMIT 3 ORDER BY frete DESC;", "SELECT MAX(frete, 3) FROM pedidos;", "SELECT * FROM pedidos ORDER BY frete DESC LIMIT 3;", "SELECT TOP frete FROM pedidos;"]
    correta: 2
    explicacao: "O LIMIT vem por último, depois do ORDER BY: primeiro o banco ordena do maior para o menor frete, depois pega as 3 primeiras linhas. Sem o ORDER BY, o LIMIT pega 3 linhas quaisquer. No SQL Server, o equivalente é SELECT TOP 3."
  - pergunta: "Por que SELECT estado, nome, COUNT(*) FROM clientes GROUP BY estado é um problema na maioria dos bancos?"
    opcoes: ["Porque COUNT(*) não funciona junto com GROUP BY", "Porque nome não está no GROUP BY nem dentro de uma agregação: cada estado tem vários nomes, e não há como escolher um", "Porque falta um ORDER BY", "Porque estado precisa vir depois do COUNT"]
    correta: 1
    explicacao: "Com GROUP BY estado, o resultado tem uma linha por estado. Cada coluna do SELECT precisa ter um valor só por grupo: ou está no GROUP BY, ou está dentro de uma agregação. A maioria dos bancos dá erro. O SQLite aceita e escolhe um nome qualquer, o que é pior, porque o erro passa despercebido."
  - pergunta: "Por que a consulta SELECT preco * 0.9 AS preco_final FROM produtos WHERE preco_final < 100 dá erro na maioria dos bancos?"
    opcoes: ["Porque o WHERE é executado antes do SELECT, e o apelido preco_final ainda não existe nesse momento", "Porque não se pode fazer contas dentro do SELECT", "Porque apelidos só podem ter uma palavra", "Porque o WHERE só aceita números inteiros"]
    correta: 0
    explicacao: "A ordem de escrita não é a ordem de execução: o banco resolve FROM, WHERE, GROUP BY e HAVING antes do SELECT. No WHERE, repita a expressão (WHERE preco * 0.9 < 100). No ORDER BY, que vem depois do SELECT, o apelido pode ser usado. O SQLite é uma exceção e aceita o apelido no WHERE, mas não conte com isso em outros bancos."
  - pergunta: "O que SELECT DISTINCT estado, cidade FROM clientes devolve?"
    opcoes: ["Cada estado uma vez só", "Cada cidade uma vez só", "Um erro, porque DISTINCT aceita uma coluna só", "Cada combinação diferente de estado e cidade uma vez só"]
    correta: 3
    explicacao: "O DISTINCT vale para a linha inteira do resultado: remove as linhas em que todas as colunas se repetem. Com estado e cidade, aparece cada par diferente, e um estado com três cidades aparece três vezes."

# Questão aberta, com rubrica de autocorreção e resposta modelo.
aberta:
  pergunta: "Explique com suas palavras a diferença entre WHERE e HAVING e dê um exemplo de pergunta de negócio que precisa dos dois na mesma consulta, com o esboço da consulta."
  rubrica:
    - "Explica que o WHERE filtra linhas antes do agrupamento, e o HAVING filtra os grupos depois que as agregações são calculadas."
    - "Diz que condições sobre agregações (COUNT, SUM, AVG) só podem ir no HAVING, e que condições sobre colunas das linhas devem ir no WHERE."
    - "Dá um exemplo coerente com os dois, como 'canais com mais de 20 pedidos entregues', com WHERE status = 'entregue', GROUP BY canal e HAVING COUNT(*) > 20."
  modelo: "O WHERE age sobre as linhas, antes do agrupamento: ele decide quais linhas entram no cálculo. O HAVING age sobre os grupos, depois que COUNT, SUM e as outras agregações foram calculadas: ele decide quais grupos aparecem no resultado. Por isso uma condição como COUNT(*) > 20 só pode ir no HAVING, porque antes do agrupamento a contagem ainda não existe. Já uma condição sobre a própria linha, como o status do pedido, deve ir no WHERE. Exemplo: 'quais canais tiveram mais de 20 pedidos entregues?'. A consulta seria SELECT canal, COUNT(*) AS pedidos FROM pedidos WHERE status = 'entregue' GROUP BY canal HAVING COUNT(*) > 20. O WHERE tira os cancelados e os em trânsito antes da contagem, e o HAVING mostra só os canais que passaram de 20."

# Desafio prático. Os arquivos do exercício ficam na pasta indicada em "pasta".
desafio:
  titulo: "Perguntas ao banco da loja"
  descricao: "O time comercial de uma loja online mandou dez perguntas sobre clientes, produtos e pedidos. Você vai responder cada uma com uma consulta SQL num banco SQLite, usando filtros, ordenação, NULL, agregações, GROUP BY, HAVING e CASE WHEN."
  pasta: "desafios/manipulacao/sql_basico"
  testes: 10
  tempo: "2 h"
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
      descricao: "Abra desafios/manipulacao/sql_basico/README.md: ele descreve as tabelas e colunas. O banco é criado pelo arquivo data/loja.sql, que você pode abrir para ver os dados."
    - titulo: "Escreva as consultas em solucao.py"
      descricao: "Cada pergunta tem uma variável. Escreva a consulta dentro das aspas triplas, com as colunas, os nomes e a ordem pedidos. Não altere a pasta tests."
      codigo: true
      comandos:
        - "CONSULTA_1 = \"\"\" SELECT ... \"\"\""
        - "CONSULTA_2 = \"\"\" SELECT ... \"\"\""
        - "..."
        - "CONSULTA_10 = \"\"\" SELECT ... \"\"\""
    - titulo: "Teste cada consulta"
      descricao: "Veja o resultado de uma consulta com o primeiro comando e rode os testes com o segundo."
      comandos:
        - "cd desafios/manipulacao/sql_basico"
        - "python -c \"import solucao; print(solucao.executar(solucao.CONSULTA_1))\""
        - "pytest -v"
    - titulo: "Envie a solução"
      descricao: "Crie um branch, faça o commit e abra um Pull Request. O histórico fica no GitHub e serve de portfólio."
      comandos:
        - "git checkout -b desafio/sql_basico"
        - "git add solucao.py"
        - 'git commit -m "Resolve o desafio de SQL básico"'
        - "git push -u origin desafio/sql_basico"

# Termos em português e em inglês, como aparecem em documentação e provas.
glossario:
  - { pt: "Banco de dados relacional", en: "relational database" }
  - { pt: "Sistema gerenciador de banco de dados (SGBD)", en: "database management system (DBMS)" }
  - { pt: "Linha (registro)", en: "row (record)" }
  - { pt: "Coluna (campo)", en: "column (field)" }
  - { pt: "Chave primária", en: "primary key" }
  - { pt: "Chave estrangeira", en: "foreign key" }
  - { pt: "Consulta", en: "query" }
  - { pt: "Apelido", en: "alias" }
  - { pt: "Nulo", en: "NULL" }
  - { pt: "Função de agregação", en: "aggregate function" }
  - { pt: "Agrupamento", en: "grouping" }
  - { pt: "Expressão condicional", en: "CASE expression" }
---

## Bancos relacionais, tabelas e chaves

Um **banco de dados relacional** guarda os dados em tabelas, e as tabelas se ligam umas às outras por colunas em comum. É onde estão os dados de quase toda empresa: vendas, clientes, estoque, cadastro. SQL é a linguagem para consultar esses dados, e é a ferramenta mais pedida em vagas de análise de dados.

Cada tabela tem colunas com tipos definidos, como texto, inteiro, decimal ou data, e cada linha é um registro. O banco da loja usado nos desafios tem quatro tabelas:

| Tabela         | Uma linha é          | Chave primária             | Liga com                        |
| -------------- | -------------------- | -------------------------- | ------------------------------- |
| `clientes`     | um cliente           | `id_cliente`               |                                 |
| `produtos`     | um produto           | `id_produto`               |                                 |
| `pedidos`      | um pedido            | `id_pedido`                | `clientes`, por `id_cliente`    |
| `itens_pedido` | um produto num pedido | `id_pedido` + `id_produto` | `pedidos` e `produtos`          |

A **chave primária** identifica cada linha de forma única. A **chave estrangeira** é uma coluna que aponta para a chave primária de outra tabela: `pedidos.id_cliente` diz de quem é o pedido. Por que separar em tabelas, em vez de repetir nome e cidade do cliente em cada pedido? Porque o dado fica num lugar só. Se o cliente muda de cidade, basta alterar uma linha, e não há risco de dois pedidos dizerem cidades diferentes para a mesma pessoa.

O SQL é **declarativo**: você diz o que quer, e o banco decide como buscar. Existem vários bancos (SQLite, PostgreSQL, MySQL, SQL Server, BigQuery), e todos falam o mesmo SQL básico. As diferenças aparecem em detalhes, como funções de data e o jeito de limitar linhas. Os desafios usam o SQLite, que já vem com o Python.

## SELECT, FROM e WHERE

Toda consulta começa com `SELECT` (quais colunas) e `FROM` (de qual tabela):

```sql
SELECT nome, categoria, preco
FROM produtos;
```

`SELECT *` traz todas as colunas. É útil para dar uma olhada, mas em consultas de verdade liste as colunas: fica claro o que é usado, e em bancos grandes, como o BigQuery, o custo depende das colunas lidas.

Dá para calcular colunas novas e dar nomes a elas com `AS`:

```sql
SELECT nome, preco, preco * 0.9 AS preco_com_desconto
FROM produtos;
```

O `WHERE` filtra as linhas:

```sql
SELECT nome, preco
FROM produtos
WHERE categoria = 'Informática'
  AND preco <= 500;
```

| Operador                     | Exemplo                                        |
| ---------------------------- | ---------------------------------------------- |
| `=`, `<>`, `<`, `>`, `<=`, `>=` | `preco >= 100`, `status <> 'cancelado'`     |
| `AND`, `OR`, `NOT`           | `estado = 'SP' AND frete > 0`                  |
| `IN`                         | `estado IN ('SP', 'RJ', 'MG')`                 |
| `BETWEEN` (inclui as pontas) | `data_pedido BETWEEN '2026-03-01' AND '2026-03-31'` |
| `LIKE`                       | `nome LIKE 'A%'` (começa com A), `nome LIKE '%Silva'` (termina com Silva) |

Três cuidados:

- **Texto vai entre aspas simples.** `'SP'` é um valor. `SP`, sem aspas, seria o nome de uma coluna.
- **O AND vem antes do OR**, como a multiplicação antes da soma. `a OR b AND c` é lido como `a OR (b AND c)`. Na dúvida, use parênteses.
- **Datas guardadas como texto 'AAAA-MM-DD'** podem ser comparadas como texto, porque a ordem alfabética coincide com a cronológica. Com 'DD/MM/AAAA', isso não funciona.

## Ordenar, limitar e remover repetidos

```sql
-- do mais caro ao mais barato; no empate, por nome;
-- e só as 5 primeiras linhas
SELECT nome, categoria, preco
FROM produtos
ORDER BY preco DESC, nome
LIMIT 5;
```

Sem `ORDER BY`, a ordem das linhas não é garantida: pode mudar de uma execução para outra. Sempre que a ordem importa, peça-a explicitamente. O `LIMIT` vem por último. No SQL Server, o equivalente é `SELECT TOP 5 ...`.

O `DISTINCT` remove linhas repetidas do resultado. Ele vale para a combinação de todas as colunas: `SELECT DISTINCT estado FROM clientes` dá cada estado uma vez, mas `SELECT DISTINCT estado, cidade` dá cada par diferente.

## NULL: o valor desconhecido

`NULL` representa um valor ausente ou desconhecido, como o e-mail de quem não informou. Ele não é zero nem texto vazio, e se comporta de um jeito próprio:

- **Qualquer comparação com NULL dá desconhecido**, e não verdadeiro. `email = NULL` nunca encontra nada. Use `email IS NULL` e `email IS NOT NULL`.
- **Contas com NULL dão NULL.** `preco + NULL` é `NULL`.
- **As agregações ignoram NULL.** `COUNT(*)` conta todas as linhas, mas `COUNT(email)` conta só as que têm e-mail. `AVG` calcula a média só dos valores presentes.
- **Para substituir NULL** por um valor padrão, use `COALESCE(email, 'sem e-mail')`, que devolve o primeiro argumento que não for NULL.

## Agregar: COUNT, SUM, AVG, GROUP BY e HAVING

As **funções de agregação** resumem várias linhas num valor: `COUNT`, `SUM`, `AVG`, `MIN` e `MAX`. Sozinhas, resumem a tabela inteira:

```sql
SELECT COUNT(*)             AS total_pedidos,
       ROUND(AVG(frete), 2) AS frete_medio
FROM pedidos;
```

Com `GROUP BY`, o resumo é feito para cada grupo:

```sql
SELECT status, COUNT(*) AS pedidos
FROM pedidos
GROUP BY status
ORDER BY pedidos DESC;
```

A regra de ouro do `GROUP BY`: **cada coluna do SELECT está no GROUP BY ou dentro de uma agregação**. Se o resultado tem uma linha por status, uma coluna como `canal` não tem um valor único por linha. A maioria dos bancos recusa a consulta. O SQLite aceita e escolhe um valor qualquer, o que é pior, porque o erro passa despercebido.

Para filtrar **grupos**, use `HAVING`, que vem depois do `GROUP BY` e pode usar agregações:

```sql
SELECT estado, COUNT(*) AS clientes
FROM clientes
GROUP BY estado
HAVING COUNT(*) >= 5
ORDER BY clientes DESC;
```

O `WHERE` filtra linhas **antes** de agrupar, e o `HAVING` filtra grupos **depois**. Uma mesma consulta pode ter os dois: `WHERE status = 'entregue'` escolhe os pedidos que entram na conta, e `HAVING COUNT(*) > 20` escolhe os grupos que aparecem.

Também existe `COUNT(DISTINCT coluna)`, que conta valores diferentes: `COUNT(DISTINCT id_cliente)` numa tabela de pedidos dá quantos clientes compraram.

## CASE WHEN e a ordem de execução de uma consulta

O `CASE` cria valores a partir de condições, como o SE do Excel:

```sql
SELECT nome,
       CASE
           WHEN preco < 100  THEN 'econômico'
           WHEN preco < 1000 THEN 'intermediário'
           ELSE 'premium'
       END AS faixa
FROM produtos;
```

As condições são testadas em ordem, e vale a primeira verdadeira. Dentro de uma agregação, o `CASE` permite contar ou somar só parte das linhas:

```sql
SELECT canal,
       COUNT(*) AS pedidos,
       SUM(CASE WHEN status = 'cancelado' THEN 1 ELSE 0 END) AS cancelados
FROM pedidos
GROUP BY canal;
```

Por fim, a peça que explica boa parte dos erros de SQL: **a ordem em que a consulta é escrita não é a ordem em que ela é executada**.

| Ordem de escrita | Ordem de execução |
| ---------------- | ----------------- |
| SELECT           | 1. FROM           |
| FROM             | 2. WHERE          |
| WHERE            | 3. GROUP BY       |
| GROUP BY         | 4. HAVING         |
| HAVING           | 5. SELECT         |
| ORDER BY         | 6. ORDER BY       |
| LIMIT            | 7. LIMIT          |

Consequências práticas:

- Um apelido criado no `SELECT` **não pode** ser usado no `WHERE`, que roda antes. Repita a expressão. O SQLite aceita o apelido no `WHERE` como exceção, mas PostgreSQL, SQL Server e BigQuery recusam: não crie o hábito.
- O apelido **pode** ser usado no `ORDER BY`, que roda depois.
- Agregações não podem ir no `WHERE`, porque os grupos ainda não existem. Vão no `HAVING`.

Alguns bancos, como SQLite, PostgreSQL, MySQL e BigQuery, aceitam o apelido também no `GROUP BY`, como uma conveniência. O SQL Server não aceita.
