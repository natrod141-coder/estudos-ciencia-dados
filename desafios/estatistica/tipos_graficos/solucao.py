"""Desafio: o gráfico certo para cada pergunta.

Implemente cada função abaixo. Leia a docstring de cada uma antes de começar.
As funções de gráfico não dizem qual gráfico fazer: dizem qual pergunta ele precisa
responder. Escolher o tipo de gráfico é parte do exercício.

Regras:
- Use pandas para preparar os dados e matplotlib para desenhar (o .plot do pandas também vale).
- Toda função de gráfico devolve a figura: comece com fig, ax = plt.subplots() e termine com return fig.
- Não chame plt.show() dentro das funções: os testes desenham sem abrir janela.
- Não altere a pasta tests.

Para conferir o seu trabalho, rode no terminal, dentro desta pasta:
    pytest -v

Para ver um gráfico enquanto trabalha, rode no terminal, dentro desta pasta:
    python -c "import solucao as s; s.grafico_categorias(s.ler_vendas('data/vendas.csv')).savefig('teste.png')"
e abra o arquivo teste.png.
"""

import matplotlib.pyplot as plt  # noqa: F401  (será usado nas funções de gráfico)
import pandas as pd


def ler_vendas(caminho_csv):
    """Já está pronta: lê o CSV de vendas e converte a coluna data para o tipo data."""
    return pd.read_csv(caminho_csv, parse_dates=["data"])


def vendas_por_categoria(vendas):
    """Devolve uma Series com o faturamento total (soma de valor) de cada categoria.

    O índice é o nome da categoria, e os valores vêm da maior para a menor,
    arredondados para 2 casas.
    Dica: vendas.groupby("categoria")["valor"].sum(), depois .sort_values(ascending=False).
    """
    raise NotImplementedError("Implemente a função vendas_por_categoria")


def vendas_por_mes(vendas):
    """Devolve uma Series com o faturamento total de cada mês, em ordem cronológica.

    O índice é o mês no formato "AAAA-MM" (ex.: "2026-01"), e os valores são
    arredondados para 2 casas.
    Dica: vendas["data"].dt.strftime("%Y-%m") dá o mês de cada pedido nesse formato.
    """
    raise NotImplementedError("Implemente a função vendas_por_mes")


def grafico_categorias(vendas):
    """Responde: quais categorias mais faturaram no semestre?

    Escolha o tipo de gráfico. Ele precisa:
    - mostrar o faturamento de cada categoria (use vendas_por_categoria);
    - ordenar da categoria que mais faturou para a que menos faturou, na ordem de leitura;
    - ter o eixo dos valores começando no zero;
    - ter título e rótulos nos dois eixos.
    Devolve a figura.
    """
    raise NotImplementedError("Implemente a função grafico_categorias")


def grafico_evolucao(vendas):
    """Responde: como o faturamento evoluiu mês a mês?

    Escolha o tipo de gráfico. Ele precisa mostrar o total de cada mês (use vendas_por_mes),
    em ordem cronológica, e ter título e rótulos nos dois eixos. Devolve a figura.
    """
    raise NotImplementedError("Implemente a função grafico_evolucao")


def grafico_distribuicao(vendas):
    """Responde: como se distribuem os valores dos pedidos? A maioria é de pedidos baratos ou caros?

    Escolha o tipo de gráfico. Ele precisa usar o valor de todos os pedidos, ter pelo menos
    5 faixas de valor, e ter título e rótulos nos dois eixos. Devolve a figura.
    """
    raise NotImplementedError("Implemente a função grafico_distribuicao")


def grafico_relacao(vendas):
    """Responde: pedidos com mais itens têm valor maior?

    Escolha o tipo de gráfico. Ele precisa mostrar um ponto por pedido, com os itens
    de um lado e o valor do outro, e ter título e rótulos nos dois eixos. Devolve a figura.
    """
    raise NotImplementedError("Implemente a função grafico_relacao")
