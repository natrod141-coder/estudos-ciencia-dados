import functools

import numpy as np
import pytest
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score

from solucao import (
    auc_por_pares,
    calibracao,
    contar,
    lucro,
    melhor_limiar,
    precisao_no_topo,
    precisao_recall_f1,
    probabilidades_de_teste,
    tabela_de_limiares,
)

LIMIARES = [round(0.05 * i, 2) for i in range(1, 13)]  # 0,05 a 0,60


@functools.lru_cache(maxsize=None)
def dados_de_teste():
    return probabilidades_de_teste()


def test_contar():
    y, probs = [1, 1, 0, 0, 1, 0], [0.9, 0.2, 0.6, 0.1, 0.5, 0.5]
    assert contar(y, probs, 0.5) == {"vp": 2, "fp": 2, "fn": 1, "vn": 1}, "Probabilidade igual ao limiar entra na lista."


def test_precisao_recall_f1():
    y, probs = dados_de_teste()
    medidas = precisao_recall_f1(contar(y, probs, 0.3))
    previsto = (probs >= 0.3).astype(int)
    assert medidas["precisao"] == pytest.approx(precision_score(y, previsto))
    assert medidas["recall"] == pytest.approx(recall_score(y, previsto))
    assert medidas["f1"] == pytest.approx(f1_score(y, previsto))
    assert precisao_recall_f1({"vp": 0, "fp": 0, "fn": 5, "vn": 10}) == {"precisao": 0.0, "recall": 0.0, "f1": 0.0}


def test_auc_por_pares():
    assert auc_por_pares([0, 0, 1, 1], [0.1, 0.4, 0.35, 0.8]) == pytest.approx(0.75)
    assert auc_por_pares([0, 1], [0.5, 0.5]) == pytest.approx(0.5), "Empate vale meio ponto."
    y, probs = dados_de_teste()
    assert auc_por_pares(y, probs) == pytest.approx(roc_auc_score(y, probs))


def test_tabela_de_limiares():
    y, probs = dados_de_teste()
    tabela = tabela_de_limiares(y, probs, LIMIARES)
    assert list(tabela.columns) == ["limiar", "lista", "precisao", "recall"]
    assert tabela["lista"].is_monotonic_decreasing and tabela["recall"].is_monotonic_decreasing, (
        "Quanto maior o limiar, menor a lista e menos cancelamentos encontrados."
    )
    assert tabela["precisao"].iloc[-1] > tabela["precisao"].iloc[0] + 0.2


def test_lucro():
    assert lucro({"vp": 100, "fp": 200, "fn": 50, "vn": 650}) == pytest.approx(100 * 0.3 * 400 - 300 * 40)
    assert lucro({"vp": 10, "fp": 0, "fn": 0, "vn": 0}, valor_cliente=1000, custo_contato=10, taxa_sucesso=0.5) == pytest.approx(4900)


def test_melhor_limiar_nao_e_o_padrao():
    y, probs = dados_de_teste()
    melhor = melhor_limiar(y, probs, LIMIARES)
    assert melhor in (0.25, 0.3, 0.35), "Com contato de R$ 40, o melhor limiar fica perto de 40 / (0,3 x 400), ou 0,33."
    assert lucro(contar(y, probs, melhor)) > 1.4 * lucro(contar(y, probs, 0.5))


def test_contato_barato_muda_o_limiar():
    y, probs = dados_de_teste()
    assert melhor_limiar(y, probs, LIMIARES, custo_contato=15) <= 0.15, (
        "Se o contato custa pouco, vale falar com quase todo mundo."
    )


def test_precisao_no_topo():
    y, probs = dados_de_teste()
    precisao, recall = precisao_no_topo(y, probs, 300)
    assert precisao == pytest.approx(0.48, abs=0.04), "Quase metade da lista de 300 ia cancelar."
    assert precisao > 1.5 * y.mean(), "Bem acima dos 27% de uma lista sorteada."
    assert recall == pytest.approx(y[np.argsort(-probs)[:300]].sum() / y.sum())


def test_calibracao():
    y, probs = dados_de_teste()
    tabela = calibracao(y, probs)
    assert list(tabela.columns) == ["prob_media", "taxa_real"] and len(tabela) == 5
    assert tabela["prob_media"].is_monotonic_increasing
    assert (tabela["prob_media"] - tabela["taxa_real"]).abs().max() < 0.06, (
        "Em cada faixa, a probabilidade média fica perto da taxa real: o modelo está bem calibrado."
    )
