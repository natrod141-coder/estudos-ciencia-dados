"""Gabarito do desafio "Três bibliotecas, três gráficos".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import seaborn as sns

COR = "#0f4c4a"


def ler_vendas(caminho_csv):
    return pd.read_csv(caminho_csv, parse_dates=["data"])


def _com_mes(vendas):
    return vendas.assign(mes=vendas["data"].dt.strftime("%Y-%m"))


def faturamento_mensal_por_uf(vendas):
    tabela = _com_mes(vendas).pivot_table(index="mes", columns="uf", values="valor", aggfunc="sum", fill_value=0)
    return tabela.round(2)


def pequenos_multiplos(vendas):
    mensal = faturamento_mensal_por_uf(vendas)
    fig, eixos = plt.subplots(2, 2, figsize=(11, 6), sharex=True, sharey=True)
    for ax, uf in zip(eixos.flat, mensal.columns):
        ax.plot(mensal.index, mensal[uf].values, color=COR)
        ax.set_title(uf)
        ax.tick_params(axis="x", labelrotation=90)
    fig.suptitle("Faturamento mensal por UF (R$)")
    fig.tight_layout()
    return fig


def mapa_de_calor(vendas):
    tabela = _com_mes(vendas).pivot_table(index="categoria", columns="mes", values="valor", aggfunc="sum", fill_value=0)
    tabela = tabela.loc[tabela.sum(axis=1).sort_values(ascending=False).index] / 1000
    fig, ax = plt.subplots(figsize=(12, 3.5))
    sns.heatmap(tabela, ax=ax, cmap="Greens", linewidths=0.5, cbar_kws={"label": "Faturamento (R$ mil)"})
    ax.set_title("Faturamento por categoria e mês")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Categoria")
    return fig


def grafico_interativo(vendas):
    resumo = vendas.groupby(["uf", "categoria"], as_index=False)["valor"].sum()
    ordem = resumo.groupby("uf")["valor"].sum().sort_values(ascending=False).index.tolist()
    return px.bar(
        resumo,
        x="uf",
        y="valor",
        color="categoria",
        barmode="stack",
        category_orders={"uf": ordem},
        title="Faturamento por UF e categoria, jan/2025 a jun/2026",
        labels={"uf": "UF", "valor": "Faturamento (R$)", "categoria": "Categoria"},
    )


def salvar_html(fig, caminho):
    fig.write_html(caminho, include_plotlyjs="cdn")
