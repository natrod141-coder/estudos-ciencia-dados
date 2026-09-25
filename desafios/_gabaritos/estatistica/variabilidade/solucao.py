"""Gabarito do desafio "Qual centro de distribuição é mais confiável".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import math

import pandas as pd


def _exigir_valores(valores):
    if len(valores) == 0:
        raise ValueError("A lista de valores não pode estar vazia.")


def _media(valores):
    return sum(valores) / len(valores)


def _mediana_ordenados(ordenados):
    meio = len(ordenados) // 2
    if len(ordenados) % 2 == 1:
        return ordenados[meio]
    return (ordenados[meio - 1] + ordenados[meio]) / 2


def amplitude(valores):
    _exigir_valores(valores)
    return max(valores) - min(valores)


def variancia(valores, amostral=True):
    _exigir_valores(valores)
    n = len(valores)
    if amostral and n < 2:
        raise ValueError("A variância amostral precisa de pelo menos 2 valores.")
    m = _media(valores)
    soma_dos_quadrados = sum((v - m) ** 2 for v in valores)
    return soma_dos_quadrados / (n - 1 if amostral else n)


def desvio_padrao(valores, amostral=True):
    return math.sqrt(variancia(valores, amostral))


def coeficiente_variacao(valores):
    _exigir_valores(valores)
    m = _media(valores)
    if m == 0:
        raise ValueError("O coeficiente de variação não existe quando a média é zero.")
    return desvio_padrao(valores) / m * 100


def intervalo_interquartil(valores):
    if len(valores) < 4:
        raise ValueError("São precisos pelo menos 4 valores para calcular os quartis.")
    ordenados = sorted(valores)
    meio = len(ordenados) // 2
    inferior = ordenados[:meio]
    superior = ordenados[meio + (len(ordenados) % 2):]  # se for ímpar, pula o valor central
    return _mediana_ordenados(superior) - _mediana_ordenados(inferior)


def comparar_centros(caminho_csv, prazo=7):
    dados = pd.read_csv(caminho_csv)
    centros = {}
    for centro, grupo in dados.groupby("centro"):
        dias = grupo["dias"].tolist()
        atrasos = sum(1 for d in dias if d > prazo)
        centros[centro] = {
            "media": round(_media(dias), 2),
            "desvio_padrao": round(desvio_padrao(dias), 2),
            "coeficiente_variacao": round(coeficiente_variacao(dias), 2),
            "amplitude": amplitude(dias),
            "iqr": intervalo_interquartil(dias),
            "percentual_atrasos": round(100 * atrasos / len(dias), 1),
        }
    mais_consistente = min(centros, key=lambda nome: centros[nome]["coeficiente_variacao"])
    return {"centros": centros, "mais_consistente": mais_consistente}
