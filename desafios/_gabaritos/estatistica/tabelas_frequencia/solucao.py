"""Gabarito do desafio "Como se distribuem os atendimentos do SAC".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import math

import pandas as pd


def tabela_frequencia(serie):
    contagem = serie.value_counts().sort_index()
    total = contagem.sum()
    acumulada = contagem.cumsum()
    return pd.DataFrame(
        {
            "frequencia": contagem,
            "relativa": (contagem / total * 100).round(1),
            "acumulada": acumulada,
            # calculada a partir da contagem acumulada, e não somando porcentagens já arredondadas
            "relativa_acumulada": (acumulada / total * 100).round(1),
        }
    )


def numero_de_classes(n):
    if n < 1:
        raise ValueError("É preciso ter pelo menos um valor.")
    return math.ceil(1 + math.log2(n))


def tabela_por_classes(valores, k):
    if len(valores) == 0 or k < 1:
        raise ValueError("É preciso ter valores e pelo menos uma classe.")
    minimo, maximo = min(valores), max(valores)
    largura = (maximo - minimo) / k
    classes = []
    for i in range(k):
        ultima = i == k - 1
        inicio = minimo + i * largura
        fim = maximo if ultima else minimo + (i + 1) * largura
        frequencia = sum(1 for v in valores if inicio <= v < fim or (ultima and v == fim))
        classes.append({"inicio": inicio, "fim": fim, "frequencia": frequencia})
    return classes


def _mediana_ordenados(ordenados):
    meio = len(ordenados) // 2
    if len(ordenados) % 2 == 1:
        return ordenados[meio]
    return (ordenados[meio - 1] + ordenados[meio]) / 2


def cinco_numeros(valores):
    if len(valores) < 4:
        raise ValueError("São precisos pelo menos 4 valores para calcular os quartis.")
    ordenados = sorted(valores)
    meio = len(ordenados) // 2
    return {
        "minimo": ordenados[0],
        "q1": _mediana_ordenados(ordenados[:meio]),
        "mediana": _mediana_ordenados(ordenados),
        "q3": _mediana_ordenados(ordenados[meio + (len(ordenados) % 2):]),
        "maximo": ordenados[-1],
    }


def limites_boxplot(valores):
    resumo = cinco_numeros(valores)
    iqr = resumo["q3"] - resumo["q1"]
    cerca_inferior = resumo["q1"] - 1.5 * iqr
    cerca_superior = resumo["q3"] + 1.5 * iqr
    dentro = [v for v in valores if cerca_inferior <= v <= cerca_superior]
    return {
        "bigode_inferior": min(dentro),
        "bigode_superior": max(dentro),
        "atipicos": sorted(v for v in valores if v < cerca_inferior or v > cerca_superior),
    }


def resumo_atendimentos(caminho_csv):
    atendimentos = pd.read_csv(caminho_csv)
    tempos = atendimentos["tempo_min"].tolist()
    return {
        "por_canal": tabela_frequencia(atendimentos["canal"]),
        "por_nota": tabela_frequencia(atendimentos["nota"]),
        "classes_tempo": tabela_por_classes(tempos, numero_de_classes(len(tempos))),
        "cinco_numeros_tempo": cinco_numeros(tempos),
        "boxplot_tempo": limites_boxplot(tempos),
    }
