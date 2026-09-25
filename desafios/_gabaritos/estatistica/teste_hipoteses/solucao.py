"""Gabarito do desafio "O pacote tem mesmo 500 gramas?".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import math
from statistics import NormalDist, mean, stdev

import pandas as pd

NORMAL = NormalDist()  # normal padrão: média 0, desvio padrão 1


def valor_p(z, alternativa="bilateral"):
    if alternativa == "bilateral":
        return 2 * (1 - NORMAL.cdf(abs(z)))
    if alternativa == "maior":
        return 1 - NORMAL.cdf(z)
    if alternativa == "menor":
        return NORMAL.cdf(z)
    raise ValueError('Use alternativa="bilateral", "maior" ou "menor".')


def teste_z_media(amostra, mu0, alternativa="bilateral"):
    n = len(amostra)
    if n < 30:
        raise ValueError("O teste z para a média precisa de pelo menos 30 valores. Use um teste t.")
    media, desvio = mean(amostra), stdev(amostra)
    z = (media - mu0) / (desvio / math.sqrt(n))
    return {"media": media, "desvio": desvio, "z": z, "p": valor_p(z, alternativa)}


def teste_z_proporcao(sucessos, n, p0, alternativa="bilateral"):
    if not 0 <= sucessos <= n:
        raise ValueError("Os sucessos precisam estar entre 0 e n.")
    if n * p0 < 10 or n * (1 - p0) < 10:
        raise ValueError("Amostra pequena demais para a aproximação normal: n x p0 e n x (1 - p0) precisam ser 10 ou mais.")
    proporcao = sucessos / n
    z = (proporcao - p0) / math.sqrt(p0 * (1 - p0) / n)
    return {"proporcao": proporcao, "z": z, "p": valor_p(z, alternativa)}


def rejeita_h0(p, alfa=0.05):
    return p <= alfa


def intervalo_confianca_media(amostra, confianca=0.95):
    z = NORMAL.inv_cdf(1 - (1 - confianca) / 2)
    media = mean(amostra)
    erro = z * stdev(amostra) / math.sqrt(len(amostra))
    return (media - erro, media + erro)


def analisar_pacotes(caminho_csv, peso_rotulo=500, alfa=0.05):
    pesos = pd.read_csv(caminho_csv)["peso_g"].tolist()
    teste = teste_z_media(pesos, peso_rotulo)
    inferior, superior = intervalo_confianca_media(pesos, 1 - alfa)
    return {
        "n": len(pesos),
        "media": round(teste["media"], 2),
        "desvio": round(teste["desvio"], 2),
        "z": round(teste["z"], 2),
        "p": round(teste["p"], 4),
        "rejeita_h0": rejeita_h0(teste["p"], alfa),
        "intervalo": (round(inferior, 2), round(superior, 2)),
    }
