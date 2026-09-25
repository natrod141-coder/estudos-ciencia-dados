"""Gabarito do desafio "Uma amostra que represente a base de clientes".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import math

import pandas as pd


def amostra_aleatoria_simples(populacao, n, semente):
    if n > len(populacao):
        raise ValueError("A amostra não pode ser maior que a população.")
    return populacao.sample(n=n, random_state=semente)


def amostra_sistematica(populacao, n, inicio=0):
    if n > len(populacao):
        raise ValueError("A amostra não pode ser maior que a população.")
    k = len(populacao) // n
    if not 0 <= inicio < k:
        raise ValueError(f"O início precisa estar entre 0 e {k - 1}.")
    return populacao.iloc[inicio::k].head(n)


def tamanhos_por_estrato(populacao, coluna, n):
    total = len(populacao)
    cotas = {estrato: n * quantidade / total for estrato, quantidade in populacao[coluna].value_counts().items()}
    tamanhos = {estrato: math.floor(cota) for estrato, cota in cotas.items()}
    faltam = n - sum(tamanhos.values())
    # maior resto primeiro; no empate, o estrato que vem antes em ordem alfabética
    fila = sorted(cotas, key=lambda estrato: (-(cotas[estrato] - tamanhos[estrato]), estrato))
    for estrato in fila[:faltam]:
        tamanhos[estrato] += 1
    return dict(sorted(tamanhos.items()))


def amostra_estratificada(populacao, coluna, n, semente):
    partes = [
        populacao[populacao[coluna] == estrato].sample(n=tamanho, random_state=semente)
        for estrato, tamanho in tamanhos_por_estrato(populacao, coluna, n).items()
    ]
    return pd.concat(partes)


def erro_de_composicao(populacao, amostra, coluna):
    na_populacao = populacao[coluna].value_counts(normalize=True) * 100
    na_amostra = amostra[coluna].value_counts(normalize=True) * 100
    na_amostra = na_amostra.reindex(na_populacao.index, fill_value=0)  # categoria ausente vale 0%
    return round(float((na_populacao - na_amostra).abs().max()), 1)


def margem_de_erro(p, n, z=1.96):
    return z * math.sqrt(p * (1 - p) / n)


def tamanho_amostra(margem, p=0.5, z=1.96):
    return math.ceil(z**2 * p * (1 - p) / margem**2)


def avaliar_amostras(caminho_csv, n=100, semente=42):
    clientes = pd.read_csv(caminho_csv)
    amostras = {
        "primeiras_linhas": clientes.head(n),
        "aleatoria_simples": amostra_aleatoria_simples(clientes, n, semente),
        "sistematica": amostra_sistematica(clientes, n),
        "estratificada": amostra_estratificada(clientes, "regiao", n, semente),
    }
    return {nome: erro_de_composicao(clientes, amostra, "regiao") for nome, amostra in amostras.items()}
