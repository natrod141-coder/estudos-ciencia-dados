import functools
from pathlib import Path

import pandas as pd
import pytest
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

from solucao import (
    auc,
    com_faltantes,
    curva_de_validacao,
    dividir_em_tres,
    melhor_iteracao,
    preparar,
    treinar_boosting,
    treinar_com_parada_antecipada,
)

ASSINATURAS = pd.read_csv(Path(__file__).parent.parent / "data" / "assinaturas.csv")


def partes():
    X, y = preparar(ASSINATURAS)
    return dividir_em_tres(X, y)


@functools.lru_cache(maxsize=None)
def rapido_e_curva():
    """Boosting com taxa alta e muitas iterações, e a curva de validação dele."""
    X_treino, X_val, _, y_treino, y_val, _ = partes()
    modelo = treinar_boosting(X_treino, y_treino, taxa=0.3, iteracoes=300)
    return modelo, curva_de_validacao(modelo, X_val, y_val)


def test_preparar_mantem_as_categorias():
    X, y = preparar(ASSINATURAS)
    assert str(X["plano"].dtype) == "category" and str(X["canal"].dtype) == "category"
    assert "plano_premium" not in X.columns, "Não crie colunas de 0 e 1: o boosting trata as categorias sozinho."
    assert "cliente_id" not in X.columns and y.tolist() == ASSINATURAS["cancelou"].tolist()


def test_dividir_em_tres():
    X_treino, X_val, X_teste, y_treino, y_val, y_teste = partes()
    assert (len(X_treino), len(X_val), len(X_teste)) == (3000, 1000, 1000)
    assert y_val.mean() == pytest.approx(y_teste.mean(), abs=0.003)


def test_curva_de_validacao():
    modelo, curva = rapido_e_curva()
    _, X_val, _, _, y_val, _ = partes()
    assert len(curva) == modelo.n_iter_ == 300
    assert all(isinstance(valor, float) for valor in curva)
    assert curva[-1] == pytest.approx(auc(modelo, X_val, y_val)), "O último ponto da curva é o modelo completo."


def test_melhor_iteracao():
    assert melhor_iteracao([0.6, 0.7, 0.72, 0.71]) == 3
    assert melhor_iteracao([0.6, 0.7, 0.7]) == 2, "No empate, a primeira."


def test_boosting_sobreajusta_com_iteracoes_demais():
    modelo, curva = rapido_e_curva()
    X_treino, _, _, y_treino, _, _ = partes()
    assert melhor_iteracao(curva) < 50, "Com taxa 0,3, a validação melhora só nas primeiras iterações."
    assert curva[-1] < max(curva) - 0.02, "Depois do pico, mais árvores pioram a validação."
    assert auc(modelo, X_treino, y_treino) > 0.99, "Enquanto isso, o treino continua melhorando: é sobreajuste."


def test_taxa_menor_precisa_de_mais_iteracoes():
    _, curva_rapida = rapido_e_curva()
    X_treino, X_val, _, y_treino, y_val, _ = partes()
    lento = treinar_boosting(X_treino, y_treino, taxa=0.03, iteracoes=400)
    curva_lenta = curva_de_validacao(lento, X_val, y_val)
    assert melhor_iteracao(curva_lenta) > 5 * melhor_iteracao(curva_rapida)
    assert max(curva_lenta) >= max(curva_rapida) - 0.01, "Passos menores chegam pelo menos tão longe."


def test_parada_antecipada():
    X_treino, X_val, X_teste, y_treino, y_val, y_teste = partes()
    X_resto, y_resto = pd.concat([X_treino, X_val]), pd.concat([y_treino, y_val])
    modelo = treinar_com_parada_antecipada(X_resto, y_resto)
    assert modelo.early_stopping is True and modelo.max_iter == 2000
    assert modelo.n_iter_ < 500, "O modelo parou sozinho, muito antes do limite de 2.000 iterações."
    floresta = RandomForestClassifier(300, min_samples_leaf=5, random_state=42, n_jobs=-1).fit(
        pd.get_dummies(X_resto, dtype=int), y_resto
    )
    auc_floresta = roc_auc_score(y_teste, floresta.predict_proba(pd.get_dummies(X_teste, dtype=int))[:, 1])
    assert auc(modelo, X_teste, y_teste) == pytest.approx(auc_floresta, abs=0.03), (
        "Nestes dados, o boosting com parada antecipada fica no mesmo nível da random forest."
    )


def test_com_faltantes():
    X, _ = preparar(ASSINATURAS)
    furado = com_faltantes(X, "nota_satisfacao", 0.15)
    assert X["nota_satisfacao"].isna().sum() == 0, "Não altere a tabela recebida."
    assert furado["nota_satisfacao"].isna().mean() == pytest.approx(0.15, abs=0.02)
    assert furado.drop(columns="nota_satisfacao").equals(X.drop(columns="nota_satisfacao"))


def test_boosting_aceita_faltantes_sem_preencher():
    X_treino, X_val, X_teste, y_treino, y_val, y_teste = partes()
    X_resto, y_resto = pd.concat([X_treino, X_val]), pd.concat([y_treino, y_val])
    modelo = treinar_com_parada_antecipada(com_faltantes(X_resto, "nota_satisfacao", 0.15), y_resto)
    assert auc(modelo, com_faltantes(X_teste, "nota_satisfacao", 0.15, semente=7), y_teste) > 0.70
