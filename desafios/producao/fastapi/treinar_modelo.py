"""Já está pronto: treina o modelo de cancelamento e grava data/modelo.json.

O modelo é a regressão logística do módulo de machine learning, com as variáveis numéricas
padronizadas e o plano e o canal em colunas 0/1. Em vez de gravar o objeto do scikit-learn com
pickle ou joblib, que só abre com a mesma versão da biblioteca, este script grava os números do
modelo num JSON: qualquer código lê, e a previsão é uma conta simples (veja modelo.py).

Para treinar de novo, dentro desta pasta:
    python treinar_modelo.py
"""

import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

PASTA = Path(__file__).parent / "data"
VERSAO = "2026-11-01"
NUMERICAS = [
    "idade", "meses_assinatura", "valor_mensal", "acessos_mes", "chamados_suporte",
    "atrasos_pagamento", "usa_app", "nota_satisfacao",
]
CATEGORICAS = ["plano", "canal"]


def treinar():
    dados = pd.read_csv(PASTA / "assinaturas.csv")
    preparo = ColumnTransformer([
        ("numericas", StandardScaler(), NUMERICAS),
        ("categoricas", OneHotEncoder(), CATEGORICAS),
    ])
    pipeline = make_pipeline(preparo, LogisticRegression(max_iter=5000))
    pipeline.fit(dados[NUMERICAS + CATEGORICAS], dados["cancelou"])
    escala = preparo.named_transformers_["numericas"]
    codificador = preparo.named_transformers_["categoricas"]
    regressao = pipeline[-1]
    nomes = NUMERICAS + [f"{coluna}={valor}" for coluna, valores in zip(CATEGORICAS, codificador.categories_) for valor in valores]
    return {
        "versao": VERSAO,
        "numericas": {
            coluna: {"media": round(float(media), 6), "desvio": round(float(desvio), 6)}
            for coluna, media, desvio in zip(NUMERICAS, escala.mean_, escala.scale_)
        },
        "categoricas": {coluna: [str(v) for v in valores] for coluna, valores in zip(CATEGORICAS, codificador.categories_)},
        "coeficientes": {nome: round(float(c), 6) for nome, c in zip(nomes, regressao.coef_[0])},
        "intercepto": round(float(regressao.intercept_[0]), 6),
    }, pipeline


if __name__ == "__main__":
    modelo, _ = treinar()
    (PASTA / "modelo.json").write_text(json.dumps(modelo, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print("Modelo gravado em data/modelo.json, versão", modelo["versao"])
