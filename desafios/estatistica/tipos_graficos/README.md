# Desafio: o gráfico certo para cada pergunta

A gerente de uma loja online pediu um relatório do primeiro semestre de 2026 com quatro perguntas:
quais categorias mais faturaram, como o faturamento evoluiu mês a mês, como se distribuem os valores
dos pedidos e se pedidos com mais itens têm valor maior. Os dados de 300 pedidos estão em
`data/vendas.csv`. Para cada pergunta, você vai escolher o tipo de gráfico que responde melhor e
desenhá-lo seguindo boas práticas.

## O que você vai praticar

- Escolher o tipo de gráfico a partir da pergunta, e não do gosto.
- Preparar os dados para cada gráfico com `groupby` do pandas.
- Desenhar barras, linhas, histogramas e dispersão com matplotlib.
- Aplicar as regras que evitam gráficos enganosos: barras em ordem, eixo começando no zero, título e
  rótulos.

## O que fazer

Abra o `solucao.py` e implemente as seis funções. A `ler_vendas` já está pronta. Sugestão de ordem:
`vendas_por_categoria`, `vendas_por_mes`, `grafico_categorias`, `grafico_evolucao`,
`grafico_distribuicao` e `grafico_relacao`.

As funções de gráfico não dizem qual gráfico fazer. Cada docstring traz a pergunta que o gráfico
precisa responder. Se escolher um tipo que não serve, o teste avisa qual era o esperado.

## Regras

1. Use pandas para preparar os dados e matplotlib para desenhar. O `.plot` do pandas também vale.
2. Toda função de gráfico devolve a figura (`return fig`) e não chama `plt.show()`.
3. Não altere a pasta `tests`.

## Como conferir

No terminal, dentro desta pasta:

```
pytest -v
```

O desafio está aprovado quando os 8 testes passam.

Para ver um gráfico enquanto trabalha, salve a figura num arquivo e abra a imagem:

```
python -c "import solucao as s; s.grafico_categorias(s.ler_vendas('data/vendas.csv')).savefig('teste.png')"
```

## Se travar

1. Rode só um teste: `pytest -v -k test_grafico_categorias`.
2. Leia as linhas que começam com `E`: elas dizem o que o teste esperava do gráfico.
3. Se as barras horizontais aparecerem na ordem invertida, lembre que o `barh` desenha de baixo para
   cima. Ordene os dados ao contrário ou use `ax.invert_yaxis()`.
4. Só então consulte o gabarito em `desafios/_gabaritos/estatistica/tipos_graficos/`.

## Depois de passar

Salve os quatro gráficos como imagem e olhe para eles como a gerente olharia. Cada um responde a sua
pergunta em poucos segundos? Depois, experimente trocar o gráfico de categorias por um gráfico de
pizza (`ax.pie`) e compare: em qual dos dois é mais fácil dizer se Casa faturou mais que Moda?
