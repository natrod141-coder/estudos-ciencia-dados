import functools
from pathlib import Path

import pandas as pd
import pytest
from sklearn.metrics import roc_auc_score
from sklearn.tree import DecisionTreeClassifier

from solucao import (
    auc_oob,
    auc_teste,
    concordancia,
    curva_de_arvores,
    dividir,
    importancia_por_impureza,
    importancia_por_permutacao,
    preparar,
    treinar_floresta,
)

ASSINATURAS = pd.read_csv(Path(__file__).parent.parent / "data" / "assinaturas.csv")


def partes():
    X, y = preparar(ASSINATURAS)
    return dividir(X, y)


@functools.lru_cache(maxsize=None)
def floresta_e_partes():
    X_treino, X_teste, y_treino, y_teste = partes()
    return treinar_floresta(X_treino, y_treino), X_treino, X_teste, y_treino, y_teste


def test_dividir():
    X_treino, X_teste, y_treino, y_teste = partes()
    assert len(X_teste) == 1250
    assert y_treino.mean() == pytest.approx(y_teste.mean(), abs=0.002)


def test_configuracao_da_floresta():
    floresta = floresta_e_partes()[0]
    assert floresta.n_estimators == 300 and floresta.min_samples_leaf == 5
    assert floresta.oob_score is True, "Ligue oob_score para ter a estimativa fora da sacola."


def test_auc_teste():
    floresta, _, X_teste, _, y_teste = floresta_e_partes()
    assert auc_teste(floresta, X_teste, y_teste) == pytest.approx(roc_auc_score(y_teste, floresta.predict_proba(X_teste)[:, 1]))


def test_floresta_bate_a_melhor_arvore():
    floresta, X_treino, X_teste, y_treino, y_teste = floresta_e_partes()
    arvore = DecisionTreeClassifier(max_depth=6, random_state=42).fit(X_treino, y_treino)
    assert auc_teste(floresta, X_teste, y_teste) > auc_teste(arvore, X_teste, y_teste) + 0.03


def test_oob_estima_o_teste_sem_gastar_dados():
    floresta, _, X_teste, y_treino, y_teste = floresta_e_partes()
    assert auc_oob(floresta, y_treino) == pytest.approx(auc_teste(floresta, X_teste, y_teste), abs=0.03), (
        "A AUC fora da sacola fica perto da AUC no teste."
    )


def test_mais_arvores_melhoram_ate_estabilizar():
    _, X_treino, X_teste, y_treino, y_teste = floresta_e_partes()
    curva = curva_de_arvores(X_treino, y_treino, X_teste, y_teste, [1, 10, 100, 300])
    assert list(curva.columns) == ["n_arvores", "auc_teste"] and curva["n_arvores"].tolist() == [1, 10, 100, 300]
    auc = curva["auc_teste"].tolist()
    assert auc[0] + 0.05 < auc[1] < auc[2], "Uma árvore só erra bem mais que dez, e dez erram mais que cem."
    assert auc[3] == pytest.approx(auc[2], abs=0.01), "Depois de umas cem árvores, o ganho quase some."


def test_floresta_e_mais_estavel_que_uma_arvore():
    X_treino, X_teste, y_treino, _ = partes()
    amostras = [(X_treino.sample(frac=0.9, random_state=s), y_treino.sample(frac=0.9, random_state=s)) for s in (1, 2)]
    arvores = [DecisionTreeClassifier(max_depth=6, random_state=s).fit(Xa, ya) for s, (Xa, ya) in zip((1, 2), amostras)]
    florestas = [treinar_floresta(Xa, ya, n_arvores=200, semente=s) for s, (Xa, ya) in zip((1, 2), amostras)]
    entre_arvores = concordancia(*arvores, X_teste)
    entre_florestas = concordancia(*florestas, X_teste)
    assert isinstance(entre_florestas, float)
    assert entre_florestas > 0.9 > entre_arvores, (
        "Treinadas com amostras um pouco diferentes, duas árvores discordam bem mais que duas florestas."
    )


def test_importancia_por_permutacao():
    floresta, _, X_teste, _, y_teste = floresta_e_partes()
    permutacao = importancia_por_permutacao(floresta, X_teste, y_teste)
    assert permutacao.is_monotonic_decreasing
    assert {"atrasos_pagamento", "chamados_suporte", "nota_satisfacao"} <= set(permutacao.index[:4])


def test_importancia_por_impureza_favorece_variaveis_com_muitos_valores():
    floresta, X_treino, X_teste, _, y_teste = floresta_e_partes()
    impureza = importancia_por_impureza(floresta, X_treino.columns)
    permutacao = importancia_por_permutacao(floresta, X_teste, y_teste)
    assert impureza.sum() == pytest.approx(1.0) and impureza.is_monotonic_decreasing
    assert "idade" in impureza.index[:2], "Pela impureza, a idade, com dezenas de valores diferentes, aparece no topo."
    posicao = list(permutacao.index)
    assert posicao.index("idade") > posicao.index("atrasos_pagamento"), (
        "Pela permutação, os atrasos de pagamento importam mais que a idade."
    )
