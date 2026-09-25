# Desafio: o contexto de filtro por dentro

No Power BI, a mesma medida `[Faturamento]` mostra o total da empresa num cartão, o total de cada
loja numa matriz e o total de cada mês num gráfico. Quem faz isso é o **contexto de filtro**: cada
célula de cada visual calcula a medida com um conjunto diferente de filtros, que descem das
dimensões para a tabela fato pelos relacionamentos. Entender esse mecanismo é a diferença entre
decorar fórmulas DAX e saber escrevê-las.

Neste desafio, você vai implementar esse mecanismo em Python, sobre o modelo estrela do desafio de
modelagem. Primeiro o filtro, depois as medidas: soma, iterador com RELATED, CALCULATE com ALL,
DIVIDE, acumulado no ano e comparação com o ano anterior. Por fim, uma matriz, para ver que o total
de um visual é recalculado, e não somado.

## O modelo

```
               dim_produto (id_produto, codigo_produto, produto, categoria, marca, custo_unitario)
                    │ 1
                    │ *
dim_data ─1───*─ fato_vendas ─*───1─ dim_loja (id_loja, codigo_loja, loja, cidade, uf)
(data, ano, mes, nome_mes, trimestre, ...)
                 (data, pedido, id_produto, id_loja, quantidade, preco_unitario, valor)
```

As vendas vão de janeiro de 2025 a junho de 2026, e o calendário cobre 2025 e 2026 inteiros.

## Como o contexto de filtro é escrito

Um dicionário, com as colunas escritas como no DAX:

```python
{"dim_loja[uf]": "PR", "dim_data[ano]": 2025}   # lojas do PR, em 2025
{"dim_loja[uf]": ["PR", "SP"]}                   # lojas do PR ou de SP
{}                                                # nenhum filtro: tudo
```

## O que fazer

Abra o `solucao.py` e implemente as dez funções, na ordem do arquivo. Acima de cada medida está a
fórmula DAX equivalente. As funções `carregar_modelo`, `separar_referencia` e `como_lista` já estão
prontas.

## Regras

1. Use pandas. Nenhuma função pode alterar o modelo nem o dicionário de filtros recebido.
2. Não altere a pasta `tests` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 11 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k filtrar`. Comece pelo `filtrar_fato`: todas as medidas dependem
   dele.
2. Teste no terminal Python, dentro desta pasta:

   ```python
   import solucao
   modelo = solucao.carregar_modelo("data")
   solucao.filtrar_fato(modelo, {"dim_loja[uf]": "PR"}).head()
   ```

3. Para o acumulado no ano e o ano anterior, primeiro imprima as datas que você está usando como
   filtro e confira se são as esperadas.
4. Só então consulte o gabarito em `desafios/_gabaritos/visualizacao/dax_basico/`.

## Depois de passar

Monte o mesmo modelo no Power BI Desktop, com as quatro tabelas de `data/`, e escreva as medidas em
DAX, copiando as fórmulas que estão acima de cada função. Faça uma matriz com a UF nas linhas e as
medidas nas colunas, filtrada no primeiro trimestre de 2026, e compare com o resultado da sua função
`matriz`. Os números precisam bater. Repare na linha de total do crescimento: 39,7%, embora as
linhas somem mais de 160%.
