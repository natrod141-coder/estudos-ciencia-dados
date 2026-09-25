"""Gabarito do desafio "Do gráfico exploratório ao explicativo".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import matplotlib.pyplot as plt
import pandas as pd

COR_DESTAQUE = "#0f4c4a"
COR_CONTEXTO = "#b0b0b0"


def ler_vendas(caminho_csv):
    return pd.read_csv(caminho_csv)


def tabela_por_canal(vendas):
    return vendas.pivot_table(index="mes", columns="canal", values="faturamento", aggfunc="sum").sort_index()


def mensagem_principal(vendas):
    tabela = tabela_por_canal(vendas)
    primeiro, ultimo = tabela.iloc[0], tabela.iloc[-1]
    crescimento = (ultimo / primeiro - 1) * 100
    canal = crescimento.idxmax()
    return {
        "canal": canal,
        "crescimento_pct": int(round(crescimento[canal])),
        "participacao_final_pct": round(float(ultimo[canal] / ultimo.sum() * 100), 1),
        "virou_lider": bool(ultimo.idxmax() == canal),
    }


def _virgula(numero):
    return f"{numero}".replace(".", ",")


def titulo(mensagem):
    inicio = f"O {mensagem['canal']} cresceu {mensagem['crescimento_pct']}% em 2025"
    if mensagem["virou_lider"]:
        return f"{inicio} e virou o maior canal de vendas"
    return f"{inicio} e já responde por {_virgula(mensagem['participacao_final_pct'])}% das vendas"


def grafico_explicativo(vendas):
    tabela = tabela_por_canal(vendas) / 1000
    mensagem = mensagem_principal(vendas)
    fig, ax = plt.subplots(figsize=(9, 5))
    for canal in tabela.columns:
        destaque = canal == mensagem["canal"]
        cor = COR_DESTAQUE if destaque else COR_CONTEXTO
        ax.plot(tabela.index, tabela[canal], color=cor, linewidth=3 if destaque else 1.5)
        ultimo = tabela[canal].iloc[-1]
        # rótulo direto no fim da linha, no lugar da legenda
        ax.text(len(tabela) - 0.8, ultimo, f"{canal} ({ultimo:.0f} mil)", color=cor, va="center",
                fontweight="bold" if destaque else "normal")
    ax.set_title(titulo(mensagem), loc="left", fontsize=13)
    ax.set_ylabel("Faturamento mensal (R$ mil)")
    ax.spines[["top", "right"]].set_visible(False)
    ax.tick_params(axis="x", labelrotation=45)
    ax.set_xlim(-0.5, len(tabela) + 2.5)
    fig.tight_layout()
    return fig


def resumo_executivo(vendas):
    total_milhoes = vendas["faturamento"].sum() / 1_000_000
    mensagem = mensagem_principal(vendas)
    return {
        "contexto": f"Em 2025, as vendas somaram R$ {_virgula(round(total_milhoes, 1))} milhões nos três canais.",
        "achado": f"{titulo(mensagem)}.",
        "recomendacao": "Priorizar o app no orçamento de 2026 e investigar por que a loja física ficou estável.",
    }
