import functools
from pathlib import Path

import numpy as np
import pandas as pd
import pytest
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score, train_test_split

from solucao import (
    auc_em_divisoes,
    auc_final,
    busca_em_grade,
    dados_de_ruido,
    preparar,
    resumo,
    selecao_antes_de_dividir,
    selecao_dentro_do_pipeline,
    validacao_cruzada,
)

ASSINATURAS = pd.read_csv(Path(__file__).parent.parent / "data" / "assinaturas.csv")
X, Y = preparar(ASSINATURAS)


@functools.lru_cache(maxsize=None)
def grade_e_teste():
    X_treino, X_teste, y_treino, y_teste = train_test_split(X, Y, test_size=0.25, random_state=42, stratify=Y)
    return busca_em_grade(X_treino, y_treino), X_teste, y_teste


def test_cada_divisao_da_uma_nota_diferente():
    notas = auc_em_divisoes(X, Y, range(10))
    assert len(notas) == 10
    assert max(notas) - min(notas) > 0.02, "Só trocando o sorteio da divisão, a AUC muda bastante."


def test_validacao_cruzada():
    notas = validacao_cruzada(LogisticRegression(max_iter=5000), X, Y)
    esperado = cross_val_score(
        LogisticRegression(max_iter=5000), X, Y,
        cv=StratifiedKFold(5, shuffle=True, random_state=42), scoring="roc_auc",
    )
    assert len(notas) == 5
    assert list(notas) == pytest.approx(list(esperado))


def test_resumo():
    assert resumo([0.70, 0.72, 0.74]) == {"media": pytest.approx(0.72), "desvio": pytest.approx(np.std([0.70, 0.72, 0.74]))}
    assert all(isinstance(valor, float) for valor in resumo([0.7, 0.8]).values())


def test_validacao_cruzada_resume_bem_as_divisoes():
    media_das_divisoes = np.mean(auc_em_divisoes(X, Y, range(10)))
    cv = resumo(validacao_cruzada(LogisticRegression(max_iter=5000), X, Y))
    assert cv["media"] == pytest.approx(media_das_divisoes, abs=0.02)
    assert 0 < cv["desvio"] < 0.05


def test_selecao_antes_de_dividir_inventa_um_modelo_bom():
    X_ruido, y_ruido = dados_de_ruido()
    assert selecao_antes_de_dividir(X_ruido, y_ruido) > 0.7, (
        "Com um alvo sorteado, nenhuma coluna prevê nada. Mesmo assim, escolher as colunas antes de dividir dá uma AUC alta."
    )


def test_selecao_dentro_do_pipeline_e_honesta():
    X_ruido, y_ruido = dados_de_ruido()
    assert selecao_dentro_do_pipeline(X_ruido, y_ruido) < 0.6, "Com a seleção dentro do pipeline, a AUC fica perto de 0,5."


def test_configuracao_da_busca():
    grade = grade_e_teste()[0]
    assert grade.scoring == "roc_auc"
    assert grade.cv.get_n_splits() == 5
    assert set(grade.param_grid) == {"max_depth", "min_samples_leaf"}
    assert len(grade.cv_results_["params"]) == 12


def test_busca_encontra_folhas_maiores():
    grade = grade_e_teste()[0]
    assert grade.best_params_["min_samples_leaf"] in (20, 50), "Folhas com muitos clientes generalizam melhor."
    assert grade.best_score_ > 0.70


def test_auc_final_no_teste():
    grade, X_teste, y_teste = grade_e_teste()
    assert auc_final(grade, X_teste, y_teste) > 0.68
