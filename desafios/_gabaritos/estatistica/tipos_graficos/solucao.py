"""Gabarito do desafio "O gráfico certo para cada pergunta".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import matplotlib.pyplot as plt
import pandas as pd

COR = "#0f4c4a"


def ler_vendas(caminho_csv):
    return pd.read_csv(caminho_csv, parse_dates=["data"])


def vendas_por_categoria(vendas):
    return vendas.groupby("categoria")["valor"].sum().sort_values(ascending=False).round(2)


def vendas_por_mes(vendas):
    meses = vendas["data"].dt.strftime("%Y-%m")
    return vendas.groupby(meses)["valor"].sum().sort_index().round(2)


def grafico_categorias(vendas):
    # comparar categorias: barras. Horizontais, porque os nomes ficam legíveis.
    # O barh desenha de baixo para cima, então a ordem crescente põe a maior no topo.
    totais = vendas_por_categoria(vendas).sort_values()
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.barh(totais.index, totais.values, color=COR)
    ax.set_title("Faturamento por categoria, 1º semestre de 2026")
    ax.set_xlabel("Faturamento (R$)")
    ax.set_ylabel("Categoria")
    return fig


def grafico_evolucao(vendas):
    # evolução no tempo: linha
    mensal = vendas_por_mes(vendas)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(mensal.index, mensal.values, marker="o", color=COR)
    ax.set_title("Faturamento mensal, 1º semestre de 2026")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Faturamento (R$)")
    return fig


def grafico_distribuicao(vendas):
    # distribuição de uma variável quantitativa: histograma
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.hist(vendas["valor"], bins=20, color=COR, edgecolor="white")
    ax.set_title("Distribuição do valor dos pedidos")
    ax.set_xlabel("Valor do pedido (R$)")
    ax.set_ylabel("Número de pedidos")
    return fig


def grafico_relacao(vendas):
    # relação entre duas variáveis quantitativas: dispersão
    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.scatter(vendas["itens"], vendas["valor"], alpha=0.5, color=COR)
    ax.set_title("Itens por pedido e valor do pedido")
    ax.set_xlabel("Itens no pedido")
    ax.set_ylabel("Valor do pedido (R$)")
    return fig
