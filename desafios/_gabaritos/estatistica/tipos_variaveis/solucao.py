"""Gabarito do desafio "Cada coluna no seu tipo".

Só olhe depois de tentar resolver. Se travar, leia a mensagem de erro do pytest primeiro:
ela costuma apontar exatamente o que está diferente do esperado.
"""

import pandas as pd

ORDEM_ESCOLARIDADE = ["fundamental", "médio", "superior", "pós-graduação"]
ORDEM_SATISFACAO = ["muito insatisfeito", "insatisfeito", "neutro", "satisfeito", "muito satisfeito"]

CLASSIFICACAO = {
    "cidade": "nominal",
    "cep": "nominal",  # é um código: tem dígitos, mas não faz sentido somar nem ordenar CEPs
    "escolaridade": "ordinal",
    "satisfacao": "ordinal",
    "dependentes": "discreta",
    "compras_no_ano": "discreta",
    "renda_mensal": "continua",
}

_MEDIDAS = {
    "nominal": ["moda"],
    "ordinal": ["moda", "mediana"],
    "discreta": ["moda", "mediana", "media"],
    "continua": ["mediana", "media"],
}


def medidas_permitidas(tipo):
    if tipo not in _MEDIDAS:
        raise ValueError(f"Tipo desconhecido: {tipo!r}. Use nominal, ordinal, discreta ou continua.")
    return list(_MEDIDAS[tipo])


def ler_pesquisa(caminho_csv):
    pesquisa = pd.read_csv(caminho_csv, dtype={"cep": str})
    pesquisa["escolaridade"] = pd.Categorical(pesquisa["escolaridade"], categories=ORDEM_ESCOLARIDADE, ordered=True)
    pesquisa["satisfacao"] = pd.Categorical(pesquisa["satisfacao"], categories=ORDEM_SATISFACAO, ordered=True)
    return pesquisa


def mediana_ordinal(serie):
    codigos = sorted(codigo for codigo in serie.cat.codes if codigo != -1)  # -1 é valor faltante
    if not codigos:
        raise ValueError("A série não tem nenhum valor.")
    return serie.cat.categories[codigos[(len(codigos) - 1) // 2]]


def resumo_central(pesquisa):
    resumo = {}
    for coluna, tipo in CLASSIFICACAO.items():
        serie = pesquisa[coluna]
        medidas = {}
        for medida in medidas_permitidas(tipo):
            if medida == "moda":
                medidas["moda"] = serie.mode().iloc[0]
            elif medida == "mediana" and tipo == "ordinal":
                medidas["mediana"] = mediana_ordinal(serie)
            elif medida == "mediana":
                medidas["mediana"] = round(float(serie.median()), 2)
            else:
                medidas["media"] = round(float(serie.mean()), 2)
        resumo[coluna] = medidas
    return resumo
