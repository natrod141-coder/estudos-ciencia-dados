# Desafio: uma camada semântica de bolso

Na reunião de resultados, três painéis mostraram três números diferentes para a "receita de março".
Um contava os pedidos cancelados, outro não; um terceiro calculava o ticket médio como a média dos
tickets de cada dia. Todos estavam "certos", cada um com a sua definição.

A solução é definir cada métrica **uma vez só**, num lugar que todos consultam: a camada semântica.
Neste desafio, as definições já estão escritas em `modelo_semantico.json`. Você vai escrever o
compilador que transforma um pedido como "receita e ticket médio por região, por mês, só no app" na
consulta SQL certa, do mesmo jeito que as ferramentas de camada semântica fazem.

## O modelo semântico

`modelo_semantico.json` tem quatro partes:

- `tabela` e `coluna_de_tempo`: de onde vêm os dados e qual coluna é a data do pedido.
- `dimensoes`: as colunas pelas quais as métricas podem ser abertas: região, canal e status.
- `medidas`: as agregações básicas, como a soma do valor e a contagem de pedidos.
- `metricas`: o que as pessoas pedem, construído a partir das medidas. Uma métrica **simples** é uma
  medida, às vezes com filtro, como a receita, que só conta pedidos aprovados. Uma métrica de
  **razão** divide uma métrica por outra, como o ticket médio.

Os dados estão em `data/pedidos.csv`: 127 pedidos de janeiro a março de 2026.

## O que fazer

Abra o `solucao.py` e implemente as funções, na ordem do arquivo. As funções `ler_modelo`,
`criar_banco` e `consultar` já estão prontas. Depois de escrever `compilar`, experimente no
terminal, digitando `python` dentro desta pasta:

```python
from solucao import *
modelo = ler_modelo("modelo_semantico.json")
print(compilar(modelo, ["receita", "ticket_medio"], por=["regiao"], grao="mes"))
consultar(criar_banco("data/pedidos.csv"), modelo, ["receita"], por=["canal"])
```

## Regras

1. As funções devolvem texto SQL. Os testes rodam esse SQL no DuckDB e conferem os números com
   contas feitas em pandas.
2. Não altere a pasta `tests`, o `modelo_semantico.json` nem os arquivos em `data`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 10 testes passam.

## Se travar

1. Rode só um teste: `pytest -v -k razao`.
2. Imprima o SQL que a sua função `compilar` gerou e rode à mão, para ver onde está o erro.
3. Para as métricas de razão, lembre do tópico de conferir código gerado por IA: média de razões
   não é razão de totais.
4. Só então consulte o gabarito em `desafios/_gabaritos/analytics_eng/camada_semantica/`.

## Depois de passar

- Compare a quantidade de clientes compradores de cada mês com a do trimestre inteiro. Por que a
  soma dos meses não dá o total do trimestre?
- Faça uma cópia do modelo e acrescente a métrica `receita_por_cliente`, a receita dividida pelos
  clientes compradores. Ela é aditiva? Dá para somar a de cada região?
- Imagine um assistente de IA que responde perguntas do time comercial. Em vez de escrever SQL
  livre, ele escolhe métricas, dimensões e filtros, e chama `compilar`. Que erros do tópico de
  limites e alucinação essa escolha evita? Quais continuam possíveis?
