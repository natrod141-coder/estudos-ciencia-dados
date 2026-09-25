# Desafio: consultas que cabem no orçamento

A empresa guarda os pedidos da loja e os eventos do app no BigQuery. No BigQuery sob demanda, cada
consulta é cobrada pelo volume de dados que lê, e uma consulta descuidada numa tabela grande pode
custar caro. Neste desafio, você vai calcular esse custo e escrever consultas no estilo BigQuery:
arrays aninhados com `UNNEST`, remoção de duplicatas com `QUALIFY`, funil com contagem condicional,
conversão segura de texto sujo e agregação por semana.

Para rodar tudo no seu computador, sem conta no Google Cloud, as consultas usam o **DuckDB**, um
banco analítico que roda dentro do Python e tem uma sintaxe muito próxima da do BigQuery.

## Os dados

- `data/pedidos.jsonl`: 404 pedidos de março de 2026. Cada pedido tem uma lista `itens`, com `sku`,
  `categoria`, `quantidade` e `preco`. É o formato aninhado típico do BigQuery: um pedido é uma linha,
  e os itens ficam dentro dela.
- `data/eventos.jsonl`: eventos do app (`visualizou_produto`, `adicionou_carrinho`, `comprou`), com
  usuário, versão do app, cupom e o momento em que o evento foi gravado (`ingerido_em`). Alguns
  eventos foram gravados duas vezes.
- `data/tamanhos_eventos.csv`: o tamanho, em bytes, de cada coluna em cada partição diária da tabela
  de eventos de produção, de janeiro a março. É o que o BigQuery usa para calcular a cobrança.

## Do BigQuery para o DuckDB

| No BigQuery                                  | No DuckDB                                        |
| -------------------------------------------- | ------------------------------------------------ |
| `FROM pedidos, UNNEST(itens) AS item`        | `FROM pedidos, UNNEST(itens) AS t(item)`         |
| `SAFE_CAST(cupom AS INT64)`                  | `TRY_CAST(cupom AS INTEGER)`                     |
| `DATE_TRUNC(data_pedido, ISOWEEK)`           | `CAST(date_trunc('week', data_pedido) AS DATE)`  |
| `FORMAT_DATE('%Y-%m', data)`                 | `strftime(data, '%Y-%m')`                        |
| `QUALIFY`, `IF`, `COUNTIF`, `ARRAY_LENGTH`   | Iguais                                           |

## O que fazer

Abra o `solucao.py`. Na parte 1, implemente as três funções de custo. Na parte 2, escreva as seis
consultas dentro das aspas triplas, no lugar do comentário.

## Regras

1. Na parte 1, use pandas e o módulo `math`.
2. Na parte 2, uma consulta por pergunta, com os nomes de coluna e a ordenação pedidos.
3. Não altere a pasta `tests` nem os arquivos em `data`.

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

1. Rode só um teste: `pytest -v -k consulta_3`.
2. Para entender o `UNNEST`, rode `SELECT id_pedido, item FROM pedidos, UNNEST(itens) AS t(item) LIMIT 10`
   e veja como cada pedido vira uma linha por item.
3. Para as funções de custo, faça a conta de um cenário pequeno no papel, como o do teste
   `test_bytes_faturados_arredonda_para_cima_e_cobra_no_minimo_10_mb`.
4. Só então consulte o gabarito em `desafios/_gabaritos/manipulacao/bigquery/`.

## Depois de passar

1. Olhe o resultado de `comparar_consultas`. Se a mesma análise rodasse todo dia, num painel, quanto
   custaria por mês em cada versão?
2. Na consulta 6, a primeira semana começa em 23 de fevereiro, embora todos os pedidos sejam de março.
   Por quê? E o que mudaria no BigQuery com `DATE_TRUNC(data_pedido, WEEK)`, cuja semana começa no
   domingo?
3. Na consulta 4, a versão 5.2 converte um pouco mais. Com o que você aprendeu em teste A/B, dá para
   dizer que a 5.2 é melhor?
