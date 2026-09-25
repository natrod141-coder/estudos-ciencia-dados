"""Gabarito do desafio "Resumo estatístico de pedidos".

Só olhe depois de tentar sozinha. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import pandas as pd


def _exigir_valores(valores):
    if len(valores) == 0:
        raise ValueError("A lista de valores não pode estar vazia.")


def media(valores):
    _exigir_valores(valores)
    return sum(valores) / len(valores)


def mediana(valores):
    _exigir_valores(valores)
    ordenados = sorted(valores)
    meio = len(ordenados) // 2
    if len(ordenados) % 2 == 1:
        return ordenados[meio]
    return (ordenados[meio - 1] + ordenados[meio]) / 2


def moda(valores):
    _exigir_valores(valores)
    contagem = {}
    for valor in valores:
        contagem[valor] = contagem.get(valor, 0) + 1
    maior = max(contagem.values())
    if maior == 1:
        return []
    return sorted(valor for valor, vezes in contagem.items() if vezes == maior)


def tem_atipico(valores):
    if len(valores) < 4:
        return False
    ordenados = sorted(valores)
    meio = len(ordenados) // 2
    inferior = ordenados[:meio]
    superior = ordenados[meio + (len(ordenados) % 2):]  # se for ímpar, pula o valor central
    q1 = mediana(inferior)
    q3 = mediana(superior)
    iqr = q3 - q1
    limite_inferior = q1 - 1.5 * iqr
    limite_superior = q3 + 1.5 * iqr
    return any(v < limite_inferior or v > limite_superior for v in ordenados)


def escolher_medida(valores):
    return "mediana" if tem_atipico(valores) else "media"


def resumo_pedidos(caminho_csv):
    valores = pd.read_csv(caminho_csv)["valor"].tolist()
    return {
        "quantidade": len(valores),
        "media": round(media(valores), 2),
        "mediana": round(mediana(valores), 2),
        "moda": moda(valores),
        "tem_atipico": tem_atipico(valores),
        "medida_recomendada": escolher_medida(valores),
    }
