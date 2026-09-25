# Desafio: perguntas ao banco da loja

Uma loja online guarda os dados num banco relacional. O time comercial mandou dez perguntas, e você
vai responder cada uma com uma consulta SQL. O banco é SQLite, que vem junto com o Python: não
precisa instalar nada.

## O banco

O arquivo `data/loja.sql` cria o banco com quatro tabelas. Neste desafio, você usa três delas:

**clientes**

| Coluna        | Tipo    | Observação                           |
| ------------- | ------- | ------------------------------------ |
| id_cliente    | INTEGER | Chave primária                       |
| nome          | TEXT    |                                      |
| cidade        | TEXT    |                                      |
| estado        | TEXT    | Sigla, como 'SP'                     |
| data_cadastro | TEXT    | Data no formato 'AAAA-MM-DD'         |
| email         | TEXT    | Pode ser NULL                        |

**produtos**

| Coluna     | Tipo    | Observação                           |
| ---------- | ------- | ------------------------------------ |
| id_produto | INTEGER | Chave primária                       |
| nome       | TEXT    |                                      |
| categoria  | TEXT    | Como 'Informática' ou 'Livros'       |
| preco      | REAL    | Preço de tabela atual                |
| ativo      | INTEGER | 1 = à venda, 0 = fora de linha       |

**pedidos**

| Coluna      | Tipo    | Observação                                   |
| ----------- | ------- | -------------------------------------------- |
| id_pedido   | INTEGER | Chave primária                               |
| id_cliente  | INTEGER | Liga ao cliente                              |
| data_pedido | TEXT    | Data no formato 'AAAA-MM-DD'                 |
| status      | TEXT    | 'entregue', 'cancelado' ou 'em trânsito'     |
| canal       | TEXT    | 'site', 'app' ou 'telefone'                  |
| frete       | REAL    |                                              |

A quarta tabela, `itens_pedido`, liga pedidos a produtos. Ela fica para o desafio de SQL avançado.

## O que você vai praticar

- `SELECT`, `FROM`, `WHERE` com `AND`, `OR`, `IN`, `LIKE` e `BETWEEN`.
- `ORDER BY`, `LIMIT` e `DISTINCT`.
- `IS NULL` para encontrar valores vazios.
- Funções de agregação (`COUNT`, `SUM`, `AVG`, `ROUND`) com `GROUP BY` e `HAVING`.
- `CASE WHEN` para criar categorias.

## O que fazer

Abra o `solucao.py`. Cada pergunta tem uma variável `CONSULTA_1` a `CONSULTA_10`: escreva a consulta
dentro das aspas triplas, no lugar do comentário. A pergunta diz quais colunas devolver, com quais
nomes e em que ordem.

## Regras

1. Uma consulta por pergunta, com um único comando `SELECT`.
2. Use exatamente os nomes de coluna pedidos, com `AS` quando a pergunta der um nome novo.
3. Respeite a ordenação pedida: o teste compara as linhas na ordem.
4. Não altere a pasta `tests` nem o arquivo `data/loja.sql`.

## Como conferir

Para ver o resultado de uma consulta enquanto escreve, dentro desta pasta:

```
python -c "import solucao; print(solucao.executar(solucao.CONSULTA_1))"
```

Para rodar os testes:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

Se preferir uma interface gráfica, o [DB Browser for SQLite](https://sqlitebrowser.org/) abre o banco:
use a opção de importar um banco a partir de arquivo SQL (no menu em inglês, File > Import > Database
from SQL file) e escolha `data/loja.sql`.

## Se travar

1. Rode só um teste: `pytest -v -k consulta_4`.
2. Compare a sua saída com a esperada: o pytest mostra as duas listas de linhas.
3. Monte a consulta aos poucos: primeiro o `SELECT ... FROM`, depois o `WHERE`, depois o `GROUP BY`,
   rodando a cada passo.
4. Só então consulte o gabarito em `desafios/_gabaritos/manipulacao/sql_basico/`.

## Depois de passar

Escreva mais três consultas por conta própria, sem teste: qual foi o dia com mais pedidos, qual canal
tem o maior frete médio e quantos clientes se cadastraram em cada ano. Para o último, procure a
função `strftime` do SQLite.
