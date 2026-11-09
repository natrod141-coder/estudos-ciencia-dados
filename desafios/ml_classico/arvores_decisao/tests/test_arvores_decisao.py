from pathlib import Path

import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score

from solucao import (
    auc,
    curva_de_profundidade,
    dividir_em_tres,
    importancias,
    melhor_profundidade,
    preparar,
    regras,
    treinar_arvore,
)

ASSINATURAS = pd.read_csv(Path(__file__).parent.parent / "data" / "assinaturas.csv")
PROFUNDIDADES = [2, 3, 4, 5, 6, 7, 8, 10, None]


def partes():
    X, y = preparar(ASSINATURAS)
    return dividir_em_tres(X, y)


def test_dividir_em_tres():
    X_treino, X_val, X_teste, y_treino, y_val, y_teste = partes()
    assert (len(X_treino), len(X_val), len(X_teste)) == (3000, 1000, 1000)
    assert y_treino.mean() == pytest.approx(y_teste.mean(), abs=0.003)
    assert y_val.mean() == pytest.approx(y_teste.mean(), abs=0.003)
    assert set(X_treino.index).isdisjoint(X_val.index) and set(X_val.index).isdisjoint(X_teste.index)


def test_profundidade_limitada():
    X_treino, _, _, y_treino, _, _ = partes()
    assert treinar_arvore(X_treino, y_treino, 3).get_depth() == 3


def test_auc():
    X_treino, X_val, _, y_treino, y_val, _ = partes()
    arvore = treinar_arvore(X_treino, y_treino, 4)
    assert auc(arvore, X_val, y_val) == pytest.approx(roc_auc_score(y_val, arvore.predict_proba(X_val)[:, 1]))


def test_arvore_sem_limite_decora_o_treino():
    X_treino, X_val, _, y_treino, y_val, _ = partes()
    livre = treinar_arvore(X_treino, y_treino)
    assert auc(livre, X_treino, y_treino) > 0.99, "Sem limite, a árvore cresce até acertar todo o treino."
    assert auc(livre, X_val, y_val) < 0.66, "Mas em clientes novos ela erra muito: decorou o treino."


def test_curva_de_profundidade():
    X_treino, X_val, _, y_treino, y_val, _ = partes()
    curva = curva_de_profundidade(X_treino, y_treino, X_val, y_val, PROFUNDIDADES)
    assert list(curva.columns) == ["profundidade", "auc_treino", "auc_validacao"]
    assert len(curva) == len(PROFUNDIDADES)
    distancia = curva["auc_treino"] - curva["auc_validacao"]
    assert distancia.iloc[-1] > 0.3 > distancia.iloc[1], "A distância entre treino e validação cresce com a profundidade."


def test_melhor_profundidade():
    X_treino, X_val, _, y_treino, y_val, _ = partes()
    curva = curva_de_profundidade(X_treino, y_treino, X_val, y_val, PROFUNDIDADES)
    assert melhor_profundidade(curva) in (4, 5, 6, 7)
    empate = pd.DataFrame({"profundidade": [3, 5, 8], "auc_treino": [0.7, 0.8, 0.9], "auc_validacao": [0.70, 0.72, 0.72]})
    assert melhor_profundidade(empate) == 5, "No empate, fica a árvore mais simples."


def test_regras_mostram_a_combinacao_de_risco():
    X_treino, _, _, y_treino, _, _ = partes()
    texto = regras(treinar_arvore(X_treino, y_treino, 3), X_treino.columns)
    assert isinstance(texto, str)
    assert "nota_satisfacao" in texto and "chamados_suporte" in texto, (
        "A árvore achou sozinha o grupo de risco: clientes insatisfeitos e com chamados ao suporte."
    )


def test_importancias():
    X_treino, _, _, y_treino, _, _ = partes()
    serie = importancias(treinar_arvore(X_treino, y_treino, 5), X_treino.columns)
    assert serie.sum() == pytest.approx(1.0)
    assert serie.is_monotonic_decreasing
    assert {"chamados_suporte", "atrasos_pagamento"} <= set(serie.index[:3])


def test_resultado_final_no_teste():
    X_treino, X_val, X_teste, y_treino, y_val, y_teste = partes()
    melhor = melhor_profundidade(curva_de_profundidade(X_treino, y_treino, X_val, y_val, PROFUNDIDADES))
    final = treinar_arvore(X_treino, y_treino, melhor)
    assert auc(final, X_teste, y_teste) > 0.62
