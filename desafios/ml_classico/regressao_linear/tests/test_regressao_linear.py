from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from solucao import (
    COLUNAS,
    ajustar,
    avaliar,
    avaliar_baseline,
    codificar,
    coeficientes,
    dividir,
    piores_previsoes,
    prever_tempo,
)

ENTREGAS = pd.read_csv(Path(__file__).parent.parent / "data" / "entregas.csv")


def treinado():
    X = codificar(ENTREGAS)
    X_treino, X_teste, y_treino, y_teste = dividir(X, ENTREGAS["tempo_min"])
    return ajustar(X_treino, y_treino), X_treino, X_teste, y_treino, y_teste


def test_codificar():
    X = codificar(ENTREGAS)
    assert list(X.columns) == COLUNAS
    centro = X[ENTREGAS["regiao"] == "centro"]
    assert (centro[["regiao_norte", "regiao_sul"]] == 0).all().all(), "Centro é a referência: zero nas duas colunas."
    assert X.loc[ENTREGAS["regiao"] == "norte", "regiao_norte"].eq(1).all()
    assert "tempo_min" in ENTREGAS.columns, "Não altere a tabela recebida."


def test_dividir():
    X = codificar(ENTREGAS)
    X_treino, X_teste, y_treino, y_teste = dividir(X, ENTREGAS["tempo_min"])
    assert (len(X_treino), len(X_teste)) == (480, 120)
    assert set(X_treino.index).isdisjoint(X_teste.index), "Nenhuma entrega pode estar no treino e no teste."
    de_novo = dividir(X, ENTREGAS["tempo_min"])[1]
    assert list(de_novo.index) == list(X_teste.index), "Com a mesma semente, a divisão se repete."


def test_coeficientes_batem_com_minimos_quadrados():
    modelo, X_treino, _, y_treino, _ = treinado()
    coefs = coeficientes(modelo, COLUNAS)
    A = np.column_stack([np.ones(len(X_treino)), X_treino.to_numpy(dtype=float)])
    solucao, *_ = np.linalg.lstsq(A, y_treino.to_numpy(), rcond=None)
    assert coefs["intercepto"] == pytest.approx(solucao[0])
    assert [coefs[coluna] for coluna in COLUNAS] == pytest.approx(list(solucao[1:]))
    assert all(isinstance(valor, float) for valor in coefs.values())


def test_coeficientes_tem_o_efeito_esperado():
    coefs = coeficientes(treinado()[0], COLUNAS)
    assert coefs["distancia_km"] == pytest.approx(2.4, abs=0.25), "Cada km a mais soma uns 2,4 minutos."
    assert coefs["chuva"] == pytest.approx(9, abs=1.5)
    assert coefs["horario_pico"] == pytest.approx(7, abs=1.5)
    assert coefs["regiao_norte"] > 0 > coefs["regiao_sul"], "Comparado ao centro, o norte demora mais e o sul, menos."


def test_avaliar():
    resultado = avaliar([10, 20, 30, 40], [12, 18, 33, 37])
    assert resultado["mae"] == pytest.approx(2.5)
    assert resultado["rmse"] == pytest.approx(np.sqrt(6.5))
    assert resultado["r2"] == pytest.approx(1 - 26 / 500)


def test_avaliar_baseline():
    _, _, _, y_treino, y_teste = treinado()
    base = avaliar_baseline(y_treino, y_teste)
    assert base["mae"] == pytest.approx(np.mean(np.abs(y_teste - y_treino.mean())))
    assert base["r2"] <= 0.01, "Prever sempre a média dá R² perto de zero."


def test_modelo_bate_o_baseline():
    modelo, _, X_teste, y_treino, y_teste = treinado()
    resultado = avaliar(y_teste, modelo.predict(X_teste))
    base = avaliar_baseline(y_treino, y_teste)
    assert resultado["mae"] < 0.5 * base["mae"], "O modelo precisa errar bem menos que a média."
    assert resultado["r2"] > 0.85
    assert resultado["mae"] == pytest.approx(4, abs=1), "O ruído dos dados é de uns 5 minutos: o erro não cai muito abaixo disso."


def test_prever_tempo():
    modelo = treinado()[0]
    coefs = coeficientes(modelo, COLUNAS)
    esperado = coefs["intercepto"] + 10 * coefs["distancia_km"] + 2 * coefs["peso_kg"] + 3 * coefs["itens"] + coefs["chuva"]
    assert prever_tempo(modelo, 10, 2, 3, 1, 0, "centro") == pytest.approx(esperado)
    norte = prever_tempo(modelo, 10, 2, 3, 1, 0, "norte")
    assert norte - esperado == pytest.approx(coefs["regiao_norte"])


def test_piores_previsoes():
    modelo, _, X_teste, _, _ = treinado()
    df_teste = ENTREGAS.loc[X_teste.index]
    previsto = modelo.predict(X_teste)
    piores = piores_previsoes(df_teste, previsto, n=5)
    assert len(piores) == 5
    erros = df_teste["tempo_min"].to_numpy() - previsto
    assert piores["erro"].abs().tolist() == pytest.approx(sorted(np.abs(erros), reverse=True)[:5])
    assert "erro" not in df_teste.columns, "Devolva uma cópia: não altere a tabela recebida."
