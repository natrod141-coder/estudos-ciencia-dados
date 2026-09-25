"""Gabarito do desafio "O botão novo vende mais?".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import math
from statistics import NormalDist

import pandas as pd

NORMAL = NormalDist()


def taxa_conversao(conversoes, visitantes):
    if visitantes <= 0:
        raise ValueError("É preciso ter pelo menos um visitante.")
    if not 0 <= conversoes <= visitantes:
        raise ValueError("As conversões precisam estar entre 0 e o número de visitantes.")
    return conversoes / visitantes


def teste_duas_proporcoes(conv_a, n_a, conv_b, n_b):
    taxa_a, taxa_b = taxa_conversao(conv_a, n_a), taxa_conversao(conv_b, n_b)
    combinada = (conv_a + conv_b) / (n_a + n_b)  # sob H0, os dois grupos têm a mesma taxa
    erro_padrao = math.sqrt(combinada * (1 - combinada) * (1 / n_a + 1 / n_b))
    z = (taxa_b - taxa_a) / erro_padrao
    return {
        "taxa_a": taxa_a,
        "taxa_b": taxa_b,
        "diferenca": taxa_b - taxa_a,
        "z": z,
        "p": 2 * (1 - NORMAL.cdf(abs(z))),
    }


def intervalo_diferenca(conv_a, n_a, conv_b, n_b, confianca=0.95):
    taxa_a, taxa_b = taxa_conversao(conv_a, n_a), taxa_conversao(conv_b, n_b)
    # para o intervalo não se supõe H0: cada grupo usa a própria taxa
    erro_padrao = math.sqrt(taxa_a * (1 - taxa_a) / n_a + taxa_b * (1 - taxa_b) / n_b)
    z = NORMAL.inv_cdf(1 - (1 - confianca) / 2)
    diferenca = taxa_b - taxa_a
    return (diferenca - z * erro_padrao, diferenca + z * erro_padrao)


def tamanho_amostra_por_grupo(taxa_base, efeito_minimo, alfa=0.05, poder=0.80):
    taxa_nova = taxa_base + efeito_minimo
    z_alfa = NORMAL.inv_cdf(1 - alfa / 2)
    z_poder = NORMAL.inv_cdf(poder)
    variancias = taxa_base * (1 - taxa_base) + taxa_nova * (1 - taxa_nova)
    return math.ceil((z_alfa + z_poder) ** 2 * variancias / efeito_minimo**2)


def divisao_balanceada(n_a, n_b, limite=0.001):
    total = n_a + n_b
    z = (n_a / total - 0.5) / math.sqrt(0.25 / total)
    p = 2 * (1 - NORMAL.cdf(abs(z)))
    return p >= limite


def decidir(conv_a, n_a, conv_b, n_b, alfa=0.05):
    if not divisao_balanceada(n_a, n_b):
        return "divisao_desbalanceada"
    teste = teste_duas_proporcoes(conv_a, n_a, conv_b, n_b)
    if teste["p"] > alfa:
        return "inconclusivo"
    return "vence_b" if teste["diferenca"] > 0 else "vence_a"


def _totais(experimento):
    soma = experimento.groupby("grupo")[["visitantes", "conversoes"]].sum()
    return (
        int(soma.loc["A", "conversoes"]),
        int(soma.loc["A", "visitantes"]),
        int(soma.loc["B", "conversoes"]),
        int(soma.loc["B", "visitantes"]),
    )


def analisar_experimento(caminho_csv, alfa=0.05):
    conv_a, n_a, conv_b, n_b = _totais(pd.read_csv(caminho_csv))
    teste = teste_duas_proporcoes(conv_a, n_a, conv_b, n_b)
    inferior, superior = intervalo_diferenca(conv_a, n_a, conv_b, n_b, 1 - alfa)
    return {
        "visitantes_a": n_a,
        "conversoes_a": conv_a,
        "visitantes_b": n_b,
        "conversoes_b": conv_b,
        "taxa_a": round(teste["taxa_a"], 4),
        "taxa_b": round(teste["taxa_b"], 4),
        "diferenca": round(teste["diferenca"], 4),
        "p": round(teste["p"], 4),
        "intervalo": (round(inferior, 4), round(superior, 4)),
        "decisao": decidir(conv_a, n_a, conv_b, n_b, alfa),
    }


def evolucao_do_p(caminho_csv):
    experimento = pd.read_csv(caminho_csv)
    datas = sorted(experimento["data"].unique())
    return [
        round(teste_duas_proporcoes(*_totais(experimento[experimento["data"] <= data]))["p"], 4)
        for data in datas
    ]
