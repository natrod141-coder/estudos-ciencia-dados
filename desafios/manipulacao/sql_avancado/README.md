# Desafio: análises com várias tabelas

O banco da loja é o mesmo do desafio de SQL básico, agora com as quatro tabelas. As perguntas desta
vez exigem juntar tabelas, fazer consultas dentro de consultas e calcular rankings e acumulados, que
é o dia a dia de quem analisa dados de negócio.

## O banco

```
clientes (id_cliente, nome, cidade, estado, data_cadastro, email)
    │ 1
    │
    │ N
pedidos (id_pedido, id_cliente, data_pedido, status, canal, frete)
    │ 1
    │
    │ N
itens_pedido (id_pedido, id_produto, quantidade, preco_unitario)
    │ N
    │
    │ 1
produtos (id_produto, nome, categoria, preco, ativo)
```

- Um cliente tem vários pedidos, e um pedido tem vários itens. Cada item é um produto.
- `produtos.preco` é o preço de tabela **atual**. `itens_pedido.preco_unitario` é o preço **cobrado
  na venda**, que às vezes teve desconto. Para faturamento, use sempre o preço cobrado.
- `status` pode ser 'entregue', 'cancelado' ou 'em trânsito'. Os detalhes de cada coluna estão no
  README do desafio de SQL básico.

**Faturamento**, em todas as perguntas, é a soma de `quantidade * preco_unitario`, considerando só os
pedidos com status 'entregue'.

## O que você vai praticar

- `JOIN` com duas e três tabelas, e `LEFT JOIN` para encontrar o que não tem par.
- A diferença entre `COUNT(*)` e `COUNT(coluna)` depois de um `LEFT JOIN`.
- Subconsultas no `WHERE` e `NOT EXISTS`.
- CTEs (`WITH`) para quebrar um problema em etapas.
- Funções de janela: `ROW_NUMBER`, `SUM() OVER` e `LAG`.

## O que fazer

Abra o `solucao.py`. Cada pergunta tem uma variável `CONSULTA_1` a `CONSULTA_10`: escreva a consulta
dentro das aspas triplas, no lugar do comentário. A pergunta diz quais colunas devolver, com quais
nomes e em que ordem.

## Regras

1. Uma consulta por pergunta. Pode usar `WITH` antes do `SELECT`.
2. Use exatamente os nomes de coluna pedidos e respeite a ordenação pedida.
3. Não altere a pasta `tests` nem o arquivo `data/loja.sql`.

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

## Se travar

1. Rode só um teste: `pytest -v -k consulta_7`.
2. Monte a consulta por partes. Numa CTE, rode primeiro só o que está dentro do `WITH` e confira o
   resultado antes de escrever o `SELECT` final.
3. Confira a quantidade de linhas depois de cada `JOIN`: se aumentou sem motivo, alguma chave se
   repete.
4. Só então consulte o gabarito em `desafios/_gabaritos/manipulacao/sql_avancado/`.

## Depois de passar

Na pergunta 4, troque `COUNT(p.id_pedido)` por `COUNT(*)` e veja o que acontece com o Bruno Freitas.
Na pergunta 8, troque `ROW_NUMBER` por `RANK`: em que situação as duas dariam resultados diferentes?
Por fim, olhe a pergunta 10: março caiu 29,5%. Use o banco para descobrir se a queda veio de menos
pedidos ou de pedidos menores.
