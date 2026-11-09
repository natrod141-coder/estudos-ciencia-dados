from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score

from solucao import (
    acuracia_ingenua,
    ajustar,
    classificar,
    clientes_mais_arriscados,
    dividir,
    matriz_confusao,
    preparar,
    probabilidades,
    razoes_de_chance,
)

ASSINATURAS = pd.read_csv(Path(__file__).parent.parent / "data" / "assinaturas.csv")


def treinado():
    X, y = preparar(ASSINATURAS)
    X_treino, X_teste, y_treino, y_teste = dividir(X, y)
    return ajustar(X_treino, y_treino), X_treino, X_teste, y_treino, y_teste


def test_preparar():
    X, y = preparar(ASSINATURAS)
    assert "cliente_id" not in X.columns and "cancelou" not in X.columns
    assert {"plano_padrao", "plano_premium", "canal_indicacao", "canal_organico", "canal_parceiro"} <= set(X.columns)
    assert "plano_basico" not in X.columns, "O plano básico é a referência: não ganha coluna."
    assert y.tolist() == ASSINATURAS["cancelou"].tolist()


def test_dividir_estratificado():
    X, y = preparar(ASSINATURAS)
    X_treino, X_teste, y_treino, y_teste = dividir(X, y)
    assert len(X_teste) == 1250
    assert y_treino.mean() == pytest.approx(y_teste.mean(), abs=0.002), "Com stratify, a taxa de cancelamento é a mesma nos dois."


def test_probabilidades_e_limiar():
    modelo, _, X_teste, _, _ = treinado()
    probs = probabilidades(modelo, X_teste)
    assert len(probs) == len(X_teste) and ((probs >= 0) & (probs <= 1)).all()
    assert classificar([0.2, 0.5, 0.7]).tolist() == [0, 1, 1]
    assert classificar([0.2, 0.5, 0.7], limiar=0.6).tolist() == [0, 0, 1]


def test_matriz_confusao():
    assert matriz_confusao([1, 1, 0, 0, 1, 0], [1, 0, 1, 0, 1, 0]) == {"vp": 2, "fp": 1, "fn": 1, "vn": 2}


def test_acuracia_engana_com_classes_desbalanceadas():
    modelo, _, X_teste, _, y_teste = treinado()
    ingenua = acuracia_ingenua(y_teste)
    assert ingenua == pytest.approx(1 - y_teste.mean()), "Prever que ninguém cancela acerta todos os que ficam."
    matriz = matriz_confusao(y_teste, classificar(probabilidades(modelo, X_teste)))
    acuracia = (matriz["vp"] + matriz["vn"]) / len(y_teste)
    recall = matriz["vp"] / (matriz["vp"] + matriz["fn"])
    assert acuracia - ingenua < 0.05, "A acurácia do modelo fica perto da ingênua."
    assert recall < 0.4, "Com limiar 0,5, o modelo deixa passar a maioria dos cancelamentos."


def test_limiar_menor_encontra_mais_cancelamentos():
    modelo, _, X_teste, _, y_teste = treinado()
    probs = probabilidades(modelo, X_teste)
    com_meio = matriz_confusao(y_teste, classificar(probs, 0.5))
    com_tres = matriz_confusao(y_teste, classificar(probs, 0.3))
    assert com_tres["vp"] > com_meio["vp"] and com_tres["fp"] > com_meio["fp"], (
        "Baixar o limiar pega mais cancelamentos, ao custo de mais alarmes falsos."
    )


def test_modelo_ordena_bem_o_risco():
    modelo, _, X_teste, _, y_teste = treinado()
    assert roc_auc_score(y_teste, probabilidades(modelo, X_teste)) > 0.68


def test_razoes_de_chance():
    modelo, X_treino, *_ = treinado()
    razoes = razoes_de_chance(modelo, X_treino.columns)
    assert razoes["atrasos_pagamento"] == pytest.approx(np.exp(modelo.coef_[0][list(X_treino.columns).index("atrasos_pagamento")]))
    assert razoes["atrasos_pagamento"] > 1.4, "Cada atraso de pagamento aumenta a chance de cancelar."
    assert razoes["usa_app"] < 1 and razoes["plano_premium"] < 1
    assert all(isinstance(valor, float) for valor in razoes.values())


def test_clientes_mais_arriscados():
    modelo, _, X_teste, _, _ = treinado()
    probs = probabilidades(modelo, X_teste)
    df_teste = ASSINATURAS.loc[X_teste.index]
    lista = clientes_mais_arriscados(df_teste, probs, n=10)
    assert len(lista) == 10
    assert lista["prob_cancelar"].tolist() == sorted(probs, reverse=True)[:10]
    assert "prob_cancelar" not in df_teste.columns, "Devolva uma cópia: não altere a tabela recebida."
